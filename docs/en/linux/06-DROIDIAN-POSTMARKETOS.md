# 06 — Droidian & postmarketOS on Xiaomi Redmi Note 8 Pro (`begonia`)

> **2026-11-21 correction / build-specific status:** this report's `Wi-Fi broken` matrix concerns the original upstream-style pmOS/Dinolek package. A **separate third-party experimental** [begonia-pmos-tianma](https://github.com/criollojoel10/begonia-pmos-tianma) build documents 2026-09-27 working WLAN (`wlan_gen4m` vendor driver, WMT firmware, `wlan0`, 2.4/5GHz, DHCP). This report was **not reproduced by this auditor**. Wi-Fi still lacks an upstream-native driver integration for this board. [Porting and evidence details](../../ru/kernels/22-KERNEL-FORWARD-PORT-AI-INTEGRITY-RU.md).

Researched 2026-11-21 (JST). Research-only: nothing was flashed or downloaded. Citation style: URL + date + verified/inferred + confidence (high/medium/low). pmOS wiki = wiki.nura.eco (continuation of wiki.postmarketos.org; redirects verified 2026-11-21). Cached full pages: pmOS wiki `oldid=109575`, devices.ubuntu-touch.io (both fetched 2026-11-21, see shared context pack).

---

## 1. postmarketOS port

### 1.1 Where the port lives (verified directly, 2026-11-21)

pmaports is re-hosted at `gitlab.nura.eco/nura/pmaports` (project id 226, branch `main`, last activity 2026-11-21 — active today). Both device packages sit in `device/testing/`:

- `device/testing/device-xiaomi-begonia/` — 4 files: `APKBUILD`, `deviceinfo`, `kernel-cmdline.conf`, `modules-initfs` (GitLab tree API: `https://gitlab.nura.eco/api/v4/projects/nura%2Fpmaports/repository/tree?path=device%2Ftesting%2Fdevice-xiaomi-begonia&ref=main`). Verified. Confidence: high.
- `device/testing/linux-postmarketos-mediatek-mt6785/` — `APKBUILD` + `config-postmarketos-mediatek-mt6785.aarch64` (same API, path `.../linux-postmarketos-mediatek-mt6785`). Verified. Confidence: high.

Raw files fetched from `https://gitlab.nura.eco/nura/pmaports/-/raw/main/...` (verified 2026-11-21, self-signed cert → `curl -sk`).

### 1.2 deviceinfo (verbatim fields, verified)

Source: `device/testing/device-xiaomi-begonia/deviceinfo`, ref `main`, 2026-11-21. Confidence: high.

| Field | Value |
|---|---|
| `deviceinfo_name` | `"Xiaomi Redmi Note 8 Pro"` |
| `deviceinfo_manufacturer` | `"Xiaomi"` |
| `deviceinfo_codename` | `"xiaomi-begonia"` |
| `deviceinfo_year` | `"2019"` |
| `deviceinfo_arch` | `"aarch64"` |
| `deviceinfo_chassis` | `"handset"` |
| `deviceinfo_drm` | `"true"` |
| `deviceinfo_external_storage` | `"true"` |
| `deviceinfo_generate_bootimg` | `"true"` |
| `deviceinfo_bootimg_custom_args` | `"--header_version 2 --dtb /boot/dtbs/mediatek/mt6785-xiaomi-begonia.dtb --recovery_dtbo /boot/empty.dtbo"` |
| `deviceinfo_flash_method` | `"fastboot"` |
| `deviceinfo_flash_sparse` | `"true"` |
| `deviceinfo_rootfs_image_sector_size` | `"4096"` (comment: "Required for devices using UFS as storage") |
| `deviceinfo_flash_kernel_on_update` | `"true"` |

boot.img offsets: base `0x40078000`, kernel `0x00008000`, ramdisk `0x07c08000`, second `0xbff88000`, tags/dtb `0x0bc08000`, pagesize `2048` (all verified from the raw file).

### 1.3 Device package APKBUILD (verified)

Source: `device/testing/device-xiaomi-begonia/APKBUILD`, ref `main`, 2026-11-21. Confidence: high.

