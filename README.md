# begonia-research — Xiaomi Redmi Note 8 Pro (begonia) research knowledge base

Research DB for the Xiaomi Redmi Note 8 Pro (`begonia`, MTK Helio G90T / MT6785) — built so an agent (or human)
unfamiliar with the device can start work from this repo alone. Dual purpose: **Linux porting** (Ubuntu Touch,
Droidian, postmarketOS, Halium/mainline — the north star is a modern Ubuntu Touch) AND the full **Android custom
ecosystem** (ROMs, kernels, recoveries — TWRP/OrangeFox/others —, firmware, vendor trees): every instruction,
artifact and forum finding for this device belongs here, with links to its sources/open code.

**Research run: 2026-11-21 (single-day multi-agent run: 6 core researchers + augmentation waves W13/W14/W15 +
synthesis + assembler).** Status: core files 02–07 delivered; augmentation (per-ROM sources, host toolbox, guide
index) delivered; corrections C1–C4 + C6 applied at the synthesis pass (C5 skip-verified — see
[_context/S1-MISSION.md](_context/S1-MISSION.md)); synthesis files [00-README.md](00-README.md),
[08-DEVELOPMENT-ROADMAP.md](08-DEVELOPMENT-ROADMAP.md), [09-OPEN-QUESTIONS.md](09-OPEN-QUESTIONS.md) delivered;
**final assembly delivered 2026-11-21** (assembler pass): 01 + sources.json + INDEX/index.json + 11 + 12 +
COVERAGE + regenerated archive index. `begonia-research.zip` is **dropped** per the REQUIREMENTS row 4 amendment
(2026-11-21): this GitHub repo itself is the distribution medium.

## Новое: происхождение ядер 4.14/4.19 и root-патчей

[20-KERNEL-419-ROOT-ECOSYSTEM-RU.md](20-KERNEL-419-ROOT-ECOSYSTEM-RU.md) — подробный русский разбор KSU/Non-KSU, Magisk, KernelSU-Next, SukiSU, APatch, SUSFS, AnyKernel3, реальных 4.19 деревьев MT6785 и проверенной NoVA build pipeline; [kernel-root-provenance.csv](kernel-root-provenance.csv) — источники, версии и степень проверки.

## Deliverables (root)

