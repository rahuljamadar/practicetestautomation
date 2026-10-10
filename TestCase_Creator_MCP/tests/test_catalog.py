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
