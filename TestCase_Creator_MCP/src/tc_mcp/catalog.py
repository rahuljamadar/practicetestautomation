from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


DEFAULT_LIMIT = 20
MAX_LIMIT = 100


class Catalog:
    def __init__(self, csv_path: Path) -> None:
        self.csv_path = csv_path.expanduser()

    def _read(self) -> tuple[list[str], list[dict[str, str]]]:
        if not self.csv_path.is_file():
            raise FileNotFoundError(f"Catalog CSV not found: {self.csv_path}")

        with self.csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            fieldnames = reader.fieldnames
            if not fieldnames:
                raise ValueError("Catalog CSV is empty or has no header row")

            rows = [
                {field: (row.get(field) or "").strip() for field in fieldnames}
                for row in reader
            ]
        return fieldnames, rows

    @staticmethod
    def _checked_limit(limit: int) -> int:
        if limit < 1 or limit > MAX_LIMIT:
            raise ValueError(f"limit must be between 1 and {MAX_LIMIT}")
        return limit

    def summary(self) -> dict[str, Any]:
        try:
            fields, rows = self._read()
        except FileNotFoundError as error:
            return {
                "available": False,
                "path": str(self.csv_path),
                "message": str(error),
            }
        except ValueError as error:
            return {
                "available": False,
                "path": str(self.csv_path),
                "message": str(error),
            }

        return {
            "available": True,
            "path": str(self.csv_path),
            "row_count": len(rows),
            "fields": fields,
        }

    def search(self, query: str, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        result_limit = self._checked_limit(limit)
        normalized_query = query.strip().casefold()
        if not normalized_query:
            raise ValueError("query must not be empty")

        fields, rows = self._read()
        matches = [
            row
            for row in rows
            if any(normalized_query in row[field].casefold() for field in fields)
        ]
        return {
            "total_matches": len(matches),
            "returned": min(len(matches), result_limit),
            "results": matches[:result_limit],
        }

    def filter(
        self, filters: dict[str, str], limit: int = DEFAULT_LIMIT
    ) -> dict[str, Any]:
        result_limit = self._checked_limit(limit)
        fields, rows = self._read()
        unknown_fields = sorted(set(filters) - set(fields))
        if unknown_fields:
            raise ValueError(f"Unknown catalog field(s): {', '.join(unknown_fields)}")

        normalized_filters = {
            field: value.strip().casefold() for field, value in filters.items()
        }
        matches = [
            row
            for row in rows
            if all(
                row[field].casefold() == expected
                for field, expected in normalized_filters.items()
            )
        ]
        return {
            "total_matches": len(matches),
            "returned": min(len(matches), result_limit),
            "results": matches[:result_limit],
        }

    def get_test_cases(
        self, value: str, field: str | None = None, limit: int = DEFAULT_LIMIT
    ) -> dict[str, Any]:
        result_limit = self._checked_limit(limit)
        fields, rows = self._read()
        selected_field = field or fields[0]
        if selected_field not in fields:
            raise ValueError(f"Unknown catalog field: {selected_field}")

        normalized_value = value.strip().casefold()
        matches = [
            row
            for row in rows
            if row[selected_field].casefold() == normalized_value
        ]
        return {
            "field": selected_field,
            "value": value,
            "total_matches": len(matches),
            "returned": min(len(matches), result_limit),
            "results": matches[:result_limit],
        }
