# Begonia (Xiaomi Redmi Note 8 Pro) — Hardware & Driver Inventory

Dimension: hardware & drivers. Per-OS status: **UT 24.04** (Ubuntu Touch noble, Halium 10.0, kernel 4.14.141), **Droidian** (community port, Halium-based, kernel begonia-linux/linux-android-begonia), **pmOS 6.16** (mainline 6.16.4, Dinolek fork), **Android custom ROMs** (downstream 4.14 kernel + full vendor blobs).
Method: components identified **only** from mainline DTS (Dinolek/mt6785-mainline, branch 7.1), vendor DTS (AgentFabulous/begonia, android-11.0), pmOS kernel config (pmaports), `/proc/iomem` + parted dumps (Nura wiki), and OS support matrices. Unverifiable part numbers are written `unknown`, never guessed.
Status vocabulary: works | partial | broken | unknown. Machine-readable twin: `hardware-support-matrix.csv` (same rows).

## 0. Key evidence anchors

| Anchor | What it is | Where |
|---|---|---|
| Mainline DTS | `mt6785-xiaomi-begonia-common.dtsi` + **two panel DTS: `mt6785-xiaomi-begonia-csot.dts`, `mt6785-xiaomi-begonia-tianma.dts`** (branch `7.1`, default, pushed 2026-06-17) | github.com/Dinolek/mt6785-mainline |
| Vendor DTS | `begonia-mt6785.dtsi` (android-11.0): `goodix,goodix-fp`, `nxp,p61`, `qcom,smb1351-charger`, `xiaomi-touch`/`xiaomi,spi-for-tp`, `xiaomi,simtray-status` | github.com/AgentFabulous/begonia |
| pmOS kernel config | `config-postmarketos-mediatek-mt6785.aarch64`, kernel pkg 6.16.4-r1, source gitlab.postmarketos.org/mt6785-mainline/linux | gitlab.nura.eco/nura/pmaports |
| On-chip map | `/proc/iomem` (Android): i2c0–i2c9, spi0–spi7, `ufshci@11270000`, `13040000.mali`, smi_larb0–7, scp@10500000, adsp@10600000, `mt6785-afe-pcm@11210000`, mac(eth) | Nura wiki (oldid=109575) |
| Storage | parted: `Model: SAMSUNG KM2H7001CM-B518 (scsi)`, 64 GB, UFS (4096B sectors; 47 partitions incl. md1img, scp1/2, sspm, tee1/2, vbmeta) | Nura wiki |

## 1. Display & backlight — works everywhere

**Panel variants confirmed at DTS level**: begonia shipped with **two panel suppliers, CSOT and Tianma**; both use a **Novatek NT36672A** driver IC but get distinct compatibles (`xiaomi,begonia-csot-nt36672a`, `xiaomi,begonia-tianma-nt36672a`) and **distinct touchscreen firmware files** (`novatek/nt36672a_begonia_csot.bin` vs `..._tianma.bin`). pmOS ships separate DTBs per variant (`deviceinfo_bootimg_custom_args` → `mt6785-xiaomi-begonia.dtb`; kernel package builds both).

| Item | ID (source) | Driver (pmOS) | UT 24.04 | Droidian | pmOS 6.16 | Android |
|---|---|---|---|---|---|---|
| Panel 6.53" 1080x2340 IPS | NT36672A (DTS) | `DRM_PANEL_NOVATEK_NT36672A=m`, `DRM_MEDIATEK=y` (ovl/rdma/color/ccorr/aal/gamma, mt8183-mipi-tx DPHY) | works | works | works | works |
| Backlight | TI LM36274 (`ti,lm36274`, backlight+regulator, DTS) | `BACKLIGHT_LM36274=m`, `lm36274_bl` in initfs; `ti-lmu` MFD | works (manual) | works | works | works |
| Auto-brightness | STK3310 ALS | — (framework) | **broken** → repowerd#11 | **broken** (README ❌) | n/a (pmOS has no such daemon issue; ALS itself works) | works |

