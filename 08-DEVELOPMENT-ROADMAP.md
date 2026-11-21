# 08 — Development roadmap (begonia, Redmi Note 8 Pro / MT6785)

Evidence-based work plan derived from files 02–07 (research date 2026-11-21; **research-only** — nothing here has been executed on hardware). Every claim links to its evidence file; confidence follows the same contract as the rest of the repo. Priorities: **P0** north star, **P1** highest leverage, **P2** Android-side maintenance.

---

## P0 — Ubuntu Touch modernization (north star)

**Current state** ([05-UBUNTU-TOUCH.md](05-UBUNTU-TOUCH.md)): UT 24.04 noble on Halium 10.0 over the stock kernel (4.14.141); stable channel 24.04-1.4 (2026-07-13), RC 24.04-1.5 (2026-10), device repos active through 2026-10-19 (porting group [xiaomi-begonia](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia), maintainer TheKit).

**Known gaps to close** (device page, high): **microphone ❌** (recording/mic-in; voice calls route OK), **RTC ❌** (clock resets without network), **auto-brightness ❌** ([repowerd#11](https://gitlab.com/ubports/core/repowerd/-/issues/11) — global issue; device config exists in the port overlay), plus global Halium-era **VoLTE / A-GPS slowness** ([location-service#13](https://gitlab.com/ubports/development/core/location-service/-/issues/13)).

**Path (three levers, in order of expected payoff):**

1. **Reuse the Droidian audio stack** — the live Droidian port gets **sound including microphone working** on the same Halium-10 vendor base ([06-DROIDIAN-POSTMARKETOS.md](06-DROIDIAN-POSTMARKETOS.md), adaptation bundle `adaptation-xiaomi-begonia`). Diff Droidian's audio policy/`audiohal` config against UT's and port the difference. This is the single most concrete fix lead for UT's worst gap. (Medium-high — same vendor base, different stacks.)
2. **Halium-11 feasibility study** — the raw material exists: [AgentFabulous/begonia](https://github.com/AgentFabulous/begonia) default branch `android-11.0` (frozen 2022-06-23) and MiCode `begonia-r-oss` (4.14.186). A Halium-11 port would remove the Android-10 ceiling on userland; cost = re-shimming the kernel + new vendor glue, and re-testing every per-feature fix UT 24.04 already carries. Decide *after* lever 1 (don't re-port onto a base that still has the mic broken). (Inferred — no Halium-11 begonia work exists anywhere yet.)
3. **Watch the mainline track (P1)** — a future UT on a mainline kernel would drop Halium entirely for the subsystems pmOS already drives (display/touch/GPU/NFC), but telephony+audio on mainline are the documented blockers ([06](06-DROIDIAN-POSTMARKETOS.md)). Long-term, not next-quarter.

**Verification loop** (research-only today, dev later): UBports Installer 0.11.2 (macOS/Windows/Linux builds exist) → stable channel first → check the exact broken rows of the device page after each channel bump → file/track issues in the two GitLab repos above.

## P1 — Mainline leverage

**State of the art** ([03 §4](03-KERNEL-HISTORY.md), [06](06-DROIDIAN-POSTMARKETOS.md)):

| Tree | Version | Status (2026-11) |
|---|---|---|
| pmOS `linux-postmarketos-mediatek-mt6785` ([nura/pmaports](https://gitlab.nura.eco/nura/pmaports)) | 6.16.4 | packaged; screen/touch/GPU/NFC/sensors work; audio/camera/WiFi/BT/GPS/modem broken (driver gaps) |
| [Dinolek/mt6785-mainline](https://github.com/Dinolek) | 6.16.4 / 7.1 | Dinolek is the pmOS begonia maintainer; last push 2026-06-17 |
| [kalpakprod/mt6785-linux](https://github.com/kalpakprod/mt6785-linux) | 7.3.4 | new (created 2026-11-15, pushed 2026-11-20) — freshest mainline tree |
| Linus master | — | **no mt6785 DTS, no lore.kernel.org patches** — mainlining is fork-only |

**What a mainline-based userland (UT-style) would need** (gap list from [04](04-HARDWARE-DRIVERS.md)/[06](06-DROIDIAN-POSTMARKETOS.md)):

- **Audio**: MT6359 PMIC codec driver path — mainline has no working begonia audio stack; DTS-side sound nodes are the missing piece. pmOS wiki documents the breakage; no WIP patch located.
- **Modem/telephony**: MT6785 modem (CCCI) is not mainlined; no oFono/ModemManager story on the mainline kernel for this device.
- **Wi-Fi/BT**: firmware glue exists in the Android vendor blobs; mainline drivers load but the pmOS rows stay broken — needs device-specific bring-up (DTS + firmware install path).
- **Camera/GPS**: sensor drivers (camera ISP, GNSS over modem) — same class of gap.
- **Practical conclusion**: a mainline-only daily driver is **not** reachable with current trees; the realistic mainline play is (a) feed fixes upstream via Dinolek/kalpakprod, (b) use pmOS as the regression dashboard for every subsystem, (c) revisit when audio+modem DTS patches appear. (Medium-high.)

## P2 — Android-side (custom-ROM) baseline

- **Freshest native base**: LineageOS 24.0 line — kernel base 4.19.325 in the LOS kernel tree ([LineageOS/android_kernel_xiaomi_mt6785](https://github.com/LineageOS/android_kernel_xiaomi_mt6785), 7 lineage branches; per-ROM inventory in [02 §7](02-FIRMWARE-HISTORY.md)).
- **Kernel choices for builders** ([03](03-KERNEL-HISTORY.md)): [Nova-Kernels/kernel_xiaomi_mt6785](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785) (`main`, Linux 4.14.356, push 2026-10-03 — active); "Suzaku Kernel V2" (4PDA, A11–A17 claims, AOSP Clang 21 — **no public repo verified**, treat as unverified until source appears).
- **Vendor baseline**: every ROM repacks the last official MIUI 12.5 vendor base ([02 §1.3/§7.2](02-FIRMWARE-HISTORY.md)); vendor image fingerprint precedent `begonia-user 10/QP1A.190711.020/20.5.14` (2.66 GiB, Erfan GSI era — [02 §2](02-FIRMWARE-HISTORY.md)).
- **Recovery tooling**: official TWRP + official OrangeFox listings exist (2026-11 verified, [07 §3](07-RECOVERY-SAFETY.md)); community unified TWRP 3.7.1 (wuxinG90) is the 4PDA-current build.

---

## AI-assisted development architecture

**Recommended toolchain per task** (host support in the table below; full details in [07](07-RECOVERY-SAFETY.md)):

| Task | Primary tool | Notes |
|---|---|---|
| Backup / unbrick / partition surgery | [mtkclient](https://github.com/bkerler/mtkclient) (`rf`, `rl`, `r … --parttype=boot1`, GUI `mtk_gui.py`) | runs natively on macOS incl. Apple Silicon; fully replaces SP Flash Tool here (pmOS wiki footnote) |
| Unlock | `mtk da seccfg unlock` via BROM | no test point (hold Vol-Up); official Mi Unlock only if the bootloader state requires it (168 h, Windows) |
| Kernel/test-build iteration | adb/fastboot loop + `fastboot boot`-style testing discipline | never flash boot without a verified restore path ([07 §5](07-RECOVERY-SAFETY.md)) |
| pmOS builds / `pmbootstrap` | Linux VM or container only ("running pmbootstrap on other operating systems is not supported" — verbatim, wiki) | macOS host → UTM/Parallels Linux VM |
| Halium/UT builds | Ubuntu VM or Docker (docs list Linux distros only) | i386 multilib on amd64 per UBports docs |
| ROM builds | Linux + lineage/Halium trees from [02 §7](02-FIRMWARE-HISTORY.md) per-ROM inventory | manifest/vendor/device-tree links included there |
| UART bring-up (if ever needed) | **unknown** — no accessible source documents a begonia UART pinout; do not buy hardware on this basis ([07 §4](07-RECOVERY-SAFETY.md)) | schematic artifact lead: [04](04-HARDWARE-DRIVERS.md) |

**Test/verification workflow** (translated from 4PDA/wiki discipline): back up preloader + full flash via mtkclient *before* any write ([07 §5](07-RECOVERY-SAFETY.md)); verify region via `fastboot getvar product` before cross-flashing; uncheck preloader/lk/lk2 when flashing foreign firmware (megathread recipe); keep vbmeta discipline (`mtk da vbmeta 3` or patched vbmeta — open question [09](09-OPEN-QUESTIONS.md)); change one variable per boot test.

**Reproducible R&D repo layout** — this repo *is* the template: `_context/` (mission, requirements, corrections queue, source census, human-assists) + `_cache/` (raw markdown twins) + `archive/` (clickable offline copies paired in `archive/index.html`) + numbered deliverables + CSV matrices + `OUTBOUND-LINKS.csv` ledger + autosync discipline (single writer, cron push). Any future device research can clone this shape.

### Host workstation summary (from [07](07-RECOVERY-SAFETY.md))

| Task | Linux | Windows | macOS | Fallback |
|---|---|---|---|---|
| adb / fastboot | ✔ | ✔ | ✔ | — |
| Mi Unlock (official path) | ✖ | ✔ | ✖ | Windows VM (USB2 ports, driver-signing off — wiki recipe) |
| mtkclient (unlock / backup / unbrick) | ✔ | ✔ | ✔ **(officially supported, incl. Apple Silicon notes)** | — |
| SP Flash Tool + bypass_utility | ✔ | ✔ | ✖ (no macOS build) | Ubuntu VM — or skip: mtkclient replaces it |
| pmbootstrap | ✔ | ✖ | ✖ | Linux VM / WSL |
| Halium / UT build | ✔ | ✖ | ✖ | Ubuntu VM / Docker |
| UBports Installer (install to device) | ✔ | ✔ | ✔ (macOS .dmg) | — |
| UART debugging | unknown | unknown | unknown | not found (searched: 4PDA caches, web) — see [09](09-OPEN-QUESTIONS.md) |

---

## Device-repair outlook (REQUIREMENTS row 25 — registered, not yet researched)

The owner's begonia idles with **battery drain**. To make a future repair decision data-driven, the following is **open research** — deliberately left un-guessed:

- **Battery model: unknown** (searched: repo sources; not yet established — no source in this repo names the battery part). First step when a device is available: read it from software (`adb shell dumpsys battery`, or recovery/`*#*#4636#*#*` era menus) before opening the phone.
- **Health-check procedures to register**: capacity/fill-cycle logging on a custom ROM (Battery Charge limit tools), idle-drain attribution (`dumpsys batterystats` after a full idle cycle), voltage/temperature sanity via `dumpsys battery`.
- **Serviceability** (from this repo's findings): back cover/battery are standard teardown-class repairs (only video-grade teardown evidence exists for begonia — [07 §4](07-RECOVERY-SAFETY.md) test-point verdict); software-level recovery of the device is excellent (BROM reachable without test point + mtkclient = full-flash restore at home, [07 §6](07-RECOVERY-SAFETY.md)); NVRAM/persist partition backup before any battery-board work ([07 §5](07-RECOVERY-SAFETY.md)).
- **Replacement-cost sources: TBD** (parts-market research pass not yet run — candidates: official Xiaomi parts channels, parts marketplaces, repair-shop quotes; see [09-OPEN-QUESTIONS.md](09-OPEN-QUESTIONS.md) §2).

*Written by the editor-in-chief pass, 2026-11-21 (JST). Evidence contract per [_context/CONTEXT.md](_context/CONTEXT.md).*
