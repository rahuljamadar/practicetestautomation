from __future__ import annotations

import json
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class CatalogOverlay:
    def __init__(self, path: Path) -> None:
        self.path = path.expanduser()

    def _read(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"annotations": {}, "exports": {}}
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Overlay must contain a JSON object")
        data.setdefault("annotations", {})
        data.setdefault("exports", {})
        return data

    def _write(self, data: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                "w", encoding="utf-8", newline="\n", dir=self.path.parent,
                delete=False,
            ) as temporary_file:
                json.dump(data, temporary_file, ensure_ascii=False, indent=2)
                temporary_file.write("\n")
                temporary_path = Path(temporary_file.name)
            temporary_path.replace(self.path)
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)

    def annotate(self, test_case_id: str, note: str, tags: list[str] | None = None) -> dict[str, Any]:
        data = self._read()
        annotation = {
            "note": note.strip(),
            "tags": [tag.strip() for tag in (tags or []) if tag.strip()],
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        data["annotations"][test_case_id] = annotation
        self._write(data)
        return {"test_case_id": test_case_id, **annotation, "overlay_path": str(self.path)}

    def export(self, name: str, rows: list[dict[str, str]]) -> dict[str, Any]:
        normalized_name = name.strip()
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", normalized_name):
            raise ValueError("name must contain only letters, numbers, underscores, or hyphens")
        data = self._read()
        record = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "row_count": len(rows),
            "results": rows,
        }
        data["exports"][normalized_name] = record
        self._write(data)
        return {"name": normalized_name, **record, "overlay_path": str(self.path)}