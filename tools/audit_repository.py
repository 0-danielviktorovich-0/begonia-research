#!/usr/bin/env python3
"""Offline integrity audit for the Begonia research repository.

Checks local Markdown links, section anchors, table geometry, machine-readable
indexes, and (optionally) preservation of the pre-refactor Git snapshot.
No third-party URLs are fetched; network reachability is a separate concern.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import html
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
BASE = "563a710658a6600896809fc0bbc21b84f768d6b0"
issues: list[str] = []
stats: Counter = Counter()

def error(message: str) -> None:
    issues.append(message)

def json_file(path: str):
    try:
        return json.loads((ROOT / path).read_text(encoding="utf-8"))
    except Exception as exc:
        error(f"cannot parse {path}: {exc}")
        return {}

def repo_file(path: str) -> bool:
    if not path:
        return False
    path = path.split("#", 1)[0]
    if path.startswith("/") or ".." in Path(path).parts:
        return False
    return (ROOT / path).is_file()

def heading_slug(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    text = text.replace(chr(96), "").replace("*", "").replace("~", "")
    text = re.sub(r"[^\w\- ]", "", text.lower(), flags=re.UNICODE)
    return text.strip().replace(" ", "-")

def headings(path: Path) -> set[str]:
    used: Counter = Counter()
    result = set()
    fenced = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"^\s*("+chr(96)*3+r"|~~~)", line):
            fenced = not fenced
            continue
        if fenced:
            continue
        found = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not found:
            continue
        slug = heading_slug(found.group(1))
        number = used[slug]
        used[slug] += 1
        result.add(slug + (f"-{number}" if number else ""))
    return result

def check_link(owner: Path, raw: str, lineno: int, anchor_map: dict[str, set[str]]) -> None:
    raw = raw.strip().strip("<>").strip()
    if not raw or raw.startswith(("mailto:", "tel:", "data:")):
        return
    raw = raw.split(' "', 1)[0].split(" '", 1)[0]
    parsed = urlsplit(raw)
    if parsed.scheme or raw.startswith("//"):
        return
    local_path = unquote(parsed.path)
    if local_path.startswith("/"):
        error(f"{owner.relative_to(ROOT)}:{lineno}: root-absolute link: {raw}")
        return
    target = (owner.parent / local_path).resolve() if local_path else owner.resolve()
    if not target.is_relative_to(ROOT):
        error(f"{owner.relative_to(ROOT)}:{lineno}: escapes repository: {raw}")
        return
    stats["links_checked"] += 1
    if not target.exists():
        error(f"{owner.relative_to(ROOT)}:{lineno}: missing link destination: {raw}")
        return
    if parsed.fragment and target.suffix.lower() == ".md" and target.is_file():
        relative = target.relative_to(ROOT).as_posix()
        if relative not in anchor_map:
            anchor_map[relative] = headings(target)
        anchor = unquote(parsed.fragment)
        stats["anchors_checked"] += 1
        if anchor not in anchor_map[relative]:
            error(f"{owner.relative_to(ROOT)}:{lineno}: unknown heading #{anchor} in {relative}")

def strip_fenced_and_inline(lines):
    fenced = False
    for number, line in enumerate(lines, 1):
        if re.match(r"^\s*("+chr(96)*3+r"|~~~)", line):
            fenced = not fenced
            continue
        if fenced:
            continue
        # Ignore inline code, but preserve non-code link destinations.
        line = re.sub(re.escape(chr(96)) + r"[^"+re.escape(chr(96))+r"]*"+re.escape(chr(96)), "", line)
        yield number, line

def audit_markdown() -> None:
    paths = [ROOT / "README.md", ROOT / "NOTICE.md"]
    paths.extend((ROOT / "docs").rglob("*.md"))
    paths.extend((ROOT / "_context").rglob("*.md"))
    paths.extend((ROOT / "_cache").rglob("*.md"))
    paths.extend((ROOT / "i18n").rglob("*.md"))
    paths.extend((ROOT / "tools").rglob("*.md"))
    paths.append(ROOT / "archive" / "README.md")
    paths.append(ROOT / "archive" / "files" / "mtkclient-README-USAGE.md")
    anchor_map: dict[str, set[str]] = {}
    for path in paths:
        if not path.is_file():
            continue
        stats["markdown_files"] += 1
        previous_columns = None
        content = path.read_text(encoding="utf-8").splitlines()
        for lineno, line in strip_fenced_and_inline(content):
            for link in re.findall(r"!?\[[^\]]*\]\(([^)]*)\)", line):
                check_link(path, link, lineno, anchor_map)
            ref = re.match(r"^\s*\[[^\]]+\]:\s*(\S+)", line)
            if ref:
                check_link(path, ref.group(1), lineno, anchor_map)
            if not path.is_relative_to(ROOT / "docs"):
                continue
            if not line.lstrip().startswith("|"):
                previous_columns = None
                continue
            # Keep escaped separators out of the table geometry count.
            columns = len(re.findall(r"(?<!\\)\|", line)) - 1
            if columns < 1:
                continue
            stats["table_rows"] += 1
            if previous_columns is not None and columns != previous_columns:
                error(f"{path.relative_to(ROOT)}:{lineno}: table columns {columns}, previous row {previous_columns}")
            previous_columns = columns

def audit_catalogs() -> None:
    source_data = json_file("data/catalog/sources.json")
    source_rows = source_data.get("sources", [])
    source_ids = [s.get("id") for s in source_rows]
    if len(source_ids) != len(set(source_ids)):
        error("data/catalog/sources.json: duplicate source IDs")
    if source_data.get("count") != len(source_rows):
        error("data/catalog/sources.json: count disagrees with sources length")
    stats["sources"] = len(source_rows)
    for s in source_rows:
        if not s.get("url", "").startswith(("https://", "http://")):
            error(f"source {s.get('id')}: invalid absolute URL")
    idx = json_file("data/catalog/index.json").get("topics", [])
    intl = json_file("i18n/topics.json")
    bilingual = intl.get("topics", [])
    ids = {t.get("topic") for t in idx}
    bidi_ids = {t.get("id") for t in bilingual}
    if len(ids) != len(idx) or len(bidi_ids) != len(bilingual) or ids != bidi_ids:
        error("topic catalog IDs are duplicated or disagree between data/catalog/index.json and i18n/topics.json")
    if intl.get("entries_count") != len(bilingual):
        error("i18n/topics.json: entries_count mismatch")
    anchor_map: dict[str, set[str]] = {}
    for entry in idx:
        file = entry.get("file")
        anchor = entry.get("section_anchor")
        if not repo_file(file):
            error(f"topic {entry.get('topic')}: missing owner file {file}")
            continue
        stats["topics"] += 1
        if anchor:
            if file not in anchor_map:
                anchor_map[file] = headings(ROOT / file)
            stats["catalog_anchors"] += 1
            if anchor not in anchor_map[file]:
                error(f"topic {entry.get('topic')}: unknown catalog anchor #{anchor} in {file}")
        for uri in entry.get("key_sources", []):
            if not uri.startswith(("https://", "http://")) and not repo_file(uri):
                error(f"topic {entry.get('topic')}: invalid key source {uri}")
    for entry in bilingual:
        file = entry.get("source_file")
        if not repo_file(file):
            error(f"bilingual topic {entry.get('id')}: missing source_file {file}")
        for lang in ("en", "ru"):
            ep = entry.get("entry_point", {}).get(lang)
            if not repo_file(ep):
                error(f"bilingual topic {entry.get('id')}: missing entry point {lang}: {ep}")
    catalog = json_file("i18n/catalog.json")
    docs = catalog.get("documents", [])
    if len(docs) != len({x.get("id") for x in docs}):
        error("i18n/catalog.json: duplicate document IDs")
    stats["documents"] = len(docs)
    for doc in docs:
        original = doc.get("original", {}).get("path")
        if not repo_file(original):
            error(f"document {doc.get('id')}: missing original path {original}")
        for lang, entry in doc.get("locales", {}).items():
            path = entry.get("path")
            if not repo_file(path):
                error(f"document {doc.get('id')}: missing {lang} path {path}")

def git_bytes(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)

def normalize_line(line: str) -> str:
    line = re.sub(r"\]\((?:[^)]*)\)", "](__link__)", line)
    line = line.replace("\\|", "|")
    return line.strip()

def audit_migration() -> None:
    manifest = json_file("data/catalog/path-migrations.json")
    try:
        subprocess.run(["git", "cat-file", "-e", BASE+"^{commit}"], cwd=ROOT, check=True, capture_output=True)
        old = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", BASE], cwd=ROOT, text=True).splitlines()
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        error(f"cannot read pinned pre-refactor Git commit {BASE}: {exc}")
        return
    prior = set(old)
    current = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts}
    entries = manifest.get("entries", [])
    moved = {e["old_path"]: e for e in entries if e.get("status") == "moved"}
    lost = sorted(prior - current - moved.keys())
    if lost:
        error(f"old files deleted without a migration entry: {lost}")
    stats["migrated_files"] = len(moved)
    for source, entry in moved.items():
        dest = entry["new_path"]
        if source not in prior or not repo_file(dest):
            error(f"missing migration source/destination: {source} -> {dest}")
            continue
        if (ROOT / source).exists():
            error(f"obsolete migrated path still present: {source}")
        old_content = git_bytes(BASE, source)
        old_sha = subprocess.check_output(["git", "rev-parse", f"{BASE}:{source}"], cwd=ROOT, text=True).strip()
        if entry.get("pre_move_blob_sha") != old_sha:
            error(f"source blob SHA mismatch: {source}")
        new_content = (ROOT / dest).read_bytes()
        if source.endswith(".csv") and old_content != new_content:
            error(f"CSV data changed during move: {source} -> {dest}")
        if source.endswith(".json") and source == "sources.json":
            baseline = json.loads(old_content).get("sources", [])
            current_sources = json.loads(new_content).get("sources", [])
            previous = {r["id"]: r["url"] for r in baseline}
            updated = {r["id"]: r["url"] for r in current_sources}
            lost_ids = [(i,u) for i,u in previous.items() if updated.get(i) != u]
            if lost_ids:
                error(f"source catalog lost/altered IDs or URLs: {lost_ids[:8]}")
        if source.endswith(".json") and source == "index.json":
            before = {r.get("topic") or r.get("id") for r in json.loads(old_content).get("topics", [])}
            after = {r["topic"] for r in json.loads(new_content).get("topics", [])}
            if before - after:
                error(f"topic index lost IDs: {sorted(before-after)}")
        if source.endswith(".md") and source not in {"docs/en/README.md", "docs/ru/README.md", "README.ru.md"}:
            before = Counter(normalize_line(x) for x in old_content.decode("utf-8").splitlines() if x.strip())
            after = Counter(normalize_line(x) for x in new_content.decode("utf-8").splitlines() if x.strip())
            difference = before-after
            if difference:
                examples = [f"{n}x {line[:105]}" for line,n in difference.items()]
                error(f"changed non-link content in move {source} -> {dest}: {examples[:4]}")
    # Full snapshots of navigation pages whose wording was deliberately rewritten.
    backups = {
        "README.md": "archive/legacy/README-main-before-refactor-2026-11-21.md",
        "README.ru.md": "archive/legacy/README-ru-before-refactor-2026-11-21.md",
        "docs/en/README.md": "archive/legacy/docs-en-index-before-refactor-2026-11-21.md",
        "docs/ru/README.md": "archive/legacy/docs-ru-index-before-refactor-2026-11-21.md",
    }
    for source, backup in backups.items():
        if not repo_file(backup):
            error(f"missing original navigation snapshot: {backup}")
        elif git_bytes(BASE, source) != (ROOT / backup).read_bytes():
            error(f"not byte-identical to original navigation: {backup}")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--migration", action="store_true", help="also compare with pinned original Git commit")
    args = parser.parse_args()
    audit_markdown()
    audit_catalogs()
    if args.migration:
        audit_migration()
    for issue in issues:
        print("ERROR: " + issue)
    print("Checked: " + ", ".join(f"{k}={v}" for k, v in sorted(stats.items())))
    print("External URL reachability, translated meaning and device boot/flashing are NOT checked.")
    if issues:
        print(f"FAILED: {len(issues)} issue(s)")
        return 1
    print("PASS: repository structure, internal references and catalogs")
    return 0

if __name__ == "__main__":
    sys.exit(main())
