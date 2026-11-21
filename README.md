# begonia-research — Xiaomi Redmi Note 8 Pro (begonia) research knowledge base

Research DB for porting Linux to the Xiaomi Redmi Note 8 Pro (`begonia`, MTK Helio G90T / MT6785):
firmware, kernels, hardware drivers, Ubuntu Touch, Droidian, postmarketOS, bootloader/recovery —
built as a reusable foundation for AI-assisted development (Ubuntu Touch first, then modern Halium/mainline).

**Research run: 2026-11-21 (single-day multi-agent run: 6 core researchers + augmentation waves).**
Status: core files 02–07 delivered; augmentation (per-ROM sources, host toolbox, guide index) in flight;
synthesis files (00, 01, 08, 09) + `sources.json` + `INDEX.md` pending final assembly.

## Deliverables (root)

| File | Content | Status |
|------|---------|--------|
| [02-FIRMWARE-HISTORY.md](02-FIRMWARE-HISTORY.md) | Official MIUI timeline (last build V12.5.15.0.RGGEUXM EEA, 2022-09-16), GSI era, native ROM catalog (crDroid = only official community ROM; LOS/Axion/EvolutionX unofficial up to Android 16) | delivered; source-inventory augmentation in flight |
| [03-KERNEL-HISTORY.md](03-KERNEL-HISTORY.md) | MiCode official drops (P=4.14.94, Q=4.14.141, R=4.14.186), AgentFabulous forks, LOS branch kernel table (17.1=4.14.194 … 24.0=4.19.325), Halium kernel, mainline forks (Dinolek 6.16.4/7.1, kalpakprod 7.3.4), toolchains | delivered |
| [04-HARDWARE-DRIVERS.md](04-HARDWARE-DRIVERS.md) | Component IDs from mainline DTS (NT36672A panels CSOT/Tianma, NVT-TS touch, MT6360, BMI120, STK3310, AK09918, Goodix FP, MT6359), GPU stacks (Panfrost/panvk vs kbase), per-OS support matrix | delivered |
| [05-UBUNTU-TOUCH.md](05-UBUNTU-TOUCH.md) | UT 24.04 noble port (Halium 10, kernel 4.14.141), active 2026-10, channels, issues, build system, upgrade-path analysis | delivered |
| [06-DROIDIAN-POSTMARKETOS.md](06-DROIDIAN-POSTMARKETOS.md) | pmOS mainline port (6.16.4-r0; what works/broken and why), live Droidian port ([begonia-linux org](https://github.com/begonia-linux), nightly 2026-11-15), architecture comparison | delivered |
| [07-RECOVERY-SAFETY.md](07-RECOVERY-SAFETY.md) | Unlock paths (Mi Unlock vs mtkclient), brick/unbrick recipe, backups, TWRP, vbmeta, partition map | delivered; toolbox augmentation in flight |
| 00 / 01 / 08 / 09 + `sources.json` + `INDEX.md` | Executive summary, source index, roadmap, open questions, master indexes | pending final synthesis |

## Data files

- [firmware-matrix.csv](firmware-matrix.csv) — official/custom/GSI ROM matrix (73 rows)
- [kernel-matrix.csv](kernel-matrix.csv) — 36 kernel tree/branch rows
- [hardware-support-matrix.csv](hardware-support-matrix.csv) — 33 component rows × 4 OS columns

## Context & governance ([_context/](_context))

- [CONTEXT.md](_context/CONTEXT.md) — shared context pack: verified device facts, canonical sources, evidence contract, tool-access verdicts. **Every collaborating agent starts here.**
- [REQUIREMENTS.md](_context/REQUIREMENTS.md) — numbered register of all user requirements (rows 1–23) with status.
- [SOURCE-CENSUS.md](_context/SOURCE-CENSUS.md) — verified census of source classes beyond GitHub/4PDA/XDA (Xiaomi mirrors, official TWRP, SourceForge, AndroidFileHost, Telegram, GSMarena, repair ecosystem).
- [CORRECTIONS.md](_context/CORRECTIONS.md) — queued factual corrections (C1: official TWRP page exists, updated 2026-11-20, maintainer theimpulson).
- [HUMAN-ASSISTS.md](_context/HUMAN-ASSISTS.md) — pages only a human browser can open (Anubis/bunny.net walls, registration-walled downloads), with instructions.

## Offline archive

[archive/index.html](archive/index.html) pairs every offline copy with its original URL (extracted-HTML canonical,
raw snapshots, small text artifacts under [archive/files/](archive/files)). Raw markdown twins: `_cache/`.
No multi-GB binaries are committed; fetch URLs are cited in the deliverables.

## Collaboration rules (ChatGPT and any agent)

1. Read [_context/CONTEXT.md](_context/CONTEXT.md) + [_context/REQUIREMENTS.md](_context/REQUIREMENTS.md) first.
2. Evidence contract: URL + title/author + date + permalink + verified-vs-inferred + confidence on every important claim; no invented data.
3. Research-only: no flashing, no untrusted scripts, no account registrations.
4. Bot-walls: real browser first → safe alternates (Wayback/API/extractor) → log to HUMAN-ASSISTS.md for the human; agents never solve CAPTCHAs or register.
5. One writer commits: agents write files, the orchestrator runs git (autosync every 15 min, attack-tested).
6. Update this README + linked context files at every milestone — a stale root is a defect (REQUIREMENTS row 22).

*Last updated: 2026-11-21 ~16:50 JST.*
