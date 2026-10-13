from __future__ import annotations

import asyncio
import json
from pathlib import Path

from fastmcp import Client

from tc_mcp.bootstrap import ensure_sample_catalog
from tc_mcp.catalog import Catalog
from tc_mcp.overlay import CatalogOverlay
from tc_mcp import server


def test_mcp_discovery_has_expected_read_only_inventory() -> None:
    async def discover() -> tuple[list, list, list]:
        async with Client(server.mcp) as client:
            return (
                await client.list_tools(),
                await client.list_resources(),
                await client.list_prompts(),
            )

    tools, resources, prompts = asyncio.run(discover())

    assert len(tools) == 19
    assert len(resources) == 4
    assert len(prompts) == 3
    assert "annotate_test_case" not in {tool.name for tool in tools}
    assert "export_test_cases" not in {tool.name for tool in tools}


def test_write_tools_require_explicit_enablement() -> None:
    server.mcp.enable(tags={"write"}, components={"tool"})

    async def discover() -> set[str]:
        async with Client(server.mcp) as client:
            return {tool.name for tool in await client.list_tools()}

    try:
        names = asyncio.run(discover())
        assert len(names) == 21
        assert {"annotate_test_case", "export_test_cases"} <= names
    finally:
        server.mcp.disable(tags={"write"}, components={"tool"})


def test_missing_default_csv_is_generated_once(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[1]
    csv_path = tmp_path / "vwo_5000_test_cases.csv"
    generator = project_root / "scripts" / "generate_sample_catalog.py"

    assert ensure_sample_catalog(csv_path, generator) is True
    assert Catalog(csv_path).summary()["row_count"] == 5000
    before = csv_path.read_bytes()
    assert ensure_sample_catalog(csv_path, generator) is False
    assert csv_path.read_bytes() == before


def test_overlay_stores_annotations_and_exports_separately(tmp_path: Path) -> None:
    overlay_path = tmp_path / "data" / "overlay.json"
    overlay = CatalogOverlay(overlay_path)

    overlay.annotate("TC-1", " Review later ", [" smoke ", ""])
    exported = overlay.export("login_cases", [{"test_case_id": "TC-1"}])
    stored = json.loads(overlay_path.read_text(encoding="utf-8"))

    assert exported["row_count"] == 1
    assert stored["annotations"]["TC-1"]["note"] == "Review later"
    assert stored["annotations"]["TC-1"]["tags"] == ["smoke"]
    assert stored["exports"]["login_cases"]["results"] == [{"test_case_id": "TC-1"}]


def test_overlay_export_name_cannot_escape_overlay(tmp_path: Path) -> None:
    overlay = CatalogOverlay(tmp_path / "overlay.json")

    try:
        overlay.export("../outside", [])
    except ValueError as error:
        assert "name must contain" in str(error)
    else:
        raise AssertionError("unsafe export name was accepted")