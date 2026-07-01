"""Knowledge retrieval — vector search with keyword fallback."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import jieba
from sqlalchemy import String, func, or_, select

from inspilot_cloud_baby.auth import CurrentUser
from inspilot_cloud_baby.config import settings
from inspilot_cloud_baby.models import (
    KnowledgeItem,
    KnowledgeSensitivity,
    KnowledgeStatus,
    Project,
    ProjectVisibility,
)
from inspilot_cloud_baby.permissions import can_read_knowledge

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class KnowledgeDocument:
    id: str
    project_id: str | None
    project_visibility: ProjectVisibility | None
    sensitivity: KnowledgeSensitivity
    title: str
    body: str
    # Optional provenance for richer display (populated for DB-backed results)
    source_type: str = ""
    metadata: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def retrieve_documents(
    *,
    query: str,
    user: CurrentUser,
    documents: list[KnowledgeDocument],
    limit: int = 5,
    db: Session | None = None,
    filters: dict | None = None,
) -> list[KnowledgeDocument]:
    """Retrieve relevant knowledge documents.

    Pipeline:
      1. (optional) LLM query rewrite for better recall.
      2. Auto-extract region/insurer/integrator filters from the *original* query.
      3. Recall candidates from two channels — keyword (jieba) + vector — over a
         wider pool (fetch_k) than *limit*.
      4. Fuse the two rankings with Reciprocal Rank Fusion (RRF).
      5. (optional) Cross-encoder rerank the fused pool, then trim to *limit*.

    Degrades gracefully: a failing channel is skipped; if both DB channels yield
    nothing, falls back to in-memory keyword search over *documents*.
    """
    # Filters use the ORIGINAL query so rewrite cannot drop region/insurer entities.
    if filters is None and db is not None:
        filters = _extract_query_filters(query=query, db=db)

    search_query = _maybe_rewrite_query(query)

    if db is None:
        return _retrieve_by_keyword(query=search_query, user=user, documents=documents, limit=limit)

    # Recall a wider pool for fusion / reranking.
    fetch_k = max(limit * 4, 20)

    keyword_results: list[KnowledgeDocument] = []
    try:
        keyword_results = _retrieve_by_db_keyword(query=search_query, user=user, db=db, limit=fetch_k)
    except Exception:
        logger.warning("DB keyword search failed", exc_info=True)

    vector_results: list[KnowledgeDocument] = []
    try:
        vector_results = _retrieve_by_vector(
            query=search_query, user=user, db=db, limit=fetch_k, filters=filters
        )
    except Exception:
        logger.warning("Vector search failed", exc_info=True)

    # Fuse the two channels (RRF). Without both, use whichever produced results.
    if settings.enable_hybrid_search and keyword_results and vector_results:
        fused = _rrf_fuse([vector_results, keyword_results])
    else:
        fused = vector_results or keyword_results

    if not fused:
        return _retrieve_by_keyword(query=search_query, user=user, documents=documents, limit=limit)

    # Cross-encoder rerank (graceful no-op when unconfigured), then trim.
    fused = _maybe_rerank(search_query, fused, limit)
    return fused[:limit]


# ---------------------------------------------------------------------------
# Fusion / rerank / query-rewrite — recall-quality enhancements
# ---------------------------------------------------------------------------


def _rrf_fuse(ranked_lists: list[list[KnowledgeDocument]], *, k: int = 60) -> list[KnowledgeDocument]:
    """Reciprocal Rank Fusion: combine multiple ranked lists into one.

    A document's fused score is sum over lists of 1 / (k + rank). Documents that
    rank highly in *either* channel bubble up; agreement across channels compounds.
    """
    scores: dict[str, float] = {}
    doc_by_id: dict[str, KnowledgeDocument] = {}
    for ranked in ranked_lists:
        for rank, doc in enumerate(ranked):
            scores[doc.id] = scores.get(doc.id, 0.0) + 1.0 / (k + rank + 1)
            doc_by_id.setdefault(doc.id, doc)
    ordered_ids = sorted(scores, key=lambda doc_id: scores[doc_id], reverse=True)
    return [doc_by_id[doc_id] for doc_id in ordered_ids]


def _maybe_rerank(query: str, docs: list[KnowledgeDocument], limit: int) -> list[KnowledgeDocument]:
    """Cross-encoder rerank when a rerank service is configured; else return as-is."""
    if len(docs) <= 1:
        return docs
    try:
        from inspilot_cloud_baby.rerank import get_rerank_service

        svc = get_rerank_service()
        if not svc.available:
            return docs
        texts = [f"{d.title}\n{d.body[:1000]}" for d in docs]
        ranked = svc.rerank(query, texts, top_n=limit)
        if not ranked:
            return docs
        reordered = [docs[idx] for idx, _ in ranked if 0 <= idx < len(docs)]
        # Append any docs the reranker omitted, preserving fused order.
        seen = {id(d) for d in reordered}
        reordered.extend(d for d in docs if id(d) not in seen)
        return reordered
    except Exception:
        logger.warning("Rerank step failed, keeping fused order", exc_info=True)
        return docs


def _maybe_rewrite_query(query: str) -> str:
    """LLM query rewrite for recall (off by default — adds an LLM round-trip)."""
    if not settings.enable_query_rewrite:
        return query
    try:
        from inspilot_cloud_baby.chat_service import get_chat_service

        svc = get_chat_service()
        if not svc.available:
            return query
        out = svc.chat(
            [
                {
                    "role": "system",
                    "content": (
                        "你是检索查询改写助手。把用户口语化的保险业务问题改写成更适合"
                        "知识库检索的简洁查询，保留关键实体（地区/保司/集成商/业务术语）。"
                        "只输出改写后的查询，不要解释、不要引号。"
                    ),
                },
                {"role": "user", "content": query},
            ],
            temperature=0.0,
        )
        rewritten = (out or "").strip()
        return rewritten[:200] if rewritten else query
    except Exception:
        logger.warning("Query rewrite failed, using original query", exc_info=True)
        return query


# ---------------------------------------------------------------------------
# Query intent extraction — auto-detect region/insurer/integrator in query text
# ---------------------------------------------------------------------------

# Insurer / integrator dictionaries (kept in sync with import_cs3_plans.py)
_INSURERS = [
    "人保", "国寿财", "中华联", "平安", "太平洋", "太保", "阳光",
    "华泰", "安诚", "浙商", "中银", "永安", "紫金", "大家",
]
_INTEGRATORS = [
    "新点", "筑龙", "品茗", "广联达", "政采云", "文锐", "数科", "杰软",
    "杰瑞", "中招", "建网", "移动", "迅捷", "金控", "乐彩云",
]
_NON_REGION_KEYWORDS = (
    "担保", "保险", "保单", "支付", "收银", "页面", "详情", "弹窗", "按钮",
    "机构", "公司", "平台", "项目", "产品", "技术", "方案", "流程", "订单",
)
_ORG_QUERY_KEYWORDS = ("担保", "公司", "机构", "经纪", "融资", "科技")
_REGION_SUFFIXES = ("省", "市", "县", "区", "州", "盟", "旗", "岛")


def _load_known_regions(db: Session) -> list[str]:
    """Return distinct region values from cs3_plan metadata, longest first."""
    try:
        rows = db.execute(
            select(func.distinct(KnowledgeItem.metadata_json["region"]))
            .where(KnowledgeItem.source_type == "cs3_plan")
        ).scalars().all()
        return sorted([r for r in rows if r], key=len, reverse=True)
    except Exception:
        logger.debug("Failed to load known regions", exc_info=True)
        return []


def _looks_like_region(value: str) -> bool:
    """Reject polluted metadata values that are business/function words, not places."""
    value = value.strip()
    if not value or any(keyword in value for keyword in _NON_REGION_KEYWORDS):
        return False
    if value in _PROVINCE_CITIES:
        return True
    if any(value == city for cities in _PROVINCE_CITIES.values() for city in cities):
        return True
    return value.endswith(_REGION_SUFFIXES)


def _extract_query_filters(*, query: str, db: Session) -> dict:
    """Detect region/insurer/integrator intent in a natural-language query.

    Region matching uses the DB's known region values (substring match), so
    "青岛的方案" matches region "青岛". Insurer/integrator use fixed dictionaries.
    Returns a dict like {"region": "青岛", "insurer": "人保"} (only keys that match).
    """
    filters: dict[str, str] = {}

    # Insurer (substring against dictionary)
    for ins in _INSURERS:
        if ins in query:
            filters["insurer"] = ins
            break

    # Integrator (substring against dictionary)
    for integ in _INTEGRATORS:
        if integ in query:
            filters["integrator"] = integ
            break

    # Region: match the longest known region that appears in the query
    # (direct substring). Longest-first avoids e.g. "杭州" winning over
    # "杭州市". Handles parent→child (衢州→衢州市) via SQL prefix matching.
    for region in _load_known_regions(db):
        if not _looks_like_region(region):
            continue
        if region and region in query:
            filters["region"] = region
            break

    # Province expansion: if the query mentions a known province name (e.g.
    # "四川省" / "浙江") but no specific city was matched above, set the
    # region to the province so _build_region_clause expands it to its cities.
    if "region" not in filters and not any(keyword in query for keyword in _ORG_QUERY_KEYWORDS):
        for prov in _PROVINCE_CITIES:
            if prov in query:
                filters["region"] = prov
                break

    return filters


# ---------------------------------------------------------------------------
# Keyword search (unchanged from original)
# ---------------------------------------------------------------------------


def _retrieve_by_keyword(
    *,
    query: str,
    user: CurrentUser,
    documents: list[KnowledgeDocument],
    limit: int,
) -> list[KnowledgeDocument]:
    terms = _query_terms(query)
    visible_docs = [
        document
        for document in documents
        if can_read_knowledge(
            user=user,
            project_id=document.project_id,
            project_visibility=document.project_visibility,
            sensitivity=document.sensitivity,
        )
    ]
    scored = sorted(
        visible_docs,
        key=lambda document: _score(document=document, terms=terms),
        reverse=True,
    )
    return scored[:limit]


# Common Chinese function words / interrogatives that add noise to keyword matching.
_STOPWORDS = frozenset({
    "的", "了", "吗", "呢", "怎么", "如何", "是", "在", "有", "和", "与", "请问",
    "一下", "什么", "哪些", "哪个", "可以", "需要", "我们", "这个", "那个", "以及",
    "怎样", "多少", "为什么", "关于", "想", "要", "吧", "啊", "呀",
})


def _query_terms(query: str) -> list[str]:
    """Tokenize a query with jieba (Chinese-aware), dropping stopwords/noise.

    ``query.split()`` is useless for Chinese (no spaces → whole sentence becomes one
    token that almost never matches an ilike). jieba search-mode produces overlapping
    sub-terms (e.g. 见费出单 → 见费/出单/见费出单) for better keyword recall.
    """
    terms: list[str] = []
    seen: set[str] = set()
    for raw in jieba.lcut_for_search(query):
        term = raw.strip().lower()
        if not term or term in _STOPWORDS:
            continue
        # Drop single non-alphanumeric chars (punctuation, lone particles).
        if len(term) == 1 and not term.isalnum():
            continue
        if term in seen:
            continue
        seen.add(term)
        terms.append(term)
    return terms


def _retrieve_by_db_keyword(
    *,
    query: str,
    user: CurrentUser,
    db: Session,
    limit: int,
) -> list[KnowledgeDocument]:
    terms = _query_terms(query)
    if not terms:
        return []

    clauses = []
    for term in terms:
        pattern = f"%{term}%"
        clauses.append(KnowledgeItem.title.ilike(pattern))
        clauses.append(KnowledgeItem.body.ilike(pattern))

    rows = db.execute(
        select(KnowledgeItem, Project.visibility)
        .join(Project, KnowledgeItem.project_id == Project.id, isouter=True)
        .where(KnowledgeItem.status == KnowledgeStatus.ACTIVE)
        .where(or_(*clauses))
        .limit(limit * 5)
    ).all()

    documents: list[KnowledgeDocument] = []
    for item, visibility in rows:
        doc = KnowledgeDocument(
            id=str(item.id),
            project_id=str(item.project_id) if item.project_id else None,
            project_visibility=visibility,
            sensitivity=item.sensitivity,
            title=item.title,
            body=item.body,
            source_type=item.source_type or "",
            metadata=item.metadata_json or {},
        )
        if can_read_knowledge(
            user=user,
            project_id=doc.project_id,
            project_visibility=doc.project_visibility,
            sensitivity=doc.sensitivity,
        ):
            documents.append(doc)

    scored = sorted(
        documents,
        key=lambda document: _score(document=document, terms=terms),
        reverse=True,
    )
    return scored[:limit]


def _score(*, document: KnowledgeDocument, terms: list[str]) -> int:
    text = f"{document.title} {document.body}".lower()
    return sum(1 for term in terms if term in text)


# ---------------------------------------------------------------------------
# Vector search via pgvector
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Province → city mapping for region expansion.
# When the user searches a province (e.g. 浙江), we expand to match any city
# under it so that 杭州/温州/湖州 plans are included.
_PROVINCE_CITIES: dict[str, list[str]] = {
    "浙江": ["杭州", "湖州", "温州", "嘉兴", "宁波", "绍兴", "台州", "舟山", "丽水", "金华", "衢州", "义乌", "温岭", "三门", "新昌", "安吉", "长兴", "德清", "桐乡", "慈溪", "余姚", "临海", "瑞安", "乐清", "永康"],
    "四川": ["成都", "绵阳", "遂宁", "眉山", "宜宾", "攀枝花", "泸州", "自贡", "德阳", "广元", "广安", "达州", "南充", "内江", "乐山", "资阳", "雅安", "巴中", "阿坝", "凉山", "西昌"],
    "江苏": ["南京", "无锡", "苏州", "常州", "南通", "扬州", "镇江", "盐城", "徐州", "淮安", "连云港", "宿迁", "泰州", "昆山", "太仓", "常熟", "张家港", "江阴", "宜兴"],
    "新疆": ["乌鲁木齐", "克拉玛依", "吐鲁番", "哈密", "阿克苏", "喀什", "和田", "伊犁", "昌吉", "博乐", "库尔勒", "阿勒泰", "塔城"],
    "广东": ["广州", "深圳", "珠海", "佛山", "东莞", "中山", "惠州", "汕头", "江门", "湛江", "茂名", "肇庆", "梅州", "汕尾", "河源", "阳江", "清远", "潮州", "揭阳", "云浮"],
    "福建": ["福州", "厦门", "泉州", "漳州", "莆田", "龙岩", "三明", "南平", "宁德", "福清", "晋江", "石狮", "南安", "长乐"],
    "安徽": ["合肥", "芜湖", "蚌埠", "淮南", "马鞍山", "淮北", "铜陵", "安庆", "黄山", "滁州", "阜阳", "宿州", "六安", "亳州", "池州", "宣城"],
    "山东": ["济南", "青岛", "烟台", "潍坊", "淄博", "威海", "日照", "临沂", "德州", "聊城", "滨州", "菏泽", "泰安", "济宁", "枣庄", "东营"],
    "湖北": ["武汉", "黄石", "十堰", "宜昌", "襄阳", "鄂州", "荆门", "孝感", "荆州", "黄冈", "咸宁", "随州", "恩施", "仙桃", "天门", "潜江"],
    "湖南": ["长沙", "株洲", "湘潭", "衡阳", "邵阳", "岳阳", "常德", "张家界", "益阳", "郴州", "永州", "怀化", "娄底", "湘西"],
    "内蒙": ["呼和浩特", "包头", "乌海", "赤峰", "通辽", "鄂尔多斯", "呼伦贝尔", "巴彦淖尔", "乌兰察布", "兴安", "锡林郭勒", "阿拉善"],
}


def _expand_region(val: str) -> list[str]:
    """Expand a province query into [province, city1, city2, ...] for matching."""
    # Strip 省/市 suffix for lookup
    bare = val.rstrip("省市自治区特别行政区")
    cities = _PROVINCE_CITIES.get(bare, [])
    return [val] + cities


def _build_region_clause(col, val: str):
    """Build a region WHERE clause that matches the value AND its province-expansion."""
    from sqlalchemy import or_

    expanded = _expand_region(val)
    parts = []
    for r in expanded:
        parts.append(col.like(r + "%"))  # prefix: 浙江 → 浙江%, 杭州 → 杭州%
    return or_(*parts)


def _metadata_filter_clauses(filters: dict) -> list:
    """Build SQLAlchemy where-clauses for metadata_json filters (region/insurer/integrator).

    Region matching expands provinces to their cities (浙江 → 浙江/杭州/温州/...)
    and uses prefix match per term. Insurer/integrator use exact match.
    """
    clauses = []
    for key in ("region", "insurer", "integrator"):
        val = filters.get(key)
        if not val:
            continue
        col = func.cast(KnowledgeItem.metadata_json.op("->>")(key), String)
        if key == "region":
            clauses.append(_build_region_clause(col, val))
        else:
            clauses.append(col == val)
    return clauses


def _retrieve_by_vector(
    *,
    query: str,
    user: CurrentUser,
    db: Session,
    limit: int,
    filters: dict | None = None,
) -> list[KnowledgeDocument]:
    from inspilot_cloud_baby.embedding import get_embedding_service  # avoid circular import at module level

    svc = get_embedding_service()
    if not svc.available:
        return []

    query_vec = svc.embed_query(query)
    if query_vec is None:
        return []

    filter_clauses = _metadata_filter_clauses(filters or {})

    def _run(clauses: list) -> list[KnowledgeDocument]:
        stmt = (
            select(KnowledgeItem, Project.visibility)
            .join(Project, KnowledgeItem.project_id == Project.id, isouter=True)
            .where(KnowledgeItem.embedding.isnot(None))
            .where(KnowledgeItem.status == KnowledgeStatus.ACTIVE)
        )
        for clause in clauses:
            stmt = stmt.where(clause)
        stmt = stmt.order_by(KnowledgeItem.embedding.cosine_distance(query_vec)).limit(limit * 3)

        rows = db.execute(stmt).all()
        documents: list[KnowledgeDocument] = []
        for item, visibility in rows:
            doc = KnowledgeDocument(
                id=str(item.id),
                project_id=str(item.project_id) if item.project_id else None,
                project_visibility=visibility,
                sensitivity=item.sensitivity,
                title=item.title,
                body=item.body,
                source_type=item.source_type or "",
                metadata=item.metadata_json or {},
            )
            if can_read_knowledge(
                user=user,
                project_id=doc.project_id,
                project_visibility=doc.project_visibility,
                sensitivity=doc.sensitivity,
            ):
                documents.append(doc)
            if len(documents) >= limit:
                break
        return documents

    # First pass: with filters (auto-extracted or manual)
    if filter_clauses:
        results = _run(filter_clauses)
        if results:
            return results
        # Fallback: filters too strict (e.g. region typo) → relax and re-search
        logger.info("Filtered vector search returned nothing; relaxing filters %s", filters)
        return _run([])

    return _run([])
