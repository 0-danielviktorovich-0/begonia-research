#!/usr/bin/env python3
"""audit_bare_urls.py — hyperlink-hygiene gate for a Markdown research repo.

Reports, per file, URLs that appear as plain text (not wrapped in a titled markdown link).
Exit code 1 if any bare URL is found in the target files (useful as a CI/pre-commit gate).

Usage: python3 audit_bare_urls.py [paths...]   (default: README.md, docs/**/*.md and _context/*.md)
"""
import re
import sys
import glob

PAT_LINK = re.compile(r"\]\((https?://[^)]+)\)")
PAT_BARE = re.compile(r"(?<!\]\()(?<!href=\")(?<!<)(https?://[^\s\)\]>,\"'`]+)")


def audit(path: str):
    txt = open(path, encoding="utf-8", errors="replace").read()
    linked = PAT_LINK.findall(txt)
    # substring match (not prefix): a URL nested INSIDE a linked destination
    # (e.g. the real URL inside a web.archive.org href) is not plain text.
    bare = [u for u in PAT_BARE.findall(txt) if not any(u in dest for dest in linked)]
    return len(linked), bare


def main(paths):
    files = []
    for p in (paths or ["README.md", "docs/en/**/*.md", "docs/ru/**/*.md", "_context/*.md"]):
        files.extend(glob.glob(p, recursive=True))
    files = sorted(set(files))
    total_bare = 0
    for f in files:
        try:
            linked, bare = audit(f)
        except OSError as e:
            print(f"{f}: SKIP ({e})")
            continue
        total_bare += len(bare)
        suffix = f" | e.g. {' ; '.join(bare[:3])}" if bare else ""
        print(f"{f}: linked={linked} bare={len(bare)}{suffix}")
    print(f"\nTOTAL bare URLs: {total_bare}")
    sys.exit(1 if total_bare else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
