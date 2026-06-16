"""Import CS3.0 项目方案 HTML files into the knowledge base.

Each HTML file is a self-contained insurance/guarantee-bond scheme document.
This script strips HTML, extracts plain text + dimensions from the title line,
and creates a KnowledgeItem (source_type="cs3_plan") with an embedding.

Dimension parsing uses DUAL sources (title line first, filename as fallback):
  region / insurer / doc_type / integrator / doc_date

Usage:
    # Dry-run: parse + print stats, write nothing to DB
    python -m inspilot_cloud_baby.scripts.import_cs3_plans --dir "/path/CS3.0 项目方案" --dry-run

    # Real import (idempotent: skips files already imported by original_file)
    python -m inspilot_cloud_baby.scripts.import_cs3_plans --dir "/path/CS3.0 项目方案"
"""
from __future__ import annotations

import argparse
import logging
import re
import sys
import time
from collections import Counter
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

logger = logging.getLogger(__name__)

# Minimum text length to consider a file a real scheme (filters out index/nav pages)
MIN_TEXT_CHARS = 200

# Known insurance companies (for tagging from raw text)
INSURERS = [
    "人保", "国寿财", "中华联", "平安", "太平洋", "太保", "阳光",
    "华泰", "安诚", "浙商", "中银", "永安", "紫金", "大家",
]
# Known integrators (技术商) — substring-matched against the whole name
INTEGRATORS = [
    "新点", "筑龙", "品茗", "广联达", "政采云", "文锐", "数科", "杰软",
    "杰瑞", "中招", "建网", "移动", "迅捷", "金控", "乐彩云", "媒婆网",
    "中控", "双讯",
]

# Region noise: title-leading words that are NOT regions (functional pages)
_REGION_NOISE = {
    "流程图", "单证说明", "投保单", "保单说明", "付款通知书", "支付页面",
    "机构", "签章", "退保", "客户端", "密码登录", "发票", "核心后台",
    "退款", "出单", "打款", "农民工", "联银", "中心", "CA",
    "CA授权签章", "CA登录", "签章样例", "签章页面", "支付凭证",
}


# ---------------------------------------------------------------------------
# HTML → plain text
# ---------------------------------------------------------------------------


class _TextExtractor(HTMLParser):
    """Collect visible text, skipping script/style/svg."""

    def __init__(self) -> None:
        super().__init__()
        self.out: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in ("script", "style", "svg"):
            self._skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style", "svg") and self._skip > 0:
            self._skip -= 1

    def handle_data(self, data: str) -> None:
        if not self._skip:
            data = data.strip()
            if data:
                self.out.append(data)


def extract_text(html_str: str) -> list[str]:
    """Return non-empty visible text lines from an HTML document."""
    p = _TextExtractor()
    p.feed(html_str)
    return p.out


# ---------------------------------------------------------------------------
# Dimension parsing
# ---------------------------------------------------------------------------

# A date like 230614 / 20240628 / 251128 — 6 or 8 digits, possibly after a separator
_DATE_RE = re.compile(r"(20\d{6}|\d{6})(?![\d])")
# doc_type tokens
_DOC_TYPES = ("ofd", "pdf", "pfd")  # pfd is a common typo of pdf


@dataclass
class ParsedPlan:
    """Result of parsing one scheme file."""

    original_file: str
    title: str
    body: str
    char_count: int
    region: str = ""
    insurer: str = ""
    doc_type: str = ""
    integrator: str = ""
    doc_date: str = ""
    skipped: bool = False
    skip_reason: str = ""
    parse_source: str = ""  # "title" or "filename"
    fields: dict = field(default_factory=dict)  # extra business fields extracted


def _normalize_date(raw: str) -> str:
    """Turn '230614' → '2023-06-14', '20240628' → '2024-06-28'."""
    digits = re.sub(r"\D", "", raw)
    if len(digits) == 6:
        yy = digits[:2]
        year = f"20{yy}" if yy <= "30" else f"19{yy}"
        return f"{year}-{digits[2:4]}-{digits[4:6]}"
    if len(digits) == 8:
        return f"{digits[:4]}-{digits[4:6]}-{digits[6:8]}"
    return ""


def _strip_status_prefix(name: str) -> str:
    """Remove leading status markers like 【履约】【未完成】【湖州长兴】(新）."""
    name = re.sub(r"^[\s]*[【\[（(][^\】\]）)]*[】\]）)]", "", name)
    name = re.sub(r"^[\s]*[（(][^）)]*[）)]", "", name)
    return name.strip()


