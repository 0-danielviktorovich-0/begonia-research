# 19 — Firmware terminology and Redmi Note 8 Pro architecture

**Language:** [English (this translation)](19-rom-terminology.md) · [Русский (authoritative original)](../../ru/android/19-ROM-TERMS-GLOSSARY-RU.md) · [English directory](../index.md).

> **Translation status: FULL DRAFT — technical/editorial review pending.** This is a complete English translation of the original Russian chapter, not just a digest. Source: [19-ROM-TERMS-GLOSSARY-RU.md](../../ru/android/19-ROM-TERMS-GLOSSARY-RU.md), Git Blob **b39c6c4d58fa47975195eae7e0e0d0f17f94bf03**, checked 2026-11-21. Dates and source verification apply to the underlying research, not a newly tested phone. Do not use this as a flashing procedure.

This guide explains terms from 4PDA/XDA and the project's technical reports. Unless specified otherwise, examples refer to Xiaomi Redmi Note 8 Pro (MT6785, begonia/begoniain).

## 0. The essentials in 30 seconds

**There is no simple progression “CFW → Non-CFW → GSI → Linux” where each subsequent type is newer or better.** These names describe different dimensions of a system.

| Question | Examples | What is being described |
|---|---|---|
| Who built Android and from what base? | Xiaomi MIUI (stock), device-specific AOSP/Lineage/crDroid, OEM port, GSI | Origin of the system image and extent of device adaptation |
| Which low-level layout is needed? | Historical begonia CFW, or Non-CFW / normal compatible factory base | Bootloader, vendor and firmware compatibility scheme |
| How is hardware supported? | Android kernel + HAL, Halium + libhybris, native/mainline Linux | Kernel and hardware access architecture |
| Which *version* of which component? | Android 16, MIUI 12.5 / Android 11 vendor, Linux 4.14 or 6.16, Ubuntu Touch 24.04 | **Four independent versioning systems** that must not be conflated |

**Typical mistake:** “A ROM with Android 16 must use Linux 6.x and drivers released in 2026.” It need not. Android userspace, vendor blobs and the kernel may come from entirely different generations. See [02 §1.3 and §4](02-FIRMWARE-HISTORY.md), [03](../kernels/03-KERNEL-HISTORY.md), and [11](../kernels/11-BLOBS-FIRMWARE-SOURCES.md).

## 1. Historical 4PDA categories (specific to begonia)

### CFW (Custom Firmware, as used by the begonia community)

**In plain language:** an early technical approach for adapting custom ROMs to the Redmi Note 8 Pro. Developers combined low-level components from different Android/MIUI generations and used **factory/engineering preloader and LK**. The approach helped boot experimental systems and offered a recovery route under the constraints of that era.

It is **not** a synonym for every custom Android ROM, ordinary root/Magisk, a visual skin or a fully open-source device.

