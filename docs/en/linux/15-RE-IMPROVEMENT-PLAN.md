# 15 — RE-driven improvement plan (begonia / Redmi Note 8 Pro, MT6785)

Written 2026-11-21 per [_context/W15-MISSION.md](_context/W15-MISSION.md) (REQUIREMENTS [#37](https://github.com/0-danielviktorovich-0/begonia-research/blob/main/_context/REQUIREMENTS.md) RE-driven plan; [#33](https://github.com/0-danielviktorovich-0/begonia-research/blob/main/_context/REQUIREMENTS.md) USB-HID). **Research-only:** the owner has AUTHORIZED downloading one firmware image and unpacking it for analysis — still **no flashing, no executing of untrusted binaries**; artifacts >50 MB stay OUT of the repo (scratch only). Evidence contract per [_context/CONTEXT.md](_context/CONTEXT.md): URL + title + date + verified/inferred + confidence on every important claim; titled links only. Facts already recorded elsewhere are **linked, not restated** (single-source rule): component IDs → [04](04-HARDWARE-DRIVERS.md); ports → [06](06-DROIDIAN-POSTMARKETOS.md); unlock/backup → [07](07-RECOVERY-SAFETY.md); roadmap → [08](08-DEVELOPMENT-ROADMAP.md); NetHunter/Wi-Fi/HID → [13](13-NETHUNTER-WIFI-EXTRAS.md); mainline gaps → [14](14-MAINLINE-UPGRADE-PATH.md).

**Standing owner facts honored here** (verified 2026-11-21): Ghidra 12.1.4 + Craft Anything are installed on the developer's Mac; [Anonym3310/AkameKernel-begonia](https://github.com/Anonym3310/AkameKernel-begonia) is treated as one third-party kernel tree among many (public history, no special access); the original MIUI 12.5 fastboot ROM is the **ground truth where everything works**.

---

## 1. Ground truth & unpacking recipe

### 1.1 The one firmware to grab: MIUI 12.5 EEA fastboot ROM `V12.5.15.0.RGGEUXM`

Primary = the **fastboot** package (per-partition images that map 1:1 onto the verified GPT in [07 §5](07-RECOVERY-SAFETY.md)); secondary = the recovery/OTA zip (single `payload.bin`, needs an extra dumper step).

| Package | Date | Size (verified-direct 2026-11-21, HTTP HEAD on Xiaomi's own CDN) | MD5 (per XM Firmware Updater — re-verify after download) | Direct link |
|---|---|---|---|---|
| **Fastboot tgz (PRIMARY)** | 2022-08-26 | **4,355,526,590 B ≈ 4.36 GB** — HTTP 200, `Accept-Ranges: bytes` (resumable) | `b8c6b15c15bb5edf8ce68e0393d2ae84` | [bigota.d.miui.com — begonia EEA fastboot V12.5.15.0.RGGEUXM](http://bigota.d.miui.com/V12.5.15.0.RGGEUXM/begonia_eea_global_images_V12.5.15.0.RGGEUXM_20220826.0000.00_11.0_eea_b8c6b15c15.tgz) |
| **Recovery zip (alternative)** | 2022-09-16 | **2,402,363,745 B ≈ 2.4 GB** — HTTP 200 | `cd5652a4c47bc061a7309afc87e94fec` | [bigota.d.miui.com — miui_BEGONIAEEAGlobal recovery V12.5.15.0.RGGEUXM](http://bigota.d.miui.com/V12.5.15.0.RGGEUXM/miui_BEGONIAEEAGlobal_V12.5.15.0.RGGEUXM_cd5652a4c4_11.0.zip) |

Verified metadata pages (both fetched 2026-11-21, verified-direct, high): [XM Firmware Updater — V12.5.15.0.RGGEUXM](https://xmfirmwareupdater.com/miui/begonia/stable/V12.5.15.0.RGGEUXM/) (package names + MD5s + sizes: fastboot `begonia_eea_global_images_V12.5.15.0.RGGEUXM_20220826.0000.00_11.0_eea_b8c6b15c15.tgz`, recovery `miui_BEGONIAEEAGlobal_V12.5.15.0.RGGEUXM_cd5652a4c4_11.0.zip`) and [XiaomiROM.com download page](https://xiaomirom.com/en/download/redmi-note-8-pro-begonia-stable-V12.5.15.0.RGGEUXM/) (same packages, 4.4/2.4 GB, 2022-08-26 / 2022-09-16 — cross-confirmed). Fallback mirrors from the census (snippet-level, medium): [mifirm.net begonia](https://mifirm.net/model/begonia.ttt), [mifirm download 11792](https://mifirm.net/downloadzip/11792). This matches "official MIUI ended 2022" ([00-README finding 1](00-README.md), [02-FIRMWARE-HISTORY.md](02-FIRMWARE-HISTORY.md)).

**Download recipe (verified/verbatim-grade):**

```bash
mkdir -p ~/AI-OS/.hermes/cache/scratch/begonia-recon/rom-v12.5.15 && cd $_
curl -L -C - -o begonia_eea_fastboot_V12.5.15.0.RGGEUXM.tgz \
  "http://bigota.d.miui.com/V12.5.15.0.RGGEUXM/begonia_eea_global_images_V12.5.15.0.RGGEUXM_20220826.0000.00_11.0_eea_b8c6b15c15.tgz"
md5 begonia_eea_fastboot_V12.5.15.0.RGGEUXM.tgz   # expect b8c6b15c15bb5edf8ce68e0393d2ae84
tar -xzf begonia_eea_fastboot_V12.5.15.0.RGGEUXM.tgz
```

`-C -` resume is safe — byte-range support verified on the CDN HEAD (2026-11-21, high). Region sanity before any later device use: `fastboot getvar product` → `begonia`/`begonia_eea` family ([07 §5](07-RECOVERY-SAFETY.md)).

### 1.2 Expected package structure (inferred, medium — confirm at first unpack)

Standard MIUI fastboot layout (cross-referenced against the **verified GPT** in [07 §5](07-RECOVERY-SAFETY.md) — 47 partitions, 64 GB Samsung UFS unit):

- Top dir `begonia_eea_global_images_V12.5.15.0.RGGEUXM.../` containing `images/` plus flash scripts (`flash_all.bat`, `flash_all_lock.bat`, `flash_all_except_storage.bat` — scripts of this class are referenced verbatim in the 4PDA full-reflash walk-through [p=90022165](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=90022165)).
- `images/` (expected, per GPT): `boot.img`, `system.img` (~3.8 GB ext4), `vendor.img` (~1.6 GB), `cust.img`, `cache.img`, `recovery.img`, `logo.img`, `dtbo.img`, `vbmeta.img` (+ likely `vbmeta_system`/`vbmeta_vendor` on A11), `lk.img`/`lk2.img`, **`preloader_begonia.bin`** (preloader has *no* GPT entry — it lives in boot0/boot1, [07 §5](07-RECOVERY-SAFETY.md)), modem `md1img.img`, **`nvram.img` / `nvdata.img` / `nvcfg.img`**, `protect1/2`, `seccfg.img`, `persist`-class images, `proinfo`, `para`, `expdb`, `misc`, `tee1/tee2` (Trusty/TEE), co-processor firmware `scp.img`, `sspm.img`, `spmfw.img`, **`audio_dsp.img`**, **`cam_vpu1/2/3.img`** (camera co-processors), `gz1/2`, `boot_para`, `flashinfo`, `oem_misc1`. File naming may use variants (`*.img.ext4`, `.win`) — record actual names at unpack.
- **`odm`? — resolved from the GPT:** the verified partition table has **no `odm` partition** → odm content (if any) is folded into `vendor`/`cust` on this device. Inferred, medium; verify inside `vendor.img` at unpack.
- MIUI fastboot `.img` files are typically **sparse ext4** → run everything through `simg2img` first (inferred, high for MTK-era MIUI).
- The recovery zip alternative unpacks to `payload.bin` (+ metadata) instead — no per-partition loose images; that is why fastboot is primary.

### 1.3 Unpack tools per artifact

| Artifact | Tool | Notes |
|---|---|---|
| `.tgz` | `tar -xzf` | built into macOS/Linux |
| Sparse ext4 (`system/vendor/cust/cache`) | `simg2img` → raw ext4 | Debian/Ubuntu: package `android-sdk-libsparse-utils` [I, medium]; **macOS: no brew formula verified** (searched 2026-11-21: `brew install --cask android-platform-tools` = [adb/fastboot only](https://formulae.brew.sh/cask/android-platform-tools), verified-direct; it does **not** ship simg2img) → build from AOSP `system/core` or run inside the Linux VM |
| Raw ext4 | `7z` (p7zip) extract; or `mount -o loop,ro` (Linux); `debugfs` (e2fsprogs) for single files | 7z is the safe cross-platform path; never mount untrusted images read-write |
| Recovery zip | `unzip` → `payload.bin` → [ssut/payload-dumper-go](https://github.com/ssut/payload-dumper-go) ("an android OTA payload dumper written in Go", Linux/macOS binaries; verified-direct 2026-11-21) | secondary package only |
| `boot.img` | AOSP `unpack_bootimg` / `magiskboot` | kernel Image + mt6785 DTB + ramdisk for kbase/defconfig diffing |
| ELF blobs (`libaudio*.so`, camera HALs, `wmt`/gen4m libs) | `strings` quick-triage → **Ghidra 12.1.4 + Craft Anything** (installed on the developer's Mac, verified 2026-11-21) for real RE | **analysis only — never execute vendor binaries** (research-only boundary) |
| Vendor configs (`mixer_paths.xml`, `audio_policy*.xml`, Wi-Fi cfg, camera xml, init `.rc`) | plain text inside `vendor.img` | these are the highest-value RE targets — register/driver specs in readable form |

### 1.4 Where results live + disk/time estimates

- Extraction workspace: `~/AI-OS/.hermes/cache/scratch/begonia-recon/rom-v12.5.15/` — **NOT the repo** (REQUIREMENTS #37; archive rule: no multi-GB binaries committed). Only extracted *small text* configs (XML, `.rc`, defconfig-grade files) may later be copied into the repo with provenance notes.
- Disk: tgz 4.36 GB + extracted package ≈ 9–11 GB + raw (simg2img) copies ≈ +9 GB + unpacked ext4 trees ≈ +15 GB → **plan ≥ 40 GB free scratch**. 
- Time (estimates, inferred): download 4.36 GB ≈ 6 min @100 Mbit/s / ≈ 20 min @30 Mbit/s; `tar` minutes; simg2img+7z per large image, tens of minutes total; Ghidra auto-analysis of a 5–20 MB HAL blob ≈ 10–60 min.

### 1.5 Partition → subsystem map (what ground truth feeds which gap)

| Image / content | Subsystem gap it feeds | Where the gap is recorded |
|---|---|---|
| `audio_dsp.img` + vendor `libaudio*.so`, `mixer_paths.xml`, `audio_policy*.xml`, ACCDET config | **Audio** — register/truth source for the missing MT6785 AFE/machine driver | [04 §4](04-HARDWARE-DRIVERS.md), [14 §1.1](14-MAINLINE-UPGRADE-PATH.md) |
| `WIFI_RAM_CODE*` firmware names + gen4m cfg in vendor | **Wi-Fi/BT** — settles the chip-ID question *from the image, without a device*; firmware inventory | [13 §1.1–1.4](13-NETHUNTER-WIFI-EXTRAS.md), [14 §1.3](14-MAINLINE-UPGRADE-PATH.md) |
| `cam_vpu1-3.img` + vendor camera libs / sensorlist xml | **Camera** — sensor part numbers (currently unknown), sensor list, tuning params | [04 §5](04-HARDWARE-DRIVERS.md), [14 §2-C-4](14-MAINLINE-UPGRADE-PATH.md) |
| `md1img.img` (modem fw) + `nvram`/`nvdata`/`nvcfg` images | **Modem/calibration** — the reference copy that the mtkclient backups ([07 §5](07-RECOVERY-SAFETY.md)) protect and can be diffed against | [07 §5](07-RECOVERY-SAFETY.md) |
| `boot.img` (kbase kernel + DTB) + `libMali` blobs in vendor | **GPU** — kbase-vs-Panfrost comparison material (Panfrost already works on pmOS) | [04 §3](04-HARDWARE-DRIVERS.md) |
| vendor battery tables / init rc (`MT6360`, `smb1351` wiring) | **Battery/charging** — the missing board glue | [04 §13](04-HARDWARE-DRIVERS.md), [14 §1.1](14-MAINLINE-UPGRADE-PATH.md) |
| `persist`/`nvdata` calibration, sensor stacks | **Sensors** — resolves contradiction C5 (BMI120 driver question) from the vendor side, no device needed | [04 §11/§18 C5](04-HARDWARE-DRIVERS.md) |
| vendor touchscreen firmware (`novatek/nt36672a_begonia_*.bin`) | **Touch — already solved**; ROM copy = version reference/refresh source | [06 §1.3](06-DROIDIAN-POSTMARKETOS.md), [04 §2](04-HARDWARE-DRIVERS.md) |

---

## 2. Per-subsystem improvement matrix (difficulty-rated)

Legend: difficulty = easy / medium / hard / extreme (+why). "Agent-drivable" = an AI agent writes/patches/analyzes while the owner only runs device tests. Every row obeys the [14 §0](14-MAINLINE-UPGRADE-PATH.md) rule: *config + DT/pinctrl + firmware + userspace* — a single layer is never enough.

| # | Subsystem | Stock firmware ground truth | Mainline/Halium lacks | Concrete RE / kernel-work path | Difficulty | Agent-drivable? |
|---|---|---|---|---|---|---|
| 1 | **Audio** | Full MTK stack: `mt6785-afe-pcm@11210000` ([04 §0](04-HARDWARE-DRIVERS.md)), MT6359 PMIC codec, `audio_dsp` DSP firmware, vendor `mixer_paths.xml` | No MT6785 AFE/machine driver in `sound/soc/mediatek/` ([04 §4](04-HARDWARE-DRIVERS.md), [14 §1.1](14-MAINLINE-UPGRADE-PATH.md)); MT6359 codec + accdet already upstream ([14 §1.2](14-MAINLINE-UPGRADE-PATH.md)) | Port upstream `mt6797/` AFE + `mt8183-mt6358`-class machine driver ([14 §1.2](14-MAINLINE-UPGRADE-PATH.md)); validate every register write against `mixer_paths.xml` extracted from the ROM (§1.5); add DTS sound card node | **hard** — weeks; same-generation register maps assumed close (inferred, medium); needs on-device audio iteration | **yes** — agent writes driver/patches + iterates from `dmesg`/PipeWire logs; owner flashes + runs `aplay`/call tests |
| 2 | **Wi-Fi/BT** | gen4m combo driver (`CONFIG_MTK_COMBO_WIFI=y`, [13 §1.1](13-NETHUNTER-WIFI-EXTRAS.md)), `WIFI_RAM_CODE*` in vendor | No WLAN DT node at all (`no-sdio` on `mmc@11240000`, [14 §0](14-MAINLINE-UPGRADE-PATH.md)); no `CONFIG_MT76*` in pmOS config ([13 §1.4](13-NETHUNTER-WIFI-EXTRAS.md)); chip ID unpinned | **Chip ID first** (§1.5 — from the ROM image, no device); then `CONFIG_MT7663S`+`MT76_SDIO` (+ firmware `mt7663pr2hw.bin` from [linux-firmware](https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/mt7663pr2hw.bin), verified in [13 §1.2](13-NETHUNTER-WIFI-EXTRAS.md)) + SDIO/pinctrl/regulator node written from vendor DTS ([AgentFabulous/begonia](https://github.com/AgentFabulous/begonia) `begonia-mt6785.dtsi`) | **medium-high** — driver+firmware exist upstream ([14 §1.3](14-MAINLINE-UPGRADE-PATH.md)); unknowns are DT/power-seq; internal-connsys-instead-of-discrete risk ([13 §1.4](13-NETHUNTER-WIFI-EXTRAS.md)) | **yes** — chip-ID extraction and DT authoring are agent work; owner tests `iw dev`/assoc |
| 3 | **Camera** | Full MTK ISP: `cam_vpu1-3`, sensor libs + tuning in vendor ([04 §5](04-HARDWARE-DRIVERS.md)) | Dinolek tree has no ISP; kalpakprod carries `seninf/camsv/cam` ([14 §1.1](14-MAINLINE-UPGRADE-PATH.md)); zero sensor nodes in begonia DTS; sensor PNs unknown ([04 §5](04-HARDWARE-DRIVERS.md)) | Extract sensor list from vendor camera libs (strings/Ghidra — RE-lite, §1.5) → write sensor nodes/drivers; port `seninf/camsv` from kalpakprod; Megapixels device config ([14 §2-C-4](14-MAINLINE-UPGRADE-PATH.md)) | **hard→extreme** — kernel pipeline is heavy, but the *tuning/userspace* half is the extreme part ([14 §2-D](14-MAINLINE-UPGRADE-PATH.md): "heavy" Ghidra-class RE of camera HAL/params) | **partial** — agent does sensor-ID/DTS/driver skeletons; ISP tuning is human-iterative on device |
| 4 | **Sensors glue** | Vendor sensor HAL + calibration in `persist` | Most ICs already mainline ([04 §11](04-HARDWARE-DRIVERS.md)); pmOS: proximity broken; accel driver mystery C5 | Settle C5 from vendor sensor list (no device needed); debug upstream STK3310 PS channel against vendor board regs | **easy-medium** — small driver/debug deltas on an otherwise-working set | **yes** |
| 5 | **Battery/charging (MT6360)** | Vendor battery framework; MT6360 + auxiliary `qcom,smb1351` node ([04 §13](04-HARDWARE-DRIVERS.md)) | Charger ICs mainline+enabled yet pmOS battery broken ([14 §1.1](14-MAINLINE-UPGRADE-PATH.md)) → missing board glue | Extract vendor battery parameters/init wiring from the ROM → DTS battery node + fuel-gauge wiring + userspace (upower); settle MT6360-vs-smb1351 duties (C6) from vendor init scripts | **medium** ([14 §2-C-3](14-MAINLINE-UPGRADE-PATH.md)) | **yes** |
| 6 | **Touch** | Novatek NT36672A touch firmware in vendor | — | **solved**: pmOS ships `firmware-xiaomi-begonia-touchscreen` + `novatek-nvt-ts-spi` ([06 §1.3](06-DROIDIAN-POSTMARKETOS.md)) | **none** — keep the ROM copy only as version reference | n/a |
| 7 | **HID/USB gadget** | AFB defconfig already has `USB_CONFIGFS_F_HID=y` etc. ([13 §3.4](13-NETHUNTER-WIFI-EXTRAS.md)) | ECM/NCM (USB-Ethernet) not enabled in AFB/Akame configs; pmOS fragment lacks CONFIGFS gadget functions | **Config-only polish** per [13 §3.4–3.5](13-NETHUNTER-WIFI-EXTRAS.md): add `F_FS`/`F_ACC`/`F_MIDI` (Akame shows the set), `USB_ETH`/ECM/RNDIS for the pmOS USB-Ethernet gadget; rebuild kernel package | **easy** — no RE, config + rebuild loop | **yes — highest ROI per hour** |
| 8 | **Monitor mode** | gen4m proprietary driver; no public monitor patch exists ([13 §1.3](13-NETHUNTER-WIFI-EXTRAS.md)) | Internal: nothing mainline binds to yet | **Internal** = only via row-2 mt76 path (mac80211 → monitor comes free if it binds, [13 §1.4](13-NETHUNTER-WIFI-EXTRAS.md)) — research-grade. **External** = proven begonia recipe: ath9k_htc AR9271 prebuilt modules + `ulan_ath9k_htc.sh` ([4PDA p=105942017](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=105942017)), Akame additional-drivers-pack ([p=97901817](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=97901817)), Kali card list ([13 §1.3](13-NETHUNTER-WIFI-EXTRAS.md)) | internal: **extreme** (nobody has published even a proof branch); external: **easy** | external: yes; internal: research-grade, agent-supported |

---

## 3. Sequencing recommendation (the user's question)

**Verdict: staged — do NOT jump straight to a newer stack.** Reasoned order (assessment, medium-high confidence; consistent with [08 P0](08-DEVELOPMENT-ROADMAP.md) and [14 §4](14-MAINLINE-UPGRADE-PATH.md)):

1. **Stage 1 — fix UT on Halium-10 first** (days–weeks). The mic is UT's worst gap and the fix lead is already identified: diff the [Droidian begonia adaptation](https://github.com/begonia-linux/adaptation-xiaomi-begonia) audio stack (mic ✔ there on the same Halium-10 vendor, [06 §2.3](06-DROIDIAN-POSTMARKETOS.md)) against UT's pulseaudio-modules-droid config ([08 P0 lever 1](08-DEVELOPMENT-ROADMAP.md)). RTC/auto-brightness follow the same diff-and-port pattern. Do not re-platform while the mic is broken ([08 P0 lever 2](08-DEVELOPMENT-ROADMAP.md)).
2. **Stage 2 — Halium-11 move, only after Stage 1 lands** (medium; weeks). Raw material verified: [AgentFabulous/begonia](https://github.com/AgentFabulous/begonia) `android-11.0` (frozen 2022-06-23), [rubencarneiro/linux-android-begonia](https://github.com/rubencarneiro/linux-android-begonia) carries a **`halium-11`** branch ([06 §2.2](06-DROIDIAN-POSTMARKETOS.md)), vendor = final MIUI 12.5 (Android 11). Cost = kernel re-shim + vendor swap + full 10-row retest ([14 §2-A](14-MAINLINE-UPGRADE-PATH.md)); no begonia Halium-11 port exists anywhere yet (searched, [14 §2-A](14-MAINLINE-UPGRADE-PATH.md)). Skipping to Halium-12/13 buys nothing: no A12+ kernel lineage for begonia and the vendor ceiling stays MIUI 12.5.
3. **Stage 3 — mainline (pmOS path) in parallel, with RE filling gaps** (the actual longevity play). Entry order per [14 §4](14-MAINLINE-UPGRADE-PATH.md), now cheaper because §1 of this plan settles inputs without a device: chip-ID from the ROM image → Wi-Fi spike (medium-high) → audio machine driver (hard — the long pole; engage [linux-mediatek](https://lore.kernel.org/linux-mediatek/) early, [14 §3](14-MAINLINE-UPGRADE-PATH.md)). UT-on-mainline stays gated ([14 §2-B](14-MAINLINE-UPGRADE-PATH.md): not viable today — no mainline modem).
- **The Mali precedent as the model:** Panfrost is a *fully reverse-engineered* Mali driver that reached mainline quality — and begonia's Mali-G76 MC4 runs it on pmOS 6.16 today ([04 §3](04-HARDWARE-DRIVERS.md)). Two lessons: (a) RE-driven bring-up can reach upstream and then maintain itself — the target state for rows 1/2/5 of §2; (b) expectation-setting — GPU-class RE consumed a community's years, while begonia's actual debts (machine driver ≈ weeks; Wi-Fi DT bring-up ≈ days–weeks; battery glue ≈ days) are far smaller because readable register/config references exist in the vendor tree and ROM (`mixer_paths.xml`, gen4m cfg, defconfigs). Apply RE where a readable reference exists; do not re-derive whole stacks.
- **What AkameKernel adds (resurrection verdict):** do **not** revive its Q-OSS base wholesale — it targets the MIUI-12/A10 era while 2026 ROMs ride 4.19.325-class kernels ([13 §2.2](13-NETHUNTER-WIFI-EXTRAS.md)). Do mine it, as a third-party source with public history ([REQUIREMENTS #37](https://github.com/0-danielviktorovich-0/begonia-research/blob/main/_context/REQUIREMENTS.md)): its NetHunter defconfig flags (`F_HID`/`F_FS`/`F_ACC`/`F_MIDI`/BT `hci0`) are the feature checklist ([13 §3.4](13-NETHUNTER-WIFI-EXTRAS.md)), its `additional-drivers-pack` is the dongle-driver source ([13 §1.3](13-NETHUNTER-WIFI-EXTRAS.md)), and the self-archived [cvnertnc/Begonia-Kernel-Builder](https://github.com/cvnertnc/Begonia-Kernel-Builder) remains the fork-and-run template for KernelSU-Next/SUSFS builds ([13 §3.1](13-NETHUNTER-WIFI-EXTRAS.md)). The realistic "resurrection" = **rebase Akame's feature set onto the active LOS-24.0/Nova 4.14.356 tree** — medium difficulty, and it doubles as the first-party testbed for kernel experiments (HID, dongles, monitor-mode patches).

---

## 4. Test-resource checklist

### 4.1 Downloads (links + sizes; all verified 2026-11-21 unless noted)

| Item | Link | Size / note |
|---|---|---|
| MIUI 12.5 EEA **fastboot** ROM (ground truth) | [bigota tgz](http://bigota.d.miui.com/V12.5.15.0.RGGEUXM/begonia_eea_global_images_V12.5.15.0.RGGEUXM_20220826.0000.00_11.0_eea_b8c6b15c15.tgz) | 4,355,526,590 B; MD5 `b8c6b15c15…` (§1.1) |
| Recovery zip (alternative) | [bigota zip](http://bigota.d.miui.com/V12.5.15.0.RGGEUXM/miui_BEGONIAEEAGlobal_V12.5.15.0.RGGEUXM_cd5652a4c4_11.0.zip) | 2,402,363,745 B |
| payload-dumper-go | [ssut/payload-dumper-go releases](https://github.com/ssut/payload-dumper-go) | macOS/Linux binaries |
| TWRP (official) | [dl.twrp.me/begonia](https://dl.twrp.me/begonia) — page [twrp.me/xiaomi/xiaomiredminote8pro.html](https://twrp.me/xiaomi/xiaomiredminote8pro.html) | newest listed build 3.7.0_9-0 per [07 §3.0](07-RECOVERY-SAFETY.md) fresh-check |
| OrangeFox (official page) | [orangefox.download/device/begonia](https://orangefox.download/device/begonia) | build freshness unverified ([07 §3.0](07-RECOVERY-SAFETY.md)) |
| UBports Installer | [github.com/ubports/ubports-installer/releases/tag/0.11.2](https://github.com/ubports/ubports-installer/releases/tag/0.11.2) | macOS .dmg exists ([07 host matrix](07-RECOVERY-SAFETY.md)) |
| MT7663 firmware (conditional on chip ID) | [linux-firmware `mt7663pr2hw.bin`](https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/mt7663pr2hw.bin) | verified present in [13 §1.2](13-NETHUNTER-WIFI-EXTRAS.md) |

### 4.2 Host tools (macOS reality per [07 host matrix](07-RECOVERY-SAFETY.md))

- **Native on macOS:** [mtkclient](https://github.com/bkerler/mtkclient) (unlock `mtk da seccfg unlock`, `rf`/`rl` backups, unbrick, GUI — incl. Apple Silicon notes, [07 §2](07-RECOVERY-SAFETY.md)); adb/fastboot via [brew cask android-platform-tools](https://formulae.brew.sh/cask/android-platform-tools) (verified-direct 2026-11-21); **Ghidra 12.1.4 + Craft Anything** (installed, owner-verified 2026-11-21); p7zip; python venvs.
- **Linux VM required:** pmbootstrap (verbatim: other OSes unsupported, [07 host matrix](07-RECOVERY-SAFETY.md)); Halium/UT builds; simg2img (§1.3 limitation).
- **Skip:** SP Flash Tool (no macOS build; mtkclient fully replaces it on begonia per the pmOS wiki footnote, [07 §3](07-RECOVERY-SAFETY.md)).
- **Rule:** vendor binaries from the ROM are analyzed (strings/Ghidra), never executed (research-only).

### 4.3 Device-side state (must be true before test phase)

1. Bootloader unlocked via `mtk da seccfg unlock` ([07 §2](07-RECOVERY-SAFETY.md)); 2. TWRP or OrangeFox installed (official pages above; unified TWRP 3.7.1 community line exists, [07 §3.0](07-RECOVERY-SAFETY.md)); 3. current ROM + slot known and recorded; 4. region checked `fastboot getvar product` ([07 §5](07-RECOVERY-SAFETY.md)); 5. **safety rails done first** — preloader backup via `mtk r preloader preloader.bin --parttype=boot1` (step 1 of unlocking per pmOS wiki), full-flash `mtk rf` + per-partition `mtk rl`, and `nvram`/`nvdata`/`nvcfg`/`persist` dumps ([07 §5](07-RECOVERY-SAFETY.md)); vbmeta discipline on every boot test ([07 §6](07-RECOVERY-SAFETY.md)).

### 4.4 The "agent proposes → owner runs" loop (exact design)

1. **Agent** (in repo + scratch): produce one *single-variable* change — patch file, defconfig diff, DTS node, or config extraction — plus (a) predicted observable outcome, (b) exact device command list, (c) rollback command, (d) what logs to capture (`adb shell dmesg`, `logcat`, pstore/last_kmsg, `iw`, `aplay -l`).
2. **Owner** runs: build (VM or native), flash/boot on device, execute the command list, collect logs — never deviating from one variable per boot test ([08](08-DEVELOPMENT-ROADMAP.md)).
3. **Agent** parses returned logs, updates the artifact, repeats — or writes a "dead end" record with evidence.
4. **Provenance:** >50 MB artifacts stay in scratch; the repo receives patches, extracted small configs (with source+date), and notes only; every landed change is appended to `sources.jsonl` and, where it corrects an existing row, queued via [_context/CORRECTIONS.md](_context/CORRECTIONS.md) (freshness protocol, REQUIREMENTS #35).
5. **Hard rule:** the agent never flashes, never writes to the device, never executes vendor binaries — the owner executes every device write after reading the rollback path.

---

## Limitations

- Fastboot-package *internal* structure (file names, sparse vs raw, vbmeta variants) is inferred from the verified GPT + standard MIUI layout — **medium** until the authorized first unpack (§1.2).
- Wi-Fi chip ID remains conditional (MT7663 family suspected, [13 §1.1](13-NETHUNTER-WIFI-EXTRAS.md)) until the `WIFI_RAM_CODE*` list is read from the image or device.
- No device-side verification of anything in this plan (research-only); all on-device steps are owner-run.
- simg2img on macOS has no verified brew formula (searched 2026-11-21) — use AOSP build or the Linux VM.

*Last updated: 2026-11-21T10:17:24Z. Sources appended to `~/AI-OS/.hermes/cache/scratch/begonia-recon/sources.jsonl`.*