def _parse_name_tokens(name: str) -> dict:
    """Parse dimension tokens from a single name string (title line or filename).

    Strategy: substring-match insurer/integrator/doc_type/date against the WHOLE
    name (so they're found even when fused into a compound token), then derive
    the region from whatever geographic-looking text remains.
    """
    result = {"region": "", "insurer": "", "doc_type": "", "integrator": "", "doc_date": ""}
    low = name.lower()

    # 1) date
    m = _DATE_RE.search(name)
    if m:
        result["doc_date"] = _normalize_date(m.group(1))

    # 2) doc_type
    for dt in _DOC_TYPES:
        if dt in low:
            result["doc_type"] = "pdf" if dt == "pfd" else dt
            break

    # 3) insurer (substring)
    for ins in INSURERS:
        if ins in name:
            result["insurer"] = ins
            break

    # 4) integrator (substring)
    for integ in INTEGRATORS:
        if integ in name:
            result["integrator"] = integ
            break

    # 5) region: strip out everything we recognised, plus status/dates/separators,
    #    and keep the residual geographic text.
    residual = _strip_status_prefix(name)
    # remove the matched dimensions from the residual
    for val in (result["insurer"], result["integrator"], result["doc_type"]):
        if val:
            residual = residual.replace(val, " ")
    # remove the raw date digits
    residual = _DATE_RE.sub(" ", residual)
    # split on separators and keep meaningful tokens
    tokens = re.split(r"[_\-\s/、,，。]+", residual)
    tokens = [t.strip("（）()【】[] ") for t in tokens if t.strip("（）()【】[] ")]
    # drop noise / non-geographic tokens
    geo = [t for t in tokens if t and t not in _REGION_NOISE and not t.isdigit() and len(t) >= 2]
    if geo:
        result["region"] = geo[0]

    return result


def parse_plan(path: Path) -> ParsedPlan:
    """Parse one HTML scheme file into a ParsedPlan."""
    fname = path.name
    try:
        html_str = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        return ParsedPlan(original_file=fname, title="", body="", char_count=0,
                          skipped=True, skip_reason=f"read error: {exc}")

    lines = extract_text(html_str)
    char_count = sum(len(x) for x in lines)

    # Skip near-empty files (index/nav pages)
    if char_count < MIN_TEXT_CHARS:
        return ParsedPlan(original_file=fname, title="", body="", char_count=char_count,
                          skipped=True, skip_reason="too short (nav/index page?)")

    # Title line: usually the 2nd non-empty line (1st is often a BOM)
    title_line = ""
    for line in lines:
        if line and line != "\ufeff" and len(line) > 1:
            title_line = line
            break

    # Strip extension from title
    title_clean = re.sub(r"\.html?$", "", title_line, flags=re.IGNORECASE).strip()

    # Parse dimensions: title line first, filename as fallback
    dims = _parse_name_tokens(title_clean)
    parse_source = "title"
    if not dims["region"] and not dims["insurer"]:
        # Fallback to filename
        fname_clean = re.sub(r"\.html?$", "", fname, flags=re.IGNORECASE)
        dims_fb = _parse_name_tokens(fname_clean)
        if dims_fb["region"] or dims_fb["insurer"]:
            dims = dims_fb
            parse_source = "filename"

    # Extract a few key business fields from the body text
    body = "\n".join(lines)
    fields = _extract_business_fields(lines)

    return ParsedPlan(
        original_file=fname,
        title=title_clean or fname,
        body=body,
        char_count=char_count,
        region=dims["region"],
        insurer=dims["insurer"],
        doc_type=dims["doc_type"],
        integrator=dims["integrator"],
        doc_date=dims["doc_date"],
        parse_source=parse_source,
        fields=fields,
    )