Known quirks: pmOS user report "GNOME freezing when changing brightness" (wiki, user Letstry_pmos). UT also lists wired/wireless external monitor as unsupported hardware.

## 2. Touchscreen — works everywhere

Novatek NT36672A touch controller on **SPI** (`novatek,nt36672a-ts` in mainline DTS; driver `TOUCHSCREEN_NOVATEK_NVT_TS_SPI=m`, initfs module `novatek-nvt-ts-spi`; vendor side `xiaomi-touch` + `xiaomi,spi-for-tp`). Variant firmware via `firmware-name`. Status: works (UT/Droidian/pmOS/Android all confirm). pmOS loads the driver from initramfs — usable for FDE unlock (unl0kr).

## 3. GPU — Mali-G76 MC4 (Bifrost)

DTS: `compatible = "mediatek,mt6785-mali", "arm,mali-bifrost"`; `/proc/iomem` `13040000.mali`; supply `mt6359_vgpu11_buck_reg` (coupled with VGPU/VPU).

| OS | Userspace / kernel driver | Status |
|---|---|---|
| UT 24.04 / Droidian | proprietary Mali Bifrost kbase from stock 4.14 kernel + vendor blob (libMali/gralloc via Halium/libhybris); UT: "boot into UI" + "hardware video playback" ✔ | works (Droidian inferred from Waydroid ✔ + UI, medium) |
| pmOS 6.16 | **Panfrost** (`CONFIG_DRM_PANFROST=m`) + Mesa **panvk** Vulkan (`mesa-vulkan-panfrost` in device APKBUILD depends); 3D acceleration "Works" | works |
| Android custom | proprietary blob (same as stock) | works |
| panthor | N/A — panthor is the Mali **CSF** driver; G76 is Bifrost → panfrost/panvk is the correct mainline path | — |

## 4. Audio (playback / mic / headset) — the mainline gap

**Codec verified**: the audio codec is integrated in the **MediaTek MT6359 PMIC** — `mt6785-xiaomi-begonia-common.dtsi` line 13 `#include "mt6359.dtsi"`, PMIC regulators/keys/vibr all `mt6359_*`; `/proc/iomem` shows `mt6785-afe-pcm@11210000` and an `adsp@10600000` block; `audio_dsp` partition exists.
Mainline kernel has an ASoC **codec** driver for MT6359, but `sound/soc/mediatek/` in the mt6785 fork (checked branch 7.1) contains only mt2701/mt6797/mt7986/mt8173/mt8183/mt8186/mt8188/mt8189/mt8192/mt8195/mt8365 — **no MT6785 AFE/machine driver** → no sound card on pmOS.

| Sub-item | UT 24.04 | Droidian | pmOS 6.16 | Android |
|---|---|---|---|---|
| Playback (speaker) | works (loudspeaker) | works | broken | works |
| Earphones/headset | works | works (incl. BT headphones) | broken | works |
| Microphone | **broken** (official matrix) | **works** (README) — see Contradictions | broken | works |
| Call audio / routing / volume | works | works | broken | works |
| FM radio | broken (matrix) | unknown | unknown | ROM-dependent, unverified |

pmOS config has `SND_SIMPLE_CARD=m` only — nothing MT6359/MT6785-specific enabled. ACCDET (headset jack detect) not found in pmOS config.

## 5. Cameras + flash

Main 64MP sensor is the **Samsung ISOCELL GW1** (shared verified device fact; UT specs page: "64 MP, 8 MP ultrawide, 2 MP macro, 2 MP depth; front 20MP"). **Ultrawide/macro/depth/front sensor part numbers: unknown** — neither the mainline DTS (`begonia` common dtsi has no camera-sensor nodes at all) nor the reachable vendor `begonia-mt6785.dtsi` names them; vendor sensor config lives in files we did not retrieve. Mainline fork's `drivers/media/platform/mediatek/` has only jpeg/mdp/mdp3/vcodec/vpu — **no ISP/sensor pipeline** (CCI controller `mediatek,mt6785-cci` exists).

