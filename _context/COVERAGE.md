# COVERAGE — what this DB contains, what it lacks, what to search next (2026-11-21)

REQUIREMENTS row 28. Verdicts: **covered** = the topic has an owning file+section with sourced claims; **partial** = owned but with named holes; **gap** = explicitly not established (never guessed). How to search the repo: single source in [INDEX.md §How to search this repo](../docs/en/research/master-topic-index.md#how-to-search-this-repo) (file map, ripgrep recipes, CSV column meanings, archive usage) — not duplicated here.

## 1. Topic inventory

| Topic | Covered in | Verdict | Note |
|---|---|---|---|
| Device overview, boot chain, variants | [00-README §The device](../docs/en/research/00-README.md) | covered | BROM-without-test-point cross-verified |
| Official MIUI timeline (regions, builds) | [02 §1](../docs/en/android/02-FIRMWARE-HISTORY.md) + [firmware-matrix.csv](../data/matrices/firmware-matrix.csv) | covered | regional last-build date mismatches kept open ([09 #9](../docs/en/research/09-OPEN-QUESTIONS.md)) |
| Vendor base & per-build dumps | [02 §1.3/§7.1](../docs/en/android/02-FIRMWARE-HISTORY.md), [11 §1](../docs/en/kernels/11-BLOBS-FIRMWARE-SOURCES.md) | covered | dump branches named per MIUI build; binary mirrors cross-agree |
| GSI era | [02 §2/§7.3](../docs/en/android/02-FIRMWARE-HISTORY.md) | partial | per-build sources for closed GSIs **not found** (searched: exact posts + GitHub) |
| Native custom-ROM catalog | [02 §3](../docs/en/android/02-FIRMWARE-HISTORY.md) | covered | crDroid official / LOS not / Axion A16 / Bliss 16.9 row added to CSV |
| Per-ROM source inventory | [02 §7](../docs/en/android/02-FIRMWARE-HISTORY.md) | partial | verified for crDroid 8-10, PE 11-14, EX ten-era, Axion device, LOS kernel; **not found**: crDroid A10 trees, LOS 20/22.2/23.x per-build trees, PE vendor, EX manifest, Axion vendor/manifest, all OEM-port trees ([02 §7.15](../docs/en/android/02-FIRMWARE-HISTORY.md)) |
| Kernels per branch | [03 §2](../docs/en/kernels/03-KERNEL-HISTORY.md) + [kernel-matrix.csv](../data/matrices/kernel-matrix.csv) | covered | Suzaku V2 base version + repo unknown; HYDRA PLUS no tree; ishan-parihar repo 404 ([09 §2](../docs/en/research/09-OPEN-QUESTIONS.md)) |
| Mainline Linux effort | [03 §4](../docs/en/kernels/03-KERNEL-HISTORY.md), [14](../docs/en/kernels/14-MAINLINE-UPGRADE-PATH.md) | covered | driver-level gaps documented per subsystem (audio/modem/camera/sensors); defconfig evidence verified |
| Ubuntu Touch | [05](../docs/en/linux/05-UBUNTU-TOUCH.md) | covered | VoLTE/A-GPS are global Halium-era issues; mic broken → [09 #5](../docs/en/research/09-OPEN-QUESTIONS.md) |
| Droidian | [06 §2](../docs/en/linux/06-DROIDIAN-POSTMARKETOS.md) | covered | mic works — key reuse lead; porter-claimed matrix (medium) |
| postmarketOS | [06 §1](../docs/en/linux/06-DROIDIAN-POSTMARKETOS.md) | covered | rendered pmaports pages behind Anubis wall (HUMAN-ASSISTS 1-2); API JSON captured |
| Hardware components | [04](../docs/en/kernels/04-HARDWARE-DRIVERS.md) + [hardware-support-matrix.csv](../data/matrices/hardware-support-matrix.csv) | partial | BMI120 contradiction ([09 #6](../docs/en/research/09-OPEN-QUESTIONS.md)), MT6360 vs SMB1351 duty split ([09 #7](../docs/en/research/09-OPEN-QUESTIONS.md)), Wi-Fi chip suspected MT7663-family but **not pinned** ([13 §1.1](../docs/en/android/13-NETHUNTER-WIFI-EXTRAS.md)) |
| Firmware/blob provenance | [11 §1-5](../docs/en/kernels/11-BLOBS-FIRMWARE-SOURCES.md) | covered | freshness column = observations as of 2026-11-21 |
| Recovery landscape | [07 §3.0](../docs/en/recovery/07-RECOVERY-SAFETY.md), [10 §2](../docs/en/android/10-GUIDE-INDEX.md) | partial | official TWRP + OrangeFox listings verified; **installed-build freshness unverified**; which-TWRP-for-which-base unresolved ([09 #2](../docs/en/research/09-OPEN-QUESTIONS.md)); twrp.me index anomaly ([09 #10](../docs/en/research/09-OPEN-QUESTIONS.md)) |
| Bootloader unlock | [07 §1-2](../docs/en/recovery/07-RECOVERY-SAFETY.md) | covered | ARB-absent claim rests on one low-confidence source ([09 #3](../docs/en/research/09-OPEN-QUESTIONS.md)) |
| Unbrick / rescue | [07 §5-7](../docs/en/recovery/07-RECOVERY-SAFETY.md), [10 §5-6](../docs/en/android/10-GUIDE-INDEX.md), [11 §7](../docs/en/kernels/11-BLOBS-FIRMWARE-SOURCES.md) | covered | dedicated 4PDA SPFT unbrick guide **not found** (searched: all cached pages); vbmeta method comparison open ([09 #4](../docs/en/research/09-OPEN-QUESTIONS.md)) |
| Host toolchain per OS × task | [07 §Host workstation](../docs/en/recovery/07-RECOVERY-SAFETY.md), [08 §Host summary](../docs/en/linux/08-DEVELOPMENT-ROADMAP.md) | covered | one brew formula URL returned 404 to our fetcher (flagged in-file, medium) |
| Guides (every instruction post) | [10](../docs/en/android/10-GUIDE-INDEX.md) | partial | XDA evidence ceiling = 2026-04-15 Wayback snapshot; live-thread re-mine pending human browser |
| NetHunter / Wi-Fi monitor | [13 §1-2](../docs/en/android/13-NETHUNTER-WIFI-EXTRAS.md) | covered (negatives) | no internal monitor-mode patch; no official NetHunter begonia support; AkameKernel = the one community kernel |
| USB gadget / HID | [13 §3.4](../docs/en/android/13-NETHUNTER-WIFI-EXTRAS.md) | covered | F_HID=y verified in 3 trees; LOS config filename open |
| UEFI (Mu-Silicium) | [02 §3.9/§7.14](../docs/en/android/02-FIRMWARE-HISTORY.md) | covered | begonia port sources unpublished upstream (verified absence) |
| Repair outlook (battery) | [08 §Device-repair](../docs/en/linux/08-DEVELOPMENT-ROADMAP.md) | gap (by design) | REQUIREMENTS row 25 = post-research; battery model unknown, first software step registered |
| Modem/baseband firmware versioning | [02 line 56](../docs/en/android/02-FIRMWARE-HISTORY.md), [11 §2](../docs/en/kernels/11-BLOBS-FIRMWARE-SOURCES.md) | gap | no consulted source states begonia baseband versions |
| UART pinout / test points | [07 §4](../docs/en/recovery/07-RECOVERY-SAFETY.md) | gap | no device-specific source found; schematic artifact exists on untrusted mirror only |
| Offline archive | [archive/index.html](../archive/index.html) | covered | regenerated 2026-11-21; all snapshots paired |

## 2. Gap ledger (consolidated)

**From the not-found lists** ([02 §7.15](../docs/en/android/02-FIRMWARE-HISTORY.md), [03 §7](../docs/en/kernels/03-KERNEL-HISTORY.md), [07 §8 + "not snapshotted"](../docs/en/recovery/07-RECOVERY-SAFETY.md), [09 §2](../docs/en/research/09-OPEN-QUESTIONS.md)): per-build trees for closed ports (GSI-era zips, OEM ports, A15/A16 ROMs); Xiaomi device tree (kernel sources only, P/Q/R); UART pinout; LK verified-partition list (pmOS wiki TODO); Suzaku V2 repo/base; HYDRA PLUS tree; mt6785 DTS/lore in Linus master; battery model; SPFT-dedicated 4PDA guide; live XDA beyond the Wayback ceiling.

**From OUTBOUND-LINKS dispositions worth a second pass** ([_context/OUTBOUND-LINKS.csv](_context/OUTBOUND-LINKS.csv), 1083 URLs): `forum post link (Q&A/comment, not a shapka guide entry)` — 131 URLs (noise, but instruction-dense Q&A may hide in here); `telegram channel link` — 7 (crawlable via `t.me/s/` previews per REQUIREMENTS row 26); `social/video/counter/low-value link` — 86 (YouTube unbrick/TWRP videos — video-only, skipped by policy; transcripts would need a video pass); `4PDA device-database page` — 27 (device-db pages, mostly chrome); `XDA non-begonia thread` — 42 and `XDA news article` — 36 (dropped by scope, correctly); auth-walled attachment downloads (never registered, row 23).

**From unresolved contradictions** ([09 §1](../docs/en/research/09-OPEN-QUESTIONS.md), 10 items): hardbrick-era framing vs mtkclient era; which-TWRP-per-base; ARB absence; vbmeta handling; UT vs Droidian mic; BMI120; charger IC duty split; shipped MIUI at launch (MIUI 10 vs 11); regional last-build mismatches; twrp.me index anomaly.

**From HUMAN-ASSISTS** ([_context/HUMAN-ASSISTS.md](_context/HUMAN-ASSISTS.md), 7 rows): nura/pmaports MR !1909 + device dir (Anubis); live XDA megathread; XDA unlock guide; begonia TWRP thread (optional); XDA device-tree-sources thread t=3999013 (no snapshot); XDA MTK-unlock thread t=4428577 (no snapshot). Plus auth-walled downloads generally (row 23).

## 3. What to search next (ranked)

1. **Battery model & service/replacement docs** (REQUIREMENTS row 25): read model from software (`dumpsys battery`) when a device is available; then parts-market + service-manual class sources (GSMarena teardowns, iFixit-class, repair-shop listings) to make the repair decision data-driven. Feeds [08 §Device-repair](../docs/en/linux/08-DEVELOPMENT-ROADMAP.md).
2. **UART pinout** ([07 §4](../docs/en/recovery/07-RECOVERY-SAFETY.md)): SoC UART base known (0x11002000); board pads unknown. Best lead = the [TUSER HP schematic artifact](https://www.androidfilehost.com/?fid=8889791610682869402) class (untrusted mirror; hash-check before any trust) + 4PDA/XDA hardware threads.
3. **Per-build ROM trees for the newest ROMs** (A15/A16 + closed ports): XDA megathread re-mine (HUMAN-ASSISTS #3) + per-ROM org searches; feeds [02 §7](../docs/en/android/02-FIRMWARE-HISTORY.md).
4. **Suzaku Kernel V2 base version + public repo** ([03 §2.3](../docs/en/kernels/03-KERNEL-HISTORY.md)): claimed AOSP Clang 21, A11-A17; no repo verified. Watch the [4PDA kernel post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=144852836) and GitHub.
5. **Modem/baseband firmware versioning** ([11 §2](../docs/en/kernels/11-BLOBS-FIRMWARE-SOURCES.md)): firmware changelogs, xmfwu firmware listing, modem-collection posts; feeds repair + connectivity work.
6. **OrangeFox + official TWRP build freshness**: pull version numbers from [dl.twrp.me/begonia](https://dl.twrp.me/begonia) and the [OrangeFox device page](https://orangefox.download/device/begonia) (snapshot: [archive/orangefox-begonia.html](../archive/orangefox-begonia.html)); both listings verified 2026-11-21 but build versions unverified ([09 §4 item 4](../docs/en/research/09-OPEN-QUESTIONS.md)).
7. **Human-assist saves first** ([_context/HUMAN-ASSISTS.md](_context/HUMAN-ASSISTS.md)): one browser sitting covers rows 1-7; then re-index `archive/human/` and update [10](../docs/en/android/10-GUIDE-INDEX.md).
8. **Telegram channel crawls** (`t.me/s/` previews per row 26) for kernel/ROM announcements (begoniaupdateindonesia, Redminote8proupdates, ProjectTreble_Updates).
9. **Which-TWRP compatibility table** ([09 #2](../docs/en/research/09-OPEN-QUESTIONS.md)): read each build's post body per base (human browser or per-post fetch).
10. **Xiaomi device tree** (never published): monitor MiCode + the XDA device-tree-sources thread (HUMAN-ASSISTS #6).

---
*Written by the assembler pass, 2026-11-21 (JST). Last updated: 2026-11-21T09:06:49Z (ISO 8601 UTC — REQUIREMENTS row 34).*
