# 00 — README: begonia-research executive summary

> **Independent 2026-11-21 update:** The Linux 4.19.325 MT6785 tree checked in LineageOS contains **rosemary** board DTS/defconfig, so it is **not verified as a ready-to-flash begonia kernel**. Community reports a begonia 4.19 port but without independently checked full test logs. Further, a [postmarketOS-derived experimental begonia build](https://github.com/criollojoel10/begonia-pmos-tianma) reports **working onboard Wi-Fi on Linux 6.16.4** (2026-09-27) using ported MediaTek vendor WLAN drivers; the baseline pmOS Wi-Fi status below still describes the standard Dinolek/Nura package. See [22-KERNEL-FORWARD-PORT-AI-INTEGRITY-RU.md](22-KERNEL-FORWARD-PORT-AI-INTEGRITY-RU.md).

Research knowledge base for the **Xiaomi Redmi Note 8 Pro** (`begonia`, MediaTek Helio G90T / MT6785, 2019), built 2026-11-21 in a single-day multi-agent run (6 core researchers + augmentation waves + synthesis pass) so that an agent or human unfamiliar with the device can start work from this repo alone.

**Dual scope** (user requirement, [_context/REQUIREMENTS.md](_context/REQUIREMENTS.md) row 24):

1. **Linux porting** — Ubuntu Touch (north star), Droidian, postmarketOS, Halium, mainline Linux.
2. **The Android custom ecosystem** — ROMs, kernels, recoveries (TWRP / OrangeFox / PitchBlack / LR.Team), firmware, vendor trees, unbrick/recovery tooling: the goal is to index important instructions and artifacts with sources, but the archived forum crawl is **sampled rather than exhaustive**.

**Research-only:** nothing was flashed, downloaded as binary, or executed against hardware. All procedures are documented public knowledge with sources.

## The device (verified facts)

- Released 2019-09-24; SoC **MT6785 / Helio G90T** (2× A76 + 6× A55, Mali-G76 MC4); 6.53" 1080×2340 IPS (NT36672A: CSOT or Tianma); 4500 mAh; 64 MP GW1 rear + 20 MP front; 4/6/8 GB RAM; 64/128/256 GB UFS 2.1.
- Two commonly discussed variants: `begonia` (global) and `begoniain` (India); the original CFW community attributes the main physical difference to NFC, but **ROM/recovery/firmware compatibility still needs verification** for each regional SKU and panel.
- Shipped Android 9; last official **MIUI 12.5** (Android 11). Xiaomi OSS kernel sources span **4.14.94 (P), 4.14.141 (Q), 4.14.186 (R)**; the actual retail OTA `uname` must be observed separately. aarch64.
- Boot chain: BROM → preloader → LK → Linux. The community documents BROM access by Vol-Up + USB and exploit-assisted recovery with mtkclient on supported firmware states; **this does not guarantee recovery on every individual brick, patch level or board failure** — this shapes the risk assessment in [07-RECOVERY-SAFETY.md](07-RECOVERY-SAFETY.md).

## Major findings (highest-confidence, cross-file)

1. **Official MIUI ended 2022**: last stable build `V12.5.15.0.RGGEUXM` (EEA), recovery 2022-09-16 / fastboot 2022-08-26 — cross-confirmed by four independent mirror classes ([02-FIRMWARE-HISTORY.md](02-FIRMWARE-HISTORY.md), [_context/SOURCE-CENSUS.md](_context/SOURCE-CENSUS.md)). High.
2. **Official kernel sources exist for P/Q/R**: MiCode `begonia-p-oss` (4.14.94), `begonia-q-oss` (4.14.141), `begonia-r-oss` (4.14.186) ([03-KERNEL-HISTORY.md](03-KERNEL-HISTORY.md)). High. The Xiaomi *device tree*, however, was never fully published ([02 §7](02-FIRMWARE-HISTORY.md)).
3. **Project-official ROM status is project-specific**: crDroid publishes begonia on its own site; AxionAOSP also labels builds official; official LineageOS begonia support was **not** established by its wiki. Newer community builds reach **Android 16** ([02](02-FIRMWARE-HISTORY.md)). High.
4. **2026 ROM/kernel lineage is mixed**: LineageOS has **MT6785-family Linux 4.19.325 source** (with rosemary DT), while 2026-11-13–15 commits in Saikrishna's **begonia device tree** explicitly target 4.19. **The matching full 4.19 begonia kernel tree was not found in his public main/kaeru branches**; his published manifest still points to 4.14.357. Suzaku V2 claims A11–A17 compatibility, but its exact kernel sublevel remains unverified ([03](03-KERNEL-HISTORY.md), [24](24-SAIKRISHNA1504-DEVICE-STACK-AUDIT.md)). Source evidence high; on-device support unverified.
5. **No mt6785 DTS in Linus master; no lore.kernel.org patches** — mainlining happens in forks: pmOS package (6.16.4), [Dinolek/mt6785-mainline](https://github.com/Dinolek) (6.16.4 / 7.1), [kalpakprod/mt6785-linux](https://github.com/kalpakprod/mt6785-linux) (7.3.4, new 2026-11-15) ([03 §4](03-KERNEL-HISTORY.md), [_context/SOURCE-CENSUS.md](_context/SOURCE-CENSUS.md)). High.
6. **pmOS mainline status (6.16.4)**: screen, touch, GPU (Panfrost), NFC, FDE, OTG, haptics, most sensors work; **audio, camera, Wi-Fi, BT, GPS, modem/telephony broken** — documented mainline driver gaps ([04](04-HARDWARE-DRIVERS.md), [06](06-DROIDIAN-POSTMARKETOS.md)). High.
7. **Ubuntu Touch is alive**: noble 24.04 port, Halium 10.0 / kernel 4.14.141; stable 24.04-1.4 (2026-07-13), RC 24.04-1.5 (2026-10), device repos active to 2026-10-19; broken: **microphone, RTC, auto-brightness** (repowerd#11) ([05-UBUNTU-TOUCH.md](05-UBUNTU-TOUCH.md)). High.
8. **Live Droidian port** ([begonia-linux org](https://github.com/begonia-linux), nightly 2026-11-15): via libhybris it runs calls/SMS/data/camera/audio-**including mic**/Wi-Fi/BT — the mic result contradicts UT and is a key reuse lead ([06](06-DROIDIAN-POSTMARKETOS.md)). Medium-high.
9. **Two unlock paths** ([07](07-RECOVERY-SAFETY.md)): official Mi Unlock = 7-day (168 h) wait, Windows-only tool, and XiaoMiToolV2's unlock died 2023-02-28 (PR #98); **exploit path = `mtk da seccfg unlock`** via BROM (MT6785 hwcode 0x813, no test point, SLA/DAA bypassed locally, no account). High.
10. **Recovery landscape (independently checked 2026-11-21):** official [TWRP begonia page](https://twrp.me/xiaomi/xiaomiredminote8pro.html) was updated 2026-11-20, but its latest **official downloadable image** is `twrp-3.7.0_9-0-begonia.img` dated **2022-10-06**. The official [OrangeFox begonia page](https://orangefox.download/device/begonia) states **device unmaintained**; its last listed beta is from **2020-07-26** and requires historical **CFW**. Thus neither listing confirms current Android 16 compatibility. Risk of hard-brick remains; exploit recovery is conditional ([07 §3](07-RECOVERY-SAFETY.md), [17](17-INDEPENDENT-AUDIT.md)).
11. **Many documented modern Android ROMs still use Xiaomi MIUI 12.5-era vendor components** (last official MIUI 12.5); per-ROM source inventories (kernel tree + device tree + vendor + manifest) are in [02 §7](02-FIRMWARE-HISTORY.md), with explicit "not found (searched: …)" markers where closed. High where marked.
12. **"Mu-Silicium" is not a ROM**: it is Project-Mu **UEFI firmware** (Windows/WinPE experiment, bootable `UEFI.img`), resolved and separated from the ROM catalog ([02 §3.9](02-FIRMWARE-HISTORY.md)). High.
13. **Curated forum guide index**: pinned index posts and a sample of later 4PDA/XDA pages and separately discovered messages are indexed in [10-GUIDE-INDEX.md](10-GUIDE-INDEX.md). **Not a full crawl** of all 1,235 + 1,110 4PDA pages; 1,083 extracted outbound URLs cover the sampled material, not the entire forums ([_context/OUTBOUND-LINKS.csv](_context/OUTBOUND-LINKS.csv)).
14. **Source census beyond the big four**: Xiaomi mirrors, official TWRP, SourceForge, AndroidFileHost (incl. a TUSER HP schematic artifact — untrusted), public Telegram channels, GSMarena, repair-shop ecosystem — standing crawl list for future research ([_context/SOURCE-CENSUS.md](_context/SOURCE-CENSUS.md)). High.
15. **Direct begonia 4.19 migration evidence and component sources**: the developer's [device tree](https://github.com/Saikrishna1504/device_redmi_begonia/tree/axion) contains six dated Nov 13–15 commits for k419, DTBO, SELinux, init/UClamp, powerhint and OTG/SD. Its linked [vendor blobs](https://github.com/Saikrishna1504/vendor_redmi_begonia), [low-level firmware](https://github.com/Saikrishna1504/vendor_redmi_begonia-firmware), audio policies and 10 IMS + 4 camera patches are **valuable reverse-engineering references**. Build manifest kernel mismatch and missing configuration fragment remain explicit gaps ([24](24-SAIKRISHNA1504-DEVICE-STACK-AUDIT.md), [inventory](saikrishna-source-inventory.csv)).

## How to use this DB

- **Start here**, then read [_context/CONTEXT.md](_context/CONTEXT.md) (evidence contract + tool-access verdicts) and [_context/REQUIREMENTS.md](_context/REQUIREMENTS.md) (maintained requirement register). Open questions and ranked next steps: [09-OPEN-QUESTIONS.md](09-OPEN-QUESTIONS.md). Planned work: [08-DEVELOPMENT-ROADMAP.md](08-DEVELOPMENT-ROADMAP.md).
- **Find a ROM/kernel/recovery**: scan the file map below → detail sections → per-ROM sources in [02 §7](02-FIRMWARE-HISTORY.md); structured rows in the CSVs; guides in [10-GUIDE-INDEX.md](10-GUIDE-INDEX.md).
- **Cite a fact**: every important claim carries URL + title/author + date + permalink + verified-vs-inferred + confidence (high/medium/low). Historical status is separated from current status everywhere.
- **Selected important sources have offline copies** in [archive/index.html](archive/index.html) (pairs original ↔ copy ↔ snapshot date); raw markdown twins in `_cache/`; small text artifacts in [archive/files/](archive/files). No multi-GB binaries are committed.

## File map

| File | Content | Status |
|---|---|---|
| [00-README.md](00-README.md) | This executive summary | delivered 2026-11-21 |
| [01-SOURCES.md](01-SOURCES.md) | Consolidated source index (class-grouped, observation-stamped) | delivered 2026-11-21 (assembler) |
| [02-FIRMWARE-HISTORY.md](02-FIRMWARE-HISTORY.md) | Official MIUI timeline, GSI era, native ROM catalog, per-ROM source inventory (§7) | delivered |
| [03-KERNEL-HISTORY.md](03-KERNEL-HISTORY.md) | MiCode drops, AgentFabulous forks, LOS kernel table, Halium kernel, mainline forks, toolchains | delivered |
| [04-HARDWARE-DRIVERS.md](04-HARDWARE-DRIVERS.md) | Component IDs from mainline DTS, GPU stacks, per-OS support matrix | delivered |
| [05-UBUNTU-TOUCH.md](05-UBUNTU-TOUCH.md) | UT 24.04 noble port: channels, issues, build system, upgrade path | delivered |
| [06-DROIDIAN-POSTMARKETOS.md](06-DROIDIAN-POSTMARKETOS.md) | pmOS mainline port, live Droidian port, architecture comparison | delivered |
| [07-RECOVERY-SAFETY.md](07-RECOVERY-SAFETY.md) | Unlock paths, recovery landscape, unbrick recipes, backups, partition map, host toolbox | delivered |
| [08-DEVELOPMENT-ROADMAP.md](08-DEVELOPMENT-ROADMAP.md) | P0/P1/P2 development paths, AI-assisted tooling, host matrix, device-repair outlook | delivered 2026-11-21 |
| [09-OPEN-QUESTIONS.md](09-OPEN-QUESTIONS.md) | Unresolved contradictions, not-found ledger, human checks, ranked next steps | delivered 2026-11-21 |
| [10-GUIDE-INDEX.md](10-GUIDE-INDEX.md) | Curated guide/index posts and selected offline snapshots; coverage not exhaustive | delivered |
| [firmware-matrix.csv](firmware-matrix.csv) · [kernel-matrix.csv](kernel-matrix.csv) · [hardware-support-matrix.csv](hardware-support-matrix.csv) | 73 ROM rows · 36 kernel rows · 33 components × 4 OS columns | delivered (Bliss 16.9 CSV row added at assembly 2026-11-21) |
| [24-SAIKRISHNA1504-DEVICE-STACK-AUDIT.md](24-SAIKRISHNA1504-DEVICE-STACK-AUDIT.md) · [saikrishna-source-inventory.csv](saikrishna-source-inventory.csv) | 21 repositories and six direct 4.19 migration commits, vendor firmware, audio/IMS/camera sources, gaps | delivered 2026-11-21 |
| [sources.json](sources.json) · [INDEX.md](INDEX.md) · [index.json](index.json) | Master source index + human/machine topic map | delivered 2026-11-21 (assembler) |
| [_context/](_context) | [CONTEXT.md](_context/CONTEXT.md) · [REQUIREMENTS.md](_context/REQUIREMENTS.md) · [SOURCE-CENSUS.md](_context/SOURCE-CENSUS.md) · [CORRECTIONS.md](_context/CORRECTIONS.md) · [HUMAN-ASSISTS.md](_context/HUMAN-ASSISTS.md) · [OUTBOUND-LINKS.csv](_context/OUTBOUND-LINKS.csv) · [S1-MISSION.md](_context/S1-MISSION.md) | governance pack |
| [archive/index.html](archive/index.html) | Offline archive index (original ↔ copy ↔ date) | delivered, regenerated at final pass |

## Limitations & research-method notes

- **Live XDA is bot-blocked** (bunny.net challenge; tested 3×) — all XDA evidence came from Wayback snapshots or search snippets; thread bodies beyond OPs were not read in full ([_context/HUMAN-ASSISTS.md](_context/HUMAN-ASSISTS.md)).
- **gitlab.nura.eco / wiki.nura.eco** sit behind an Anubis bot-check — data came from the GitLab REST API (JSON in `archive/files/`) and the extractor.
- **4PDA** allows our server-side extractor (full-page snapshots in `archive/`), but spoiler-block content is dropped by text extraction and attachment downloads are registration-walled (never registered; logged for human assist).
- **GitHub API** unauthenticated pool exhausts fast — `git ls-remote` + `raw.githubusercontent.com` were preferred; a few per-branch commit dates are missing ([03 §6 limitations](03-KERNEL-HISTORY.md)).
- **Official TWRP / OrangeFox pages**: listings verified-direct 2026-11-21, but the freshness/version of the current downloadable builds was **not** verified; the OrangeFox page snapshot is [archive/orangefox-begonia.html](archive/orangefox-begonia.html) (verified 2026-11-21).
- One-day run: no on-device verification of anything; wiki rows and forum claims are cited, not re-tested.

## Corrections & governance

Queued corrections **C1–C4 + C6 were applied** at this synthesis pass (official TWRP existence + warnings → 07; Bliss OS 16.9 → 02; schematic artifact → 04+07; HYDRA PLUS Clang 14.0.1 toolchain + Erfan vendor-base → 03+02; recovery-landscape subsection → 07); **C5 was skip-verified** before the pass ([_context/S1-MISSION.md](_context/S1-MISSION.md)). Row history is preserved in [_context/CORRECTIONS.md](_context/CORRECTIONS.md). Repo rules: one writer commits (orchestrator autosync every 15 min), root files refreshed at every milestone, no invented data, research-only.

*Written by the editor-in-chief pass, 2026-11-21 (JST).*
