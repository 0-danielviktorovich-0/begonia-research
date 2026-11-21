# 18 — Read-only device preflight before any Redmi Note 8 Pro porting experiment

Research/audit worksheet for the owner's **currently unknown custom ROM** on Redmi Note 8 Pro (`begonia` / possible `begoniain`). Companion: [17-INDEPENDENT-AUDIT.md](17-INDEPENDENT-AUDIT.md), [07-RECOVERY-SAFETY.md](07-RECOVERY-SAFETY.md), [11-BLOBS-FIRMWARE-SOURCES.md](11-BLOBS-FIRMWARE-SOURCES.md).

**Mode: observation only.** Do not unlock/relock, wipe, run a flash utility, patch vbmeta, repartition, install recovery, or reboot into an unsafe image as part of this worksheet. No phone has been connected for this report. If the phone cannot be identified confidently, stop before the first write.

## A. Minimum equipment

- A reliable **USB-C data** cable, charged handset, host computer and known-good USB port.
- Android Platform Tools: `adb` and `fastboot` installed on the host. On macOS, the official [Google Platform Tools](https://developer.android.com/tools/releases/platform-tools) archive is sufficient; Homebrew is an optional packaging route. On Linux, install from a trusted distribution or Google source.
- For actual **building** Halium kernel images, a Linux build environment is preferable; Apple Silicon macOS is fine for the *initial read-only audit*, and a Linux VM/remote builder can be prepared afterward.
- UART adapter, test-point cables, SP Flash Tool and mtkclient are **not** prerequisites for these discovery commands. They belong in a preplanned *recovery* procedure, after compatibility has been checked.

## B. Read-only Android commands (while the current ROM boots)

Enable USB debugging with the owner's consent; allow the host on the handset. Run one command at a time and copy results into a **private** workspace.

```sh
adb version
adb devices -l
adb shell getprop ro.product.device
adb shell getprop ro.product.model
adb shell getprop ro.product.name
adb shell getprop ro.build.version.release
adb shell getprop ro.build.version.sdk
adb shell getprop ro.build.display.id
adb shell getprop ro.build.fingerprint
adb shell getprop ro.vendor.build.fingerprint
adb shell getprop ro.boot.verifiedbootstate
adb shell getprop ro.boot.flash.locked
adb shell getprop ro.build.ab_update
adb shell uname -a
adb shell cat /proc/version
adb shell dumpsys battery
```

Interpretation notes:
- `adb devices -l` and full build fingerprints can contain identifiers: **redact before publishing**.
- `ro.boot.flash.locked` may be absent, vendor-specific or nonauthoritative; treat it as one clue, not proof.
- A newer Android API level does not reveal whether the kernel or radio firmware is modern. `uname -a` provides the running kernel version only.
- A custom ROM can alter props. Cross-check in Fastboot mode **without writing** when practical.
- `dumpsys battery` reports charge/temperature/state; it does **not** reliably identify the battery spare-part model.
- If ADB debugging is disabled or unauthorized, **do not force access**; get model/Android/build from Settings and use the owner's normal on-device permissions.

## C. Read-only Fastboot checks (optional, if accessible)

Using the device's normal UI or **only after confirming the standard fastboot entry procedure**, enter Fastboot and run:

```sh
fastboot devices
fastboot getvar product
fastboot getvar unlocked
fastboot getvar current-slot
```

`current-slot` may return “unknown variable” because boot partitions can be non-A/B. Do not infer an A/B layout from a generic Android guide. Reboot normally using the phone's hardware controls. Avoid `fastboot getvar all` in shared logs because it may reveal serials or hardware identifiers.

**No `fastboot flash`, `fastboot erase`, `fastboot flashing unlock`, `fastboot oem lock`, `mtk da seccfg`, or `SP Flash Download` commands belong in preflight.**

## D. Per-device hardware/build inventory

Fill in only from observed outputs or validated vendor documentation; `unknown` is an acceptable value.

| Field | Value to record | Why it matters |
|---|---|---|
| Codename / region | `begonia` / `begoniain` / unknown; region variant | Avoid incompatible firmware, recovery and baseband |
| Present ROM | Exact name, version, date, URL if available | Reproduce current state |
| Android version/API | Exact observed value | System/userspace compatibility |
| Vendor version/fingerprint | Exact observed value | Blob/HAL provenance, not necessarily same as ROM |
| Kernel | Full `uname -a`, source branch if known | DTB, driver and ABI compatibility |
| Bootloader status | Read-only props + fastboot getvar if available | Recovery/preflight path |
| Recovery image | Name/version **only if already known** | Avoid assumptions about decrypt or dynamic partitions |
| Panel type | Tianma / CSOT / unknown | Different DT/panel firmware may be necessary |
| Touch controller | Model/firmware if exposed / unknown | Vendor-specific touchscreen blobs |
| WLAN/BT chipset | Vendor/chip/bus based on actual logs / unknown | Do not assume MT7663 just from family |
| Camera sensors | Exact modules if known / unknown | HAL/ISP tuning |
| Modem/baseband | Version from device settings/logs (no IMEI) | Calls/VoLTE/region carrier testing |
| Charge/battery | Capacity/health if measurable; physical model unknown | Prevent failure during writes |
| Unique partition backups | Present, verified, protected, or absent | Recovery ability |
| Restore baseline | Specific *matching* trusted MIUI Fastboot ROM | Rollback target |
| Experimental target | Ubuntu Touch stable / Droidian / mainline branch | Isolate hypotheses |

## E. Safety gates before an actual flash (no actions in this document)

1. Identify **exact SKU/region** and validate the genuine factory restore package and its cryptographic digest; do not borrow another variant's preloader.
2. Agree on an **immutable rollback baseline** with kernel, vbmeta, recovery, DTBO, vendor and modem version provenance.
3. Read and **verify backups of original partitions** using an appropriate tested method, including device-unique NVRAM/NVDATA/NVCFG/persist/protect calibration partitions wherever accessible. Store them **encrypted, offline and outside Git**. A named file is not a usable backup unless checksum and size checks pass.
4. Independently verify that the unit can enter **Fastboot and/or supported MediaTek BROM mode**, and check that the chosen recovery tool/version supports its current state. Do **not** intentionally brick the phone to prove this.
5. Check battery/USB reliability, host USB passthrough, disk space and a plan to revert, *before* writes. Do not treat a community rescue procedure as an official or guaranteed recovery route.
6. Never casually relock the bootloader with a nonstock/custom/cross-region system; never choose MiFlash “clean all and lock” during experiments.
7. All post-flash tests must be **version-specific**: verify microphone recording **separately** from voice in calls, then Wi-Fi suspend/resume, charging, sleep/power, dual SIM, modem, camera, Bluetooth, OTA and recovery.

## F. Safe first engineering experiment

Once preflight and backup gates are satisfied, first benchmark the existing custom Android ROM (no change yet), then plan a reproducible Ubuntu Touch 24.04 / Halium 10 base from [05-UBUNTU-TOUCH.md](05-UBUNTU-TOUCH.md).

**Recommended debug hypothesis:** the UBports device status reports *microphone recording broken* while *voice in calls works*. Droidian's community adaptation reports microphone support on the same handset. Treat this as a potential route/HAL/config discrepancy, not evidence of hardware damage. Inventory UT's 2026-10 audio-policy/fast-output overlay and compare with Droidian's adaptation before binary reverse engineering. Do not assume a single copied blob fixes two different audio stacks.

Do **not** attempt “latest kernel + latest firmware + Android 16 blobs + newest UT” in one flash. For every future port, record a compatibility matrix tying *kernel commit → device tree → vendor HAL/firmware hashes → userspace version → observed test outcome*. An OS update date alone says nothing about driver freshness.

## G. Privacy and evidence retention

- GitHub repository is private today, but it may be shared/published later. **Never commit** the original complete `getprop` dump, IMEI, MAC address, serial number, SIM details, APN credentials, account tokens, encryption keys, modem calibration or unredacted NVRAM images.
- Keep machine-readable sanitized logs under a future `device-observations/` folder, with date, source command, command exit code, build fingerprint **redacted** or hashed, and a short status.
- Keep device-specific backups encrypted outside the repository; document only that the backups exist and their *non-secret* verification status.
- Preserve before/after logs as separate immutable captures for each tested kernel, recovery or ROM; mark all absent tests **NOT TESTED**.

*Status: checklist prepared 2026-11-21; no commands have been executed on the owner's device.*