| File | Content | Status |
|------|---------|--------|
| [00-README.md](00-README.md) | Executive summary: device facts, 14 major findings, file map, limitations | delivered (synthesis 2026-11-21) |
| [01-SOURCES.md](01-SOURCES.md) | Consolidated source index: 8 titled-link classes + census classes + limitations, every entry observation-stamped | **delivered 2026-11-21 (assembler)** |
| [02-FIRMWARE-HISTORY.md](02-FIRMWARE-HISTORY.md) | Official MIUI timeline (last build V12.5.15.0.RGGEUXM EEA, 2022-09-16), GSI era, native ROM catalog (crDroid = only official community ROM; LOS/Axion/EvolutionX unofficial up to Android 16) | delivered; source inventory + Bliss OS 16.9 correction (C2) applied |
| [03-KERNEL-HISTORY.md](03-KERNEL-HISTORY.md) | MiCode official drops (P=4.14.94, Q=4.14.141, R=4.14.186), AgentFabulous forks, LOS branch kernel table (17.1=4.14.194 … 24.0=4.19.325), Halium kernel, mainline forks (Dinolek 6.16.4/7.1, kalpakprod 7.3.4), toolchains | delivered |
| [04-HARDWARE-DRIVERS.md](04-HARDWARE-DRIVERS.md) | Component IDs from mainline DTS (NT36672A panels CSOT/Tianma, NVT-TS touch, MT6360, BMI120, STK3310, AK09918, Goodix FP, MT6359), GPU stacks (Panfrost/panvk vs kbase), per-OS support matrix | delivered |
| [05-UBUNTU-TOUCH.md](05-UBUNTU-TOUCH.md) | UT 24.04 noble port (Halium 10, kernel 4.14.141), active 2026-10, channels, issues, build system, upgrade-path analysis | delivered |
| [06-DROIDIAN-POSTMARKETOS.md](06-DROIDIAN-POSTMARKETOS.md) | pmOS mainline port (6.16.4-r0; what works/broken and why), live Droidian port ([begonia-linux org](https://github.com/begonia-linux), nightly 2026-11-15), architecture comparison | delivered |
| [07-RECOVERY-SAFETY.md](07-RECOVERY-SAFETY.md) | Unlock paths (Mi Unlock vs mtkclient), brick/unbrick recipe, backups, TWRP, vbmeta, partition map, host workstation matrix | delivered; toolbox + recovery-landscape/official-TWRP corrections (C1, C3, C6) applied |
| [08-DEVELOPMENT-ROADMAP.md](08-DEVELOPMENT-ROADMAP.md) | P0/P1/P2 development paths, AI-assisted tooling, host matrix, device-repair outlook | delivered (synthesis 2026-11-21) |
| [09-OPEN-QUESTIONS.md](09-OPEN-QUESTIONS.md) | 10 dated contradictions, not-found ledger, human-check queue, ranked next steps | delivered (synthesis 2026-11-21) |
| [10-GUIDE-INDEX.md](10-GUIDE-INDEX.md) | Every mined guide/instruction post (4PDA t=974421/965629 + XDA via Wayback): permalinks, offline copies, confidence, used-by | delivered |
| [11-BLOBS-FIRMWARE-SOURCES.md](11-BLOBS-FIRMWARE-SOURCES.md) | Blob/firmware provenance per artifact class + freshness column + RE entry points + build recipes (ROM/kernel/recovery/pmOS/UT) + rescue-hardware minimum | **delivered 2026-11-21 (assembler)** |
| [12-SKILLS-AND-REUSE.md](12-SKILLS-AND-REUSE.md) | Skills/harnesses that built the repo, in-repo tools, authored reusable improvements, pre-release gaps | **delivered 2026-11-21 (assembler)** |
| [13-NETHUNTER-WIFI-EXTRAS.md](13-NETHUNTER-WIFI-EXTRAS.md) | NetHunter, Wi-Fi monitor mode (MT7663-family verdict), root/kernel harnesses, USB-HID surface, sibling-device portables | delivered (W13) |
| [14-MAINLINE-UPGRADE-PATH.md](14-MAINLINE-UPGRADE-PATH.md) | Mainline upgrade options A–D with defconfig-verified gap verdicts per tree | delivered (W14) |
| `15-RE-IMPROVEMENT-PLAN.md` (not yet on disk at packaging time) | RE-driven improvement plan (unpacking recipe, per-subsystem matrix, sequencing, test checklist) | **delivered 2026-11-21 (W15)** (W15 mission: [_context/W15-MISSION.md](_context/W15-MISSION.md)) |
| [16-ROOT-METHODS.md](16-ROOT-METHODS.md) | root-methods registry: Magisk / KernelSU-Next+SUSFS / APatch / SukiSU / custom kernels / mtkclient chain — matrix + begonia datapoints + TG channels | delivered 2026-11-21 (orchestrator, after W17 provider stall) |
| [INDEX.md](INDEX.md) | Human master topic map (topic → file#section) + "how to search this repo" (file map, ripgrep recipes, CSV columns, archive usage) | **delivered 2026-11-21 (assembler)** |
| [sources.json](sources.json) · [index.json](index.json) | Machine twins: 185 observation-stamped source records; 35-topic topic map | **delivered 2026-11-21 (assembler)** |

## Data files

- [firmware-matrix.csv](firmware-matrix.csv) — official/custom/GSI ROM matrix (74 data rows; 15 fixed columns; Bliss OS 16.9 row added at assembly)
- [kernel-matrix.csv](kernel-matrix.csv) — 36 kernel tree/branch rows
- [hardware-support-matrix.csv](hardware-support-matrix.csv) — 33 component rows × 4 OS columns

## Context & governance ([_context/](_context))

- [CONTEXT.md](_context/CONTEXT.md) — shared context pack: verified device facts, canonical sources, evidence contract, tool-access verdicts. **Every collaborating agent starts here.**
- [REQUIREMENTS.md](_context/REQUIREMENTS.md) — numbered register of all user requirements (rows 1–36) with status.
- [SOURCE-CENSUS.md](_context/SOURCE-CENSUS.md) — verified census of source classes beyond GitHub/4PDA/XDA (Xiaomi mirrors, official TWRP, SourceForge, AndroidFileHost, Telegram, GSMarena, repair ecosystem).
- [CORRECTIONS.md](_context/CORRECTIONS.md) — correction queue: C1–C4 + C6 **applied** at the 2026-11-21 synthesis pass (C5 skip-verified); row history kept in-file.
- [HUMAN-ASSISTS.md](_context/HUMAN-ASSISTS.md) — pages only a human browser can open (Anubis/bunny.net walls, registration-walled downloads), with instructions (7 rows).
- [COVERAGE.md](_context/COVERAGE.md) — topic coverage inventory, consolidated gap ledger, ranked "what to search next" (**delivered 2026-11-21, assembler**).
- Mission files (S1, S2, W13–W16) — the per-agent mission briefs; reusable templates ([12-SKILLS-AND-REUSE.md](12-SKILLS-AND-REUSE.md)).

## Offline archive

[archive/index.html](archive/index.html) pairs every offline copy with its original URL (offline copy | original | type | size | cited-in; regenerated 2026-11-21 with all 37 snapshots mapped — extracts, raw/Wayback HTML, `files/` text artifacts, OrangeFox device-page snapshot). Raw markdown twins: `_cache/`. No multi-GB binaries are committed; fetch URLs are cited in the deliverables.

## Tools

[tools/](tools) — [audit_bare_urls.py](tools/audit_bare_urls.py) (hyperlink-hygiene gate), [build_archive_html.sh](tools/build_archive_html.sh) (pandoc renderer), [gen_archive_index.py](tools/gen_archive_index.py) (archive index regenerator); usage in [tools/README.md](tools/README.md) and [12-SKILLS-AND-REUSE.md](12-SKILLS-AND-REUSE.md).

## Collaboration rules (ChatGPT and any agent)

1. Read [_context/CONTEXT.md](_context/CONTEXT.md) + [_context/REQUIREMENTS.md](_context/REQUIREMENTS.md) first; then [INDEX.md](INDEX.md) for one-hop navigation.
2. Evidence contract: URL + title/author + date + permalink + verified-vs-inferred + confidence on every important claim; no invented data; freshness = observation stamps (REQUIREMENTS row 36).
3. Research-only: no flashing, no untrusted scripts, no account registrations.
4. Bot-walls: real browser first → safe alternates (Wayback/API/extractor) → log to HUMAN-ASSISTS.md for the human; agents never solve CAPTCHAs or register.
5. One writer commits: agents write files, the orchestrator runs git (autosync every 15 min, attack-tested).
6. Update this README + linked context files at every milestone — a stale root is a defect (REQUIREMENTS row 22).

*Last updated: 2026-11-21T09:06:49Z (ISO 8601 UTC; all update stamps here use ISO 8601 UTC — see REQUIREMENTS row 34).*
