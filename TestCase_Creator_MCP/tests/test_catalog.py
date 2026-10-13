from pathlib import Path

import pytest

from tc_mcp.catalog import Catalog


@pytest.fixture
def catalog_path(tmp_path: Path) -> Path:
    path = tmp_path / "cases.csv"
    path.write_text(
        "id,module,scenario\n"
        "TC-1,Login,Valid credentials\n"
        "TC-2,Checkout,Declined card\n"
        "TC-3,Login,Locked account\n",
        encoding="utf-8",
    )
    return path


def test_summary_reports_fields_and_row_count(catalog_path: Path) -> None:
    summary = Catalog(catalog_path).summary()

    assert summary["available"] is True
    assert summary["row_count"] == 3
    assert summary["fields"] == ["id", "module", "scenario"]


def test_search_matches_any_field_case_insensitively(catalog_path: Path) -> None:
    result = Catalog(catalog_path).search("LOGIN", limit=1)

    assert result["total_matches"] == 2
    assert result["returned"] == 1
    assert result["results"][0]["id"] == "TC-1"


def test_filter_uses_exact_case_insensitive_values(catalog_path: Path) -> None:
    result = Catalog(catalog_path).filter({"module": "login"})

    assert result["total_matches"] == 2
    assert [row["id"] for row in result["results"]] == ["TC-1", "TC-3"]


def test_get_test_cases_defaults_to_first_field(catalog_path: Path) -> None:
    result = Catalog(catalog_path).get_test_cases("tc-2")

    assert result["field"] == "id"
    assert result["total_matches"] == 1
    assert result["results"][0]["scenario"] == "Declined card"


def test_missing_catalog_is_reported(catalog_path: Path) -> None:
    missing_path = catalog_path.parent / "missing.csv"

    result = Catalog(missing_path).summary()

    assert result["available"] is False
    assert "not found" in result["message"]


def test_unknown_filter_field_is_rejected(catalog_path: Path) -> None:
    with pytest.raises(ValueError, match="Unknown catalog field"):
        Catalog(catalog_path).filter({"priority": "P1"})


def test_limit_is_bounded(catalog_path: Path) -> None:
    with pytest.raises(ValueError, match="limit must be between"):
        Catalog(catalog_path).search("login", limit=101)


def test_statistics_and_value_counts(catalog_path: Path) -> None:
    catalog = Catalog(catalog_path)

    assert catalog.statistics()["row_count"] == 3
    assert catalog.list_values("module")["values"] == [
        {"value": "Checkout", "count": 1},
        {"value": "Login", "count": 2},
    ]


def test_browse_and_multi_id_lookup(catalog_path: Path) -> None:
    catalog = Catalog(catalog_path)

    page = catalog.browse(offset=1, limit=1)
    cases = catalog.get_test_cases_by_ids(["TC-1", "missing"])

    assert page["results"][0]["id"] == "TC-2"
    assert cases["missing_ids"] == ["missing"]
    assert [row["id"] for row in cases["results"]] == ["TC-1"]


def test_coverage_report_uses_confirmed_fields(catalog_path: Path) -> None:
    coverage = Catalog(catalog_path).coverage_report("module")

    assert coverage["total_rows"] == 3
    assert sum(group["percentage"] for group in coverage["groups"]) == 100


def test_quality_report_and_duplicate_scenarios(tmp_path: Path) -> None:
    path = tmp_path / "quality.csv"
    path.write_text(
        "test_case_id,module,scenario,status\n"
        "TC-1,Login,Valid credentials,Active\n"
        "TC-2,Login,Valid credentials,Deprecated\n"
        "TC-2,Checkout,Declined card,Active\n",
        encoding="utf-8",
    )
    catalog = Catalog(path)

    duplicates = catalog.duplicate_groups(["scenario"])
    quality = catalog.data_quality_report()
    deprecated = catalog.deprecated_cases()

    assert duplicates["duplicate_groups"] == 1
    assert duplicates["duplicate_rows"] == 1
    assert quality["duplicate_id_groups"] == 1
    assert quality["deprecated_cases"] == 1
    assert deprecated["results"][0]["test_case_id"] == "TC-2"


def test_rank_test_cases_is_bounded_and_deterministic(catalog_path: Path) -> None:
    result = Catalog(catalog_path).rank_test_cases("login")

    assert result["total_matches"] == 2
    assert result["results"][0]["id"] == "TC-1"
    assert result["results"][0]["score"] >= result["results"][1]["score"]


def test_high_cardinality_reports_and_id_batches_are_bounded(tmp_path: Path) -> None:
    path = tmp_path / "many_cases.csv"
    path.write_text(
        "test_case_id,scenario\n"
        + "".join(f"TC-{index:03d},Repeated scenario\n" for index in range(105)),
        encoding="utf-8",
    )
    catalog = Catalog(path)

    coverage = catalog.coverage_report("test_case_id", limit=1)
    duplicates = catalog.duplicate_groups(limit=1)["groups"][0]

    assert coverage["group_count"] == 105
    assert coverage["returned"] == 1
    assert duplicates["count"] == 105
    assert len(duplicates["test_case_ids"]) == 100
    assert duplicates["omitted_test_case_ids"] == 5
    with pytest.raises(ValueError, match="cannot contain more than 100"):
        catalog.get_test_cases_by_ids(["TC-001"] * 101)
