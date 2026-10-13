"""Skill catalog: scan the ``skills/`` directory and expose search/read helpers.

The catalog is pure filesystem logic with no MCP or network dependency, so it can
be unit-tested directly. Every skill is a folder that contains a ``SKILL.md`` with
YAML frontmatter (``name`` / ``description`` / ``license`` / ``metadata``) followed
by a Markdown body.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


DEFAULT_LIMIT = 20
MAX_LIMIT = 100
SKILL_FILENAME = "SKILL.md"

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
_MAX_FILE_BYTES = 200_000


@dataclass
class Skill:
    """One discoverable skill parsed from a ``SKILL.md`` folder."""

    name: str
    description: str
    category: str
    pack: str | None
    phase: str | None
    license: str | None
    author: str | None
    version: str | None
    metadata: dict[str, Any]
    folder: Path
    files: list[str]
    frontmatter: dict[str, Any]
    body: str

    def index_entry(self) -> dict[str, Any]:
        """Compact representation used by list/search/index responses."""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "pack": self.pack,
            "phase": self.phase,
            "folder": self.folder.name,
            "file_count": len(self.files),
        }


@dataclass
class ScanReport:
    skills: dict[str, Skill] = field(default_factory=dict)
    errors: list[dict[str, str]] = field(default_factory=list)


def _split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.lstrip().startswith("---"):
        raise ValueError("missing YAML frontmatter")
    match = _FRONTMATTER_RE.match(text)
    if match is None:
        raise ValueError("malformed YAML frontmatter (no closing '---')")
    data = yaml.safe_load(match.group(1)) or {}
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a mapping")
    return data, text[match.end():].lstrip("\n")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _classify(skills_root: Path, folder: Path) -> tuple[str, str | None]:
    """Return (category, pack) derived from the folder path under ``skills_root``."""
    relative = folder.relative_to(skills_root)
    parts = relative.parts
    if len(parts) >= 3:
        return parts[0], parts[1]
    if len(parts) == 2:
        return parts[0], None
    return "(root)", None


class SkillCatalog:
    """Loads and queries the skills folder. Re-scans on demand."""

    def __init__(self, skills_root: Path | str) -> None:
        self.skills_root = Path(skills_root).expanduser()
        self._skills: dict[str, Skill] = {}
        self._errors: list[dict[str, str]] = []
        self._loaded = False

    # ------------------------------------------------------------------ loading
    @property
    def skills(self) -> dict[str, Skill]:
        if not self._loaded:
            self.load()
        return self._skills

    @property
    def errors(self) -> list[dict[str, str]]:
        if not self._loaded:
            self.load()
        return self._errors

    def load(self) -> "SkillCatalog":
        report = ScanReport()
        if self.skills_root.is_dir():
            for skill_md in sorted(self.skills_root.rglob(SKILL_FILENAME)):
                folder = skill_md.parent
                try:
                    skill = self._parse_skill(skill_md)
                except (ValueError, yaml.YAMLError) as error:
                    report.errors.append(
                        {
                            "path": str(skill_md.relative_to(self.skills_root)),
                            "error": str(error),
                        }
                    )
                    continue
                report.skills[skill.name.casefold()] = skill
        else:
            report.errors.append(
                {"path": str(self.skills_root), "error": "skills directory not found"}
            )
        self._skills = report.skills
        self._errors = report.errors
        self._loaded = True
        return self

    def refresh(self) -> "SkillCatalog":
        self._loaded = False
        return self.load()

    def _parse_skill(self, skill_md: Path) -> Skill:
        text = _read_text(skill_md)
        frontmatter, body = _split_frontmatter(text)
        folder = skill_md.parent
        metadata = frontmatter.get("metadata") or {}
        if not isinstance(metadata, dict):
            metadata = {}
        category, pack = _classify(self.skills_root, folder)
        name = str(frontmatter.get("name") or folder.name).strip()
        files = sorted(
            path.relative_to(folder).as_posix()
            for path in folder.rglob("*")
            if path.is_file()
        )
        return Skill(
            name=name,
            description=str(frontmatter.get("description") or "").strip(),
            category=category,
            pack=pack,
            phase=_opt_str(metadata.get("stlc-phase")),
            license=_opt_str(frontmatter.get("license")),
            author=_opt_str(metadata.get("author")),
            version=_opt_str(metadata.get("version")),
            metadata=metadata,
            folder=folder,
            files=files,
            frontmatter=frontmatter,
            body=body,
        )

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def _checked_limit(limit: int) -> int:
        if limit < 1 or limit > MAX_LIMIT:
            raise ValueError(f"limit must be between 1 and {MAX_LIMIT}")
        return limit

    def _ordered(self) -> list[Skill]:
        return sorted(self.skills.values(), key=lambda skill: skill.name.casefold())

    def _find(self, name: str) -> Skill:
        key = name.strip().casefold()
        skill = self.skills.get(key)
        if skill is None:
            raise ValueError(f"Unknown skill: {name}")
        return skill

    # ------------------------------------------------------------------ queries
    def summary(self) -> dict[str, Any]:
        by_category: dict[str, int] = {}
        by_pack: dict[str, int] = {}
        for skill in self.skills.values():
            by_category[skill.category] = by_category.get(skill.category, 0) + 1
            if skill.pack:
                by_pack[skill.pack] = by_pack.get(skill.pack, 0) + 1
        return {
            "available": bool(self.skills),
            "skills_root": str(self.skills_root),
            "total_skills": len(self.skills),
            "category_count": len(by_category),
            "pack_count": len(by_pack),
            "by_category": dict(sorted(by_category.items())),
            "by_pack": dict(sorted(by_pack.items())),
            "malformed": self.errors,
        }

    def list_categories(self) -> dict[str, Any]:
        by_category: dict[str, list[str]] = {}
        by_pack: dict[str, list[str]] = {}
        for skill in self._ordered():
            by_category.setdefault(skill.category, []).append(skill.name)
            if skill.pack:
                by_pack.setdefault(skill.pack, []).append(skill.name)
        return {
            "categories": [
                {"category": name, "count": len(skills), "skills": skills}
                for name, skills in sorted(by_category.items())
            ],
            "packs": [
                {"pack": name, "count": len(skills), "skills": skills}
                for name, skills in sorted(by_pack.items())
            ],
        }

    def list_skills(
        self,
        category: str | None = None,
        pack: str | None = None,
        limit: int = DEFAULT_LIMIT,
    ) -> dict[str, Any]:
        result_limit = self._checked_limit(limit)
        selected = [
            skill
            for skill in self._ordered()
            if (category is None or skill.category.casefold() == category.strip().casefold())
            and (pack is None or (skill.pack or "").casefold() == pack.strip().casefold())
        ]
        return {
            "total_matches": len(selected),
            "returned": min(len(selected), result_limit),
            "results": [skill.index_entry() for skill in selected[:result_limit]],
        }

    def filter_skills(
        self,
        category: str | None = None,
        pack: str | None = None,
        phase: str | None = None,
        limit: int = DEFAULT_LIMIT,
    ) -> dict[str, Any]:
        result_limit = self._checked_limit(limit)
        selected = [
            skill
            for skill in self._ordered()
            if (category is None or skill.category.casefold() == category.strip().casefold())
            and (pack is None or (skill.pack or "").casefold() == pack.strip().casefold())
            and (phase is None or (skill.phase or "").casefold() == phase.strip().casefold())
        ]
        return {
            "filters": {
                "category": category,
                "pack": pack,
                "phase": phase,
            },
            "total_matches": len(selected),
            "returned": min(len(selected), result_limit),
            "results": [skill.index_entry() for skill in selected[:result_limit]],
        }

    def rank(
        self,
        query: str,
        category: str | None = None,
        pack: str | None = None,
        limit: int = DEFAULT_LIMIT,
    ) -> dict[str, Any]:
        result_limit = self._checked_limit(limit)
        normalized = query.strip().casefold()
        if not normalized:
            raise ValueError("query must not be empty")
        tokens = [token for token in re.split(r"[\s\-_/]+", normalized) if token]

        scored: list[tuple[int, Skill, list[str]]] = []
        for skill in self._ordered():
            if category is not None and skill.category.casefold() != category.strip().casefold():
                continue
            if pack is not None and (skill.pack or "").casefold() != pack.strip().casefold():
                continue
            name = skill.name.casefold()
            description = skill.description.casefold()
            body = skill.body.casefold()
            score = 0
            if normalized in name:
                score += 20
            if normalized in description:
                score += 8
            if normalized in body:
                score += 3
            matched_tokens: list[str] = []
            for token in tokens:
                token_score = 0
                if token in name:
                    token_score += 6
                if token in description:
                    token_score += 3
                if token in body:
                    token_score += 1
                if token_score:
                    score += token_score
                    matched_tokens.append(token)
            if score:
                scored.append((score, skill, matched_tokens))

        scored.sort(key=lambda item: (-item[0], item[1].name.casefold()))
        results = [
            {**skill.index_entry(), "score": score, "matched_terms": matched}
            for score, skill, matched in scored[:result_limit]
        ]
        return {
            "query": query,
            "total_matches": len(scored),
            "returned": len(results),
            "results": results,
        }

    def recommend(self, task: str, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        ranked = self.rank(task, limit=min(self._checked_limit(limit), MAX_LIMIT))
        return {
            "task": task,
            "recommendation_note": (
                "Ranked by keyword relevance across skill name, description, and body. "
                "Review the returned skills before acting; this does not guarantee fit."
            ),
            "total_matches": ranked["total_matches"],
            "returned": ranked["returned"],
            "results": ranked["results"],
        }

    def get_skill(self, name: str) -> dict[str, Any]:
        skill = self._find(name)
        return {
            "name": skill.name,
            "category": skill.category,
            "pack": skill.pack,
            "phase": skill.phase,
            "license": skill.license,
            "author": skill.author,
            "version": skill.version,
            "folder": str(skill.folder),
            "files": skill.files,
            "frontmatter": skill.frontmatter,
            "content": _read_text(skill.folder / SKILL_FILENAME),
        }

    def get_skill_metadata(self, name: str) -> dict[str, Any]:
        skill = self._find(name)
        return {
            "name": skill.name,
            "description": skill.description,
            "category": skill.category,
            "pack": skill.pack,
            "phase": skill.phase,
            "license": skill.license,
            "author": skill.author,
            "version": skill.version,
            "files": skill.files,
            "frontmatter": skill.frontmatter,
        }

    def list_skill_files(self, name: str) -> dict[str, Any]:
        skill = self._find(name)
        return {
            "name": skill.name,
            "folder": str(skill.folder),
            "file_count": len(skill.files),
            "files": skill.files,
        }

    def get_skill_file(self, name: str, file: str) -> dict[str, Any]:
        skill = self._find(name)
        target = self._resolve_within(skill.folder, file)
        if not target.is_file():
            raise ValueError(f"File not found in skill '{skill.name}': {file}")
        raw = target.read_bytes()
        truncated = len(raw) > _MAX_FILE_BYTES
        text = raw[:_MAX_FILE_BYTES].decode("utf-8", errors="replace")
        return {
            "name": skill.name,
            "file": target.relative_to(skill.folder).as_posix(),
            "size_bytes": len(raw),
            "truncated": truncated,
            "content": text,
        }

    def search_in_skill(self, name: str, query: str, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        result_limit = self._checked_limit(limit)
        skill = self._find(name)
        needle = query.strip().casefold()
        if not needle:
            raise ValueError("query must not be empty")

        matches: list[dict[str, Any]] = []
        for relative in skill.files:
            path = skill.folder / relative
            try:
                text = _read_text(path)
            except OSError:
                continue
            for line_number, line in enumerate(text.splitlines(), start=1):
                if needle in line.casefold():
                    matches.append(
                        {"file": relative, "line": line_number, "text": line.strip()[:200]}
                    )
                    if len(matches) >= result_limit:
                        break
            if len(matches) >= result_limit:
                break
        return {
            "name": skill.name,
            "query": query,
            "total_matches": len(matches),
            "returned": len(matches),
            "matches": matches,
        }

    def index(self) -> list[dict[str, Any]]:
        return [skill.index_entry() for skill in self._ordered()]

    @staticmethod
    def _resolve_within(folder: Path, file: str) -> Path:
        candidate = Path(file)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise ValueError(f"Illegal file path: {file}")
        resolved = (folder / candidate).resolve()
        if resolved != folder.resolve() and folder.resolve() not in resolved.parents:
            raise ValueError(f"Illegal file path: {file}")
        return resolved


def _opt_str(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)
