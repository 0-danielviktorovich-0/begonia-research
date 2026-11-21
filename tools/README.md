# tools/ — the research-pipeline toolkit

Small, dependency-light scripts that power this repository's workflow, so any agent (or human) can
reproduce the whole system independently. Everything here is sanitized: no tokens, no personal paths
beyond `$HOME` fallbacks; third-party tools are NOT bundled — they are linked in
[12-SKILLS-AND-REUSE.md](../docs/en/tools/12-SKILLS-AND-REUSE.md) and [_context/SOURCE-CENSUS.md](../_context/SOURCE-CENSUS.md).

| Script | What it does | Needs |
|--------|--------------|-------|
| `autosync-push.sh` (not tracked in this repository) | Historical agent autosync mechanism referenced in research notes; source must be recovered and security-reviewed before running. Do not assume it is available. | bash, git (if restored) |
| [audit_bare_urls.py](audit_bare_urls.py) | Scans Markdown for URLs not wrapped in titled links (`](…)`), reports per-file counts — the hyperlink-hygiene gate (REQUIREMENTS row 14) | python3 |
| [build_archive_html.sh](build_archive_html.sh) | Converts `_cache/*.md` extracts into standalone, browser-openable HTML via pandoc (the canonical offline-archive layer) | pandoc |
| [gen_archive_index.py](gen_archive_index.py) | (Re)generates `archive/index.html` — pairs every offline copy with its original URL, type, size, snapshot date | python3 |

## Replicating the system (short version)

1. Start a repo with `_context/CONTEXT.md` (context pack: verified facts, evidence contract, tool-access
   verdicts) and `_context/REQUIREMENTS.md` (numbered, status-tracked user requirements — nothing stays
   conversation-only).
2. Cache raw source extracts in `_cache/` (the citation layer), render human copies into `archive/`
   (pandoc), keep small text artifacts in `archive/files/`, and index everything in `archive/index.html`.
3. Run parallel research agents with ≤20-call budgets that WRITE FILES ONLY; one orchestrator owns git.
4. Queue factual corrections in `_context/CORRECTIONS.md` (numbered, APPLIED-marked, ISO 8601 UTC stamps).
5. Do not schedule the historical `tools/autosync-push.sh` until its source exists and has been reviewed. If restored, test the happy path with remote read-back, restricted `env -i`, held lock, broken remote, missing repo, and parallel race.
6. Stamp everything with ISO 8601 UTC; observation-anchored freshness (`observed_at`,
   `source_last_change_observed`) so staleness is detectable and re-verification is triggered, never silent.

Full methodology lives in [_context/REQUIREMENTS.md](../_context/REQUIREMENTS.md) (rows 1–36) and
[_context/CONTEXT.md](../_context/CONTEXT.md); the skills layer that orchestrates this is described in
[12-SKILLS-AND-REUSE.md](../docs/en/tools/12-SKILLS-AND-REUSE.md).
