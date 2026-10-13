from __future__ import annotations

from pathlib import Path

import pytest

from skillfinder_mcp.catalog import SkillCatalog


def _write_skill(
    root: Path,
    relative: str,
    name: str,
    description: str,
    body: str = "",
) -> Path:
    folder = root / relative
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "SKILL.md").write_text(
        "---\n"
        f"name: {name}\n"
        "description: >-\n"
        f"  {description}\n"
        "license: MIT\n"
        "metadata:\n"
        "  author: Tester\n"
        "  stlc-phase: Test Design\n"
        "  version: 1.0.0\n"
        "---\n\n"
        f"# {name}\n\n{body}\n",
        encoding="utf-8",
    )
    return folder


@pytest.fixture
def skills_root(tmp_path: Path) -> Path:
    _write_skill(
        tmp_path,
        "01-requirement-analysis/req-analyzer",
        "req-analyzer",
        "Analyze requirements for gaps.",
    )
    _write_skill(
        tmp_path,
        "framework-packs/playwright-pack/pw-api-tester",
        "pw-api-tester",
        "Test APIs with Playwright's request context.",
        body="Use request.get and validate responses.",
    )
    _write_skill(
        tmp_path,
        "framework-packs/playwright-pack/pw-flaky-debugger",
        "pw-flaky-debugger",
        "Debug flaky Playwright tests.",
    )
    broken = tmp_path / "99-broken/broken-skill"
    broken.mkdir(parents=True, exist_ok=True)
    (broken / "SKILL.md").write_text("no frontmatter here", encoding="utf-8")
    return tmp_path


def test_scan_finds_skills_and_parses_frontmatter(skills_root: Path) -> None:
    catalog = SkillCatalog(skills_root).load()

    assert len(catalog.skills) == 3
    skill = catalog.get_skill("pw-api-tester")
    assert skill["category"] == "framework-packs"
    assert skill["pack"] == "playwright-pack"
    assert skill["phase"] == "Test Design"
    assert skill["license"] == "MIT"
    assert "request.get" in skill["content"]


def test_malformed_frontmatter_is_reported_not_fatal(skills_root: Path) -> None:
    catalog = SkillCatalog(skills_root).load()

    assert len(catalog.errors) == 1
    assert "broken-skill" in catalog.errors[0]["path"]


def test_search_ranks_name_match_first(skills_root: Path) -> None:
    result = SkillCatalog(skills_root).rank("playwright api")

    assert result["total_matches"] >= 1
    assert result["results"][0]["name"] == "pw-api-tester"
    assert "playwright" in result["results"][0]["matched_terms"]


def test_search_can_filter_by_pack(skills_root: Path) -> None:
    result = SkillCatalog(skills_root).rank("playwright", pack="playwright-pack")

    names = {item["name"] for item in result["results"]}
    assert names == {"pw-api-tester", "pw-flaky-debugger"}


def test_empty_query_and_bad_limit_are_rejected(skills_root: Path) -> None:
    catalog = SkillCatalog(skills_root).load()

    with pytest.raises(ValueError, match="query must not be empty"):
        catalog.rank("   ")
    with pytest.raises(ValueError, match="limit must be between"):
        catalog.rank("playwright", limit=101)


def test_list_skills_and_categories(skills_root: Path) -> None:
    catalog = SkillCatalog(skills_root).load()

    listing = catalog.list_skills(pack="playwright-pack")
    categories = catalog.list_categories()

    assert listing["total_matches"] == 2
    packs = {entry["pack"]: entry["count"] for entry in categories["packs"]}
    assert packs["playwright-pack"] == 2


def test_get_skill_file_reads_nested_file(skills_root: Path) -> None:
    folder = skills_root / "framework-packs/playwright-pack/pw-api-tester"
    references = folder / "references"
    references.mkdir()
    (references / "checklist.md").write_text("Check auth headers.", encoding="utf-8")
    catalog = SkillCatalog(skills_root).load()

    files = catalog.list_skill_files("pw-api-tester")
    content = catalog.get_skill_file("pw-api-tester", "references/checklist.md")

    assert "references/checklist.md" in files["files"]
    assert content["content"] == "Check auth headers."


def test_get_skill_file_rejects_path_traversal(skills_root: Path) -> None:
    catalog = SkillCatalog(skills_root).load()

    with pytest.raises(ValueError, match="Illegal file path"):
        catalog.get_skill_file("pw-api-tester", "../../../secrets.txt")
    with pytest.raises(ValueError, match="Illegal file path"):
        catalog.get_skill_file("pw-api-tester", "C:/Windows/win.ini")


def test_recommend_and_search_in_skill(skills_root: Path) -> None:
    catalog = SkillCatalog(skills_root).load()

    recommendation = catalog.recommend("how do I test an api endpoint")
    hits = catalog.search_in_skill("pw-api-tester", "request.get")

    assert recommendation["results"][0]["name"] == "pw-api-tester"
    assert recommendation["recommendation_note"]
    assert hits["matches"][0]["file"] == "SKILL.md"