| Sub-item | UT 24.04 | Droidian | pmOS 6.16 | Android |
|---|---|---|---|---|
| Photo/video, camera switching | works | works ("droidian-camera & gst backend") | broken | works |
| Camera flash (torch) | works (torchlight+flashlight) | unknown (not in README) | **works** | works |

## 6. IR blaster

- pmOS: **broken** (wiki), despite `CONFIG_IR_PWM_TX=m` being enabled in the 6.16.4 config — **no IR node exists in begonia's mainline DTS** (grep over common dtsi found none), so the driver has nothing to bind.
- UT: no feature-matrix row → unknown. Droidian: not listed → unknown.
- Android: works; ColorOS 17 rev 13 changelog (2026-11-15, 4PDA post p=146061439) literally says "**IR blaster works again**" → it had regressed on some ROMs and was re-fixed.

## 7. Modem / calls / SMS / data / VoLTE

MT6785 integrated modem (md1img/boot_para partitions; pmOS wiki boot chain BROM→PL→LK→Linux).

| Sub-item | UT 24.04 | Droidian | pmOS 6.16 | Android |
|---|---|---|---|---|
| Calls | works | works | broken | works |
| SMS/MMS | works | works | broken | works |
| Mobile data, dual SIM, carrier info, PIN | works | works | broken | works |
| VoLTE | **broken — global issue** gitlab.com/ubports/ubuntu-touch/-/issues/1335 (experimental, carrier/region dependent) | unknown | broken | unknown (not separately verified in fetched posts) |

## 8. Wi-Fi & Bluetooth

**Chip: unknown.** Neither the mainline DTS nor the vendor dtsi we could reach names the SDIO combo chip, and per the rules it stays unknown. pmOS 6.16.4 config contains **no MediaTek WLAN driver** (no `CONFIG_MT76*`/MT7663 entries; only CFG80211/MAC80211 stacks) → consistent with "Wi-Fi: Broken".

| Sub-item | UT 24.04 | Droidian | pmOS 6.16 | Android |
|---|---|---|---|---|
| Wi-Fi (STA) | works | works | broken | works |
| Hotspot | works | **broken** ("can work with some fixes") | broken | works (assumed; not separately verified) |
| Bluetooth | works | works (incl. BT audio) | broken | works |

## 9. NFC — works on every OS

Mainline DTS: `nxp,nxp-nci-i2c` (NXP NCI controller over I2C); vendor DTS adds the secure element node **`nxp,p61`** (NXP P61/SN100-family SE). pmOS driver `CONFIG_NFC_NXP_NCI_I2C=m`. Exact controller part number beyond "NXP NCI": unknown. Status: works (pmOS ✔, UT ✔, Droidian ✔; Android assumed ✔).

## 10. GPS

MT6785 integrated GNSS. UT: works but **global issue** — slow first fix from missing A-GPS (gitlab.com/ubports/development/core/location-service/-/issues/13). Droidian: works (README: "partially"). pmOS: broken. Android: works.

## 11. Sensors