- `maintainer="Dinolek <git@dinolek.me>"` — Dinolek is the pmOS begonia maintainer (matches Nura wiki and the `mt6785-mainline` work).
- `pkgname=device-xiaomi-begonia`, `pkgver=6`, `pkgrel=0`, `license="MIT"`, `arch="aarch64"`.
- `depends="firmware-xiaomi-begonia-touchscreen linux-postmarketos-mediatek-mt6785 mesa-vulkan-panfrost mkbootimg postmarketos-base"` — note `mesa-vulkan-panfrost` (Mali-G76 MC4 via Panfrost/PanVK Vulkan) and the **mainline** kernel package as the only kernel.
- Custom build step (verbatim comment): *"begonia bootloader needs empty dtbo, build it and add as recovery_dtbo to final image"* — it compiles a trivial DTS with `dtc`, packs it with `mkdtboimg`, and ships it as `/boot/empty.dtbo`.
- `modules-initfs` (initramfs-critical mainline modules, verified): `lm36274_bl`, `lm363x-regulator`, `novatek-nvt-ts-spi`, `panel-novatek-nt36672a`, `ti-lmu` — i.e. TI LMU backlight, Novatek SPI touchscreen, Novatek NT36672a panel: all **vanilla mainline drivers**.
- `kernel-cmdline.conf` (verified): `bootopt=64S3,32N2,64N2` (MediaTek boot-option string preserved for LK).

### 1.4 Kernel package — what "Mainline: yes / (Close to) Mainline" means here

Source: `device/testing/linux-postmarketos-mediatek-mt6785/APKBUILD`, ref `main`, 2026-11-21. Confidence: high.

- `pkgname=linux-postmarketos-mediatek-mt6785`, **`pkgver=6.16.4`**, `pkgrel=1`, `pkgdesc="Mainline kernel fork for MT6785"`, `arch="aarch64"`, license `GPL-2.0-only`.
- `source="https://gitlab.postmarketos.org/mt6785-mainline/linux/-/archive/6.16.4-r0/linux-6.16.4-r0.tar.gz"` (tag `6.16.4-r0`); built with clang/LLVM (`LLVM=1`, `lld`), `pmb:kconfigcheck-community` option; config comment: *"Kernel config based on: arch/arm64/configs/defconfig"*.
- Note: `gitlab.postmarketos.org/mt6785-mainline/linux` API did not return JSON for my unauthenticated tag query (see Limitations); the URL/tag above are taken verbatim from the APKBUILD `source=` (verified file content). Dinolek also has a GitHub `Dinolek/mt6785-mainline` repo (API-verified, last push 2026-06-17).

Explanation of the wiki terminology — pmOS device pages carry a "Mainline" field. On the begonia page (Nura wiki, `oldid=109575`, cached 2026-11-21) the row reads verbatim: *"Mainline … Instead of a Linux kernel fork, it is possible to run [(Close to) Mainline] … | yes"*. Concretely for begonia:

- "Downstream" would be the Android vendor kernel (stock: 4.14.141) — an Android driver fork with proprietary glue.
- "(Close to) Mainline" means a small fork of the **vanilla Linux kernel** carrying only the enablement patches for MT6785/begonia (here: 6.16.4 + the `mt6785-mainline` series).
- "yes" = the port ships exactly that: Linux 6.16.4 base, not an Android kernel. The `modules-initfs` list above (mainline panel/touch/backlight drivers) and `mesa-vulkan-panfrost` confirm it. Confidence: high (verbatim sources).

### 1.5 What works / what's broken on pmOS

From the pmOS/Nura wiki status table (cached full page, `oldid=109575`, fetched 2026-11-21):

Broken (each row verbatim `| Broken |`): **Battery** ("Whether charging and battery level reporting work"), **Audio** ("Audio playback, microphone, headset and buttons"), **Camera**, **IR TX**, **Wi-Fi**, **Bluetooth**, **GPS**, **Calls**, **SMS**, **Mobile data**, **Proximity**. Confidence: high.

