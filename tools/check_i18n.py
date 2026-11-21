#!/usr/bin/env python3
"""Validate bilingual research navigation and detect outdated translations.

Run from repository root: python3 tools/check_i18n.py
Standard library only. Validates structure/provenance, NOT linguistic quality.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
VALID_STATES = {"source", "full-draft", "full-reviewed", "digest", "directory-only", "missing"}
LINK = re.compile(r"!?(?<!\\)\[[^\]\n]*\]\(([^)]+)\)")
errors: list[str] = []
warnings: list[str] = []


def load_json(path: str):
    try:
        return json.loads((ROOT / path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        errors.append(f"{path}: cannot read valid JSON: {exc}")
        return {}


def check_path(raw: str, where: str) -> None:
    local = raw.split("#", 1)[0].split("?", 1)[0]
    if local and not (ROOT / local).exists():
        errors.append(f"{where}: target does not exist: {raw}")


def git_blob(path: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "hash-object", "--", path],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        warnings.append(f"Could not compute Git Blob SHA for {path}: {exc}")
        return None


catalog = load_json("i18n/catalog.json")
topics = load_json("i18n/topics.json")
canonical = load_json("data/catalog/index.json")

for path in [
    "README.md", "docs/ru/overview.md", "docs/en/index.md", "docs/ru/index.md",
    "i18n/README.md", "i18n/TERMINOLOGY.md"
]:
    check_path(path, "required navigation")

docs = catalog.get("documents", [])
if len(docs) != len({x.get("id") for x in docs}):
    errors.append("catalog documents: duplicated IDs")

for entry in docs:
    ident = entry.get("id", "unknown")
    original = entry.get("original", {})
    path = original.get("path", "")
    check_path(path, f"catalog {ident} original")
    if original.get("lang") not in {"en", "ru"}:
        errors.append(f"catalog {ident}: original language must be en or ru")
    local = entry.get("locales", {})
    for lang in ("en", "ru"):
        obj = local.get(lang)
        if obj is None:
            errors.append(f"catalog {ident}: {lang} locale missing")
            continue
        if obj.get("coverage") not in VALID_STATES:
            errors.append(f"catalog {ident}: invalid {lang} coverage: {obj.get('coverage')}")
        if obj.get("coverage") != "missing":
            check_path(obj.get("path", ""), f"catalog {ident} {lang}")
        source_sha = obj.get("derived_from_blob")
        if source_sha:
            actual = git_blob(path)
            if actual and actual != source_sha:
                errors.append(
                    f"STALE TRANSLATION {ident}/{lang}: source blob changed "
                    f"{source_sha} -> {actual}; update translation and revision marker"
                )
        if obj.get("coverage") == "full-reviewed" and not source_sha:
            errors.append(f"catalog {ident}/{lang}: full-reviewed requires pinned source blob")

canonical_ids = {x.get("topic", x.get("id")) for x in canonical.get("topics", [])}
translated = topics.get("topics", [])
translated_ids = [x.get("id") for x in translated]
if len(translated_ids) != len(set(translated_ids)):
    errors.append("i18n topic index contains duplicate IDs")
if canonical_ids != set(translated_ids):
    errors.append(
        f"topic mismatch: missing localized IDs {sorted(canonical_ids - set(translated_ids))}; "
        f"extra localized IDs {sorted(set(translated_ids) - canonical_ids)}"
    )
if topics.get("entries_count") != len(translated):
    errors.append("i18n topics.entries_count differs from actual array length")

for entry in translated:
    ident = entry.get("id", "unknown")
    for lang in ("en", "ru"):
        if not entry.get("title", {}).get(lang):
            errors.append(f"topic {ident}: blank {lang} title")
        check_path(entry.get("entry_point", {}).get(lang, ""), f"topic {ident} {lang}")
    check_path(entry.get("source_file", ""), f"topic {ident} original")


def check_markdown_links(relative: str) -> None:
    text = (ROOT / relative).read_text(encoding="utf-8")
    # Ignore fenced code examples; they may intentionally contain placeholder URLs.
    parts = re.split(r"^\s*\x60\x60\x60.*$", text, flags=re.MULTILINE)
    text = "".join(part for idx, part in enumerate(parts) if idx % 2 == 0)
    for m in LINK.finditer(text):
        target = m.group(1).strip().split(' "', 1)[0].strip("<>")
        if target.startswith(("https://", "http://", "mailto:", "tel:", "#", "data:")):
            continue
        path = unquote(urlsplit(target).path)
        if not path:
            continue
        if not (ROOT / relative).parent.joinpath(path).exists():
            line = text[: m.start()].count("\n") + 1
            errors.append(f"{relative}:{line}: broken local Markdown link to {target}")


localized = ["README.md", "docs/ru/overview.md", "docs/en/index.md", "docs/ru/index.md",
             "i18n/README.md", "i18n/TERMINOLOGY.md"]
localized += [str(p.relative_to(ROOT)) for p in (ROOT / "docs/en").rglob("*.md")]
localized += [str(p.relative_to(ROOT)) for p in (ROOT / "docs/ru").rglob("*.md")]
for path in sorted(set(localized)):
    if (ROOT / path).exists():
        check_markdown_links(path)

migration = load_json("data/catalog/path-migrations.json")
for entry in migration.get("entries", []):
    if entry.get("status") == "moved":
        check_path(entry["new_path"], "migration destination")
        if (ROOT / entry["old_path"]).exists():
            errors.append("obsolete path still exists: " + entry["old_path"])

if warnings:
    for warning in warnings:
        print("WARNING: " + warning)
if errors:
    for error in errors:
        print("ERROR: " + error)
    print(f"FAILED with {len(errors)} error(s).")
    sys.exit(1)
print(f"OK: {len(docs)} documents, {len(translated)} bilingual topics, "
      f"{len(set(localized))} localized Markdown entry points checked.")
print("Content and translation-equivalence review still requires a human/editor.")
