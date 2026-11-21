# Ubuntu Touch (24.04 noble) on Xiaomi Redmi Note 8 Pro (begonia) — Port Deep-Dive

> **Potential microphone/audiopath lead (2026-11-21):** [Saikrishna's current begonia device tree](https://github.com/Saikrishna1504/device_redmi_begonia/tree/axion) includes [audio_policy_configuration.xml](https://github.com/Saikrishna1504/device_redmi_begonia/blob/axion/configs/audio/audio_policy_configuration.xml) mapping built-in front/back mic, Voice Call In and Echo Ref, a comprehensive `configs/audio/audio_param` directory, audio shim and blob fixups. Compare with Droidian and UT Halium 10 before swapping vendor images. [Detailed audit](../research/24-SAIKRISHNA1504-DEVICE-STACK-AUDIT.md).

> **Browser access reconciliation (2026-11-21):** Early fetch attempts to XDA/4PDA were blocked, but subsequent Hermes Brave/owner captures succeeded for selected pages (details in [_context/HUMAN-ASSISTS.md](../../../_context/HUMAN-ASSISTS.md)); the feature matrix still needs physical begonia validation.

Research date: 2026-11-21 (JST). Method: GitLab REST API (unauthenticated) against both port repos, cached devices.ubuntu-touch.io device page, docs.ubports.com porting docs, GitHub API repo search, forums.ubports.com (search API down — see Limitations). All dates UTC unless noted.

---

## 1. Current status

- **Channel**: community port, hosted by UBports, **Halium 10.0** (Android 10 base), running **Ubuntu Touch 24.04 "noble"**.
  - Source: https://devices.ubuntu-touch.io/device/begonia (verified from full page cache; badge "This is the latest Ubuntu Touch release" — confidence: high, verified-direct).
- **Official port status**: "Under heavy development relying only on the device porters. Many features including basic functionality may not work." Core connectivity state: **"Basic support"** — "The device has basic data capabilities and can connect to mobile networks (as applicable), but currently offers minimal features... It can be a very nice second device." (verbatim, devices page).
- **Support indicators** (devices page, all green): Easy install with UBports Installer · Has a maintainer · Actively receiving commits from porters (→ "Last commit on 10/10/2026") · Has a stable release channel · Repositories hosted by UBports · Latest UT release.
- **Compatibility rating**: page displays **★★★★★★★ (7 filled stars)**; no denominator is rendered in the captured page, so "out of 8" is not verifiable from this source. Community strength badge: **medium**. (verified-direct for what is displayed; denominator: low confidence, not shown.)
- **People**: Maintainer **TheKit** (Konstantin... forums.ubports.com/user/thekit), Developer **Rúben Carneiro** (forums.ubports.com/user/rubencarneiro) — devices page, verified-direct.
- **Live repo activity (verified via GitLab API 2026-11-21)**:
  - Device repo `ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia` (id 23878040, branch `master`): `last_activity_at` **2026-10-19T12:36Z**; newest commit 220f9bdf "Add Apache-2.0 license" (Marius Gripsgard, 2026-10-19). Repo description: "Xiaomi Redmi Note 8 Pro"; 2 stars. https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia — confidence: high.
  - Kernel repo `.../kernel-xiaomi-mt6785` (id 23877901, branch `halium-10.0`): `last_activity_at` **2026-07-08T23:15Z**; newest commit 4c74d0e8 "scripts/dtc: add -fcommon..." (TheKit, dated 2026-07-09 in commit metadata). — confidence: high.
  - Slight tension: devices page says "Last commit on 10/10/2026" (last device-repo *code* commit: TheKit's audio overlay commits 2026-10-10); GitLab `last_activity_at` 2026-10-19 reflects the license commit. No real contradiction, different metrics.

### Release channels table (from devices page, verified-direct)

| Ubuntu release | Channel | Version | Release date | Description |
|---|---|---|---|---|
| 24.04 - noble | **stable** | 24.04-1.4 | 2026-07-13 | "Stability over newer features (recommended)" |
| 24.04 - noble | **rc** | 24.04-1.5 RC 5 | 2026-10-09 | "Testing before the next stable release" |
| 24.04 - noble | **daily** | 24.04-1.x (2026-10-14) | 2026-10-14 | "Daily built development releases" |

- Historical channels still listed on the device page as tabs: **16.04 xenial** and **20.04 focal** (the port existed in the xenial era — issue #16 from 2022 references a `xenial-hybris-android9` rootfs CI build; all tracker issues #1–#16 are 2021–2023, i.e. xenial/focal era). Current shipping line is noble only. (verified-direct / inferred: issue-era attribution.)

---

## 2. Architecture & Halium

- **Stack composition** (docs.ubports.com porting Intro, verified-direct): an Ubuntu Touch port = **UT rootfs + Halium (boot & system images) + vendor blobs**. Halium is built from LineageOS sources; version table (verbatim): Android 10.0 → Halium 10.0 → LineageOS 17.1; Android 11.0 → Halium 11.0 → LOS 18.1; Android 12.0 → Halium 12.0 → LOS 19.1. "Since 20.04, Ubuntu Touch ports are normally based on Halium 9.0 or later."
- **GSI architecture** (Intro, verified-direct): since Android 9, vendor blobs live on a separate partition, enabling the prebuilt **Halium GSI**; porters build a device **halium-boot** (kernel + initramfs) instead of a full device system image. Docs: "Nowadays there is just The One method" (full-system-image, halium-boot and standalone-kernel are deprecated as separate methods) — https://docs.ubports.com/en/latest/porting/build_and_boot/ — confidence: high.
- **begonia specifics** (all from repo files fetched raw via API — verified-direct, confidence: high):
  - `deviceinfo`: `deviceinfo_halium_version="10"`, arch `aarch64`, kernel source = the UBports-hosted kernel repo branch `halium-10.0`, defconfig **`begonia_user_defconfig`**, clang build, DTB `mediatek/mt6785.dtb`, boot image **header v2**, `bootimg_os_version=10`, os patch level 2020-11-01, `deviceinfo_use_unified_recovery="true"`, `deviceinfo_has_recovery_partition="true"`, `rootfs_image_sector_size=4096`, cmdline `bootopt=64S3,32N2,64N2 buildvariant=userdebug systempart=/dev/disk/by-partlabel/system halium_lvm_vg=ubports`, prebuilt boot ramdisk from `github.com/halium/initramfs-tools-halium/releases/download/dynparts/initrd.img-touch-arm64`.
  - Kernel base: **Linux 4.14.141** — kernel repo `Makefile`: `VERSION=4, PATCHLEVEL=14, SUBLEVEL=141` ("Petit Gorille"); matches stock kernel per devices page. Platform defconfigs `k85v1_64_defconfig` (k85v1 = MT6785 board family) confirm an Android 10 MTK vendor tree. — verified-direct, high.
  - Kernel patches (halium-10.0 branch commit log, 13 commits mention "halium"): initial defconfig enablement (2021-08-01: AppArmor, SquashFS, KVM + extra binder devices, Bluetooth options, cpu-cgroup `#endif` fix), **binder fixes** ("ignore txn_security_ctx flag", "Configurable global PID lookups"), RFKill, `CONFIG_BINFMT_MISC`, extra squashfs compression for Snap, `CONFIG_CGROUP_DEVICE`, torchlight driver fix `flashlights-mt6360` (2022-08-02), build fix `dtc -fcommon` (2026-07-09). Authorship: TheKit/NeKit/NotKit + Rúben Carneiro. — verified-direct, high.
  - Device repo layout: `build.sh` + `.gitlab-ci.yml` + `deviceinfo` + `overlay/` (halium overlay: NetworkManager, ofono `mtk.conf` ril_subscription, repowerd `config-begonia.xml`, usb-moded `begonia.conf`, udev rules, apparmor android10 profile), `ramdisk-overlay/` (LVM tools + hooks), `ramdisk-recovery-overlay/` (unified recovery: `system-image-upgrader`, `lvm-fs-migrator`, `recovery.fstab`, `prop.halium`).
  - Installer device metadata `overlay/system/etc/deviceinfo/devices/halium.yaml`: names, `GridUnit: 21`, backlight sysfs `/sys/class/leds/lcd-backlight`, `MirAndroidPlatformClientEglFlush` quirk, and the audio note: `# Fast output gets stuck on the earpiece after calls; 44.1 kHz crashes droid-card. PulseaudioModulesDroid_ExtraCardArgs: "rate=48000 quirks=-output_fast"` — verified-direct, high.

---

## 3. What works & what doesn't (noble 24.04 feature matrix)

Source for every row: devices.ubuntu-touch.io/device/begonia feature table (cached full page, verified-direct). Legend: page icons = working / not-working / global issue.

**Sound**: Earphones ✅, Loudspeaker ✅, Volume control ✅, **Microphone ❌ NOT WORKING** — the only broken audio item; voice in calls is marked working, so this is chiefly recording/mic-in.
**Misc**: **RTC time ❌ NOT WORKING** (clock resets without network), **Wireless External monitor ❌**, FM radio ❌; Waydroid ✅*, AppArmor patches ✅, battery % ✅, offline/online charging ✅, recovery image ✅, reset to factory ✅, SD card ✅, shutdown/reboot ✅ (*Waydroid flag contradicted by open issue #8, see §5).
**Sensors**: **Automatic brightness ❌ → links to https://gitlab.com/ubports/core/repowerd/-/issues/11** (global repowerd issue; device repo ships `overlay/system/usr/share/repowerd/device-configs/config-begonia.xml`); Fingerprint reader ✅; **GPS ✅ + GLOBAL badge → https://gitlab.com/ubports/development/core/location-service/-/issues/13** ("Devices may take longer than usual to get the first GPS fix because of missing Assisted GPS support" — verbatim; the "slow fix" is A-GPS absence, a global Halium-era issue, not begonia-specific); Proximity ✅, Rotation ✅, Touchscreen ✅.
**Cellular**: carrier info/signal ✅, data ✅, dual SIM ✅, calls in/out ✅, MMS ✅, PIN ✅, SMS ✅, audio routing ✅, voice in calls ✅, volume ✅; **VoLTE ❌ + GLOBAL badge → https://gitlab.com/ubports/ubuntu-touch/-/issues/1335** ("Calling over VoLTE is experimental and depends on the cellular carrier, available bands and geographical region" — verbatim).
**Network**: Bluetooth ✅, Flight mode ✅, Hotspot ✅, NFC ✅, WiFi ✅ (each contradicted to some degree by open tracker issues, §5).
**GPU**: boots into UI ✅, hardware video playback ✅. **Endurance**: 24+h battery ✅, 7-day stability ✅. **Actors**: manual brightness ✅, notification LED ✅, torchlight ✅, vibration ✅. **Camera**: flashlight/photo/video/switching all ✅. **USB**: MTP ✅, ADB ✅.
**Unsupported by hardware** (page statement): wireless charging, double-touch-to-wake, wired external monitor.

Confidence: high for matrix values (page verified), but the matrix reflects maintainer-reported state; user reports disagree on several items (§5).

---

## 4. Recent fixes & open issues

**Issue tracker census** (GitLab API `issues?state=all`, X-Total=16, verified-direct 2026-11-21): 16 issues, **9 open / 7 closed**. All were filed 2021–2023 (xenial/focal era); none filed in 2024–2026. Recent 2026 work is all in commits, not the tracker.

### Recently closed / fixed (with URLs)
| Issue | Closed | Fix evidence |
|---|---|---|
| [#1 SD card not detected](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia/-/issues/1) | 2022-04-01 | "fixed by" MR !2 commit 61233a81 |
| [#3 Anbox patch not complete](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia/-/issues/3) | 2022-06-27 | gbinder bootloop resolved |
| [#4 Video playback won't work](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia/-/issues/4) | 2022-04-01 | MR !2 commit 7aa359b3 |
| [#5 MTP and ADB not working](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia/-/issues/5) | 2022-02-03 | MR !2 commits |
| [#6 Cannot get ADB](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia/-/issues/6) | 2022-05-13 | — |
| [#15 Installation renders stock Android unusable](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia/-/issues/15) | 2023-12-15 | imported from GitHub (iamshadow2008) |
| [#16 Screen tearing/artifacts](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia/-/issues/16) | 2023-12-15 | filed by rubencarneiro (xenial-era rootfs build) |

### Recent 2026 fix work (commits, verified-direct)
- **2026-07-09 → 2026-07-14 (TheKit)**: dynamic-partition **LVM** adoption — `halium_lvm_vg=ubports`, dynparts ramdisk, LVM binaries/hooks imported, LVM migration via props, "[temp] WIP LVM migrator" — enables the noble-era dynparts/LVM data layout on the unified recovery.
- **2026-07-09 (kernel, TheKit)**: `dtc -fcommon` build fix for current toolchains (kernel-side fix enabling 2026 rebuilds).
- **2026-09-24**: `ramdisk-recovery-overlay: drop /cache partition from recovery.fstab`.
- **2026-10-10 (TheKit, 2 commits)**: `overlay: use stock audio policy, disable fast output via deviceinfo` + `drop unused PulseAudio and upstart files` — this directly targets the long-standing **"audio stuck on earpiece after call"** bug (open issue [#10](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia/-/issues/10)) per the `halium.yaml` comment `quirks=-output_fast`. *Analysis (medium confidence): the matrix was updated after this (page cached 2026-11-21 still shows voice-in-calls working); issue #10 remains formally open.*
- **2026-10-19**: Apache-2.0 license added (repo hygiene).

### Open issues (9) — what is broken NOW per tracker
| # | State/open since | Title | Note |
|---|---|---|---|
| [#2](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia/-/issues/2) | open, 2021-11-16 | Data connection not working properly | "user must go to settings and select the data manually... maybe needs ofono tweaks" |
| [#7](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia/-/issues/7) | open, 2022-08-29 | Status bar behind edges | notch overlaps clock |
| [#8](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia/-/issues/8) | open, 2022-09-14 | Waydroid does not work | "container doesn't start" |
| [#9](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia/-/issues/9) | open, 2022-09-14 | Wi-Fi doesn't want to turn on | `wlan CONNAC: Direct firmware load for ...` failed |
| [#10](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia/-/issues/10) | open, 2022-10-03 | Audio stuck on earpiece after call | likely mitigated 2026-10-10 (above) |
| [#11](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia/-/issues/11) | open, 2023-03-17 | No OTA updates, can't change channels | user stuck on 2021-09-11 build (xenial-era symptom) |
| [#12](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia/-/issues/12) | open, 2022-09-15 | Bluetooth not working | contradicts matrix |
| [#13](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia/-/issues/13) | open, 2022-09-15 | WiFi and Hotspot issue | wifi off after sleep |
| [#14](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia/-/issues/14) | open, 2022-09-15 | NFC issue | NFC entry disappears from Settings over time |

### Broken NOW — consolidated verdict (matrix + tracker)
**Hard-broken (matrix)**: Microphone, RTC time, auto-brightness (repowerd#11), wireless external monitor, FM radio. **Global/blocked**: VoLTE (ubuntu-touch#1335), slow first GPS fix / no A-GPS (location-service#13).
**Flaky per tracker (open, unfixed 2022→)**: manual network-mode selection (#2), Wi-Fi reconnect after sleep (#9/#13), earpiece audio after calls (#10), OTA channel stuck (legacy, #11), notch/status-bar (#7), Waydroid (#8), BT (#12), NFC (#14).
**Confidence**: tracker state = high (API-verified); whether each still reproduces on noble 24.04 = **low/medium** — all reports predate noble stable (2026-07) and none was re-confirmed on 24.04 in the tracker.

---

## 5. Build instructions (for begonia specifically)

No README exists in the device repo (raw fetch → HTTP 404, verified-direct). The authoritative build path is the repo itself + generic docs:

1. **Prereqs** (docs.ubports.com porting Intro): Linux host, git, C/C++ familiarity; UT port = rootfs + Halium + vendor blobs; Halium built from LineageOS sources (Halium 10.0 ← LOS 17.1/Android 10). https://docs.ubports.com/en/latest/porting/introduction/Intro.html — verified-direct.
2. **Method**: current docs describe one method (deprecated: full-system-image / halium-boot / standalone-kernel): build the Halium kernel+initramfs ("halium-boot"), pair with the prebuilt **Halium GSI**, overlay device config. https://docs.ubports.com/en/latest/porting/build_and_boot/ — verified-direct.
3. **begonia wrapper** (verified-direct): device repo root `build.sh` = `git clone https://gitlab.com/ubports/community-ports/halium-generic-adaptation-build-tools build && ./build/build.sh "$@"`. CI (`.gitlab-ci.yml`) includes `halium-generic-adaptation-build-tools/-/raw/main/gsi-port-ci.yml` with `ADAPTATION_TOOLS_BRANCH: main`, `BUILD_DEVEL_FLASHABLE_FOCAL: 1` (auto-builds flashable devel images).
4. **Kernel**: clone `kernel-xiaomi-mt6785` branch `halium-10.0`, build `begonia_user_defconfig` with clang (deviceinfo drives this); boot.img header v2, DTB `mediatek/mt6785.dtb`; initramfs from Halium `initramfs-tools-halium` dynparts release.
5. **System image / install**: UBports Installer supports begonia ("Easy install with UBports installer" ✅, devices page); device-specific prep = confirm model begonia + **OEM unlock** via Xiaomi's unlock tool (en.miui.com/unlock/download_en.html, linked on devices page). Rootfs is the noble system-image; recovery partition (32 MB) hosts the unified UBports recovery with `system-image-upgrader`; data on dynamic partitions handled via LVM VG `ubports` (halium_lvm_vg=ubports + lvm-fs-migrator, 2026-07 commits).
6. **Channels for testing**: stable 24.04-1.4 / rc 24.04-1.5 RC 5 / daily (table in §1).

---

## 6. Upgrade paths (ANALYSIS — clearly marked; verified facts flagged)

**Halium 11 (Android 11 / LOS 18.1):**
- *Verified facts*: Halium 11 exists and is officially paired with LOS 18.1 (docs Intro table). begonia has Android 11 kernel/vendor sources: `github.com/AgentFabulous/begonia` branch `android-11.0` (last push 2022-06-23; also android-12.0 branch exists) — context pack, verified 2026-11-21. GitHub repo search for `mt6785 halium` (API, 2026-11-21): total_count=1 → `jhuny-arj/kernel_mt6785_halium` (pushed 2023-11-12, 0 stars, no description); `begonia halium` → `Flame-Lab-begonia/halium_manifest` ("halium 9 device manifest", pushed 2020-09-21). — verified-direct, high.
- *Analysis (inferred, low-medium confidence)*: A Halium-11 begonia port is **plausible but has no visible active work** — no UBports-hosted halium-11 tree, no maintained community Halium-11 kernel found in GitHub search; GitLab-wide search unavailable (§8). TheKit's 2026 LVM/unified-recovery work is forward-compatible infrastructure but not itself a Halium-11 step.

**Halium 12/12.1+ / 13:**
- *Analysis (low confidence)*: Halium 12/13 exist as versions (docs table), but no MT6785/Helio-G90T Halium-12+ port was found in this session. MTK Dimensity-era Halium 12/13 ports exist elsewhere in UBports; for begonia the blocker would be blob compat and lack of porter interest. No verified project → treat as not available.

**Reusing pmOS mainline kernel work (Dinolek / `mt6785-mainline`) inside UT:**
- *Verified facts*: `github.com/Dinolek/mt6785-mainline` exists (last push 2026-06-17) and powers the Nura/pmOS begonia port (mainline kernel 6.16.4); pmOS status: screen/touch/GPU/NFC/sensors work, **audio/camera/wifi/bt/gps/modem broken** (context pack, Nura wiki). — verified, high.
- *Analysis (inferred, medium confidence on mechanism, low on feasibility)*: Ubuntu Touch is built on **libhybris + Android vendor blobs + the Halium GSI** (docs Intro, verified); a mainline-kernel UT port would discard the Halium HAL path and would need UT's telephony/media stacks re-plumbed onto mainline drivers (Panfrost exists for Mali-G76 in mainline, but RIL/oFono, sensors, audio topologies would all need new backends). Given the pmOS mainline port still has **no modem/audio**, a mainline-based UT port today would be a phone without calls — strictly a long-term research direction, not a realistic upgrade path. No such project exists as of 2026-11-21.

---

## 7. Community

- **Telegram**: **@ut_begonia** — device-specific channel, linked from the devices page ("Telegram - @ut_begonia", https://t.me/ut_begonia) — verified-direct (link presence). Also @ubports, @WelcomePlus (install help), t.me/ut_troubleshooting. *Content of the channel not inspected (Telegram mention-only per task scope).*
- **Forum** (forums.ubports.com):
  - Device-family category: **[Xiaomi Redmi Note 8 (category 113)](https://forums.ubports.com/category/113/xiaomi-redmi-note-8)** — snippet: "Apparently it was a driver problem that has since been solved. begonia / Note 8 Pro…" (via web search snippet; search API down — see Limitations).
  - [Topic 11798 "Redmi Note 8 Pro"](https://forums.ubports.com/topic/11798/redmi-note-8-pro) — snippet: "Ubuntu touch on Redmi Note 8 Pro. Yes, it's possible but the port is outdated and abandoned." → **contradicts** devices page/GitLab (active commits Oct 2026); post date not verifiable in this session (search snippet only).
  - [Topic 8114 "[Request] Redmi note 8 Pro Android 11 Begonia/Global Rom"](https://forums.ubports.com/topic/8114/request-redmi-note-8-pro-android-11-begonia-global-rom) — user confusion about installer requiring a specific Android version.
  - General porting help channels per docs: forum category 33 "Porting" + Telegram @ubports_porting (docs Intro, verified-direct).
- **Bug reporting flow** (devices page): search the device issue tracker first, then file per docs.ubports.com/en/latest/contribute/bugreporting.html.

---

## 8. Limitations

- **No README in the device repo**: `/repository/files/README.md/raw?ref=master` → **HTTP 404** (verified-direct); tree (99 items) contains no README* — build info reconstructed from `deviceinfo`, `build.sh`, `.gitlab-ci.yml`, `halium.yaml` instead.
- **forums.ubports.com search API down for us**: `https://forums.ubports.com/search.json?q=begonia` and `/search/query.json` both return **HTTP 404** (verified-direct 2026-11-21). Forum facts above come from web-search snippets — **topic/post dates and full thread contents unverified**; live thread reads would need the browser (not spent, budget).
- **GitLab global project search requires auth**: `/api/v4/search?scope=projects` → HTTP 401 unauthenticated, so a GitLab-wide scan for Halium-11 mt6785 work could not be done (GitHub-side scan done; GitLab-side unknown).
- **Compatibility-rating denominator not visible** in the captured devices page (7 stars rendered; "out of 8" is an assumption, not verified).
- **Issue tracker staleness**: no issue filed since 2023-03; open issues may or may not reproduce on noble 24.04 — cannot be verified without a device (research-only scope).
- Devices-page VoLTE/location-service/repowerd global-issue threads (gitlab.com/ubports/ubuntu-touch/-/issues/1335, development/core/location-service/-/issues/13, core/repowerd/-/issues/11) were **cited from the device page, not fetched** this session.

## Sources appended to shared log (new records this task)
`ut-gitlab-device-repo`, `ut-gitlab-device-issues`, `ut-gitlab-device-commits`, `ut-gitlab-kernel-repo`, `ut-gitlab-raw-files` (deviceinfo/build.sh/halium.yaml/CI/Makefile), `docs-ubports-porting-intro`, `docs-ubports-build-and-boot`, `forums-topic-11798`, `forums-topic-8114`, `forums-category-113`, `github-jhuny-kernel-mt6785-halium`, `github-flamelab-halium-manifest`, `gitlab-volte-issue-1335-cited`, `gitlab-agsps-location-service-13-cited`, `gitlab-repowerd-11-cited`.


---

## Appendix — Droidian on begonia (the working-mic Halium sibling, added 2026-11-22)

This file is UT-centric; Droidian deserves its own record because **its adaptation has the working
microphone this port lacks**. Facts verified live 2026-11-22:

- **Kernel**: [begonia-linux/linux-android-begonia](https://github.com/begonia-linux/linux-android-begonia),
  branch `droidian` — Makefile **4.14.141** (stock MIUI-12-A10 base + Halium-10 patches). The UT GitLab
  kernel (halium-10.0) is the same 4.14.141 base — the two ports share the Halium-10 plumbing.
- **Adaptation**: [begonia-linux/adaptation-xiaomi-begonia (droidian branch)](https://github.com/begonia-linux/adaptation-xiaomi-begonia/tree/droidian),
  release `latest` 2024-09-15 (3 .debs). Porter-claimed hardware matrix: **microphone ✔, camera ✔
  (droidian-camera + gst), calls/data/SMS/dual-SIM/MMS ✔, fingerprint ✔, rotation ✔, proximity ✔,
  vibration ✔, speaker/headphones/volume/BT-audio ✔, WiFi ✔, Bluetooth ✔, NFC ✔, SDcard ✔, Waydroid ✔,
  MTP ✔; auto-brightness ✗, hotspot ✗ (fixable), GPS partial, encryption ✗.**
- Porters: Halhadus (main), rifux; support t.me/begonia_linux. Full build route:
  [_context/HALIUM-UT-BUILD-PLAN.md](_context/HALIUM-UT-BUILD-PLAN.md).

### Kernel ladder for the Linux phase (owner's "latest kernel" ambition, mapped honestly)

Halium-10 rootfs (Droidian AND UT) binds to the **A10 vendor** + a Halium-10-patched kernel. The newest
public begonia kernels (4.19.325 PoWeR+ shipped in Axion 2.9 — device-verified; 4.14.357-openela on
Saikrishna's `main`) are **not** Halium-patched. Ladder:

1. **Baseline (ship as-is)**: 4.14.141 halium kernel from begonia-linux — install Droidian, walk the
   hardware matrix on-device, compare against the porter table. Days, not weeks.
2. **Modern 4.14**: backport Halium-10 patches (config fragment: paranoid networking off, binder/fs
   bits) onto **Saikrishna's 4.14.357-openela** (`main`) — same 4.14 ABI keeps the A10 vendor happy;
   this is the "latest working 4.14" the owner wants. Medium difficulty; the clean-upstream target for
   the RE exercises ([15](15-RE-IMPROVEMENT-PLAN.md) unpacking recipe).
3. **4.19+**: only with a Halium-11+ base (newer vendor) — that is the later stage of
   [15]'s sequencing (mic fix → halium-11), not a Droidian-10 step. The 4.19.325 experience from Axion
   informs this but cannot be dropped into Halium-10 directly.

### Test plan (owner-approved)

1. Droidian baseline on stock 4.14.141 halium kernel → hardware matrix on-device vs porter claims.
2. Same device, compare battery/thermals against Axion 2.9 (current daily: A16, 4.19.325).
3. Kernel experiments (ladder step 2) on Droidian first; UT port on the shared Halium-10 base after the
   mic fix lands ([15] Stage 1). Reflash-to-older-version remains the fallback at any point
   ([07 §N.2](../recovery/07-RECOVERY-SAFETY.md) return path).