- Historical account by developer Kshitij Gupta: [“Modding the Redmi Note 8 Pro — An Adventure”](https://medium.com/swlh/modding-the-redmi-note-8-pro-an-adventure-e473e84d4d14). It describes combining Android 9/10 firmware and using factory preloader/LK.
- Explanation by 4PDA topic curator TTTT555, dated 10 February 2021, around posts #7212–7214: [4PDA page covering CFW, Non-CFW and GSI](https://4pda.to/forum/index.php?showtopic=974421&st=7200). The key distinction is that CFW mixed older and newer low-level drivers around leaked service-oriented preloader components. **Evidence limit:** indexed snippets expose the explanation, but the reviewer's direct forum access returned HTTP 403; Hermes captured selected browser snapshots.
- [XDA CFW Megathread](https://xdaforums.com/t/guide-info-psa-redmi-note-8-pro-megathread-cfw.4056527/); archives and Brave captures exist in the research repository under archive/ and _cache/.

**Status:** historical/obsolete lineage; 4PDA's pinned catalog now treats old CFW ROMs as obsolete. **Risk:** incompatible LK, preloader, boot, dtbo or vbmeta images can render the device unbootable. Migration away from CFW must follow a tested, model-specific procedure. “CFW” **does not** imply guaranteed recovery.

### Non-CFW

**In plain language:** newer custom Android ROMs built for the ordinary compatible factory bootloader base of begonia, without the old engineering preloader/LK CFW bundle. Non-CFW **does not mean “no firmware.”**

- TTTT555 described Non-CFW as the descendant of CFW adapted to later stock bootloaders, with a more uniform recovery environment and simpler installation: [4PDA](https://4pda.to/forum/index.php?showtopic=974421&st=7200).
- The current [4PDA pinned custom-ROM index](https://4pda.to/forum/index.php?showtopic=974421) treats Non-CFW as the standard custom-ROM category.
- **Caution:** Non-CFW is not automatically compatible with every vendor image, recovery or kernel. Community instructions distinguish MIUI 11/12 Android 10 vendor bases from MIUI 12.5 Android 11 vendor bases. See [02 §1.3](02-FIRMWARE-HISTORY.md) and [10 §2](10-GUIDE-INDEX.md).

### GSI (Generic System Image)

**In plain language:** a broadly reusable Android system image enabled by [Project Treble](https://source.android.com/docs/core/architecture/treble), rather than necessarily built specifically for begonia.

- In typical GSI deployments the system layer changes while the existing vendor and kernel remain. Some devices also require vendor patches, vbmeta configuration or other adjustments: not every GSI ZIP changes only the system partition.
- GSI and Non-CFW are **not opposites**. One term describes the generality of the system image; the other describes begonia's historical low-level compatibility approach.
- [Google's official GSI definition](https://developer.android.com/topic/generic-system-image); [02 §2](02-FIRMWARE-HISTORY.md) documents historical begonia GSI problems involving sound, connectivity and animations.
- Do not confuse an **Android GSI** with a **Halium GSI** in UBports documentation: they are different images/environments that both use a generalized system layer.

### “Other” in 4PDA's index

“Other” is a **forum catalog section**, not a distinct firmware-image format. The index groups GSI-related experiments, Linux/UEFI and unusual builds there. The section label says nothing by itself about stock preloader compatibility.

## 2. Android ROM types: a separate classification dimension

| Term | Meaning | Example or caveat |
|---|---|---|
| **Stock / MIUI / factory ROM** | Manufacturer-provided Android and related images for an exact device/region | Rollback baseline; begonia's last official series is MIUI 12.5 / Android 11. [02 §1](02-FIRMWARE-HISTORY.md) |
| **Custom ROM** | Any third-party Android system modification; an umbrella term | May be CFW, Non-CFW, device-specific or GSI-derived |
| **Native ROM / device-specific build** | Android built with device tree, vendor configuration and kernel adaptations specifically for begonia | For example [crDroid for begonia](https://crdroid.net/begonia); verify exact releases and source trees in [02 §7.4](02-FIRMWARE-HISTORY.md) |
| **AOSP** | Android Open Source Project, the open platform underpinning Android | Does not imply every hardware driver is open-source |
| **LineageOS-based / crDroid / Evolution X** | Different Android operating-system projects | The project name does not determine vendor/kernel generation: identify the exact manifest, device, kernel and vendor revisions |
| **OEM port** | A manufacturer's Android UI and services ported from another device/vendor | OriginOS, ColorOS, EMUI or ROGUI; often additional proprietary dependencies. [02 §3.7](02-FIRMWARE-HISTORY.md) |
| **GSI-based adaptation** | A GSI plus targeted device-specific compatibility patches | May resemble a native ROM, but its build architecture differs |

**OFFICIAL/UNOFFICIAL**, when attached to a custom ROM, describes recognition by **that ROM project's maintainers**, not approval by Xiaomi, Android or LineageOS. “Official AxionOS” and “official crDroid” are separate statuses. Verify the tag against the actual project's own release site rather than only a forum post.

**Vanilla / GApps:** without/with preinstalled Google services. **OSS:** open-source components or a source-branch tag (such as Q-OSS/R-OSS); not proof that the complete driver stack is open-source. **Root, Magisk, KernelSU and APatch** describe privilege/kernel modification approaches, not separate ROM types.

## 3. Four layers of the device — the key porting model

    [APPLICATIONS AND INTERFACE]
    Android 16 / MIUI / crDroid
    or Ubuntu Touch 24.04 / Droidian / postmarketOS
                      |
                      v
    [SYSTEM SERVICES AND HARDWARE APIs]
    Android HAL and vendor blobs, used through Halium/libhybris by some Linux ports
    or native Linux drivers and userspace
                      |
                      v
    [KERNEL AND DEVICE TREE / DTBO]
    e.g. Linux 4.14.x (Android vendor/Halium)
    or a Linux 6.16.x+ MT6785 mainline-based port
                      |
                      v
    [BOOT CHAIN AND LOW-LEVEL FIRMWARE]
    BROM -> preloader -> LK -> kernel; vbmeta/AVB, modem, PMIC,
    panel/touch controller and other binary firmware

### Firmware is an overloaded word

1. **“Phone firmware”** in casual conversation may mean the entire ROM or operating-system environment.
2. A Xiaomi **firmware bundle/package** may contain low-level modem, bootloader, DSP, trusted-environment and related images, sometimes distributed apart from a complete MIUI ROM.
3. **Peripheral firmware** is device microcode loaded by Wi-Fi, Bluetooth, touch, DSP or similar drivers.
4. **Vendor blobs / vendor.img** contain often proprietary HAL libraries, configuration and sometimes peripheral firmware. They are neither the entire firmware package nor the kernel.
5. **Kernel source / kernel image** refers to source code or a compiled Linux kernel. Q-OSS and R-OSS are Xiaomi's Android 10/11-era source labels; an OSS label does not ensure that all modules are open or that blobs will work in every Android 16 ROM. See [03 §1](../kernels/03-KERNEL-HISTORY.md).

**Consequence:** there is no single safe “install the latest drivers” operation. Identify where each component is stored, which interfaces it implements and whether kernel, HAL, DTB/DTBO, modem firmware and userspace versions are compatible.

## 4. Linux ports do not necessarily use Android userspace

| Port | User-facing OS | Hardware-enablement approach | Advantages and limitations |
|---|---|---|---|
| [Ubuntu Touch begonia](https://devices.ubuntu-touch.io/device/begonia/) | Ubuntu Touch 24.04 | **Halium 10**, Android-vendor Linux 4.14.141 plus proprietary HAL | Many components work, but the official matrix reports microphone recording unavailable; VoLTE is experimental |
| [Droidian begonia](https://github.com/begonia-linux/adaptation-xiaomi-begonia) | Linux / Droidian | Android-derived kernel, libhybris and vendor components | Porter's README reports microphone support; useful comparison for Ubuntu Touch, not independently device-tested |
| [postmarketOS begonia](https://wiki.postmarketos.org/wiki/Xiaomi_Redmi_Note_8_Pro_(xiaomi-begonia)) | Alpine-based mobile Linux | Mainline-based MT6785 kernel fork and more native drivers | More flexible architecture, but the baseline port still lacks several functions such as telephony, cameras and audio; see [06](../linux/06-DROIDIAN-POSTMARKETOS.md) |

**Halium 10 is not “Ubuntu Touch 10” nor necessarily Android 10 as the visible OS.** Halium 10 denotes hardware-interface compatibility with Android 10-era vendor components, while the actual OS can be Ubuntu Touch 24.04.

**Mainline-based fork does not equal upstream Linux support.** Dinolek's MT6785 kernel may track a modern Linux release while retaining board- and SoC-specific changes absent from the upstream kernel tree. See [03 §4](../kernels/03-KERNEL-HISTORY.md) and [14](../kernels/14-MAINLINE-UPGRADE-PATH.md).

Translator's evidence note: a separate [2026-09 experimental Wi-Fi port](../../ru/kernels/22-KERNEL-FORWARD-PORT-AI-INTEGRITY-RU.md) reports wireless support on a non-baseline Linux 6.16.4 configuration. It does not negate the baseline status table.

## 5. Bootloaders and special partitions — a concise guide

| Term | Purpose |
|---|---|
| **BROM / BootROM** | Startup code inside the MediaTek SoC; possible emergency recovery access on supported firmware/security configurations |
| **Preloader** | Early platform/memory/USB initialization; incompatible images can cause serious boot failure |
| **LK / Little Kernel** | Next boot stage, potentially implementing checks and mode selection |
| **Fastboot** | A bootloader communication protocol for reading device info and writing partitions; it is **not** a ROM |
| **Recovery (TWRP/OrangeFox/PBRP)** | Separate maintenance/flashing environment, **version and vendor/encryption/layout compatibility matter** |
| **boot.img** | Usually kernel plus boot data/ramdisk, with composition depending on Android generation |
| **dtb / dtbo** | Device Tree hardware descriptions and overlays for panel, power and board peripherals |
| **vbmeta / AVB** | Android Verified Boot metadata; incorrect setup may prevent boot |
| **NVRAM / NVDATA / persist** | Per-device calibration and configuration; backups must remain private |
| **OTA** | Over-the-air OS update; does not guarantee low-level driver or boot-chain updates |
| **Treble / VNDK** | Android's system/vendor separation and compatibility interfaces |

**A-only / A/B** describe update-slot schemes; **dynamic partitions / super** describe logical partition layout. Neither can be inferred from Android version alone. Inspect the actual begonia partition scheme rather than copying instructions for another handset.

## 6. Frequent and potentially dangerous misconceptions

1. **“Android 16 = Android 16 drivers.”** Incorrect; the ROM may still use MIUI 12.5/Android 11-era vendor components and Linux 4.x.
2. **“Non-CFW means no firmware.”** Incorrect; it means no dependency on the *old CFW scheme*.
3. **“GSI is a newer Non-CFW.”** Incorrect: GSI describes a generic system image, while Non-CFW describes begonia's low-level compatibility.
4. **“OS version equals kernel version.”** Incorrect: Ubuntu Touch 24.04 can run Linux 4.14 when based on Halium 10.
5. **“An official recovery web page proves that its binary is new or Android 16-compatible.”** Incorrect. [Independent recovery audit](../research/17-INDEPENDENT-AUDIT.md): official TWRP site refreshed in 2026, newest listed official image from 2022; OrangeFox begonia is unmaintained and its last listed beta is CFW-only.
6. **“mtkclient always unbricks this phone.”** Incorrect; success depends on the exact hardware/software state and preserved unique partition data.
7. **“Enabling CONFIG_* is enough for a driver to work.”** Incorrect; device-tree nodes, pinctrl, regulators, firmware, compatible APIs and userspace configuration may all be necessary. [14 §0](../kernels/14-MAINLINE-UPGRADE-PATH.md).
8. **“OSS means every driver is open-source.”** Incorrect; proprietary vendor blobs may remain.
9. **“A mainline-based fork is fully upstream.”** Incorrect; verify whether the exact MT6785 patches reached upstream kernel.org.

## 7. How to describe a specific ROM precisely

Rather than labelling an image merely “Non-CFW Android 16,” record these fields (example, **not a real validated build**):

    name: "example, not a verified real build"
    kind: "native device-specific / GSI / OEM-port / Linux-port"
    cfw_era_compat: "CFW / Non-CFW / n-a / unknown"
    android_userspace: "unknown"
    halium_generation: "n-a or version"
    vendor_base: "MIUI branch + fingerprint/hash or unknown"
    firmware_bundle: "build + region + hashes or unknown"
    kernel: "version + tree + exact commit or unknown"
    boot_chain_requisites: "documented only / unknown"
    recovery_compat: "exact image + source + tested or unknown"
    panel_revision: "Tianma / CSOT / unknown"
    source_url: "link to original build post"
    source_code: "kernel/device/vendor/manifest, missing explicitly"
    tested_device: "begonia/begoniain; hardware revision"
    verified_on_device: false

For real images, never fill unknown fields by borrowing data from an adjacent ROM name or a newer Android release date.

### What to pursue in this project

- **First practical line:** the established Ubuntu Touch 24.04/Halium 10 port; work on sound, microphone, RTC, suspend and reliability.
- **Driver reference:** Droidian and related Android device/vendor/kernel trees, especially microphone routing.
- **Separate experimental line:** postmarketOS with a mainline-based MT6785 fork; prioritize power, Wi-Fi and audio before modem/camera.
- **Recovery line:** exactly identified matching stock Xiaomi images for the actual region/SKU, private NVRAM/NVDATA backups and an independently validated recovery route. Do not blindly replace the vendor base with the newest available bundle without ABI analysis.

## Evidence and limits of verification

- [TTTT555's 2021 4PDA explanation](https://4pda.to/forum/index.php?showtopic=974421&st=7200), search-indexed; direct fetch returned HTTP 403 to this reviewer, while Hermes captured selected pages/posts.
- [4PDA custom-ROM pinned index](https://4pda.to/forum/index.php?showtopic=974421), based on cached pages and indexed snippets.
- [XDA CFW Megathread](https://xdaforums.com/t/guide-info-psa-redmi-note-8-pro-megathread-cfw.4056527/), with live/archived captures in archive/ and _cache/.
- [Kshitij Gupta's historical engineering article](https://medium.com/swlh/modding-the-redmi-note-8-pro-an-adventure-e473e84d4d14).
- [Android Developers: GSI](https://developer.android.com/topic/generic-system-image), [UBports porting introduction](https://docs.ubports.com/en/latest/porting/introduction/Intro.html), [Ubuntu Touch begonia matrix](https://devices.ubuntu-touch.io/device/begonia/).
- More detailed version- and hardware-specific evidence: [02](02-FIRMWARE-HISTORY.md), [03](../kernels/03-KERNEL-HISTORY.md), [05](../linux/05-UBUNTU-TOUCH.md), [06](../linux/06-DROIDIAN-POSTMARKETOS.md), [07](../recovery/07-RECOVERY-SAFETY.md), [11](../kernels/11-BLOBS-FIRMWARE-SOURCES.md).

**Confidence:** high for general definitions and primary Google/UBports documentation; high that this is the terminology used by the cited 2021 curator, subject to direct 4PDA access limitations; **no physical device verification** of individual ROM/recovery compatibility. Source-linked research is not a guarantee that flashing will work.

---

**Translation review checklist for this draft:** section 0–7 and subheadings present; all technical tables and example fields retained; original URLs preserved; root-level relative Markdown paths normalized with ../../. Editorial/technical line-by-line sign-off still pending. [Translation policy](../../../i18n/README.md).
