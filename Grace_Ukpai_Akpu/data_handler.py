"""Read and write students.csv using Python's built-in csv module.

Owned by: Grace Ukpai Akpu  |  Branch: feature/file-handling
"""

from __future__ import annotations

import csv
import os
import tempfile
from pathlib import Path
from typing import Dict, List

from Ismail_Muhammed.exceptions import FileOperationError
from Ismail_Muhammed.safe_action import safe_action

FIELDNAMES = ["student_id", "name", "email", "phone", "course", "grade"]


def _read_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        _write_rows(path, [])
        return []

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is not None and reader.fieldnames != FIELDNAMES:
            raise FileOperationError("CSV headers do not match the student register format.")
        rows: List[Dict[str, str]] = []
        for index, raw in enumerate(reader, start=2):
            if None in raw:
                raise FileOperationError(f"Row {index} has extra columns.")
            if not raw or not any((value or "").strip() for value in raw.values()):
                continue
            row = {field: (raw.get(field) or "").strip() for field in FIELDNAMES}
            if not row["student_id"]:
                raise FileOperationError(f"Row {index} in {path.name} is missing a student ID.")
            rows.append(row)
        return rows


def _write_rows(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="", dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
            writer.writeheader()
            for row in rows:
                writer.writerow({field: row.get(field, "") for field in FIELDNAMES})
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def load_from_file(filepath: str | Path) -> List[Dict[str, str]]:
    """Load every student row from CSV. Returns [] if the file is new/empty."""
    path = Path(filepath)
    ok, result, error = safe_action(_read_rows, path, default=[])
    if not ok:
        raise FileOperationError(error)
    return result or []


def save_to_file(filepath: str | Path, rows: List[Dict[str, str]]) -> None:
    """Overwrite the CSV with the current in-memory student list."""
    path = Path(filepath)
    ok, _, error = safe_action(_write_rows, path, rows)
    if not ok:
        raise FileOperationError(error)
