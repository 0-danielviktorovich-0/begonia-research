# 12 — Skills & harnesses used to build this repo (and how to reuse them)

REQUIREMENTS row 30: this file documents the skills/harnesses that built the knowledge base — what each does, where it lives, how to install/reuse it, and which authored improvements are ready to copy. Public release is expected after first reuse tests; authored files listed here are sanitized (no credentials, no private paths beyond the harness layout described below).

## 1. Skills & harnesses at a glance

| Skill / harness | What it does | Where it lives | How to reuse |
|---|---|---|---|
| **Mission-driven multi-agent runs** | One research day = several focused agents (core researchers, augmentation waves W13/W14/W15, indexer, census, editor-in-chief, assembler), each with a written mission file: repo path, READ-FIRST list, deliverables, tool budget, output contract | [_context/S1-MISSION.md](../../../_context/S1-MISSION.md), [S2-MISSION.md](../../../_context/S2-MISSION.md), [W13-MISSION.md](../../../_context/W13-MISSION.md), [W14-MISSION.md](../../../_context/W14-MISSION.md), [W15-MISSION.md](../../../_context/W15-MISSION.md) | Copy a mission file as the template; keep the READ-FIRST + "do not touch other files" + ≤N-tool-calls discipline; the orchestrator (human or agent) runs git, workers only write files |
| **Context pack + evidence contract** | Every agent starts from one file: verified device facts, canonical sources, output contract, tool-access verdicts, format doctrine | [_context/CONTEXT.md](../../../_context/CONTEXT.md) | Clone the section skeleton (Device / Canonical sources / Output contract / Access verdicts / Rules) and fill per device |
| **Shared sources log → sources.json** | Append-only JSONL log (`id,url,title,author,date,access,credibility,used_for`), one object per fetch; at packaging it is deduped by URL and stamped **observation-anchored** freshness (`observed_at`, `source_last_change_observed`, `observation_note` — never invented) | log: harness scratch (`sources.jsonl`); merged output: [sources.json](../../../data/catalog/sources.json) + [01-SOURCES.md](../research/01-SOURCES.md) | Keep the JSONL append discipline during research; run the assembler merge at packaging. The observation-stamp merge is an **authored improvement of this run** (REQUIREMENTS row 36) |
| **CSV-first matrices** | Fixed-header CSVs as the machine layer (ROM matrix, kernel matrix, hardware support, outbound-links ledger) | [firmware-matrix.csv](../../../data/matrices/firmware-matrix.csv), [kernel-matrix.csv](../../../data/matrices/kernel-matrix.csv), [hardware-support-matrix.csv](../../../data/matrices/hardware-support-matrix.csv), [_context/OUTBOUND-LINKS.csv](../../../_context/OUTBOUND-LINKS.csv) | Headers are written in [CONTEXT.md §CSV headers](../../../_context/CONTEXT.md) — write exactly those columns; keep one row per artifact with source_url + confidence |
| **Bot-wall escalation policy** | When a fetcher is bot-blocked: real browser first → safe alternates (Wayback, API endpoints, server-side extractor) → human-assist log; agents never register accounts or solve CAPTCHAs | [_context/CONTEXT.md §Bot-block escalation](../../../_context/CONTEXT.md) + [_context/HUMAN-ASSISTS.md](../../../_context/HUMAN-ASSISTS.md) | Copy the policy block verbatim into any new research repo; maintain the assist table (URL / wall / why / filename) |
| **Offline archive pipeline** | Every important page gets a locally-openable copy: raw markdown twins in `_cache/` → pandoc HTML in `archive/` → index pairs original ↔ copy ↔ type ↔ size ↔ cited-in | [_cache/](../../../_cache), [archive/](../../../archive), tools below | See tools in §2; regenerate the index after adding snapshots |
| **Guide-index mining pattern** | Every instruction post in the target forums gets a row: entry, source, permalink, offline copy, confidence, used-by | [10-GUIDE-INDEX.md](../android/10-GUIDE-INDEX.md) | Reuse the table schema and the `showtopic=<id>&view=findpost&p=<pid>` permalink convention |
| **Per-ROM source inventory pattern** | Per ROM: kernel / device tree / vendor / manifest with verification method and explicit `not found (searched: …)` markers | [02 §7](../android/02-FIRMWARE-HISTORY.md) | Copy the table shape; keep "never invent" markers when trees are closed |
| **Corrections queue** | Factual errors are never silently overwritten — numbered items with was/new/applied-at stamps | [_context/CORRECTIONS.md](../../../_context/CORRECTIONS.md) | Append numbered items; editor applies and marks APPLIED with ISO 8601 UTC stamp |
| **Git single-writer autosync** | One writer commits (cron every 15 min): area-grouped typed commits, silent exit 0 when clean, LOUD non-zero on push failure / lock race / repo missing; workers never run git | harness-side script `autosync-push.sh` (see §3) | See §3 — the hardened v2 script is authored but **not yet committed to this repo**; add a sanitized copy before public release |
| **Browser-based discovery** | Real-browser sessions (Playwright-style control) for pages fetchers can't reach; verdicts documented per host | harness capability; verdicts in [_context/CONTEXT.md §Access verdicts](../../../_context/CONTEXT.md) | Follow the escalation policy above; log outcomes into the context pack so future agents don't re-test |

