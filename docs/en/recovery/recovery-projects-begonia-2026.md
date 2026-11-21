# Begonia recovery landscape: provenance, maintainers, builds and compatibility (2026-11-22)

**Device:** Xiaomi Redmi Note 8 Pro, `begonia` (check `begoniain` and regional firmware separately). **Nature:** research inventory, NOT a recommendation to flash any particular image; no handset or image was tested. **Canonical recovery inventory:** this report + [machine-readable comparison](../../../data/matrices/recovery-matrix.csv). [Русский конспект](../../ru/recovery/recovery-projects-begonia-2026.md).

## 1. Executive verdict and dated evidence

**“Official”, “current”, “active”, “latest build”, “works on Android 16”, and “supports dynamic partitions” are six different claims.** No web listing can substitute for testing an exact image with an exact firmware, partition map, encryption scheme, and restore procedure.

| Family / variant | Project affiliation | Latest relevant *verified* evidence | Practical interpretation |
|---|---|---|---|
| TWRP for begonia | **Official TeamWin listing**; maintainer theimpulson | Official [device page](https://twrp.me/xiaomi/xiaomiredminote8pro.html) says “Current” on 2026-11-21. [Official build index](https://eu.dl.twrp.me/begonia/) lists **3.7.0_9-0, 2022-10-06** as newest device image. [TeamWin device tree](https://github.com/TeamWin/android_device_redmi_begonia) default `android-9.0`, last pushed **2020-12-31** per GitHub API observation 2026-11-22. | Official listing is real; **do not interpret it as a 2026 binary release or confirmed Android 16 compatibility**. |
| Community TWRP / Unified TWRP | **Unofficial** device-specific forks | [begonia-recovery tree (`twrp-12.1`)](https://github.com/begonia-recovery/twrp_device_xiaomi_begonia), last push **2022-11-12**; [Neebe3289 (`android-12.1`)](https://github.com/Neebe3289/android_device_xiaomi_begonia), last push **2023-10-23**; [4PDA WuXing90 unified 3.7.1](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=144354114), original thread requires additional validation. | Alternative layouts and Android versions; a branch named 12.1 is a source baseline, NOT a release date. |
| PitchBlack Recovery Project (PBRP) | **Official PBRP device listing**, maintainer Flamefusion | [PBRP begonia page](https://pitchblackrecovery.com/begonia/) says **Official** and names **Flamefusion**, but build listing dynamically loads and was not resolved in this text audit. [Project-org device tree](https://github.com/PitchBlackRecoveryProject/android_device_redmi_begonia-pbrp) default `android-9.0`, last push **2020-09-25**; [PitchBlackRecoveryDevices tree](https://github.com/PitchBlackRecoveryDevices/android_device_redmi_begonia-pbrp) last push **2022-02-12**. | Official *catalog* entry verified; current official binary date and decryption/modern-layout coverage **not verified**. Do not infer from project-wide releases. |
| PBRP 4.0 — krispgece | **Unofficial maintainer-patched fork**, not an official PBRP build | [Maintainer's SourceForge recovery directory](https://sourceforge.net/projects/infinity-x-begonia/files/begonia/recovery/) lists **PBRP-4.0-begonia-20261011-krispgece-UNOFFICIAL.img**, 2026-10-11, ~67.1 MB and companion `.sha256`; [maintainer changelog](https://github.com/krispgece/infinity_ota/blob/16/changelog/begonia.md) dates new recovery to 2026-10-06; [XDA recovery thread](https://xdaforums.com/t/4804111/) provided by author. | Freshest specific image verified here; author claims one image handles their own *static and dynamic* Infinity-X builds. This does **not** establish universal compatibility, third-party source reproducibility or successful owner-device testing. |
| OrangeFox for begonia | **Formerly official, currently unmaintained for this device** | [Official begonia listing](https://orangefox.download/device/5eef879f5a65e7146387c434) explicitly states **“This device is not currently maintained”**; last official **R11.0_0 Beta, 2020-07-26**, “Use with CFW firmware only”. | OrangeFox as a *global project* is active, but its **official begonia support is not active**. |
| Unofficial OrangeFox | Community forks, NOT official OrangeFox | Historical R11.1 unified, R10.x, and alleged newer builds mentioned in [07 — Recovery & Safety](07-RECOVERY-SAFETY.md) and [4PDA guide index](../android/10-GUIDE-INDEX.md). One [unofficial source mirror](https://github.com/OrangeFoxUnOfficial/twrp_redmi_begonia) exists. | Preserve as leads, not evidence of current official device support. OrangeFox warns against impersonators and distinguishes official download sources. |
| BRP (“Begonia Recovery Project”), LR.Team TWRP | Historical / community-themed TWRP variants | [BRP themed TWRP XDA discussion](https://xdaforums.com/t/4242717/), [historical references in 07](07-RECOVERY-SAFETY.md). | Historical reference; no current maintainer image independently verified. |
| SHRP (SkyHawk Recovery Project), RedWolf | General recovery families, **no verified begonia release found** | [SHRP official announcements](https://t.me/s/shrp_official) list **Redmi Note 8/8T (`ginkgo`)**, which is **not `begonia`**. | Do not list as supported or flash another device's image. Needs device-specific evidence. |
| ROM-distributed recovery (Lineage Recovery, PixelExperience Recovery, AOSP recovery) | ROM-specific project or unofficial port | [Historic PixelExperience begonia download page](https://get.pixelexperience.org/begonia) lists a recovery image; current LineageOS support/build should be checked against the **exact ROM maintainer's installation instructions**, not inferred from source-tree existence. | Often optimized for installing the matching ROM, not all-purpose partitions/backup. |
| Xiaomi stock MIUI recovery | OEM | Original per-variant MIUI recovery, sourced with **matching stock firmware**. | Stock rollback / limited vendor-defined package operations; not a substitute for custom ROM flashing capabilities. |
| **UBports unified recovery** | UBports/Ubuntu Touch, **separate from TWRP forks** | [Official UBports recovery porting guide](https://docs.ubports.com/en/latest/porting/finalize/UBports_recovery.html), [UBports recovery sources](https://github.com/ubports/halium_bootable_recovery), [begonia Halium 10 device repo](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia). The existing begonia deviceinfo declares `deviceinfo_use_unified_recovery="true"` and carries recovery overlay, LVM migrator and `system-image-upgrader`. | **Primary recovery target for our Ubuntu Touch update/OTA work**; TWRP may assist preparation where explicitly documented but is not equivalent to UBports recovery. |

Observations made **2026-11-22 JST**; GitHub `pushed_at` dates refer to the specific inspected *repository*, not every branch, release mirror or project. SourceForge listing dates are file publication dates. An official webpage's last edit date is **not** the device binary's build date.

## 2. Primary documentation, downloads, device trees, source code

### TWRP / TeamWin
- Device-specific official page and warnings: https://twrp.me/xiaomi/xiaomiredminote8pro.html
- Official download directory (link to **page**, not hotlinked files): https://eu.dl.twrp.me/begonia/ ; alternate https://dl.twrp.me/begonia/
- TeamWin device tree: https://github.com/TeamWin/android_device_redmi_begonia
- TWRP project: https://twrp.me/ ; build reference: https://twrp.me/faq/howtocompiletwrp.html
- Other begonia tree candidates: https://github.com/HyperTeam/android_device_redmi_begonia-TWRP ; https://github.com/begonia-recovery/twrp_device_xiaomi_begonia ; https://github.com/Neebe3289/android_device_xiaomi_begonia ; https://github.com/ZyCromerZ/twrp_redmi_begonia . **No claim that these all match recent ROM builds.**

### PitchBlack (PBRP)
- Official device entry: https://pitchblackrecovery.com/begonia/ ; project home: https://pitchblackrecovery.com/
- Official organization tree: https://github.com/PitchBlackRecoveryProject/android_device_redmi_begonia-pbrp
- Historical device-team tree: https://github.com/PitchBlackRecoveryDevices/android_device_redmi_begonia-pbrp
- Additional developer tree (candidate): https://github.com/Saikrishna1504/device_xiaomi_begonia-pbrp
- Active 2026 **unofficial** release and checksum: https://sourceforge.net/projects/infinity-x-begonia/files/begonia/recovery/ ; maintainer's ROM/recovery integration evidence: https://github.com/krispgece/infinity_ota/blob/16/changelog/begonia.md ; https://xdaforums.com/t/4804111/

### OrangeFox
- Official device page including unmaintained and CFW-only release status: https://orangefox.download/device/5eef879f5a65e7146387c434
- Official project: https://orangefox.tech/ ; docs: https://wiki.orangefox.tech/ ; downloads: https://orangefox.download/
- Build source guidance: https://wiki.orangefox.tech/dev/building ; [maintainer requirements](https://wiki.orangefox.tech/dev/maintainers_guidelines); [impersonation and untrusted downloads warning](https://wiki.orangefox.tech/warning-impersonators)
- Official sources live under the OrangeFox development infrastructure per docs, while random `OrangeFox`-named GitHub accounts do not establish authorization.

### UBports, stock and ROM-specific
- UBports unified recovery specification: https://docs.ubports.com/en/latest/porting/finalize/UBports_recovery.html
- Recovery implementation: https://github.com/ubports/halium_bootable_recovery
- Begonia adaptation source: https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia
- UBports installer/device: https://devices.ubuntu-touch.io/device/begonia/
- PixelExperience historical recovery listing: https://get.pixelexperience.org/begonia
- ROM maintainer's own installation instructions take precedence over generic recovery tutorials; for example [AxionAOSP begonia guide](https://github.com/AxionAOSP/official_devices/blob/main/Wiki/begonia.md).

## 3. Compatibility is a per-build matrix, not a brand ranking

Record **all** of these for each candidate, with `unknown` rather than assumptions:

1. **Hardware**: actual `ro.product.device` / board ID; `begonia` vs `begoniain`, panel variants, region; Android build & vendor fingerprint, bootloader status.
2. **Firmware lineage**: stock MIUI Android 9/10/11, vendor base, CFW vs non-CFW, device-specific preloader/LK/TEE and the ROM's installer contract.
3. **Layout**: stock static vs custom dynamic `super` mapping; partitions and recovery/boot/DTBO/vbmeta placement; A-only vs A/B **verified**, never assumed from Android version.
4. **Filesystem/cryptography**: FDE vs FBE, `metadata` / keymaster version, ability to decrypt **without formatting** `/data`; full backup/restore is not equivalent to readable decrypted internal storage.
5. **Installer mechanism**: zip updater-script vs update-engine/payload.bin vs ADB sideload vs fastbootd vs UBports `system-image-upgrader`. Test the exact OTA path and rollback separately.
6. **Image geometry**: actual target partition byte capacity vs recovery image byte length; ensure boot header, DTBO, compression and partition selector match the intended path. The [pmOS 64 GB sample GPT](07-RECOVERY-SAFETY.md#partition-map-begonia-64-gb-unit-gpt-from-pmos-wiki-parted-dump-oldid109575-verified-direct-high) has a ~67.1 MB recovery partition; the October 2026 PBRP image is also displayed as ~67.1 MB by SourceForge. **That is not proof the image fits; verify exact bytes and target partition on the physical handset first.**
7. **Security and recovery**: AVB/dm-verity, keymaster, SELinux, authorized flashing modes, whether recovery is overwritten by stock boot, verified backups of partition map + device-unique NVRAM/NVDATA/NVCFG/persist stored encrypted and offline.
8. **Observed tests**: GUI/touch, ADB sideload, MTP/USB-OTG, external SD, read-only mounts, backup/restore, data decryption, logical partitions, install & updates, reboot to recovery. Failures carry logs/build hashes, not just an anecdote.

**Concrete 2026 conflict:** krispgece states their PBRP 4.0 installs both static and dynamic Infinity-X builds, whereas *static PBRP 4.1* stops at the start of installation for their dynamic builds ([maintainer's source-hosted README](https://sourceforge.net/projects/infinity-x-begonia/files/begonia/recovery/)). This is one author's tested ROM scope, **not** evidence that all PBRP 4.1 versions are globally inferior. Never generalize it to other ROMs.

**Safety:** TeamWin's official page explicitly warns that begonia can hard-brick and that upgrades break TWRP data decryption. Older “unbrick requires paid service” language reflects its source era; mtkclient rescue paths exist but **have not been validated on this particular handset**. Do not suggest unlocking, erasing, repartitioning, disabling AVB or flashing a random mirror as a diagnostic action. First follow [read-only preflight](18-DEVICE-PREFLIGHT-READONLY.md) and [recovery risk study](07-RECOVERY-SAFETY.md).

## 4. Ubuntu Touch, Droidian and postmarketOS implications

- **Ubuntu Touch (priority):** the begonia Halium 10 source already uses unified UBports recovery with `ramdisk-recovery-overlay`, `recovery.fstab`, `system-image-upgrader` and `halium_lvm_vg=ubports`. Inspect exact upstream files and CI output, then test *UBports recovery + OTA + LVM migration* as a unit. Generic TWRP feature claims do not prove compatible system-image OTA. See [Ubuntu Touch port research](../linux/05-UBUNTU-TOUCH.md).
- **Droidian:** a recovery-flashable zip may require a TWRP-like recovery with working `adb sideload` (see [rifux Droidian installation README](https://github.com/rifux/droidian-begonia/blob/trixie/README.md)); confirm the exact release/install path before trying it. This is different from an OTA-capable UBports recovery.
- **postmarketOS:** `pmbootstrap` can build recovery-installable artifacts or use its documented fastboot flow. The **pmOS installer format** is not guaranteed to match an Android 16 recovery. Consult [OS comparison](../linux/06-DROIDIAN-POSTMARKETOS.md) and [recovery safety](07-RECOVERY-SAFETY.md).
- **Mainline Linux:** a bring-up ramdisk and debug/SSH/USB gadget can be more valuable than a TWRP GUI. Don't conflate kernel/DTB test boots with an Android recovery build.

## 5. Research and test acceptance gates (zero writes by default)

1. Save each device-specific release page, exact date, image filename/version and source URL, license, maintainer identity, build tree branch/commit and reproducible build instructions if provided.
2. Resolve the image checksum (SHA-256 preferred) from the same trustworthy maintainer; compare bytes after download. A checksum on the same compromised mirror is integrity, not authenticity.
3. Compare required ROM, firmware, static/dynamic layout and encryption with **read-only device diagnostics**. Do not silently move images between boot and recovery partitions.
4. Verify signed-off recovery/update procedure and a restore route with *independent* original partition backups; avoid uploading unique device data into Git.
5. Build from reviewed source in an isolated environment when binaries are unverified; inspect `BoardConfig.mk`, `recovery.fstab` and image assembly definitions before ever trying the artifact.
6. On a designated test handset **only after** owner approval and backups, test individual functions and record PASS / FAIL / UNKNOWN, logs, restore evidence and exact ROM/firmware/image hashes.
7. Recheck upstream *device-level* releases and open issues periodically; do not promote a global project version as a begonia release.

**Open leads:** Official PBRP dynamic build feed not readable in text-only capture; no current official OrangeFox maintainer; source/patch correspondence for krispgece's PBRP-4.0 binary not independently established; SHRP/RedWolf begonia binaries unverified; TWRP 3.7.0 support for Android 16 dynamic/FBE unverified; new 2026 community forks require exact partition/decryption and reproducible-build tests.

*Evidence captured 2026-11-22; last GitHub API `pushed_at` observations recorded above. Research-only; no binary reflashed or executed.*
