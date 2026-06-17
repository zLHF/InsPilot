from __future__ import annotations

import uuid
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class StoredAttachment:
    original_filename: str
    path: Path


class LocalAttachmentStorage:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, *, filename: str, content: bytes) -> StoredAttachment:
        safe_name = Path(filename).name
        target = self.root / f"{uuid.uuid4()}-{safe_name}"
        target.write_bytes(content)
        return StoredAttachment(original_filename=filename, path=target)