Working (per the same table, from the shared context pack's verified full-page read — page structure confirmed by the broken rows above): **screen, touch, GPU, NFC, FDE, OTG, sensors (partial — proximity broken), haptics**. Confidence: high for the set, medium for individual rows (not re-quoted line-by-line here).

### 1.6 UIs tested — user reports (medium confidence, quoted as user notes)

From the wiki "Users owning this device" section (cached page, lines 81 & 85, 2026-11-21):

- User **Halhadus** (also a member of the begonia-linux Droidian org, see §2.2): *"running pmOS, using as server, you can enable kernel configs to use USB Ethernet, Phosh working good"*
- User **Letstry pmos**: *"Posh working the best. KDE not passing load screen, GNOME freezing when changing brightness. Haven´t suceeded in having Internet via USB."*

These are individual user reports on a community wiki, not maintainer test results. Confidence: medium. Net: **Phosh works; KDE Plasma Mobile doesn't reach the lock screen; GNOME shell freezes on brightness changes; USB networking unsuccessful for that user** (Halhadus implies USB Ethernet gizmo is possible with extra kernel configs).

### 1.7 MR !1909 — the initial port MR (verified via GitLab API, 2026-11-21)

`https://gitlab.nura.eco/nura/pmaports/-/merge_requests/1909` (API: `/api/v4/projects/nura%2Fpmaports/merge_requests/1909`). Confidence: high for all fields below.

- **Title:** `xiaomi-begonia: new device`
- **Description:** only a link — `https://wiki.postmarketos.org/wiki/Xiaomi_Redmi_Note_8_Pro_(xiaomi-begonia)`
- **State:** `merged`; **created** 2021-01-30T17:26:15Z; **merged** 2021-01-31T13:29:47.669Z; source branch `xiaomi-begionia` (sic, typo preserved); target `master`.
- **Single commit:** `xiaomi-begonia: new device (Redmi Note 8 Pro) (MR 1909)` (short id `2748241a`, created 2021-01-31T14:29:09+01:00) — verified via the MR `commits` endpoint.
- **MR !1909 authorship RESOLVED (live page capture 2026-11-21T09:52Z, archive/human-nura-mr1909-page-live-2026-11-21.html)**: the port branch originated from gitlab.com:michaelskyf/pmaports ('xiaomi-begionia'); imported to the Nura re-host by "Administrator @root" (import by Michał Kaborodo, 2021-01-30); reviewed/approved by Alexey Min and Bart Ribbers (postmarketOS); merged 2021-01-31 as 2748241a. The 'Administrator' author is an import artifact, not a mystery author.
- Historical vs current: the MR added the device package in Jan 2021; the **mainline kernel package (`linux-postmarketos-mediatek-mt6785`, 6.16.4) is the current state** — when the switch from the original 2021 kernel happened is not established by this research (see Limitations).

### 1.8 Installation (from wiki + deviceinfo; verified/inferred mix)

- Supported flash method per deviceinfo: **fastboot** (`deviceinfo_flash_method="fastboot"`, boot.img v2 with DTB) — i.e. standard pmbootstrap flow: `pmbootstrap install`, then fastboot flash boot + push/flash rootfs image. Confidence: high (deviceinfo) / high for pmbootstrap being the canonical path.
- The wiki also documents a **recovery-mode install** (`adb push /tmp/postmarketOS-export/pmos-xiaomi-begonia.zip /sdcard`, then flash from recovery — snippet verified in search result of the Nura wiki page, 2026-11-21). Bootloader unlock for begonia is via mtkclient (`mtk da seccfg unlock`) per the wiki (shared context pack, verified 2026-11-21).

---

## 2. Droidian port

### 2.1 What Droidian is (verified from official docs)

Source: `https://docs.droidian.org/` (fetched 2026-11-21). Verbatim: *"Droidian is a GNU/Linux distribution based on Debian for mobile devices. The goal of Droidian is to be able to run Debian on Android phones. This is accomplished by using well-known technologies such as libhybris and Halium."* The device-image README adds: *"Droidian is a GNU/Linux distribution based on top of Mobian, a Debian-based distribution for mobile devices"* (`https://raw.githubusercontent.com/begonia-linux/droidian-xiaomi-begonia/trixie/README.md`, 2026-11-21). So: Debian/Mobian user space + **libhybris bridging to the Android vendor blobs**, running on a Halium-adapted Android kernel. Confidence: high (verbatim).

Image-install model (same README, verified): two flavors — (a) **fastboot-flashable device image** (`flash_all.sh`, supports Full Disk Encryption, uses whole userdata); (b) **recovery-flashable zip** via `adb sideload` in TWRP: rootfs zip + optional `devtools` + optional **adaptation bundle** (kernel + device settings). Vendor-API mapping (verbatim): *"Device with an Android 9 vendor: api28; Android 10 vendor: api29; Android 11 vendor: api30"*. Default unlock passcode `1234`. Confidence: high.

### 2.2 Begonia Droidian builds — they exist and are actively built (verified, 2026-11-21)

Found via web search + GitHub API. The Droidian work lives in the device-specific GitHub org **`begonia-linux`** ("Linux on Xiaomi Begonia", 5 repos), members (API-verified): **behdanisohrab** and **Halhadus** (the same Halhadus who runs pmOS per §1.6).

| Repo | Purpose | Last push | Default branch |
|---|---|---|---|
| `begonia-linux/droidian-xiaomi-begonia` | "Droidian unified ci builds" | **2026-11-15** | `trixie` |
| `begonia-linux/adaptation-xiaomi-begonia` | "Droidian adaptation files for xiaomi-begonia" | 2025-04-27 | `droidian` |
| `begonia-linux/linux-android-begonia` | kernel — **fork of `rubencarneiro/linux-android-begonia`** (API-verified parent) | 2025-04-27 | `droidian` |
| `begonia-linux/linux` | (mainline kernel work) | 2024-05-09 | `next` |

**Release (verified via GitHub API 2026-11-21):** `droidian-xiaomi-begonia` has one release, tag/name `nightly`, published 2026-11-15T04:45:20Z, assets: `droidian-UNOFFICIAL-phosh-phone-xiaomi_begonia-api29-arm64-next_20261115.zip` (1,613,403,036 bytes ≈ 1.6 GB) + `SHA256SUMS`. Decoded: **UNOFFICIAL**, UI **Phosh**, device `xiaomi_begonia`, **api29** (= Android 10 vendor per the README mapping), arm64, rootfs channel `next`, build date 2026-11-15. Confidence: high.

**Halium version:** the image filename pins api29 (Android 10 vendor) → **Halium 10** by Droidian's api→vendor mapping; corroborated by the kernel being a fork of `rubencarneiro/linux-android-begonia`, whose branches (API-verified) are `halium-10.0`, `halium-10.0-cfw`, `halium-11`, `bookworm`, `lineage-17.1`, and by the UBports begonia port using `halium-10.0` (shared context pack). Inferred, not stated verbatim in fetched docs. Confidence: medium-high.

**Official vs unofficial:** official Droidian images are published by the `droidian-images` org (`rootfs-api28gsi-all` deprecated, `rootfs-api29gsi-all`/`api30gsi-all` archived, `droidian` = "Droidian unified ci builds" — API-verified 2026-11-21). Begonia is **not** in the official image set; it is a community build (asset literally marked `UNOFFICIAL`). Confidence: high.

### 2.3 Feature matrix of the Droidian begonia port (porter-claimed)

Source: `https://raw.githubusercontent.com/begonia-linux/adaptation-xiaomi-begonia/droidian/README.md` (verified 2026-11-21; repo last push 2025-04-27). These are the porter's claims, not independently tested. Confidence: medium (porter-authored list).

- **Camera:** ✔ *"With droidian-camera & gst backend it's working"*
- **Sensors:** brightness ✔, rotation ✔, **fingerprint ✔**, auto-brightness ❌, proximity ✔, vibration ✔
- **Cellular:** calls ✔, data ✔, SMS ✔, carrier info ✔, dual SIM ✔, MMS ✔
- **Sound:** speaker ✔, **microphone ✔**, headphones ✔, volume ✔, Bluetooth headphones ✔, call audio ✔
- **Network:** WiFi ✔, Bluetooth ✔, hotspot ❌ (*"can work with some fixes"*), NFC ✔
- **Misc:** SD card ✔, **Waydroid ✔**, GPS ✔ (partially), **encryption ❌**, MTP ✔
- **Credits (README):** Rúben Carneiro (rubencarneiro), Sohrab Behdani (behdanisohrab), NotKit; bases include `rubencarneiro/adaptation-xiaomi-begonia`, the UBports begonia port (`gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia`), `droidian-mt6765/adaptation-droidian-garden`, `dyingwillow/droidian-rosemary` (rosemary = also MT6785). Support: `https://t.me/begonia_linux`.

### 2.4 What the Droidian-on-begonia path required (inferred from verified artifacts)

Confidence: medium (each element individually verified, the assembly is inference).

1. **Halium-compatible vendor partition**: Android 10 vendor (api29) — begonia has official Android 9/10/11 builds, so a 9-vendor (api28) or 10-vendor (api29) base is available; the port chose api29.
2. **Halium kernel**: an Android-kernel fork patched to the Halium 10 spec — reused from the Ubuntu Touch port's kernel tree (`rubencarneiro/linux-android-begonia`, branch `halium-10.0`), not written from scratch (`begonia-linux/linux-android-begonia` is a fork of it).
3. **Adaptation bundle**: device packages (audio policy, camera backend `droidian-camera` + GStreamer, sensors, network config) in `adaptation-xiaomi-begonia`, shipped as a recovery-sideloadable bundle alongside the generic api29 rootfs zip.
4. Bootloader unlocked (mtkclient) and TWRP recovery for sideload.

---

## 3. Architecture comparison — pmOS vs Droidian vs Ubuntu Touch

All three rows cite verified sources (§1, §2; UT: devices.ubuntu-touch.io device page for begonia, cached 2026-11-21, Halium 10.0, "Under heavy development relying only on the device porters", noble 24.04 stable 24.04-1.4 2026-07-13 per shared context pack).

| | **postmarketOS** | **Droidian (begonia build)** | **Ubuntu Touch** |
|---|---|---|---|
| Base OS | Alpine Linux (pmOS) | Debian/Mobian + libhybris | Ubuntu Touch (noble 24.04) |
| Kernel | **Mainline Linux 6.16.4** (`mt6785-mainline` fork of vanilla; not an Android kernel) | Halium kernel: Android kernel fork to Halium 10 spec (fork of rubencarneiro's tree) | Halium 10.0 kernel (`kernel-xiaomi-mt6785`, branch `halium-10.0`) |
| Hardware access | Native mainline drivers only, no Android blobs | libhybris → Android vendor blobs (audio, camera, modem, WiFi/BT firmware glue) | libhybris → Android vendor blobs (same principle, UT stack) |
| UI | Phosh (works best per user notes); KDE/GNOME problematic | Phosh (image is `phosh-phone`) | Lomiri (UT shell) |
| Works | Screen, touch, GPU (Panfrost/Mesa), NFC, FDE, OTG, haptics, most sensors | Calls, SMS, data, camera, sound incl. mic, WiFi, BT, NFC, fingerprint, Waydroid, SD, MTP | Calls, SMS, data, camera, WiFi, BT, hotspot, NFC, fingerprint, battery/charging, Waydroid, SD, MTP |
| Broken | Battery, audio, camera, WiFi, BT, GPS, calls/SMS/data (modem), proximity | Encryption, hotspot, auto-brightness; GPS partial | Microphone, RTC time, VoLTE (global), FM radio, auto-brightness (repowerd#11, global), GPS slow first fix (global) |
| Maturity | `device/testing`; port merged 2021-01-31; mainline kernel era active (kernel 6.16.4, pmaports activity 2026-11-21); NOT usable as a phone today | **UNOFFICIAL nightly**, CI active (2026-11-15); adaptation README dated 2025-04-27; community org | "Under heavy development", Basic support rating, medium popularity; stable 24.04-1.4 (2026-07-13); porting active (commits 2026-10) |
| Install | pmbootstrap → fastboot boot.img + rootfs; or recovery zip | Recovery `adb sideload` (rootfs api29 + adaptation bundle) or fastboot image | UBports Installer / manual Halium flash |
| Encryption | FDE works (per wiki) | ❌ | ❌ (per UT matrix — not listed as working) |

Assessment (my reasoning, marked as assessment): the pattern in the table is structural, not accidental — see §4.

---

## 4. Which port for which goal (assessment — reasoned, medium confidence)

**Why pmOS is broken where UT/Droidian work.** pmOS runs the mainline kernel: for MT6785, drivers for WiFi/BT (likely a MediaTek combo chip needing firmware+driver work), audio (MT6785 sound via MediaTek AFE/codec drivers), camera (MIPI/ISP pipeline), modem (Mediatek Genio/MTK modem interface), battery/fuel-gauge are missing or incomplete in vanilla Linux — the wiki "Broken" list is exactly the hardware that has no mainline driver yet. Droidian and Ubuntu Touch keep the **Android kernel** (Halium-fied) and reach the same hardware through the **Android vendor blobs** (blob → HAL → libhybris → glibc user space). The Android 10 vendor for begonia contains working audio/camera/modem/WiFi HALs, so everything the HALs cover works on day one; everything outside the HALs (FDE in Droidian's case, RTC on UT) does not. This is the standard Halium trade-off: instant phone functionality vs. dependency on the Android vendor stack and eventual dead-end for mainline convergence. (Architecture-level explanation; confidence: high for the mechanism, inferred for individual driver names — mainline MT6785 support status not audited per-driver.)

- **Goal: phone first** (calls, SMS, mobile data, camera, sound) → **Droidian** (per its matrix everything a phone does works, incl. mic) or **Ubuntu Touch** (same Halium base, more mature port infra, but its begonia matrix says **microphone broken** and RTC broken). Note the direct **contradiction**: Droidian README claims microphone ✔ while UT reports microphone ✘ on the same Halium 10 vendor — different audio stacks (Droidian `droidian-camera`/gst + Debian audio vs UT pulseaudio-modules-droid); both are porter-claimed, neither independently verified here.
- **Goal: pocket Linux computer / tablet-style, GPU-accelerated UI, longevity, FDE** → **pmOS**: true mainline (6.16.4), Mesa/Panfrost, full disk encryption works, no Android blob dependency, kernel keeps tracking upstream. Cost: today it is not a phone (no audio, no modem, no WiFi/BT, battery reporting broken) — currently suited to "server/gadget" use, exactly as wiki user Halhadus does ("using as server … USB Ethernet").
- **Droidian vs UT** (both Halium 10): Droidian gives a plain Debian rootfs (apt, normal GNU/Linux stack, Phosh) with more claimed features on begonia (mic, camera via gst, Waydroid) but is an UNOFFICIAL nightly from a 2-person org; UT has official-ish porting infrastructure, an installer, and a dated stable release, but a more restrictive app ecosystem and more broken items on this device (mic, RTC).

---

## 5. Limitations

- **`gitlab.postmarketos.org/mt6785-mainline/linux` API returned non-JSON** to an unauthenticated tag query (2026-11-21) — kernel repo tags not independently verified; source URL/tag cited verbatim from the pmaports APKBUILD instead.
- **Droidian Halium version is inferred** (api29 mapping + kernel fork lineage), not stated verbatim in any fetched page; docs.droidian.org is minimal and its `/info/` page is a 404. No begonia Droidian page exists on docs.droidian.org.
- **Droidian feature matrix is porter-claimed** (adaptation README, repo last pushed 2025-04-27); no independent test or issue tracker evidence was collected; CI builds are newer (2026-11-15). Treat individual ✔/❌ as unverified claims.
- **MR !1909 author is unresolvable** ("root"/Administrator on the Nura re-host); original upstream authorship not established.
- **pmOS "works" list** (screen/touch/GPU/NFC/FDE/OTG/sensors/haptics) is taken from the shared context pack's verified full-page read; this session re-verified only the "Broken" rows line-by-line. Proximity is broken on pmOS — "sensors work" is therefore partial.
- **Not consulted:** 4PDA threads for Droidian (not needed — GitHub sources were sufficient), live XDA (blocked per context pack), Telegram group `t.me/begonia_linux` (not fetched).
- Historical claim (MR merged 2021-01-31) is from the re-hosted Nura GitLab; upstream gitlab.postmarketos.org MR was not cross-checked.
