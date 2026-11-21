# Consolidated requirements register — begonia-research

All user requirements accumulated across this research run (2026-11-21), with status.
Every collaborating agent (Hermes subagents, ChatGPT, future contributors) must honor them.

| # | Requirement | Status |
|---|-------------|--------|
| 1 | Research-only: no device flashing, no execution of untrusted scripts | enforced |
| 2 | Evidence contract: every important claim carries URL, title/author, date, forum permalink, repo branch/commit, verified-vs-inferred flag, confidence (high/medium/low) | enforced (CONTEXT.md) |
| 3 | Never invent versions/URLs/compatibility; unfindable = explicit "not found (searched: …)"; inaccessible pages recorded as limitations | enforced (CONTEXT.md) |
| 4 | Deliverable structure: 00-README … 09-OPEN-QUESTIONS + firmware/kernel/hardware CSVs + sources.json + begonia-research.zip | pending final assembly |
| 5 | Private GitHub repo as shared hub for Hermes agents + ChatGPT: `0-danielviktorovich-0/begonia-research` | done (autosynced) |
| 6 | Auto-sync to GitHub: cron every 15m, hardened script v2 (attack-tested: restricted env, push failure, lock race, repo-missing; loud non-zero exits) | done |
| 7 | Study pinned/шапка posts of both 4PDA threads + XDA megathread post #1 | done (page-1 caches + extracts) |
| 8 | Include OFFICIAL Xiaomi kernel sources (MiCode/Xiaomi_Kernel_OpenSource: begonia-p-oss/q-oss/r-oss) alongside community trees | in kernel file (W2) + orchestrator final pass |
| 9 | Per-ROM SOURCE INVENTORY: for every ROM attach kernel source+branch, device tree, vendor tree, manifest, build docs — reusable for development | running (augmentation agent) |
| 10 | Catalog quality custom kernels (best work of their time) for reuse | running (kernel agent) + final pass |
| 11 | Offline archive: every important source page gets a locally-openable clickable copy (`archive/`, extracted→pandoc HTML canonical + raw HTML where clean + small text artifacts; NO multi-GB binaries) + index pairing original↔copy | v1 done, regenerated at final pass |
| 12 | Dev & recovery toolbox: host requirements per task × OS (Linux/macOS/Windows, cable, software), preserved 4PDA unbrick/unlock/root instructions | running (toolbox agent) |
| 13 | XDA instructions are also valid sources — check both forums, not only 4PDA | running + final pass |
| 14 | Hyperlinks: embed proper titled markdown links everywhere possible; no bare plain-text URLs in final docs | final pass (audit in progress) |
| 15 | Public-release readiness: repo may go public — clean navigation for an outside dev/agent, privacy scan, LICENSE decision, known-limitations section | final pass (checklist in this dir) |
| 16 | Project must live inside AI-OS: move `~/begonia-research` → `~/AI-OS/begonia-research` once research agents finish (workers hold absolute paths; move must not race their writes) | pending |
| 17 | Use the real browser when standard fetchers fail (done: XDA/4PDA attempts documented; blocked pages use Wayback; user's own browser noted as fallback) | documented (CONTEXT.md) |

## Known tool-access constraints (verified 2026-11-21)

- Live `xdaforums.com`: bunny.net challenge — blocked for web_extract AND headless browser; Wayback snapshots in `archive/`.
- Live 4PDA: HTTP 403 to plain curl; our fetcher (server-side extractor) passes — extracts in `_cache/` + `archive/`.
- `gitlab.nura.eco` / `wiki.nura.eco`: Anubis bot-check ("Making sure you're not a bot") for curl and headless browser; GitLab REST API works (JSON captured in `archive/files/`); wiki page readable via our extractor.
- GitHub REST API: unauthenticated 60 req/h shared pool exhausts fast — prefer `git ls-remote` + `raw.githubusercontent.com`.
| 18 | Full indexing: EVERY guide/instruction post across 4PDA + XDA threads is mined, re-checked, written down and indexed (10-GUIDE-INDEX.md with permalinks + offline copies); the research itself gets a master topic `INDEX.md` so important things are found in one hop | running (indexer agent) + final pass |
| 19 | PRIMARY optimization target: AI consumption; SECONDARY: human reading. Machine-readable structures (CSV/JSON, stable anchors, predictable filenames, sources.json, index.json topic map) wrapped in human-readable INDEX/README with clickable links | enforced at final packaging |
| 20 | Knowledge-base organization: ONE informational repo for all researches (no per-research repos); device work artifacts (kernels/ROMs/ports) live in their own upstream repos — the DB stores pointers + small text artifacts only. Inside the repo: single-source rule (a fact lives in exactly ONE file; everything else links to it) to prevent cross-file divergence; retrieval via INDEX.md + index.json + CSVs + grep-friendly naming. Future second research → decide repo naming (rename vs monorepo import) at packaging | recorded; final decision at packaging |
| 21 | Agent-vs-bot policy: when a fetcher is bot-blocked, agents FIRST try the real browser (isolated session), then safe workarounds (Wayback, API endpoints, extractor), including RE-skill-based approaches — and only after repeated failure escalate to the human (Даниил can solve a CAPTCHA by hand; assist-points listed in _context/HUMAN-ASSISTS.md). Source diversity: verify what exists BEYOND GitHub/4PDA/XDA (GitLab instances, SourceForge, kernel.org/lore, Xiaomi official mirrors, Telegram publics, TWRP mirrors) | recorded; census agent running |
| 22 | Root-file freshness: README.md + _context/CONTEXT.md (repo copy) + linked context files are refreshed at EVERY milestone (agent wave, new finding class, corrections) — a stale root file is treated as a defect; root must carry hyperlinks, never bare URLs | active (README rewritten 2026-11-21 ~16:45; CONTEXT repo-copy resynced) |
| 23 | Auth-walled downloads: some forums (4PDA attachments, XDA downloads) require registration to download files. Agents NEVER register accounts; such files are cited by URL + logged to _context/HUMAN-ASSISTS.md; the human may download with his own accounts into archive/human/ (small files commit, large ones stay URL-only) | active |
| 24 | SCOPE (user, 2026-11-21): the DB serves BOTH Linux porting AND Android custom development for this device — ROMs, kernels, recoveries (TWRP, OrangeFox, others), firmware, all custom-software work; every ecosystem artifact (instructions, files, forum data) belongs here. North star stays: modern Ubuntu Touch. During synthesis, re-review the outbound-links ledger for Android-ecosystem artifacts dropped as 'unrelated' and re-include on-topic ones | active |
| 25 | Device-repair outlook (POST-RESEARCH, not now): the owner's phone idles with battery drain — register battery model/health-check procedures, serviceability (what is fixable), and replacement-cost references so a future repair decision is data-driven. Becomes a section in 09/08 or a standalone note | registered |
| 26 | Source discipline: every firmware/kernel/custom/community artifact carries links to its GitHub/source; agents must ATTEMPT source discovery themselves and record open code only if actually published. Telegram: use t.me/s/<channel> web previews — no subscription required; pull useful data when channels surface in sources | active |
