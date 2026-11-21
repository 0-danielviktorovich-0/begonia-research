# 11 — Blobs, firmware & per-component sources (begonia): provenance, freshness, RE entry points, build recipes

> **New high-priority public component inventory (2026-11-21):** [Saikrishna1504/vendor_redmi_begonia@bka](https://github.com/Saikrishna1504/vendor_redmi_begonia/tree/bka) (HAL/audio/IMS/camera/GNSS/Codec2 blobs), [vendor_redmi_begonia-firmware@bka](https://github.com/Saikrishna1504/vendor_redmi_begonia-firmware/tree/bka) (preloader/LK/TEE/modem/DSP/VPU etc) and [device_redmi_begonia@axion](https://github.com/Saikrishna1504/device_redmi_begonia/tree/axion) (extract-files.py fixups, Android 11 MIUI V12.5.8.0.RGGMIXM extraction baseline). **Reference only; proprietary payloads not mirrored, low-level images not safe to flash without matched region/firmware.** See [24](../research/24-SAIKRISHNA1504-DEVICE-STACK-AUDIT.md) and [source inventory](../../../data/matrices/saikrishna-source-inventory.csv).

REQUIREMENTS rows 27 (provenance & RE reuse), 36 (observation-anchored freshness) and the 2026-11-21 build-recipe user request. **Research-only:** nothing here was flashed, downloaded as a binary, or executed; every "how it is extracted" is documented public knowledge with sources. Facts come from the research files (02-07, 10, 13, 14) — this file only consolidates WHERE each reusable artifact class lives, HOW it is re-extracted, and WHERE the LATEST version appears first. Source-level detail: [01-SOURCES.md](../research/01-SOURCES.md); per-ROM inventory: [02 §7](../android/02-FIRMWARE-HISTORY.md); kernel detail: [03](03-KERNEL-HISTORY.md); planned RE work: [_context/W15-MISSION.md](../../../_context/W15-MISSION.md) → `15-RE-IMPROVEMENT-PLAN.md` (in flight at writing time).

## 1. Vendor blobs & dumps

**WHAT it is:** the `/vendor` partition content (proprietary blobs, HALs, firmware files, audio parameters) plus system-extractable extras — the base every Android custom ROM repacks ([02 §1.3/§4](../android/02-FIRMWARE-HISTORY.md): even 2026 Android-16 ROMs ride the Android-11-era MIUI 12.5 vendor).

**WHERE the latest copy lives (repo + branch):**

| Source | What's inside | Branches / builds |
|---|---|---|
| [ZIDAN44/redmi_begonia_dump](https://github.com/ZIDAN44/redmi_begonia_dump) | extracted vendor/system dump, one branch per MIUI build | 15 branches, V11.0.4 → V12.5.7 (Global/CN/weeklies) |
| [ZyCromerZ/redmi_begonia_dump](https://github.com/ZyCromerZ/redmi_begonia_dump) | same, second dump series | 24 branches, A9 PGG → A11 RGG (IDXM/EUXM/RUXM/MIXM) |
| [AndroidBlobs/vendor_redmi_begonia](https://github.com/AndroidBlobs/vendor_redmi_begonia) | vendor blobs mirror (search hit, branches not enumerated) | unknown |
| [xmfirmwareupdater.com/vendor/begonia/](https://xmfirmwareupdater.com/vendor/begonia/) (+ [/firmware/begonia/](https://xmfirmwareupdater.com/firmware/begonia/)) | binary `vendor.img` + non-vendor firmware images per MIUI build | full official history to V12.5.15.0 |
| [xiaomirom.com begonia fastboot/recovery page](https://xiaomirom.com/en/rom/redmi-note-8-pro-begonia-global-fastboot-recovery-rom/), [mifirm.net begonia](https://mifirm.net/model/begonia.ttt) | full fastboot ROMs (`vendor.img` inside the tgz) | V10.4.2.0 (A9) → V12.5.15.0 EEA (fastboot 2022-08-26, 4.4 GB) |
| [SourceForge begoniadump](https://sourceforge.net/projects/begoniadump/) · [romdevelopers "begonia Dump/NvRam" listings](https://www.romdevelopers.com/) | community partition dumps | **untrusted** — verify before any use |

**HOW it is extracted:** dump trees are already-extracted blobs — clone the branch matching the MIUI build and consume it from a device/vendor tree via standard Android `vendor` setup ([02 §7.1](../android/02-FIRMWARE-HISTORY.md)). Binary route: fetch the last official fastboot ROM (V12.5.15.0.RGGEUXM EEA), unpack the tgz, `simg2img` if sparse, then mount/7z the ext4/ext2 `vendor.img`. Research-only note: results stay in scratch, not the repo ([_context/W15-MISSION.md](../../../_context/W15-MISSION.md)).

**RE-entry points:** [§4](#4-reverse-engineering-entry-points-research-only); audio-params diff lead = [begonia-linux/adaptation-xiaomi-begonia](https://github.com/begonia-linux/adaptation-xiaomi-begonia) (the Droidian stack that makes the mic work — [06 §2.3](../linux/06-DROIDIAN-POSTMARKETOS.md)).

**Freshness:** the newest vendor material per build = the matching dump branch (branch-per-MIUI-build; ZyCromerZ reaches A11 RGG builds, ZIDAN44 up to V12.5.7). The newest *binary* base = the last official fastboot ROM (V12.5.15.0 EEA, 2022-08-26). Nothing newer than the A11 vendor exists to build on ([02 §4](../android/02-FIRMWARE-HISTORY.md)).

## 2. Per-component firmware

**Touchscreen (works everywhere).** Mainline side: pmOS ships the package `firmware-xiaomi-begonia-touchscreen` with variant files `nt36672a_begonia_csot.bin` / `nt36672a_begonia_tianma.bin` ([06 §1.3](../linux/06-DROIDIAN-POSTMARKETOS.md) — device APKBUILD `depends`; [14 §2 Option C](14-MAINLINE-UPGRADE-PATH.md) calls touch "solved"). Driver: `novatek-nvt-ts-spi` (`TOUCHSCREEN_NOVATEK_NVT_TS_SPI=m` in the pmOS kernel config; panel/touch IDs in [04 §2](04-HARDWARE-DRIVERS.md)); the DTS `firmware-name` property selects CSOT vs Tianma ([Dinolek DTS](https://github.com/Dinolek/mt6785-mainline/tree/7.1/arch/arm64/boot/dts/mediatek)). Android side: touch firmware lives inside the vendor image (`xiaomi-touch`, `xiaomi,spi-for-tp` — [04 §2](04-HARDWARE-DRIVERS.md)).

**GPU userspace.** Android/Halium: proprietary Mali-G76 (Bifrost) kbase in the stock 4.14 kernel + vendor blob (libMali/gralloc through libhybris) — [04 §3](04-HARDWARE-DRIVERS.md). pmOS/mainline: **Panfrost** (`CONFIG_DRM_PANFROST=m`) + Mesa **panvk** Vulkan (`mesa-vulkan-panfrost` in the device APKBUILD). panthor is CSF-only → not applicable. Extraction: kbase + blobs come from the vendor/kernel trees in [§1](#1-vendor-blobs--dumps)/[§3](#3-kernel-side-sources--toolchains); the pmOS stack comes from Alpine/mesa packaging.

**Modem / NVRAM partitions.** Per the GPT partition map ([07 §5](../recovery/07-RECOVERY-SAFETY.md), pmOS wiki `parted` dump): `nvram` (67.1 MB), `nvdata` (67.1 MB), `nvcfg` (33.6 MB), `persist` (73.9 MB), `proinfo`, `seccfg`, `otp`, plus the modem image partition `md1img` (157 MB) and companions (`spmfw`, `scp1/2`, `sspm_1/2`, `cam_vpu1-3`, `gz1/2`, `tee1/2`, `lk/lk2`). *No source in this repo states begonia baseband/modem firmware versions* ([02 line 56](../android/02-FIRMWARE-HISTORY.md) — explicit gap). Re-entry: `mtk r <partition>` / `mtk rl` ([mtkclient README-USAGE](https://raw.githubusercontent.com/bkerler/mtkclient/main/README-USAGE.md)); stock modem collections: [4PDA modems post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=99355057); NVRAM/IMEI restore guides indexed in [10 §5](../android/10-GUIDE-INDEX.md).

**Audio parameters.** `mixer_paths`-class XML and audio HAL configs live in the vendor trees of [§1](#1-vendor-blobs--dumps) (per-MIUI-build branches); no standalone published "audio params" repo exists for begonia (nothing found in the per-ROM inventory). The working reference config is Droidian's adaptation bundle ([begonia-linux/adaptation-xiaomi-begonia](https://github.com/begonia-linux/adaptation-xiaomi-begonia)) — the mic-working stack ([06 §2.3](../linux/06-DROIDIAN-POSTMARKETOS.md), [08 P0 lever 1](../linux/08-DEVELOPMENT-ROADMAP.md)).

**Wi-Fi/BT firmware (mainline path).** `mt7663pr2hw.bin` ships in linux-firmware ([kernel.org firmware tree](https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/mt7663pr2hw.bin); Arch package listing cross-check) for the mt76 driver — but firmware+config alone was **not sufficient** for the owner's test ([14 §0 caveat](14-MAINLINE-UPGRADE-PATH.md)); Android-side the Wi-Fi/BT firmware rides the gen4m combo driver + vendor firmware in the dumps ([13 §1](../android/13-NETHUNTER-WIFI-EXTRAS.md)).

## 3. Kernel-side sources & toolchains

**Driver sources per component** live in the kernel trees of [kernel-matrix.csv](../../../data/matrices/kernel-matrix.csv) (36 rows): stock gen4m combo Wi-Fi + touch + camera ISP drivers in [MiCode begonia-p/q/r-oss](https://github.com/MiCode/Xiaomi_Kernel_OpenSource) (4.14.94/141/186) and [AgentFabulous/begonia](https://github.com/AgentFabulous/begonia) (12 branches, default `android-11.0`); [LineageOS/android_kernel_xiaomi_mt6785](https://github.com/LineageOS/android_kernel_xiaomi_mt6785) (7 lineage branches, default `lineage-24.0` = 4.19.325); [Nova-Kernels/kernel_xiaomi_mt6785](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785) (`main`, 4.14.356, push 2026-10-03). Mainline component IDs come from the Dinolek DTS ([04 §0 anchors](04-HARDWARE-DRIVERS.md): `novatek,nt36672a-ts`, `mediatek,mt6785-mali`, MT6359, MT6360, BMI120, STK3310, AK09918, Goodix FP).

**Defconfigs:** `begonia_user_defconfig` is the recurring name — verified in [AFB android-11.0](https://github.com/AgentFabulous/begonia/blob/android-11.0/arch/arm64/configs/begonia_user_defconfig), [MiCode begonia-r-oss](https://github.com/MiCode/Xiaomi_Kernel_OpenSource/blob/begonia-r-oss/arch/arm64/configs/begonia_user_defconfig), [AkameKernel Q-OSS-SLMK](https://github.com/Anonym3310/AkameKernel-begonia/blob/Q-OSS-SLMK/arch/arm64/configs/begonia_user_defconfig) and the UBports kernel (`begonia_user_defconfig`, clang — [05 §5](../linux/05-UBUNTU-TOUCH.md)); the mainline trees use in-tree `arch/arm64/configs/defconfig` ([14 §1.1](14-MAINLINE-UPGRADE-PATH.md)). Caution: the LOS `lineage-24.0` `begonia_defconfig` is a 29-char stub — the real LOS config filename is an open lead ([13 §3.4 addendum](../android/13-NETHUNTER-WIFI-EXTRAS.md)).

**Toolchains (as evidenced, [03 §6](03-KERNEL-HISTORY.md)):** **AOSP Clang 21** (Suzaku Kernel V2, [4PDA post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=144852836)); **clang/LLVM=1 + lld** (pmOS APKBUILD, verbatim); **"Ubuntu Pure Linux Clang 14.0.1"** (HYDRA PLUS community builds, [t.me/s/begoniaupdateindonesia](https://t.me/s/begoniaupdateindonesia)); LOS builds with its own Android clang (no manifest in repo — inferred); UBports Halium kernel builds GCC-based (inferred from commit evidence).

## 4. Reverse-engineering entry points (research-only)

- **Local host (owner-verified):** Ghidra 12.1.4 + Craft Anything are installed on the owner's Mac (stated 2026-11-21; REQUIREMENTS row 27). Use for ELF-class blobs (camera HAL, audio HAL, gen4m firmware glue) once extracted.
- **Partition extraction:** [mtkclient](https://github.com/bkerler/mtkclient) — `mtk printgpt`, `mtk r <part>`, `mtk rl out`, `mtk rf flash.bin`, preloader via `mtk r preloader ... --parttype boot1` ([README-USAGE, archived copy](../../../archive/files/mtkclient-README-USAGE.md)).
- **Image unpacking:** `simg2img` (sparse images), `payload-dumper-go` (OTA `payload.bin`), 7z/mount for ext4, `strings`/Ghidra for ELF blobs — the planned recipe is written up in [_context/W15-MISSION.md](../../../_context/W15-MISSION.md) (deliverable: `15-RE-IMPROVEMENT-PLAN.md`, in flight at writing time).
- **Kernel-side RE model:** the Mali precedent — panfrost exists because the community reverse-engineered and upstreamed; applied to MT6785 the first targets are audio (mt6797-template AFE/machine driver) and Wi-Fi chip confirmation ([14 §2 Option D](14-MAINLINE-UPGRADE-PATH.md)).
- **Boundary (REQUIREMENTS row 1):** document, do not execute. No flashing, no untrusted binaries, artifacts >50 MB stay out of the repo; extraction results live in scratch, never committed.

## 5. Freshness — where the latest version of each artifact appears first

Observation-anchored ([_context/REQUIREMENTS.md](../../../_context/REQUIREMENTS.md) row 36: as of 2026-11-21; a source may have changed after we looked).

| Artifact class | Freshest source observed 2026-11-21 | Last change observed |
|---|---|---|
| Vendor blobs per MIUI build | [ZyCromerZ/redmi_begonia_dump](https://github.com/ZyCromerZ/redmi_begonia_dump) branch matching the build (24 branches to A11 RGG) | frozen dump series (no newer MIUI exists) |
| Binary vendor/fastboot ROM | [xmfirmwareupdater.com/miui/begonia/](https://xmfirmwareupdater.com/miui/begonia/) — last official V12.5.15.0.RGGEUXM EEA | fastboot 2022-08-26 / recovery 2022-09-16 |
| Android kernel tree | [Nova-Kernels/kernel_xiaomi_mt6785](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785) (`main`, 4.14.356) | push 2026-10-03 |
| LOS-based ROM kernel | [LineageOS/android_kernel_xiaomi_mt6785](https://github.com/LineageOS/android_kernel_xiaomi_mt6785) `lineage-24.0` (4.19.325) | repo pushed 2026-10 (per [03 §7](03-KERNEL-HISTORY.md) note) |
| Mainline kernel | [kalpakprod/mt6785-linux](https://github.com/kalpakprod/mt6785-linux) (7.3.4) — newest; pmOS package stays 6.16.4 | created 2026-11-15, pushed 2026-11-20 |
| Official TWRP build | [twrp.me device page](https://twrp.me/xiaomi/xiaomiredminote8pro.html) (maintainer theimpulson) | page updated 2026-11-20; **build freshness unverified** |
| OrangeFox | [orangefox.download/device/begonia](https://orangefox.download/device/begonia) (official listing; snapshot [archive/orangefox-begonia.html](../../../archive/orangefox-begonia.html)) | verified-direct 2026-11-21; **build freshness unverified** |
| Community recovery | unified TWRP 3.7.1 by wuxinG90 ([4PDA post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=144354114)) | thread page 2026-08 |
| Ubuntu Touch | [device repo](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia) + stable channel 24.04-1.4 | repos active to 2026-10-19; stable 2026-07-13 |
| pmOS packages | [nura/pmaports](https://gitlab.nura.eco/nura/pmaports) device/testing packages | activity 2026-11-21 (API) |
| Droidian images | [begonia-linux/droidian-xiaomi-begonia releases](https://github.com/begonia-linux/droidian-xiaomi-begonia/releases) | nightly published 2026-11-15 |
| UEFI (Mu-Silicium) | [Project-Silicium/Mu-Silicium](https://github.com/Project-Silicium/Mu-Silicium) — **no begoniaPkg in the main repo** (port sources unpublished, [02 §7.14](../android/02-FIRMWARE-HISTORY.md)) | pushed 2026-11-20 |

## 6. Build & development recipes

Legend: **[verified-steps]** = the steps/manifests are verified in the linked trees or docs (we did not run builds); **[pointer]** = the entry point is verified but the step list lives at the link, not here.

### 6.1 Android ROM build (LineageOS/AOSP trees) **[pointer, manifests verified]**

1. Pick the ROM family and sync its manifest ([02 §7](../android/02-FIRMWARE-HISTORY.md) has the per-ROM table): crDroid → [crdroidandroid/android](https://github.com/crdroidandroid/android) @12.0/13.0/14.0 with device [android_device_redmi_begonia](https://github.com/crdroidandroid/android_device_redmi_begonia), vendor [android_vendor_redmi_begonia](https://github.com/crdroidandroid/android_vendor_redmi_begonia) (+[-ims](https://github.com/crdroidandroid/android_vendor_redmi_begonia-ims)), kernel [android_kernel_xiaomi_mt6785](https://github.com/crdroidandroid/android_kernel_xiaomi_mt6785) @matching branch; PixelExperience → [PixelExperience/manifest](https://github.com/PixelExperience/manifest) (ten…fourteen) + [device](https://github.com/PixelExperience-Devices/device_xiaomi_begonia)/[kernel](https://github.com/PixelExperience-Devices/kernel_xiaomi_begonia) trees; PixelOS → [PixelOS-AOSP/manifest](https://github.com/PixelOS-AOSP/manifest) (eleven…sixteen, device tree **not found**).
2. A11-era builds ride community forks instead of the orgs: crDroid 7.x = [MaloyBegonia device tree @11.0](https://github.com/MaloyBegonia/android_device_redmi_begonia_crDroid) + [AgentFabulous kernel @android-11.0](https://github.com/AgentFabulous/begonia); shared A11-A14 infrastructure: [begonia-dev](https://github.com/begonia-dev), [xiaomi-begonia-dev](https://github.com/xiaomi-begonia-dev), [Trinity-ROMS](https://github.com/Trinity-ROMS), [BitsAndBytes-dev](https://github.com/BitsAndBytes-dev) trios ([02 §7.11](../android/02-FIRMWARE-HISTORY.md)).
3. Axion (A16): device tree [AxionAOSP-devices/android_device_redmi_begonia](https://github.com/AxionAOSP-devices/android_device_redmi_begonia) (`axion`); **no manifest repo** — build/install docs only: [AxionAOSP/official_devices `Wiki/begonia.md`](https://github.com/AxionAOSP/official_devices) **[verified-steps for install]**.
4. Standard flow: `repo init`/sync with the manifest → `source build/envsetup.sh` → `breakfast begonia` → `brunch begonia` (LOS-style; branch/`lunch` target names live in each ROM's docs — not reproduced here, not executed). Vendor baseline always comes from [§1](#1-vendor-blobs--dumps).

### 6.2 Kernel builds **[pointer, defconfigs verified]**

1. Tree per target from [kernel-matrix.csv](../../../data/matrices/kernel-matrix.csv): AFB [android-11.0](https://github.com/AgentFabulous/begonia) (4.14.x, A9-A12 ROMs); LOS [lineage-24.0](https://github.com/LineageOS/android_kernel_xiaomi_mt6785) (4.19.325, A15/A16-era ROMs); Nova [`main`](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785) (4.14.356, A11-16 zips); mainline: [Dinolek/mt6785-mainline](https://github.com/Dinolek/mt6785-mainline) (6.16/7.1), [kalpakprod/mt6785-linux](https://github.com/kalpakprod/mt6785-linux) (7.3.4).
2. Defconfig: `begonia_user_defconfig` (Android trees — [AFB path](https://github.com/AgentFabulous/begonia/blob/android-11.0/arch/arm64/configs/begonia_user_defconfig)); in-tree `defconfig` for the mainline trees ([14 §1.1](14-MAINLINE-UPGRADE-PATH.md)).
3. Toolchain: match the tree ([§3](#3-kernel-side-sources--toolchains)) — AOSP Clang for Android trees, `LLVM=1` clang/llvm/lld for pmOS-style mainline builds.
4. CI template (KernelSU-Next + SUSFS, self-archived): [cvnertnc/Begonia-Kernel-Builder](https://github.com/cvnertnc/Begonia-Kernel-Builder) (GitHub Actions; fork lineage from PhamtomK12/Android-Kernel-Builder). External module linking how-to: [4PDA post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=105817890).
5. Compatibility rule (pinned-index, verified): A11+ kernels require MIUI 12.5-based ROMs; A10 kernels require MIUI 11/12 bases ([10 §4](../android/10-GUIDE-INDEX.md)).

### 6.3 Recovery builds (TWRP / OrangeFox) **[pointer]**

- Trees: [HyperTeam/android_device_redmi_begonia-TWRP](https://github.com/HyperTeam/android_device_redmi_begonia-TWRP) (`android-9.0`) and [BitsAndBytes-dev/twrp_device_redmi_begonia](https://github.com/BitsAndBytes-dev/twrp_device_redmi_begonia) (`11`) — ls-remote-verified ([02 §7.2](../android/02-FIRMWARE-HISTORY.md)).
- **Unified vs base-specific is an unresolved contradiction** ([09 #2](../research/09-OPEN-QUESTIONS.md)): unified TWRP 3.7.1 ([post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=144354114)) vs base-specific builds for A12-14 / A12.1-13 / A11 / MIUI-12.5 / A10 ([10 §2](../android/10-GUIDE-INDEX.md)). Choose per target ROM base until a compatibility table settles it.
- Official TWRP device tree + XDA support thread are linked from the [official device page](https://twrp.me/xiaomi/xiaomiredminote8pro.html); official OrangeFox builds ship from the [official device page](https://orangefox.download/device/begonia).

### 6.4 postmarketOS **[verified-steps from wiki/deviceinfo]**

- Host: **Linux only** — verbatim: *"Running pmbootstrap on other operating systems than Linux is not supported. If you run another OS, consider setting up a virtual machine with Linux. Some people also made it work with WSL"* ([pmbootstrap/Installation, Nura wiki](https://wiki.nura.eco/wiki/Pmbootstrap/Installation)); on macOS use a Linux VM ([07 host matrix](../recovery/07-RECOVERY-SAFETY.md)).
- Packages: device [device-xiaomi-begonia](https://gitlab.nura.eco/nura/pmaports/-/tree/main/device/testing/device-xiaomi-begonia) + kernel [linux-postmarketos-mediatek-mt6785](https://gitlab.nura.eco/nura/pmaports/-/tree/main/device/testing/linux-postmarketos-mediatek-mt6785) (APKBUILD source tag `6.16.4-r0` from [gitlab.postmarketos.org/mt6785-mainline/linux](https://gitlab.postmarketos.org/mt6785-mainline/linux)) — [06 §1.3/§1.4](../linux/06-DROIDIAN-POSTMARKETOS.md).
- Install: `pmbootstrap install` → fastboot flash boot + rootfs (`deviceinfo_flash_method="fastboot"`, boot.img v2 + DTB), or the recovery-zip path (`pmbootstrap install --android-recovery-zip` → push zip → flash in stock recovery) — [06 §1.8](../linux/06-DROIDIAN-POSTMARKETOS.md); vbmeta bootloop fix: `pmbootstrap flasher flash_vbmeta` then `flash_kernel` ([07 §3.0](../recovery/07-RECOVERY-SAFETY.md)).

### 6.5 Ubuntu Touch (Halium) **[verified-steps from device repo]**

- Host: Linux (Debian/Ubuntu per [UBports Setting-up docs](https://docs.ubports.com/en/latest/porting/introduction/Setting_up.html)); macOS/Windows → VM/Docker ([07 host matrix](../recovery/07-RECOVERY-SAFETY.md)).
- Device repo root [`build.sh`](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia) = a two-liner: `git clone` of [halium-generic-adaptation-build-tools](https://gitlab.com/ubports/community-ports/halium-generic-adaptation-build-tools) into `./build`, then `./build/build.sh "$@"`; CI runs `gsi-port-ci.yml` (`halium.yaml` tooling) — [05 §5](../linux/05-UBUNTU-TOUCH.md).
- Kernel: clone [kernel-xiaomi-mt6785](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/kernel-xiaomi-mt6785) @`halium-10.0`, build `begonia_user_defconfig` with clang; boot.img header v2, DTB `mediatek/mt6785.dtb` ([05 §5](../linux/05-UBUNTU-TOUCH.md)).
- Vendor: stock MIUI vendor via Halium (no separate repo found — [02 §7.12](../android/02-FIRMWARE-HISTORY.md)); install end-user path = UBports Installer 0.11.2 ([device page](https://devices.ubuntu-touch.io/device/begonia/)).

## 7. Rescue hardware minimum ("is a cable enough?")

Answer from the evidence (megathread + pmOS wiki, both verified-direct): **for the mtkclient BROM path, yes — a USB data cable and a host are enough; no disassembly, no test point** (MT6785 enters BROM with Vol-Up held while plugging USB; the megathread says verbatim *"You do not need to take the phone apart to short any pins"*). Full reasoning: [07 §4/§6](../recovery/07-RECOVERY-SAFETY.md).

| Method | Host | Extra hardware | Source |
|---|---|---|---|
| mtkclient (unlock / backup / full unbrick) | Linux / Windows / **macOS native** (incl. Apple Silicon notes) | **USB-C data cable only**; no test point (Vol-Up + USB at boot) | [README-INSTALL](https://raw.githubusercontent.com/bkerler/mtkclient/main/README-INSTALL.md) · [megathread (Wayback)](http://web.archive.org/web/20260415164458/https://xdaforums.com/t/guide-info-psa-redmi-note-8-pro-megathread-cfw.4056527/) · [pmOS wiki](https://wiki.nura.eco/wiki/Xiaomi_Redmi_Note_8_Pro_(xiaomi-begonia)) |
| SP Flash Tool + bypass_utility | Windows or Linux (no macOS build) | cable + bypass_utility (UART mode per its README); SPFT 5.2208 circulates in MTK channels | [bypass_utility](https://github.com/MTK-bypass/bypass_utility) · [wiki SPFT flow](https://wiki.nura.eco/wiki/Xiaomi_Redmi_Note_8_Pro_(xiaomi-begonia)) · [spflashtool.com](https://spflashtool.com/) |
| Official Mi Unlock (if BL state requires it) | **Windows only** (VM otherwise) | cable; Mi account + 168 h wait | [07 §1](../recovery/07-RECOVERY-SAFETY.md) · [unlock guide (Wayback)](http://web.archive.org/web/20230316035523/https://forum.xda-developers.com/t/guide-begonia-unlock-bootloader-flash-twrp-and-root-proper.3995919/) |
| fastboot reflash (device alive) | Linux / Windows / macOS (adb+fastboot) | cable only; MediaTek VCOM drivers on Windows | [07 host matrix](../recovery/07-RECOVERY-SAFETY.md) · [flash walk-through](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=90022165) |
| UART debugging | any host | **optional** USB-TTL adapter — begonia pinout **NOT found** (open question; don't buy on this basis) | [07 §4](../recovery/07-RECOVERY-SAFETY.md) · [09 §2](../research/09-OPEN-QUESTIONS.md) |
| Paid remote service | — | none locally (alternative to all of the above) | [07 §3.0 era-tension note](../recovery/07-RECOVERY-SAFETY.md) |

## 8. Sources

Class-grouped index with observation stamps: [01-SOURCES.md](../research/01-SOURCES.md); machine records: [sources.json](../../../data/catalog/sources.json). The dominant classes for this file: GitHub dump/kernel trees (§4/K), Xiaomi firmware mirrors (§2/M), pmOS/UBports packages (§6/L), forum guides (§1/F). No new research was done in this file — every claim resolves to an existing record or an explicit not-found marker.

---
*Written by the assembler pass, 2026-11-21 (JST). Last updated: 2026-11-21T09:06:49Z (ISO 8601 UTC — REQUIREMENTS row 34).*
