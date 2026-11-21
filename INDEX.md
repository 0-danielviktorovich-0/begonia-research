# INDEX — master topic map (begonia-research)

One-hop navigation for humans and agents. Every major topic → the file + section that owns it (single-source rule: the fact lives in exactly ONE file; everything else links there). Machine twin: [index.json](index.json). Source-level index: [01-SOURCES.md](01-SOURCES.md) + [sources.json](sources.json). Offline copies of every important source: [archive/index.html](archive/index.html).

All "verified" dates are observation stamps (REQUIREMENTS row 36): the day we last looked at the underlying source — **2026-11-21 for the whole research run** unless noted.

**Language:** [English topic directory](docs/en/README.md) · [Русский каталог](docs/ru/README.md) · [English README](README.md) · [README на русском](README.ru.md).

**Localized search:** [42 bilingual topic labels and aliases](i18n/topics.json) · [translation coverage](i18n/catalog.json) · [i18n/l10n policy](i18n/README.md). Stable topic IDs remain in English; search labels support EN/RU independently.

**New bilingual research routes:** [CFW, Non-CFW and GSI glossary](docs/en/19-rom-terminology.md) (full English draft; [RU original](19-ROM-TERMS-GLOSSARY-RU.md)); [Linux 4.19 and KernelSU](docs/en/20-kernel-root-ecosystem.md); [NoMount and mount backends](docs/en/21-nomount-and-mount-backends.md); [AI kernel porting and Play Integrity](docs/en/22-kernel-forward-port.md); [4.19 developer announcement and contact](23-419-TELEGRAM-OUTREACH.md). English pages 20–22 are **digests**, not complete translations.

**GitHub workflows:** [obsolete branch cleanup](.github/workflows/branch-cleanup.yml), [multilingual QA](.github/workflows/i18n-check.yml).

