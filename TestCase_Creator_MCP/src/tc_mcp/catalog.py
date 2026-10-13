from __future__ import annotations

import csv
from collections import Counter, defaultdict
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

    def statistics(self) -> dict[str, Any]:
        fields, rows = self._read()
        return {
            "row_count": len(rows),
            "field_count": len(fields),
            "unique_values": {
                field: len({row[field].casefold() for row in rows if row[field]})
                for field in fields
            },
            "empty_values": {
                field: sum(not row[field] for row in rows) for field in fields
            },
        }

    def list_values(
        self,
        field: str,
        limit: int = DEFAULT_LIMIT,
        filters: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        result_limit = self._checked_limit(limit)
        fields, rows = self._read()
        if field not in fields:
            raise ValueError(f"Unknown catalog field: {field}")
        filter_values = filters or {}
        unknown_fields = sorted(set(filter_values) - set(fields))
        if unknown_fields:
            raise ValueError(f"Unknown catalog field(s): {', '.join(unknown_fields)}")
        normalized = {key: value.strip().casefold() for key, value in filter_values.items()}
        selected = [
            row for row in rows
            if all(row[key].casefold() == value for key, value in normalized.items())
        ]
        counts = Counter(row[field] for row in selected if row[field])
        values = [
            {"value": value, "count": count}
            for value, count in sorted(counts.items(), key=lambda item: item[0].casefold())
        ]
        return {
            "field": field,
            "total_unique": len(values),
            "returned": min(len(values), result_limit),
            "values": values[:result_limit],
        }

    def get_test_cases_by_ids(
        self, test_case_ids: list[str], limit: int = DEFAULT_LIMIT
    ) -> dict[str, Any]:
        result_limit = self._checked_limit(limit)
        if len(test_case_ids) > MAX_LIMIT:
            raise ValueError(f"test_case_ids cannot contain more than {MAX_LIMIT} values")
        fields, rows = self._read()
        id_field = "test_case_id" if "test_case_id" in fields else fields[0]
        wanted = {value.strip().casefold() for value in test_case_ids}
        matches = [row for row in rows if row[id_field].casefold() in wanted]
        found = {row[id_field].casefold() for row in matches}
        return {
            "id_field": id_field,
            "total_matches": len(matches),
            "returned": min(len(matches), result_limit),
            "missing_ids": [value for value in test_case_ids if value.strip().casefold() not in found],
            "results": matches[:result_limit],
        }

    def browse(self, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        result_limit = self._checked_limit(limit)
        if offset < 0:
            raise ValueError("offset must be zero or greater")
        _, rows = self._read()
        return {
            "total_rows": len(rows),
            "offset": offset,
            "returned": len(rows[offset : offset + result_limit]),
            "results": rows[offset : offset + result_limit],
        }

    def coverage_report(
        self,
        group_by: str = "module",
        filters: dict[str, str] | None = None,
        limit: int = DEFAULT_LIMIT,
    ) -> dict[str, Any]:
        result_limit = self._checked_limit(limit)
        fields, rows = self._read()
        if group_by not in fields:
            raise ValueError(f"Unknown catalog field: {group_by}")
        filter_values = filters or {}
        unknown_fields = sorted(set(filter_values) - set(fields))
        if unknown_fields:
            raise ValueError(f"Unknown catalog field(s): {', '.join(unknown_fields)}")
        normalized = {key: value.strip().casefold() for key, value in filter_values.items()}
        selected = [
            row for row in rows
            if all(row[key].casefold() == value for key, value in normalized.items())
        ]
        counts = Counter(row[group_by] or "(empty)" for row in selected)
        total = len(selected)
        groups = [
            {"value": value, "count": count, "percentage": round(count * 100 / total, 2)}
            for value, count in sorted(counts.items(), key=lambda item: item[0].casefold())
        ] if total else []
        return {
            "group_by": group_by,
            "total_rows": total,
            "group_count": len(groups),
            "returned": min(len(groups), result_limit),
            "groups": groups[:result_limit],
        }

    def duplicate_groups(
        self, fields: list[str] | None = None, limit: int = DEFAULT_LIMIT
    ) -> dict[str, Any]:
        result_limit = self._checked_limit(limit)
        catalog_fields, rows = self._read()
        selected_fields = fields or (["scenario"] if "scenario" in catalog_fields else catalog_fields)
        unknown_fields = sorted(set(selected_fields) - set(catalog_fields))
        if unknown_fields:
            raise ValueError(f"Unknown catalog field(s): {', '.join(unknown_fields)}")
        grouped: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
        for row in rows:
            key = tuple(row[field].strip().casefold() for field in selected_fields)
            grouped[key].append(row)
        duplicates = [
            {
                "values": {field: group[0][field] for field in selected_fields},
                "count": len(group),
                "test_case_ids": [row.get("test_case_id", "") for row in group[:MAX_LIMIT]],
                "omitted_test_case_ids": max(0, len(group) - MAX_LIMIT),
            }
            for group in grouped.values()
            if len(group) > 1
        ]
        return {
            "fields": selected_fields,
            "duplicate_groups": len(duplicates),
            "duplicate_rows": sum(item["count"] - 1 for item in duplicates),
            "returned": min(len(duplicates), result_limit),
            "groups": duplicates[:result_limit],
        }

    def deprecated_cases(self, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        result_limit = self._checked_limit(limit)
        fields, rows = self._read()
        status_field = next((field for field in fields if field.casefold() == "status"), None)
        if status_field is None:
            return {"status_field": None, "total_matches": 0, "returned": 0, "results": []}
        retired_states = {"deprecated", "retired", "obsolete", "inactive"}
        matches = [row for row in rows if row[status_field].strip().casefold() in retired_states]
        return {
            "status_field": status_field,
            "total_matches": len(matches),
            "returned": min(len(matches), result_limit),
            "results": matches[:result_limit],
        }

    def data_quality_report(self) -> dict[str, Any]:
        fields, rows = self._read()
        duplicate_ids = self.duplicate_groups(["test_case_id"], MAX_LIMIT) if "test_case_id" in fields else None
        duplicate_scenarios = self.duplicate_groups(["scenario"], MAX_LIMIT) if "scenario" in fields else None
        source_values = sorted({row["source"] for row in rows if row.get("source")}) if "source" in fields else []
        return {
            "row_count": len(rows),
            "empty_values": {field: sum(not row[field] for row in rows) for field in fields},
            "duplicate_id_groups": duplicate_ids["duplicate_groups"] if duplicate_ids else None,
            "duplicate_scenario_groups": duplicate_scenarios["duplicate_groups"] if duplicate_scenarios else None,
            "deprecated_cases": self.deprecated_cases(MAX_LIMIT)["total_matches"],
            "source_value_count": len(source_values),
            "source_values": source_values[:MAX_LIMIT],
        }

    def rank_test_cases(
        self,
        query: str,
        module: str | None = None,
        feature: str | None = None,
        priority: str | None = None,
        limit: int = DEFAULT_LIMIT,
    ) -> dict[str, Any]:
        result_limit = self._checked_limit(limit)
        fields, rows = self._read()
        normalized_query = query.strip().casefold()
        if not normalized_query:
            raise ValueError("query must not be empty")
        required_filters = {"module": module, "feature": feature, "priority": priority}
        required_filters = {key: value.strip().casefold() for key, value in required_filters.items() if value is not None}
        unknown_fields = sorted(set(required_filters) - set(fields))
        if unknown_fields:
            raise ValueError(f"Unknown catalog field(s): {', '.join(unknown_fields)}")
        tokens = [token for token in normalized_query.split() if token]
        ranked: list[tuple[int, dict[str, str]]] = []
        for row in rows:
            if not all(row[key].casefold() == value for key, value in required_filters.items()):
                continue
            searchable = " ".join(row[field].casefold() for field in fields)
            if normalized_query not in searchable and not any(token in searchable for token in tokens):
                continue
            score = sum(3 for field in fields if normalized_query in row[field].casefold())
            score += sum(1 for token in tokens if any(token in row[field].casefold() for field in fields))
            if "priority" in fields:
                score += {"p1": 4, "p2": 3, "p3": 2, "p4": 1}.get(row["priority"].casefold(), 0)
            if "status" in fields and row["status"].casefold() == "active":
                score += 2
            ranked.append((score, row))
        ranked.sort(key=lambda item: (-item[0], item[1].get("test_case_id", "")))
        results = [{"score": score, **row} for score, row in ranked[:result_limit]]
        return {
            "query": query,
            "total_matches": len(ranked),
            "returned": len(results),
            "results": results,
        }