| Sensor | Part number (source) | pmOS driver | UT 24.04 | Droidian | pmOS 6.16 | Android |
|---|---|---|---|---|---|---|
| Accelerometer | **Bosch BMI120** (`bosch,bmi120`, mainline DTS) | none found — see Contradiction C4 | works (rotation) | works | works ⚠ | works |
| Magnetometer | **Asahi Kasei AK09918** (`asahi-kasei,ak09918`) | `CONFIG_AK8975=m` (AK8975 driver family) | no matrix row → unknown | unknown | works | works |
| Ambient light + proximity | **Sensortek STK3310** (`sensortek,stk3310`, combined ALS+PS) | `CONFIG_STK3310=m` | sensor present; auto-brightness broken (repowerd#11) | proximity ✔, auto-brightness ❌ | **ALS works, proximity broken** | works |
| Proximity (as reported) | same chip | — | works | works | broken | works |
| Gyroscope | not named in mainline DTS → unknown | — | unknown | unknown | unknown | unverified |

## 12. Fingerprint reader

Vendor DTS (AgentFabulous/begonia, android-11.0, `begonia-mt6785.dtsi`): node `fingerprint@0` with **`compatible = "goodix,goodix-fp"`** → **Goodix** (exact model unknown). No node in the mainline DTS and no pmOS wiki row.
Status: UT **works**, Droidian works, Android works (all blob/biometric-stack paths); pmOS **unknown** (no row, no driver evidence).

## 13. Charging & battery

- **Charger IC: MediaTek MT6360** — mainline DTS `mediatek,mt6360-chg` (+ `mediatek,mt6360-adc`, `-led`, `-regulator`, `-tcpc` for USB-C PD); pmOS config `CONFIG_CHARGER_MT6360=y`, `MFD_MT6360=y`, `TYPEC_MT6360=m`.
- Vendor DTS additionally carries a **`qcom,smb1351-charger`** node — a Qualcomm SMB1351 charger block present in the stock board description (likely auxiliary charge path); do not treat MT6360 as the exclusive charger without on-device verification.
- Fuel gauge/battery: MT6359 PMIC (`MEDIATEK_MT6359_AUXADC=m`).
- pmOS: battery/charging **broken** (wiki row). UT: offline + online charging, battery percentage **work**. Droidian: not listed → unknown. Android: works.

## 14. Power management / suspend / RTC

- pmOS: power domains `MTK_SCPSYS_PM_DOMAINS=y`; co-processors visible in iomem (scp, sspm, adsp). No suspend row on the wiki → **unknown**.
- UT: "24+ hours battery lifetime", "7+ days stability" → effectively works.
- RTC: **MT6359 PMIC RTC** via `CONFIG_RTC_DRV_MT6397=m` (MT6397 MFD family covers MT6359). UT matrix: **RTC time not working**. pmOS: driver built but no wiki row → unknown. Droidian: unknown. Android: works.

## 15. USB

Controller: `mediatek,mt6785-mtu3` + `mt6785-xhci`, **dual role** (`CONFIG_USB_MTU3=y`, `USB_MTU3_DUAL_ROLE=y`), TPHY v2; Type-C PD via MT6360 TCPC.

| Sub-item | UT 24.04 | Droidian | pmOS 6.16 | Android |
|---|---|---|---|---|
| Role switching / OTG | unknown (matrix lists only MTP/ADB) | partial (MTP ✔; host not documented) | **works** ("USB OTG / role switching: Works" + USB networking) | works |
| MTP / ADB | works / works | MTP works | ADB+SSH during install works | works |

## 16. Haptics / notification LED / buttons

- Haptics: `regulator-haptic` supplied by **`mt6359_vibr_ldo_reg`**; `CONFIG_INPUT_REGULATOR_HAPTIC=m`. works on all four (pmOS ✔, UT vibration ✔, Droidian ✔).
- Notification LED: UT **works**; pmOS no row (`LEDS_MT6360=m` present) → unknown; Droidian unknown; Android works.
- Buttons: gpio-keys + `mediatek,mt6359-keys` (pmOS DTS); pmOS USB/flashing paths work. Droidian note: one pmOS-wiki user reports broken side buttons on their unit (hardware failure, not driver).

## 17. Storage: SD card + UFS

- **UFS**: Samsung **KM2H7001CM-B518** (parted "Model:" line, 64 GB unit); driver `mediatek,mt6785-ufshci` + `mt6785-ufsphy` (`CONFIG_SCSI_UFS_MEDIATEK=y`, `PHY_MTK_UFS=y`); 4096B logical sectors (`deviceinfo_rootfs_image_sector_size=4096`). works everywhere (pmOS internal storage ✔).
- **SD card**: `mediatek,mt6785-mmc` (mt8183-mmc compatible), two MMC nodes; pmOS ✔, UT ✔, Droidian ✔, Android ✔. (UEFI/Mu-Silicium experiment boots WinPE only from SD — 4PDA p=146118602.)

## 18. Contradictions & open questions

- **C1 — Fingerprint: UT "works" vs pmOS silent.** Not a real conflict: UT/Droidian/Android use the Goodix blob stack (vendor node `goodix,goodix-fp`), pmOS mainline has **no fingerprint node/driver and no wiki row** → pmOS = unknown, others = works. Resolved.
- **C2 — Proximity: UT/Droidian "works" vs pmOS "broken".** Same physical STK3310; Halium uses the vendor sensor stack, mainline STK3310 driver exposes ALS but its proximity channel is broken on pmOS while ambient light works. Resolved (per-stack difference).
- **C3 — Camera/charging/battery/audio "UT works vs pmOS broken".** Same cause: Halium rides the stock 4.14 vendor stack; mainline 6.16 lacks the sensor/ISP, audio machine driver, and fuel-gauge/charging glue. Resolved.
- **C4 — Microphone: UT matrix says broken, Droidian README says works** — both Halium-based ports. Not resolved; possibly fixed in Droidian's pulseaudio/policy or the UT matrix is stale. Flagged, medium confidence both sides.
- **C5 — Accelerometer: pmOS wiki says works, but pmOS 6.16.4 config has no BMI120 driver** (only `BMI160`, `HID_SENSOR_ACCEL_3D`; drivers/iio/imu + accel dirs of the fork list no bmi120). Either an out-of-tree driver lives outside the audited dirs, another driver serves it, or the wiki row is stale. **Unresolved — needs on-device check.** Medium confidence.
- **C6 — Charger IC:** mainline DTS = MT6360; vendor DTS also has `qcom,smb1351-charger`. Both documented; split of duties unverified.

## 19. Limitations

- Live XDA (megathread + unlock guide) blocked by bunny.net challenge for our tools (per shared context; not retested) — used only 4PDA/Wayback-independent sources; nothing hardware-critical was left pending on XDA.
- Wi-Fi/BT combo chip, gyroscope, ultrawide/macro/depth/front camera sensor PNs, exact NXP NFC part number, Goodix FP model: **unknown** (not named in reachable DTS/vendor files; no guessing).
- Vendor camera sensor definitions were not located in the reachable vendor DTS files (begonia.dts is a 630-byte stub; begonia-mt6785.dtsi has no camera nodes) — sensors are defined elsewhere in the vendor tree (not fetched).
- Droidian statuses come from the adaptation README (no date stamp); treat Droidian "works" as single-source medium confidence.
- Mu-Silicium **UEFI** experiment (4PDA post #24679, p=146118602, 2026-11-19/20): display ✅, SD ✅, buttons ✅, USB entirely ❌ — firmware demo, not a daily OS; cited only as mainline-activity evidence.

## 20. Sources (also appended to sources.jsonl)

1. Dinolek/mt6785-mainline DTS (branch 7.1): github.com/Dinolek/mt6785-mainline/tree/7.1/arch/arm64/boot/dts/mediatek — verified-direct, high.
2. AgentFabulous/begonia vendor DTS (android-11.0): arch/arm64/boot/dts/mediatek/begonia-mt6785.dtsi — verified-direct, high.
3. pmaports device + kernel packages (main, 2026-11-21): gitlab.nura.eco/nura/pmaports — verified-direct, high.
4. Nura/pmOS wiki device page (oldid=109575): wiki.nura.eco/wiki/Xiaomi_Redmi_Note_8_Pro_(xiaomi-begonia) — cache, high.
5. UBports device page: devices.ubuntu-touch.io/device/begonia — cache, high. Issues: repowerd#11, ubuntu-touch#1335, location-service#13.
6. Droidian adaptation: github.com/begonia-linux/adaptation-xiaomi-begonia (README) — verified-direct, medium.
7. 4PDA custom-ROM thread topic 974421, p.1234 (st=24660): ColorOS 17 post p=146061439 (IR blaster), UEFI/Mu-Silicium post p=146118602 — verified-direct, medium.