**[24 — Saikrishna's begonia 4.19 migration and source-stack audit](24-SAIKRISHNA1504-DEVICE-STACK-AUDIT.md)** — actual Nov 13–15 2026 device-tree commits, Android HAL/vendor/firmware/IMS/camera provenance, build-manifest mismatch, [21-repo machine register](saikrishna-source-inventory.csv), [русский конспект](docs/ru/24-saikrishna-source-audit.md).

## Topic map

| Topic | Where | What's there | Verified |
|---|---|---|---|
| Device overview & boot chain | [00-README.md](00-README.md) §The device | MT6785/Helio G90T facts, variants (begonia/begoniain), BROM→preloader→LK chain, no-test-point BROM entry | 2026-11-21 |
| Official MIUI history (per region/build) | [02-FIRMWARE-HISTORY.md](02-FIRMWARE-HISTORY.md) §1 + [firmware-matrix.csv](firmware-matrix.csv) rows 2-22 | Timeline 2019→2022, last build V12.5.15.0.RGGEUXM EEA (recovery 2022-09-16 / fastboot 2022-08-26), region table | 2026-11-21 |
| Vendor base every ROM rides | [02-FIRMWARE-HISTORY.md](02-FIRMWARE-HISTORY.md) §1.3, §7.1-7.2 | MIUI 12.5 vendor blobs; ZIDAN44 (15 branches) + ZyCromerZ (24 branches) dump trees | 2026-11-21 |
| GSI era (2019-2021) | [02-FIRMWARE-HISTORY.md](02-FIRMWARE-HISTORY.md) §2, §7.3 | Erfan/phh/TrebleDroid GSIs, vendor patches, per-build source gaps | 2026-11-21 |
| Native custom-ROM catalog (per-ROM sources) | [02-FIRMWARE-HISTORY.md](02-FIRMWARE-HISTORY.md) §3, §7 | crDroid official; LOS not official; Axion A16; Bliss 16.9; per-ROM kernel/device/vendor/manifest inventory with not-found markers | 2026-11-21 |
| ROM build recipes (manifests, breakfast/brunch) | [11-BLOBS-FIRMWARE-SOURCES.md](11-BLOBS-FIRMWARE-SOURCES.md) §6.1 | Where device/vendor/kernel repos come from per ROM family; verified steps vs pointers | 2026-11-21 |
| Kernels per branch | [03-KERNEL-HISTORY.md](03-KERNEL-HISTORY.md) §2, §4 + [kernel-matrix.csv](kernel-matrix.csv) (36 rows) | MiCode P/Q/R (4.14.94/141/186), AgentFabulous (12 branches), LOS lineage-17.1→24.0 (4.19.325), Nova 4.14.356, mainline forks 6.16.4/7.1/7.3.4 | 2026-11-21 |
| Kernel build recipes + toolchains | [11-BLOBS-FIRMWARE-SOURCES.md](11-BLOBS-FIRMWARE-SOURCES.md) §6.2, §3 | defconfigs (begonia_user_defconfig…), AOSP Clang 21 / LLVM=1 / community Clang 14, per-tree steps | 2026-11-21 |
| Mainline status & upgrade path | [14-MAINLINE-UPGRADE-PATH.md](14-MAINLINE-UPGRADE-PATH.md) + [03-KERNEL-HISTORY.md](03-KERNEL-HISTORY.md) §4 | No mt6785 DTS in Linus master; Dinolek/kalpakprod/pmOS trees; defconfig gap verdicts; option tree A-D | 2026-11-21 |
| Ubuntu Touch port | [05-UBUNTU-TOUCH.md](05-UBUNTU-TOUCH.md) | Halium 10.0 over 4.14.141; stable 24.04-1.4; broken mic/RTC/auto-brightness; build system (build.sh, halium.yaml) | 2026-11-21 |
| UT build recipe | [11-BLOBS-FIRMWARE-SOURCES.md](11-BLOBS-FIRMWARE-SOURCES.md) §6.5 + [05-UBUNTU-TOUCH.md](05-UBUNTU-TOUCH.md) §5 | halium-generic-adaptation-build-tools path, kernel begonia_user_defconfig | 2026-11-21 |
| Droidian port | [06-DROIDIAN-POSTMARKETOS.md](06-DROIDIAN-POSTMARKETOS.md) §2 | begonia-linux org, nightly 2026-11-15, mic works (vs UT) — key reuse lead | 2026-11-21 |
| postmarketOS port | [06-DROIDIAN-POSTMARKETOS.md](06-DROIDIAN-POSTMARKETOS.md) §1 | 6.16.4 mainline; works/broken matrix; MR !1909; pmbootstrap install path | 2026-11-21 |
| pmOS build recipe | [11-BLOBS-FIRMWARE-SOURCES.md](11-BLOBS-FIRMWARE-SOURCES.md) §6.4 + [07-RECOVERY-SAFETY.md](07-RECOVERY-SAFETY.md) §Host matrix | pmbootstrap = Linux-only (VM/WSL otherwise), android-recovery-zip + fastboot paths | 2026-11-21 |
| Hardware components (per-OS support) | [04-HARDWARE-DRIVERS.md](04-HARDWARE-DRIVERS.md) + [hardware-support-matrix.csv](hardware-support-matrix.csv) | DTS-derived IDs: NT36672A (CSOT/Tianma), Mali-G76 MC4, MT6359, MT6360, BMI120…; UT/Droidian/pmOS/Android columns | 2026-11-21 |
| Firmware/blob provenance (what lives where) | [11-BLOBS-FIRMWARE-SOURCES.md](11-BLOBS-FIRMWARE-SOURCES.md) §1-4 | Vendor dumps, touchscreen fw (nt36672a_begonia_{csot,tianma}.bin), GPU userspace, modem/NVRAM partitions, audio params — with freshness column | 2026-11-21 |
| Recovery landscape (TWRP/OrangeFox/PBRP/LR.Team) | [07-RECOVERY-SAFETY.md](07-RECOVERY-SAFETY.md) §3.0 + [10-GUIDE-INDEX.md](10-GUIDE-INDEX.md) §2 | Official TWRP page (2026-11-20), official OrangeFox page, per-base community builds; era contradictions kept | 2026-11-21 |
| Recovery build recipes | [11-BLOBS-FIRMWARE-SOURCES.md](11-BLOBS-FIRMWARE-SOURCES.md) §6.3 | TWRP/OrangeFox trees (HyperTeam, BitsAndBytes-dev), unified-vs-base-specific caveat | 2026-11-21 |
| Bootloader unlock paths | [07-RECOVERY-SAFETY.md](07-RECOVERY-SAFETY.md) §1-2 | Mi Unlock (168 h, Windows) vs `mtk da seccfg unlock` via BROM (no account); ARB question | 2026-11-21 |
| Unbrick / rescue | [07-RECOVERY-SAFETY.md](07-RECOVERY-SAFETY.md) §5-7 + [10-GUIDE-INDEX.md](10-GUIDE-INDEX.md) §5 | mtkclient full-flash restore, SP Flash Tool without service account, NVRAM/IMEI restore | 2026-11-21 |
| Rescue hardware minimum ("is a cable enough?") | [11-BLOBS-FIRMWARE-SOURCES.md](11-BLOBS-FIRMWARE-SOURCES.md) §7 | mtkclient = USB-C cable + host only; SPFT = + Windows/Linux; UART = optional, pinout unknown | 2026-11-21 |
| Backups before flashing | [07-RECOVERY-SAFETY.md](07-RECOVERY-SAFETY.md) §5 + partition map | preloader via `--parttype boot1`, `mtk rl/rf`, nvram/nvdata/nvcfg/persist list, GPT map | 2026-11-21 |
| Host toolchain per OS × task | [07-RECOVERY-SAFETY.md](07-RECOVERY-SAFETY.md) §Host workstation requirements + [08-DEVELOPMENT-ROADMAP.md](08-DEVELOPMENT-ROADMAP.md) §Host summary | adb/fastboot, Mi Unlock (Windows), mtkclient (native macOS), SPFT, pmbootstrap (Linux-only), Halium builds | 2026-11-21 |
| Guides index (every instruction post) | [10-GUIDE-INDEX.md](10-GUIDE-INDEX.md) | All mined guide posts from 4PDA t=974421/965629 + XDA, permalinks + offline copies + confidence | 2026-11-21 |
| Root / Magisk / harnesses | [10-GUIDE-INDEX.md](10-GUIDE-INDEX.md) §2 + [13-NETHUNTER-WIFI-EXTRAS.md](13-NETHUNTER-WIFI-EXTRAS.md) §3.1 | Magisk v31 thread, KernelSU-Next/SUSFS builder, patched vbmeta | 2026-11-21 |
| NetHunter & Wi-Fi monitor mode | [13-NETHUNTER-WIFI-EXTRAS.md](13-NETHUNTER-WIFI-EXTRAS.md) §1-2 | MT7663-family verdict, mt76 coverage, AkameKernel (NetHunter), external dongle recipe | 2026-11-21 |
| USB gadget / HID attack surface | [13-NETHUNTER-WIFI-EXTRAS.md](13-NETHUNTER-WIFI-EXTRAS.md) §3.4 | F_HID/configfs defconfig evidence per tree; what needs a rebuild | 2026-11-21 |
| RE entry points & improvement plan | [11-BLOBS-FIRMWARE-SOURCES.md](11-BLOBS-FIRMWARE-SOURCES.md) §4 + plan per [_context/W15-MISSION.md](_context/W15-MISSION.md) (15-RE-IMPROVEMENT-PLAN.md in flight) | Ghidra 12.1.4 + Craft Anything (owner host), mtkclient extraction, unpackers; per-subsystem RE matrix | 2026-11-21 |
| Device-repair outlook (battery) | [08-DEVELOPMENT-ROADMAP.md](08-DEVELOPMENT-ROADMAP.md) §Device-repair | Battery model unknown (do not guess), health-check procedures, serviceability verdicts | 2026-11-21 |
| Open questions & not-found ledger | [09-OPEN-QUESTIONS.md](09-OPEN-QUESTIONS.md) | 10 dated contradictions, explicit "searched, absent" list, human-assist queue | 2026-11-21 |
| 4.19 begonia port developer (Saikrishna1504) | [23-419-TELEGRAM-OUTREACH.md](23-419-TELEGRAM-OUTREACH.md) | Original post text, likely Nov 17 2026 date (unverified message ID), developer contacts, source-request draft | 2026-11-21 |
| Saikrishna1504 source stack: begonia 4.19, vendor, IMS and camera | [24-SAIKRISHNA1504-DEVICE-STACK-AUDIT.md](24-SAIKRISHNA1504-DEVICE-STACK-AUDIT.md) · [Russian digest](docs/ru/24-saikrishna-source-audit.md) · [CSV](saikrishna-source-inventory.csv) | Six audited Nov 2026 device-tree commits; current kernel 4.19 manifest mismatch; 21-repository inventory and 10+4 blob-patch leads | 2026-11-21 |
| Sources & freshness | [01-SOURCES.md](01-SOURCES.md) + [sources.json](sources.json) | 244 deduped records with observation stamps; census classes; limitations | 2026-11-21 |
| Coverage audit & next searches | [_context/COVERAGE.md](_context/COVERAGE.md) | Per-topic completeness verdicts + ranked "what to search next" | 2026-11-21 |
| Offline archive | [archive/index.html](archive/index.html) (+ [archive/README.md](archive/README.md)) | original ↔ copy ↔ type ↔ size ↔ cited-in for every snapshot | 2026-11-21 |

## How to search this repo

**File map.** `00-README` (executive summary) · `01-SOURCES` (source index) · `02` firmware/ROMs · `03` kernels · `04` hardware · `05` Ubuntu Touch · `06` pmOS/Droidian · `07` recovery/safety/host tools · `08` roadmap · `09` open questions · `10` guide index · `11` blobs/firmware provenance + build recipes · `13` NetHunter/Wi-Fi/hacks · `14` mainline path · `15` RE improvement plan (if present) · CSVs: `firmware-matrix.csv` (15 cols), `kernel-matrix.csv` (12 cols), `hardware-support-matrix.csv` · `_context/` governance (CONTEXT, REQUIREMENTS, SOURCE-CENSUS, CORRECTIONS, HUMAN-ASSISTS, OUTBOUND-LINKS.csv, mission files) · `archive/` offline copies · `_cache/` raw markdown twins · `sources.json` / `index.json` machine indexes.

**Ripgrep recipes** (run from repo root):

```bash
# find everything about a ROM/kernel/recovery by name
rg -n "Suzaku" --md
rg -n -i "orangefox" 07-RECOVERY-SAFETY.md 10-GUIDE-INDEX.md
# all guide posts for one topic class (permalinks)
rg -n "findpost&p=144" 10-GUIDE-INDEX.md
# CSV work: column meanings are in the header row of each CSV
rg -n -i "twrp" *.csv
rg -n "not found" 02-FIRMWARE-HISTORY.md   # explicit absence markers, never guessed
# every source touching one deliverable
rg -n "used by: 07" 01-SOURCES.md
# observation stamps (freshness protocol, REQUIREMENTS 36)
rg -n "source_last_change_observed" sources.json | head -40
# which archive snapshot covers a URL
rg -n "twrp" archive/index-manifest.tsv
```

**CSV column meanings.** `firmware-matrix.csv` (15): category, name, version, android_base, region_variant, maintainer, release_or_latest_date, status, kernel_source_url, device_tree_source_url, vendor_source_url, manifest_url, notes, source_url, confidence. `kernel-matrix.csv` (12): kernel_name, repo_url, linux_base, android_base, branch_or_ref, maintainer, last_commit_date, status, used_by, notes, source_url, confidence. `hardware-support-matrix.csv`: component + one status column per OS (Android/UT/Droidian/pmOS) + notes/variant columns. `_context/OUTBOUND-LINKS.csv` (6): url, found_in, category, disposition, reason, confidence — the full 1083-URL ledger with keep/drop decisions.

**Archive usage.** [archive/index.html](archive/index.html) pairs every offline copy with its original URL (columns: offline copy | original | type | size | cited-in). `*-extracted.html` = canonical pandoc extracts (what the deliverables quote); raw `*.html` = verbatim server/Wayback HTML; `archive/files/` = small text artifacts (scatter, deviceinfo, API JSON, mtkclient docs). Raw markdown twins of the same fetches: `_cache/`. Multi-GB binaries are intentionally not committed — fetch URLs are cited in the deliverables.

**Machine consumption.** [sources.json](sources.json) (244 records, observation-stamped), [index.json](index.json) (this topic map), stable section headings in every file, CSVs with fixed headers — written AI-first per REQUIREMENTS row 19.

---
*Generated by the assembler pass, 2026-11-21 (JST). Last updated: 2026-11-21T09:06:49Z (ISO 8601 UTC — REQUIREMENTS row 34).*
### Рут-методы
- [16-ROOT-METHODS.md](16-ROOT-METHODS.md) — матрица Magisk/KSU-Next/APatch/SukiSU/кастом-ядра/mtkclient; бега-датапоинты; TG-каналы; not-found ledger.