## 2. In-repo tools (verified present in `tools/`)

- [tools/audit_bare_urls.py](../../../tools/audit_bare_urls.py) — hyperlink-hygiene gate: reports URLs that appear as plain text instead of titled markdown links; exit 1 on any bare URL. Run: `python3 tools/audit_bare_urls.py [paths...]` (defaults to root `*.md` + `_context/*.md` + `archive/*.md`). Use as a pre-commit/CI gate for the "no bare URLs" rule (REQUIREMENTS row 14).
- [tools/build_archive_html.sh](../../../tools/build_archive_html.sh) — renders `_cache/*.md` extracts into standalone browser-openable HTML. Run: `./tools/build_archive_html.sh <cache_dir> <archive_dir> [title-prefix]` — requires **pandoc** in PATH.
- [tools/gen_archive_index.py](../../../tools/gen_archive_index.py) — regenerates [archive/index.html](../../../archive/index.html) from [archive/index-manifest.tsv](../../../archive/index-manifest.tsv) (`file<TAB>original_url<TAB>type<TAB>cited_in`); files on disk but missing from the manifest surface as UNMAPPED so nothing disappears silently. Run: `python3 tools/gen_archive_index.py [archive_dir]`.
- [tools/README.md](../../../tools/README.md) — short usage notes for the three tools.

## 3. Authored improvements ready for reuse

- **Hardened autosync script (v2/v3)** — area-grouped typed commits + cron push with attack-tested failure handling (restricted env, push-failure detection, lock-race guard, repo-missing guard, loud non-zero exits; REQUIREMENTS row 6). The repo's [README.md](../../../README.md) references `autosync-push.sh`; the script itself lives in the AI-OS harness and is **not committed here yet** — before public release, drop a sanitized copy into `tools/` and link it from this file (tracked as a packaging gap in [_context/COVERAGE.md](../../../_context/COVERAGE.md)).
- **Observation-stamped sources.json merge** (this run) — the dedupe + `observed_at` / `source_last_change_observed` / `observation_note` stamping rules are written in [01-SOURCES.md](../research/01-SOURCES.md) and REQUIREMENTS row 36; reusable for any research repo.
- **Topic-map pairing** (this run) — human [INDEX.md](../research/master-topic-index.md) ↔ machine [index.json](../../../data/catalog/index.json) with stable section anchors, so agents get one-hop retrieval (REQUIREMENTS rows 18/19).
- **Rescue-hardware-minimum framing** (this run) — "is a cable enough?" answered as a compact method/host/hardware table from existing evidence ([11 §7](../kernels/11-BLOBS-FIRMWARE-SOURCES.md)).

## 4. Before public release (tracked gaps)

1. Sanitized `autosync-push.sh` committed into `tools/` (§3).
2. LICENSE decision + privacy scan (REQUIREMENTS row 15) — owner decision, not yet executed.
3. Human-assist saves ([_context/HUMAN-ASSISTS.md](../../../_context/HUMAN-ASSISTS.md)) then re-index of `archive/human/`.
4. Repo move into `~/AI-OS/begonia-research` (REQUIREMENTS row 16) after research agents finish.

---
*Written by the assembler pass, 2026-11-21 (JST). Last updated: 2026-11-21T09:06:49Z (ISO 8601 UTC — REQUIREMENTS row 34).*
