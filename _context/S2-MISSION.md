# S2 MISSION — assembler & indexer pass (begonia-research, 2026-11-21)

Repo: /Users/danielviktorovich/begonia-research (GitHub hub; orchestrator runs git — you do NOT).
Run this AFTER the editor-in-chief finishes (00/08/09 exist, CORRECTIONS.md items marked APPLIED).
≤24 tool calls. English. AI-first structures (fixed columns, stable names) + human-readable tops.
Hyperlink discipline: titled markdown links everywhere; no bare URLs in deliverables.

## READ FIRST
1. /Users/danielviktorovich/begonia-research/_context/REQUIREMENTS.md (rows 14, 19, 27, 28 are yours)
2. /Users/danielviktorovich/begonia-research/00-README.md, 08, 09 (editor's synthesis)
3. 02-07, 10-GUIDE-INDEX.md, _context/SOURCE-CENSUS.md, _context/OUTBOUND-LINKS.csv (1083 URLs)
4. /Users/danielviktorovich/AI-OS/.hermes/cache/scratch/begonia-recon/sources.jsonl (~137 records; append-only)

## YOUR DELIVERABLES

### D1 — sources.json (repo root)
Merge sources.jsonl (dedupe by URL; keep id/title/author/date/access/credibility/used_for; add found_in-file
if trivially derivable). Validate JSON. Also write 01-SOURCES.md: a human index grouped by class
(primary forum threads / official vendor / mirrors / repos / docs / community), each entry as titled link +
access status + date + credibility + which deliverables use it; incorporate SOURCE-CENSUS.md classes;
Limitations subsection (bot-walls, auth-walls, 404s, rate-limits — from REQUIREMENTS row 21/23 and census).

### D2 — INDEX.md (repo root, human) + index.json (repo root, machine)
INDEX.md: topic → file#section map covering EVERY major topic (per-ROM sources, kernels per branch,
hardware components, recovery landscape, unlock paths, unbrick, host toolchain, guides index, repair outlook…)
with links + one-line descriptions; a "how to search this repo" block (file map + ripgrep recipes:
`rg -n "Suzaku" --md`, `rg -i "twrp" *.csv`, column-meaning of each CSV, archive usage).
index.json: {"topics":[{"topic","file","section_anchor","key_sources":[urls],"status"}...], "generated": date}.

### D3 — archive/index.html REGENERATION
Include ALL archive files now present (rec-*, rec2-*, twrp-*, extracted-*, raw snapshots, files/).
Same table schema as the v1 index (offline copy | original | type | size | cited-in). Archive/orangefox:
add a snapshot of https://orangefox.download/device/begonia (curl works; HTML 143KB as of 2026-11-21) —
save as archive/orangefox-begonia.html first.

### D4 — 11-BLOBS-FIRMWARE-SOURCES.md (REQUIREMENTS 27)
For each artifact class: WHAT it is, WHERE the latest copy lives (repo+branch+path), HOW it is extracted,
RE-entry points. Classes (use facts already in the repo — do not invent):
- Vendor blobs/dumps: ZIDAN44 + ZyCromerZ vendor trees (39 MIUI build branches, see 02 §7) as source of
  /vendor blobs per MIUI build; MIUI fastboot ROMs (xiaomirom/xiaomifirmware mirrors; vendor.img inside);
  community dumps (SourceForge begoniadump, romdevelopers NVRAM/Dump — untrusted).
