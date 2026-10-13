"""Download skills from the upstream SkillMasterclass repo into the local catalog.

The upstream repository layout is::

    skillmasterclass/skills/<phase-or-pack>/<skill>/SKILL.md

We fetch the repository tarball once, then copy every folder that contains a
``SKILL.md`` into ``skills/<relative path>``, preserving ``references/``,
``scripts/``, ``copilot/`` and asset sub-folders. Authored skills that live under
categories the upstream repo does not have (``08-`` / ``09-`` / ``10-``) are never
touched, so a re-sync cannot overwrite local work.
"""

from __future__ import annotations

import io
import shutil
import tarfile
import tempfile
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_REPO = "PramodDutta/skillmasterclass"
DEFAULT_BRANCH = "main"
DEFAULT_SUBTREE = "skillmasterclass/skills"
SKILL_FILENAME = "SKILL.md"

_TARBALL_URL = "https://codeload.github.com/{repo}/tar.gz/refs/heads/{branch}"
_USER_AGENT = "testskill-finder-mcp"


def _download(url: str, timeout: int = 120) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
        return response.read()


def _extract_archive(data: bytes, destination: Path) -> Path:
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        extract_filter = {"filter": "data"} if hasattr(tarfile, "data_filter") else {}
        archive.extractall(destination, **extract_filter)
    children = [path for path in destination.iterdir() if path.is_dir()]
    if len(children) != 1:
        raise RuntimeError("Unexpected archive layout: expected a single root folder")
    return children[0]


def sync_skills(
    skills_root: Path | str,
    repo: str = DEFAULT_REPO,
    branch: str = DEFAULT_BRANCH,
    subtree: str = DEFAULT_SUBTREE,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Download and install upstream skills. Returns a JSON-friendly report."""
    skills_root = Path(skills_root).expanduser()
    url = _TARBALL_URL.format(repo=repo, branch=branch)
    report: dict[str, Any] = {
        "source": url,
        "subtree": subtree,
        "skills_root": str(skills_root),
        "dry_run": dry_run,
        "added": [],
        "updated": [],
        "skipped": [],
        "errors": [],
    }

    data = _download(url)
    with tempfile.TemporaryDirectory() as temporary:
        extracted_root = _extract_archive(data, Path(temporary))
        source_dir = extracted_root / subtree
        if not source_dir.is_dir():
            raise RuntimeError(f"Subtree not found in archive: {subtree}")

        for skill_md in sorted(source_dir.rglob(SKILL_FILENAME)):
            folder = skill_md.parent
            relative = folder.relative_to(source_dir)
            destination = skills_root / relative
            if dry_run:
                report["skipped"].append(relative.as_posix())
                continue
            existed = destination.exists()
            try:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(folder, destination, dirs_exist_ok=True)
            except OSError as error:
                report["errors"].append(
                    {"skill": relative.as_posix(), "error": str(error)}
                )
                continue
            key = "updated" if existed else "added"
            report[key].append(relative.as_posix())

    report["added_count"] = len(report["added"])
    report["updated_count"] = len(report["updated"])
    report["skipped_count"] = len(report["skipped"])
    report["error_count"] = len(report["errors"])
    report["total"] = (
        report["added_count"] + report["updated_count"] + report["skipped_count"]
    )
    return report
