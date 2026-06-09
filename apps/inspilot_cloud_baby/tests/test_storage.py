from pathlib import Path

from inspilot_cloud_baby.storage import LocalAttachmentStorage


def test_local_storage_writes_file_under_root(tmp_path: Path) -> None:
    storage = LocalAttachmentStorage(root=tmp_path)

    stored = storage.save(filename="需求说明.txt", content=b"hello")

    assert stored.path.exists()
    assert stored.path.read_bytes() == b"hello"
    assert stored.original_filename == "需求说明.txt"


def test_local_storage_removes_path_separators(tmp_path: Path) -> None:
    storage = LocalAttachmentStorage(root=tmp_path)

    stored = storage.save(filename="../secret.txt", content=b"safe")

    assert stored.path.parent == tmp_path
    assert stored.path.name.endswith("secret.txt")
