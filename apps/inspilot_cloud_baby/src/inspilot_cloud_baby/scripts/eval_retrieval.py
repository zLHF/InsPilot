"""检索评估脚本 — 计算 recall@k 与 MRR，量化检索改动的收益。

没有"尺子"就无法判断 rerank / 混合检索 / chunk 化是否真的更准。本脚本提供该尺子：
给定 (query → 期望命中的方案 id)，跑当前检索管线，输出 recall@k 与 MRR。

用法:
  # 用知识库标题自动生成弱 eval（冒烟用，验证管线连通 + 给一个基线数字）
  python -m inspilot_cloud_baby.scripts.eval_retrieval

  # 用人工标注的 eval 集（推荐：从 query_logs 的真实问题里挑标注）
  python -m inspilot_cloud_baby.scripts.eval_retrieval --file eval.jsonl --k 5
  # eval.jsonl 每行一个 JSON: {"query": "衢州有哪些方案", "expected_ids": ["<uuid>", ...]}

A/B 用法：改一项配置（如 BUSINESS_ROBOT_ENABLE_RERANK=false）前后各跑一次，对比数字。
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from dataclasses import dataclass

from inspilot_cloud_baby.auth import CurrentUser
from inspilot_cloud_baby.db import SessionLocal
from inspilot_cloud_baby.models import KnowledgeItem, KnowledgeStatus
from inspilot_cloud_baby.retrieval import retrieve_documents

_EVAL_USER = CurrentUser(user_id="eval", is_company_user=True, project_ids=set())


@dataclass
class EvalCase:
    query: str
    expected_ids: set[str]


def _load_cases(path: str) -> list[EvalCase]:
    cases: list[EvalCase] = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            cases.append(EvalCase(query=obj["query"], expected_ids=set(obj["expected_ids"])))
    return cases


def _auto_cases(db, sample: int) -> list[EvalCase]:
    """Weak eval: use each item's own title as the query, expecting to retrieve itself."""
    rows = db.query(KnowledgeItem.id, KnowledgeItem.title).filter(
        KnowledgeItem.status == KnowledgeStatus.ACTIVE
    ).all()
    if not rows:
        return []
    random.seed(42)
    picked = random.sample(rows, min(sample, len(rows)))
    return [EvalCase(query=title, expected_ids={str(item_id)}) for item_id, title in picked]


def _evaluate(cases: list[EvalCase], k: int) -> dict:
    hits = 0
    reciprocal_ranks = 0.0
    zero = 0
    db = SessionLocal()
    try:
        for case in cases:
            docs = retrieve_documents(
                query=case.query, user=_EVAL_USER, documents=[], limit=k, db=db
            )
            ids = [d.id for d in docs]
            if not ids:
                zero += 1
            rank = next((i for i, doc_id in enumerate(ids) if doc_id in case.expected_ids), None)
            if rank is not None:
                hits += 1
                reciprocal_ranks += 1.0 / (rank + 1)
    finally:
        db.close()
    n = len(cases) or 1
    return {
        "cases": len(cases),
        f"recall@{k}": round(hits / n, 4),
        "mrr": round(reciprocal_ranks / n, 4),
        "zero_result": zero,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="检索评估 — recall@k / MRR")
    parser.add_argument("--file", help="eval jsonl 文件路径（缺省则用标题自动生成弱 eval）")
    parser.add_argument("--k", type=int, default=5, help="top-k（默认 5）")
    parser.add_argument("--sample", type=int, default=50, help="自动模式抽样条数（默认 50）")
    args = parser.parse_args()

    if args.file:
        cases = _load_cases(args.file)
    else:
        db = SessionLocal()
        try:
            cases = _auto_cases(db, args.sample)
        finally:
            db.close()
        print(f"[自动弱 eval] 用 {len(cases)} 条方案标题作为 query（期望命中自身）")

    if not cases:
        print("没有可评估的样本（知识库为空或 eval 文件为空）", file=sys.stderr)
        return 1

    metrics = _evaluate(cases, args.k)
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