- Per-component firmware: touchscreen firmware packages (pmaports firmware-xiaomi-begonia-touchscreen,
  files nt36672a_begonia_{csot,tianma}.bin — from 04/06); GPU userspace (kbase + blob in Android trees vs
  Panfrost/panvk in pmOS); modem/NVRAM partitions (07's partition map: nvram/nvdata/nvcfg/modem_sting?...);
  audio params (mixer_paths etc. in vendor trees).
- Kernel-side: driver sources per component from the kernel trees in kernel-matrix.csv (mainline DTS names
  from 04); toolchains (AOSP Clang 21 for Suzaku, clang/LLVM=1 for pmOS, Ubuntu Clang 14 community).
- RE entry points: local host has Ghidra 12.1.4 + Craft Anything (verified installed by the owner); mtkclient
  for partition extraction; note research-only boundary: document, do not execute.
Include a "freshness" column: where the LATEST version of each artifact appears first (vendor tree branch
per MIUI build, mirror dates, etc.).

### D5 — _context/COVERAGE.md (REQUIREMENTS 28)
Inventory: per major topic → where covered (file + section) + completeness verdict (covered / partial / gap).
Gaps consolidated from: 02/03/07/10 not-found lists, OUTBOUND-LINKS dropped-with-reason categories worth a
second pass, indexer contradictions unresolved, HUMAN-ASSISTS rows. "What to search next": ranked list
(battery model & service docs for REQUIREMENTS 25; UART pinout; per-build ROM trees; Suzaku base version;
modem firmware versioning; OrangeFox build freshness; XDA threads #6/#7 in HUMAN-ASSISTS).
Include the same "how to search" recipes as INDEX.md (single source: write in INDEX.md, reference from here).

## RULES
Do NOT edit 02-07/10 or CORRECTIONS.md (editor's domain); if you spot a factual error there, log it as a
new numbered item in _context/CORRECTIONS.md instead. No git. Final message ≤300 words: files written,
sources.json record count after dedupe, top gaps found, anything unverifiable.

### D4b — Build & development recipes (ONE place; user request 2026-11-21 ~17:10)
Add a "Build & development recipes" section to 11-BLOBS-FIRMWARE-SOURCES.md (or a sibling section) covering
each build variant with steps + source links, marking verified-steps vs pointers:
- Android ROM build (LineageOS/AOSP trees + begonia local_manifests from 02 §7: crDroid/PE/Axion manifests
  found by the per-ROM inventory; breakfast/brunch begonia), incl. where the device/vendor/kernel repos come from.
- Kernel builds (trees from kernel-matrix.csv: AFB android-11.0, LOS lineage-24.0 4.19.325, Nova 4.14.356,
  Dinolek mt6785-mainline, kalpakprod 7.3.4; defconfigs begonia_user_defconfig etc. from 05/04; toolchains).
- Recovery builds (TWRP/OrangeFox trees; unified vs base-specific from 10-GUIDE-INDEX contradictions).
- postmarketOS (pmbootstrap init/install — Linux or VM only, cite 07 host matrix).
- Ubuntu Touch (Halium build per 05 build.sh/halium.yaml; host = Linux).
- Unbrick/rescue HARDWARE minimum (user question: "is a cable enough?"): per 07 evidence — mtkclient BROM
  path = USB-C cable + Linux/macOS/Windows host ONLY (megathread: "You do not need to take the phone apart
  to short any pins"); SP Flash Tool path = cable + Windows or Linux host (+bypass utility); UART debugging =
  optional USB-TTL adapter, begonia pinout NOT found (open question); paid remote service = alternative.
  Present as a compact table: method | host | extra hardware | source.

### D1b — source freshness ledger (REQUIREMENTS 36)
sources.json records get OBSERVATION-anchored stamps (NOT guarantees — the source may have changed after
we looked): `observed_at` (ISO 8601 UTC, when we last looked) and `source_last_change_observed` (the source's
own last-change date AS EXPOSED: repo pushed_at, page/oldid date, thread last-post date), plus
`observation_note` where framing needs words. Render in 01-SOURCES.md as: "As of <observed_at>, the last
change observed in this source was <date>" (RU: "на момент <observed_at> последнее зафиксированное изменение
источника — <date>"). INDEX.md items carry verified-at dates. Where a source exposes nothing date-like, set
source_last_change_observed: null — never invent.
