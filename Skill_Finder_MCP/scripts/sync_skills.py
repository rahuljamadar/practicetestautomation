"""CLI wrapper: download upstream skills into the local ``skills/`` catalog.

Usage::

    uv run python scripts/sync_skills.py [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from skillfinder_mcp.sync import (  # noqa: E402
    DEFAULT_BRANCH,
    DEFAULT_REPO,
    DEFAULT_SUBTREE,
    sync_skills,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download skills from the upstream repo")
    parser.add_argument(
        "--skills-dir",
        default=str(PROJECT_ROOT / "skills"),
        help="Destination skills folder (default: <project>/skills)",
    )
    parser.add_argument("--repo", default=DEFAULT_REPO, help="owner/name of the source repo")
    parser.add_argument("--branch", default=DEFAULT_BRANCH, help="Git branch to download")
    parser.add_argument(
        "--subtree",
        default=DEFAULT_SUBTREE,
        help="Path inside the repo that contains the skill folders",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Report what would change without writing"
    )
    arguments = parser.parse_args()

    report = sync_skills(
        arguments.skills_dir,
        repo=arguments.repo,
        branch=arguments.branch,
        subtree=arguments.subtree,
        dry_run=arguments.dry_run,
    )
    print(json.dumps(report, indent=2))
    if report["errors"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
