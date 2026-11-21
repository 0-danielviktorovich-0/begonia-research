# 24 — Saikrishna1504: Redmi Note 8 Pro source-stack audit and Linux 4.19 migration evidence

**Language:** [English (source)](24-SAIKRISHNA1504-DEVICE-STACK-AUDIT.md) · [Русский (подробный конспект)](../../ru/research/24-saikrishna-source-audit.md) · [English directory](../index.md).

**Observed:** 2026-11-21. **Evidence:** public GitHub metadata, trees, Makefiles, selected diffs/patches and manifests read directly; original Telegram announcement available in the [project's post record](23-419-TELEGRAM-OUTREACH.md). **No code compiled, firmware flashed, camera APK run, or boot image tested**. Public files and upstream claims are not hardware-validation results.

## 1. Executive finding

The developer's [GitHub account](https://github.com/Saikrishna1504) has **over 100 publicly indexed repositories** (103 returned by repository search pages 1–2 during this audit), but many are unrelated coursework or other phones. The critical begonia assets are a **device tree, proprietary vendor tree, separate firmware bundle, kernel source, boot-image/prebuilt kernel tree, MediaTek hardware adaptation, SELinux policies, recovery source, OTA metadata, IMS/camera patches and historical manifests**.

**Major new discovery:** the [current device tree on branch axion](https://github.com/Saikrishna1504/device_redmi_begonia/tree/axion) explicitly configures **Linux 4.19** using `TARGET_KERNEL_CONFIG := k85v1_64_k419_defconfig vendor/begonia.config` and `Image.gz-dtb`. Its dated commits document actual **begonia-specific Android userspace adaptation from rosemary for Linux 4.19**, not merely a Telegram claim. This is **strong evidence of active forward-port engineering**, but **not yet a reproducible public 4.19 kernel source release**.

## 2. Repositories worth integrating into the research database

| Priority | Repository / branch inspected | Evidence and purpose | Porting value; caveat |
|---|---|---|---|
| **P0** | [device_redmi_begonia](https://github.com/Saikrishna1504/device_redmi_begonia/tree/axion), `axion` (pushed 2026-11-15) | `BoardConfig.mk`, `device.mk`, `rootdir/etc/init.mt6785.rc`, `configs/powerhint.json`, `blob-patches/`, audio configuration, `sepolicy/` | **Main living Android device adaptation**; current 4.19 build intent, root device tree, hardware HAL configuration. A source tree does **not** prove a usable boot image |
| **P0** | [vendor_redmi_begonia](https://github.com/Saikrishna1504/vendor_redmi_begonia/tree/bka), `bka` (pushed 2026-11-15) | `proprietary/` with 1,269 tree entries: modem/RIL, MediaTek Codec2, camera, HAL, IMS, GNSS, DSP, power, graphics, wireless | Essential **binary ABI inventory** for Linux ports and Android; blob origin/licensing must be checked |
| **P0** | [vendor_redmi_begonia-firmware](https://github.com/Saikrishna1504/vendor_redmi_begonia-firmware/tree/bka), `bka` (pushed 2026-10-31) | 34 tree entries including `audio_dsp`, `cam_vpu1/2/3`, `md1img`, `scp`, `spmfw`, `sspm`, `tee`, `gz`, `lk`, `preloader_ufs` and paired `_in` images | Low-level partition/firmware **reference**, **NOT** an automatically safe flash package; identify regional compatibility and image hashes |
| **P0** | [kernel_xiaomi_mt6785](https://github.com/Saikrishna1504/kernel_xiaomi_mt6785), `main`/`kaeru` | `main` observed Makefile **4.14.357-openela**; current GitHub branch listing contains only `main` and `kaeru` | Power/4.14 lineage and comparison baseline. **Not a published 4.19 tree on the checked branches** |
| **P1** | [hardware_mediatek](https://github.com/Saikrishna1504/hardware_mediatek/tree/lineage-23.2), `lineage-23.2` (pushed 2026-11-15) | Shared MTK HAL components: `aidl/bluetooth`, `aidl/boot`, `aidl/gadget`, `aidl/health`, `aidl/thermal`, `aidl/memtrack` | Android 16/modern userspace compatibility; HAL AIDL code **not** a standalone mainline Linux driver |
| **P1** | [hardware_xiaomi](https://github.com/Saikrishna1504/hardware_xiaomi/tree/lineage-24.0), `lineage-24.0` | Device-vendor glue / hardware abstraction | Pair exact version with `device.mk`; shared code may serve many Xiaomi devices |
| **P1** | [Imsservice](https://github.com/Saikrishna1504/Imsservice/tree/new), `new` | APKTool/decompiled MediaTek IMS app with smali and resources; pushed 2026-04-28 | Investigate VoLTE/VoWiFi/ViLTE compatibility; proprietary code, redistribution/license review required |
| **P1** | [device_xiaomi_begonia-pbrp](https://github.com/Saikrishna1504/device_xiaomi_begonia-pbrp/tree/twrp-12.1), `twrp-12.1` (2024 source) | PBRP recovery device tree, `prebuilt/Image.gz`, `dtb/mtk.dtb`, `dtbo.img`, fstab and keymaster/gatekeeper/TEE binaries | Recovery archival reference; README checkboxes are **maintainer claims**, not modern Android 16 compatibility proof |
| **P1** | [local_manifests](https://github.com/Saikrishna1504/local_manifests/blob/udc/mt6785.xml), `udc` | Reproducibility manifest linking device, kernel, vendor, firmware, MTK/Xiaomi hardware, SELinux and external camera repo | **Detects an important kernel mismatch (see §4)**; old branch labels may be stale |
| **P2** | [vendor_redmi_begonia-ims](https://github.com/Saikrishna1504/vendor_redmi_begonia-ims), `udc` **archived** (2025) | IMS blobs/packages from an earlier ROM generation | Historical reference, not current primary source |
| **P2** | [vendor_MiuiCameraLeica](https://github.com/Saikrishna1504/vendor_MiuiCameraLeica), `udc` **archived** | Camera vendor payload / configs; README says “for begonia” | Compare historical camera integration; license and Xiaomi proprietary assets |
| **P2** | [MiuiCamera_smali](https://github.com/Saikrishna1504/MiuiCamera_smali), `OS2.0.200.0.VNLMIXM` | Decompilation/patch research for MIUI Camera, not driver source | Reverse engineering lead, **not** proof this port works on begonia |
| **P2** | [device_redmi_begonia-kernel](https://github.com/Saikrishna1504/device_redmi_begonia-kernel/tree/vlc), `vlc` (2024) | Prebuilt `Image`, DTB/DTBO and .ko modules including `wlan_drv_gen4m`, `wmt_drv`, `gps_drv`, `bt_drv`, `fpsgo` | Historical *prebuilt binary* baseline; no modern 4.19 claim, verify matching hashes/license |
| **P2** | [OTA](https://github.com/Saikrishna1504/OTA/blob/16/begonia.json), `16` | `begonia.json` lists an **old** VoltageOS 5.3 build from **2025-11-20**, not the latest Axion kernel | Useful release metadata/hashes; **historical** and project-specific |
| **P2** | [local_manifest](https://github.com/Saikrishna1504/local_manifest/blob/main/local_manifest.xml), `main` (2023) | Historical Android 13-era Trinity/Nova-based manifest | Do not confuse with current `local_manifests/mt6785.xml` |
| **P2** | [AnyKernel](https://github.com/Saikrishna1504/AnyKernel) `master` | Kernel flashing ZIP/payload tooling (2023) | Analyze packaging and device assertions; do **not** run/fl ash unreviewed ZIP |
| **Low** | [Begonia_OSS](https://github.com/Saikrishna1504/Begonia_OSS) `main` | Contains only README and Dolby EQ `dax-default.xml` in this audit | **Not a complete begonia OSS device/kernel tree**, despite name |

### Excluded misleading leads

- [android_kernel_device_modules_6.1](https://github.com/Saikrishna1504/android_kernel_device_modules_6.1) is a **fork of mt6897-devs**, for a different modern MediaTek platform, **not evidence of Linux 6.1 running on begonia**.
- [device_xiaomi_duchamp](https://github.com/Saikrishna1504/device_xiaomi_duchamp) belongs to **duchamp**, not begonia; [flashing_guide](https://github.com/Saikrishna1504/flashing_guide) currently has only `duchamp/` pages. The identical maintainer does not imply shared board images.
- [manifests](https://github.com/Saikrishna1504/manifests/tree/lineage-23.2) is a **large generic Axion/Lineage manifest** with snippets for multiple kernel generations, including 6.1/6.18; those snippet numbers **are not begonia kernel claims**.

## 3. Exact 4.19 transition commits — newly identified

[device_redmi_begonia `axion` `BoardConfig.mk`](https://github.com/Saikrishna1504/device_redmi_begonia/blob/axion/BoardConfig.mk) contains:

- `TARGET_KERNEL_SOURCE := kernel/xiaomi/mt6785`
- `TARGET_KERNEL_CONFIG := k85v1_64_k419_defconfig vendor/begonia.config`
- `BOARD_KERNEL_IMAGE_NAME := Image.gz-dtb`
- `BOARD_BOOTIMG_HEADER_VERSION := 2`
- `TARGET_KERNEL_CLANG_VERSION := r416183b`
- `VENDOR_SECURITY_PATCH := 2022-04-01` — an *old vendor security patch label*, even if current Android userspace is modern.

Commit history inspected from GitHub's actual commit APIs:

| UTC date | Commit | Technical change | Why it matters |
|---|---|---|---|
| **2026-11-13 15:01:01** | [d78e16d11686](https://github.com/Saikrishna1504/device_redmi_begonia/commit/d78e16d11686806b1f0b24c6b3c149255a950ac0) | “Build 4.19 kernel”: defconfig + `vendor/begonia.config` fragment, DTBO generation | Explicit begonia 4.19 build-target declaration |
| **2026-11-13 15:01:21** | [46c71c286a14](https://github.com/Saikrishna1504/device_redmi_begonia/commit/46c71c286a14d0be1fd262e9ebe17749258c200e) | SELinux rules for 4.19 sysfs, GPU/battery, HAL | Bridges changed driver/sysfs paths and security policies |
| **2026-11-13 15:01:21** | [1f27a5cc808d](https://github.com/Saikrishna1504/device_redmi_begonia/commit/1f27a5cc808d3eb13dc0b093a85c33fc50498165) | `init.mt6785.rc` changes: scheduler `schedutil`, UClamp, performance/power groups | Userspace initialization migrated from older 4.14 interface |
| **2026-11-13 15:01:21** | [f0255137e02a](https://github.com/Saikrishna1504/device_redmi_begonia/commit/f0255137e02ab26039392f795c72a03a97fb2287) | `configs/powerhint.json` migrated to 4.19; 302 lines changed | Device-specific performance/power policy |
| **2026-11-14 09:43:20** | [dd3c64579236](https://github.com/Saikrishna1504/device_redmi_begonia/commit/dd3c6457923662570d4b83212112cd55c74d8a41) | fstab USB OTG and SD-card sysfs paths for 4.19 | Platform and device-path differences |
| **2026-11-15 09:53:44** | [38c6dfbba60f](https://github.com/Saikrishna1504/device_redmi_begonia/commit/38c6dfbba60f008be7f07ff8fb77614bd45c46a1) | Clang `r416183b`, NO_GCC, `Image.gz-dtb` | Toolchain and boot-image artifact compatibility |

**Very important provenance detail:** commit messages for SELinux, init and powerhint explicitly cite **rosemary** patches as their starting point; this supplies an actionable path for a side-by-side Git patch comparison instead of speculative reverse engineering.

### Key gap: the exact build manifest is inconsistent

The separately published [`local_manifests/mt6785.xml`](https://github.com/Saikrishna1504/local_manifests/blob/udc/mt6785.xml) selects **`device_redmi_begonia@axion`** while pinning **`kernel_xiaomi_mt6785@main`**. The latter was separately inspected and still has a **Linux 4.14.357-openela Makefile**, and only `main`/`kaeru` public branches were listed. So the *manifest as read* does **not** establish a working 4.19 build; it may be an old manifest or the new kernel code lives elsewhere.

In the inspected [LineageOS MT6785 4.19 tree](https://github.com/LineageOS/android_kernel_xiaomi_mt6785/tree/lineage-24.0), `arch/arm64/configs/k85v1_64_k419_defconfig` exists, but **`arch/arm64/configs/vendor/begonia.config` returned 404**, and the axion device tree does not contain a file by that name either. **This is a concrete missing build artifact, not proof the kernel port is fake.** Request the kernel URL + exact SHA + fragment file and check whether a separate fork contains them.

**Avoid claiming the 4.19 kernel itself is published merely from these userspace commits.** [Developer post #1657](https://t.me/RedmiNote8ProUpdates/1657) states he has a working prototype; the full reproducible source-to-image chain is still unverified. Our earlier [23](23-419-TELEGRAM-OUTREACH.md) has the outreach draft.

## 4. Blob compatibility patches: valuable reverse-engineering inputs

The [axion device tree](https://github.com/Saikrishna1504/device_redmi_begonia/tree/axion/blob-patches) exposes **10 IMS patches** and **4 MIUI Camera patches** as readable patches. Exact source attribution remains in patch headers; **do not credit every individual change to one developer**.

### IMS/VoWiFi

- [ImsService patch 0010](https://github.com/Saikrishna1504/device_redmi_begonia/blob/axion/blob-patches/ImsService/0010-ImsService-WfcHandler-Fix-fatal-crash.patch) fixes a crash caused by a `ClassCastException` from `ImsManager` to `MtkImsManager` in `WfcHandler.onWfcPdnError`. This is a concrete **VoWiFi** lead, not proof end-to-end carrier certification.
- [Patch 0006](https://github.com/Saikrishna1504/device_redmi_begonia/blob/axion/blob-patches/ImsService/0006-ImsService-Fix-NPE-on-ImsCallSessionProxy.patch) guards a null `MtkImsCallSessionProxy` after a reported crash.
- [Patch 0008](https://github.com/Saikrishna1504/device_redmi_begonia/blob/axion/blob-patches/ImsService/0008-ImsService-Switch-to-shared-libs-to-mtk-frameworks.patch) adds MediaTek framework shared-library declarations. Other patches adapt API method signatures, avoid outdated telephony APIs and update SMS paths.
- The actual upstream packages also appear in [vendor blobs](https://github.com/Saikrishna1504/vendor_redmi_begonia/tree/bka/proprietary/system/priv-app/ImsService) and the decompiled [Imsservice](https://github.com/Saikrishna1504/Imsservice) tree; remember proprietary licensing and carrier-specific modem provisioning.

### Camera and Codec2

- [MiuiCamera patch 0001](https://github.com/Saikrishna1504/device_redmi_begonia/blob/axion/blob-patches/MiuiCamera/0001-ICustomCaptureResult-Fix-CaptureResultExtras-and-Tot.patch), dated **2026-10-15** in patch header, updates reflected `CaptureResultExtras` and `TotalCaptureResult` constructor arguments for modern Android.
- Patches 0002–0004 adapt gallery intent, process handling and application behavior. The device tree includes `camera/CameraProviderExtension.cpp` and `libshims/camera`.
- [`extract-files.py`](https://github.com/Saikrishna1504/device_redmi_begonia/blob/axion/extract-files.py) contains concrete `blob_fixups`: MediaTek Codec2 service dependency updates, old `libcodec2_hidl@1.x` renamed versioned bindings, camera libraries and `libshim_c2`. This is an **excellent map of binary ABI breakages** that could also inform compatible Android/Halium ports.
- Proprietary vendor archives include MIUI Camera APK split chunks and camera tuning binaries: **reference provenance, do not duplicate into the research repo**.

**Linux-port scope:** Android APK smali and JNI patches are **not directly reusable as native Linux drivers**. The reusable lessons are ABI/protocol behavior, configuration, reported bugs and possible device-specific driver parameters. Porting to Ubuntu Touch may involve Halium/libhybris, while mainline Linux needs native kernel/userspace work.

## 5. Audio, GPU, power and peripheral research opportunities

- [`configs/audio/audio_policy_configuration.xml`](https://github.com/Saikrishna1504/device_redmi_begonia/blob/axion/configs/audio/audio_policy_configuration.xml) declares `Built-In Mic`, `Built-In Back Mic`, `Voice Call In`, and `Echo Ref In` routes. The `configs/audio/audio_param/` folder contains mic gain, DMNR, speech, echo, VOW, NXP smart amp and recording profiles. **High priority for UT microphone comparison** with Droidian; audio HAL availability and runtime logs still required.
- [`libshims/audio/libshim_audio.cpp`](https://github.com/Saikrishna1504/device_redmi_begonia/blob/axion/libshims/audio/libshim_audio.cpp) and extraction script replace/append old library dependencies; useful for Android audio compatibility triage.
- [`configs/powerhint.json`](https://github.com/Saikrishna1504/device_redmi_begonia/blob/axion/configs/powerhint.json), `rootdir/etc/init.mt6785.rc`, SELinux `genfs_contexts` and MediaTek thermal policies document CPU frequency, UClamp and daemon/sysfs expectations.
- [`hardware_mediatek`](https://github.com/Saikrishna1504/hardware_mediatek/tree/lineage-23.2) provides reusable **Android** services for Bluetooth, USB gadget, boot partitions, thermal and battery/health, memory tracking and more; compatibility with a given begonia kernel **must be checked**.
- [`vendor_redmi_begonia-firmware`](https://github.com/Saikrishna1504/vendor_redmi_begonia-firmware/tree/bka/images) includes paired files with `_in` suffix and critical boot/secure-world pieces. **Do not infer _in = India model automatically**; establish naming/region intent from the specific build and source before using any image. **Never cross-flash preloader/LK, modem or trusted firmware merely because the repository is public**.
- [`proprietary-files.txt`](https://github.com/Saikrishna1504/device_redmi_begonia/blob/axion/proprietary-files.txt) identifies an extraction baseline **MIUI V12.5.8.0.RGGMIXM / Android 11**. This is a **blob-source fingerprint**, not a statement that every binary in the current repo has been individually matched/hardened or that it is safe to flash any vendor partition.

## 6. Test and research backlog — next actionable steps

1. **Ask @Saikrishna1504:** 4.19 kernel repository URL, SHA, complete `vendor/begonia.config` fragment, DTS/DTBO changes, exact Android ROM/vendor/firmware pairing, bootlogs, known working hardware, expected release/license. Include the concrete [13–15 Nov commits](#3-exact-419-transition-commits--newly-identified) in the request.
2. **Reproduce the source graph read-only:** `device_redmi_begonia@axion` + `vendor_redmi_begonia@bka` + `vendor_redmi_begonia-firmware@bka` + the kernel source he confirms; do **not** claim the published historical `local_manifests/mt6785.xml` fully resolves the 4.19 stack.
3. **Audio bug study for UT:** compare this Android 11-derived `audio_policy_configuration.xml`, `audio_param`, `audio.primary.mt6785.so` dependencies against Droidian and UT Halium 10 audio policy, keeping reference versions and avoiding incompatible binary swaps.
4. **Video Codec2 and camera:** analyze `extract-files.py` fixup chains and `libshim_c2` for Android ABI maintenance; log which changes are userspace versus kernel.
5. **IMS:** evaluate 10 patches as an *Android telephony* compatibility series with precise test conditions (carrier, region, LTE/VoWiFi provisioning). Never equate an APK patch with certified VoLTE on Linux.
6. **Firmware safety:** inventory partitions and hashes in the low-level image bundle; verify provenance/region and check licenses; keep **NVRAM/NVDATA/IMEI** private and untouched.
7. **Recovery comparison:** compare 2024 PBRP tree with official TWRP/OrangeFox and current recovery requirements; README’s checked boxes are **historical maintainer assertions**.
8. **Machine-readable inventory:** see [saikrishna-source-inventory.csv](../../../data/matrices/saikrishna-source-inventory.csv) for exact repo, branch, role, status and test gaps.

## Evidence summary

**High-confidence directly observed:** GitHub repo metadata/branches, file trees, `BoardConfig.mk`, `proprietary-files.txt`, `local_manifests/mt6785.xml`, 2026-11-13 through 15 commit messages and changed files, patch text including WfcHandler failure, specific media/camera fixups and vendor firmware filename inventory.

**Author-reported only:** working Linux 4.19 on real begonia with video fix, VoWiFi/ViLTE and MIUI Camera on custom Android; the attached image and full source-to-binary chain have not been independently checked here.

**Not established:** exact published Linux 4.19 kernel patchset and `vendor/begonia.config`, successful end-to-end reproduction/boot on the owner’s device, hardware support of all panel revisions, full legality of distributing third-party binaries, current OTA/certified payment compatibility.

**No phone operations or binary copying were undertaken.** Use [18](../recovery/18-DEVICE-PREFLIGHT-READONLY.md) before any hands-on work.
