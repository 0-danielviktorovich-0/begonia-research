#!/usr/bin/env bash
# build_archive_html.sh — render _cache/*.md extracts into standalone browser-openable HTML (archive layer).
# Usage: ./build_archive_html.sh <cache_dir> <archive_dir> [title-prefix]
# Requires: pandoc. Each <name>.md becomes archive/<name-without-hash>.html with an embedded title.
set -euo pipefail
CACHE="${1:?cache dir}"; OUT="${2:?archive dir}"; PREFIX="${3:-offline extract}"
command -v pandoc >/dev/null || { echo "pandoc not found in PATH" >&2; exit 2; }
mkdir -p "$OUT"
for md in "$CACHE"/*.md; do
  base=$(basename "$md" .md)
  # strip fetcher hash suffixes like 'wiki.nura.eco-6e9668ea25' -> keep readable slug
  slug=$(echo "$base" | sed -E 's/-[0-9a-f]{10,}$//')
  pandoc -s -t html5 --metadata title="$PREFIX: $slug" -o "$OUT/$slug.html" "$md"
  echo "$OUT/$slug.html  <-  $md"
done
