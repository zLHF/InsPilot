"""Backfill embeddings for existing knowledge items.

Usage:
    python -m inspilot_cloud_baby.scripts.migrate_embeddings
"""
from __future__ import annotations

import logging
import sys
import time

from inspilot_cloud_baby.db import SessionLocal
from inspilot_cloud_baby.embedding import get_embedding_service
from inspilot_cloud_baby.models import KnowledgeItem, KnowledgeStatus

logger = logging.getLogger(__name__)


def migrate_embeddings(batch_size: int = 50, dry_run: bool = False) -> int:
    """Generate embeddings for all active knowledge items that lack one.

    Returns the number of items processed.
    """
    svc = get_embedding_service()
    if not svc.available:
        print("ERROR: Embedding service is not available (check OPENAI_API_KEY).")
        sys.exit(1)

    session = SessionLocal()
    try:
        query = (
            session.query(KnowledgeItem)
            .filter(
                KnowledgeItem.embedding.is_(None),
                KnowledgeItem.status == KnowledgeStatus.ACTIVE,
            )
            .order_by(KnowledgeItem.created_at)
        )
        total = query.count()
        if total == 0:
            print("All active knowledge items already have embeddings. Nothing to do.")
            return 0

        print(f"Found {total} knowledge items without embeddings.")
        if dry_run:
            print("(dry-run mode — no changes will be written)")
            return total

        processed = 0
        failed = 0
        start = time.time()

        for item in query.yield_per(batch_size):
            vector = svc.embed_text(f"{item.title}\n{item.body}")
            if vector is not None:
                item.embedding = vector
                session.commit()
                processed += 1
            else:
                failed += 1
                logger.warning("Failed to embed item %s", item.id)

            if processed % 10 == 0:
                elapsed = time.time() - start
                print(f"  Progress: {processed}/{total} ({failed} failed) — {elapsed:.1f}s elapsed")

        elapsed = time.time() - start
        print(f"\nDone! Processed: {processed}, Failed: {failed}, Time: {elapsed:.1f}s")
        return processed

    except KeyboardInterrupt:
        print("\nInterrupted. Progress has been saved — re-run to continue.")
        return 0
    finally:
        session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    migrate_embeddings()