def _extract_business_fields(lines: list[str]) -> dict:
    """Extract a handful of business dimensions from field labels."""
    fields = {}
    # Client config: look for "客户端配置说明（支持：...）"
    for line in lines:
        if "客户端配置说明" in line and "支持" in line:
            fields["client_config"] = line[:120]
            break
    return fields


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(description="Import CS3.0 scheme HTML files into the knowledge base.")
    ap.add_argument("--dir", required=True, help="Directory of .html scheme files.")
    ap.add_argument("--dry-run", action="store_true", help="Parse + print stats only; write nothing to DB.")
    args = ap.parse_args()

    src = Path(args.dir).expanduser()
    if not src.is_dir():
        print(f"ERROR: not a directory: {src}")
        sys.exit(1)

    html_files = sorted(src.glob("*.html"))
    print(f"Found {len(html_files)} .html files in {src}")
    print(f"Mode: {'DRY-RUN (no DB writes)' if args.dry_run else 'IMPORT'}\n")

    plans: list[ParsedPlan] = []
    for path in html_files:
        plans.append(parse_plan(path))

    # ---- Stats ----
    kept = [p for p in plans if not p.skipped]
    skipped = [p for p in plans if p.skipped]

    print("=" * 60)
    print("PARSE SUMMARY")
    print("=" * 60)
    print(f"  Total files:    {len(plans)}")
    print(f"  Kept (valid):   {len(kept)}")
    print(f"  Skipped:        {len(skipped)}")

    # Parse coverage
    has_region = sum(1 for p in kept if p.region)
    has_insurer = sum(1 for p in kept if p.insurer)
    has_integrator = sum(1 for p in kept if p.integrator)
    has_date = sum(1 for p in kept if p.doc_date)
    print(f"\n  Dimension coverage (of {len(kept)} kept):")
    print(f"    region:      {has_region:4d}  ({has_region*100//max(len(kept),1)}%)")
    print(f"    insurer:     {has_insurer:4d}  ({has_insurer*100//max(len(kept),1)}%)")
    print(f"    integrator:  {has_integrator:4d}  ({has_integrator*100//max(len(kept),1)}%)")
    print(f"    doc_date:    {has_date:4d}  ({has_date*100//max(len(kept),1)}%)")

    # Distribution
    print("\n  Top regions:")
    for r, c in Counter(p.region for p in kept if p.region).most_common(15):
        print(f"    {c:4d}  {r}")
    print("\n  Top insurers:")
    for r, c in Counter(p.insurer for p in kept if p.insurer).most_common(10):
        print(f"    {c:4d}  {r}")
    print("\n  Top integrators:")
    for r, c in Counter(p.integrator for p in kept if p.integrator).most_common(10):
        print(f"    {c:4d}  {r}")

    # Source breakdown
    src_counter = Counter(p.parse_source for p in kept)
    print(f"\n  Parse source: {dict(src_counter)}")

    # Skipped reasons
    print(f"\n  Skipped files ({len(skipped)}):")
    skip_reasons = Counter(p.skip_reason for p in skipped)
    for reason, c in skip_reasons.most_common():
        print(f"    {c:4d}  {reason}")
    print(f"    sample: {[p.original_file for p in skipped[:5]]}")

    # Sample parsed rows
    print(f"\n{'=' * 60}")
    print("SAMPLE PARSED ROWS (first 8 kept)")
    print("=" * 60)
    for p in kept[:8]:
        print(f"  • {p.title[:50]}")
        print(f"      region={p.region!r} insurer={p.insurer!r} type={p.doc_type!r} "
              f"integ={p.integrator!r} date={p.doc_date!r} [{p.parse_source}]")

    if args.dry_run:
        print(f"\n{'=' * 60}")
        print("DRY-RUN complete — no DB writes. Re-run without --dry-run to import.")
        return

    # ---- Real import ----
    _do_import(kept)


def _do_import(plans: list[ParsedPlan]) -> None:
    """Write parsed plans into the knowledge base (idempotent)."""
    from sqlalchemy import select

    from inspilot_cloud_baby.db import SessionLocal
    from inspilot_cloud_baby.embedding import get_embedding_service
    from inspilot_cloud_baby.models import (
        KnowledgeItem,
        KnowledgeSensitivity,
        KnowledgeStatus,
    )

    svc = get_embedding_service()
    embed_ok = svc.available
    if not embed_ok:
        print("WARNING: embedding service unavailable — items imported WITHOUT embeddings.")

    session = SessionLocal()
    try:
        existing = {
            row[0]
            for row in session.execute(
                select(
                    KnowledgeItem.metadata_json["original_file"]
                ).where(KnowledgeItem.source_type == "cs3_plan")
            ).all()
        }

        imported = 0
        skipped_existing = 0
        start = time.time()

        for p in plans:
            if p.original_file in existing:
                skipped_existing += 1
                continue

            title = p.title or p.original_file
            body = p.body

            vector = None
            if embed_ok:
                vector = svc.embed_text(f"{title}\n{body}")

            item = KnowledgeItem(
                title=title[:500],
                body=body,
                source_type="cs3_plan",
                sensitivity=KnowledgeSensitivity.PUBLIC_SUMMARY,
                status=KnowledgeStatus.ACTIVE,
                metadata_json={
                    "original_file": p.original_file,
                    "region": p.region,
                    "insurer": p.insurer,
                    "doc_type": p.doc_type,
                    "integrator": p.integrator,
                    "doc_date": p.doc_date,
                    "char_count": p.char_count,
                    "client_config": p.fields.get("client_config", ""),
                    "parse_source": p.parse_source,
                },
                created_by="cs3_import",
            )
            if vector is not None:
                item.embedding = vector
            session.add(item)
            imported += 1

            if imported % 20 == 0:
                session.commit()
                elapsed = time.time() - start
                print(f"  Progress: {imported} imported ({elapsed:.1f}s)")

        session.commit()
        elapsed = time.time() - start
        print(f"\nDone! Imported: {imported}, Skipped (already exist): {skipped_existing}, Time: {elapsed:.1f}s")
    except KeyboardInterrupt:
        session.rollback()
        print("\nInterrupted. Committed progress saved — re-run to continue.")
    finally:
        session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
    main()
