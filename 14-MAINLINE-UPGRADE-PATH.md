# 14 — Mainline upgrade path & open-driver development (begonia / MT6785)

Researched 2026-11-21 (JST). Research-only: nothing flashed, nothing downloaded except small text artifacts (defconfigs, Makefiles). Companion files: kernel landscape → [03-KERNEL-HISTORY.md](03-KERNEL-HISTORY.md) §4; per-component status + driver gaps → [04-HARDWARE-DRIVERS.md](04-HARDWARE-DRIVERS.md); pmOS/Droidian/UT ports → [06-DROIDIAN-POSTMARKETOS.md](06-DROIDIAN-POSTMARKETOS.md). Per repo single-source rule, already-recorded facts are linked, not restated.

Legend: **[V]** verified directly this session (URL fetched); **[I]** inferred (basis given); confidence high/medium/low per claim.

---

## 0. Owner caveat — "enabling a config alone was NOT sufficient" (first-hand, 2026-11-21)

The owner enabled a kernel config on this device once and the feature still did not work (details forgotten). This is the norm on MTK, not the exception. What is typically the missing piece, with concrete examples:

| Missing layer | Concrete begonia evidence | Source |
|---|---|---|
| **DT nodes / pinctrl / regulators** | IR blaster: pmOS 6.16 config has `CONFIG_IR_PWM_TX=m` **enabled**, yet IR is broken because **no IR node exists in begonia's mainline DTS** — the driver has nothing to bind to | [04-HARDWARE-DRIVERS.md](04-HARDWARE-DRIVERS.md) §6 [V] |
| Same class, found this session | begonia mainline DTS: `mmc@11240000` carries **`no-sdio;`** and the board dtsi has **no WLAN device node at all** — enabling `CONFIG_MT7663S` would produce a driver with no device | local copy of [mt6785-xiaomi-begonia-common.dtsi](https://github.com/Dinolek/mt6785-mainline/blob/7.1/arch/arm64/boot/dts/mediatek/mt6785-xiaomi-begonia-common.dtsi), branch `7.1` [V] |
| **Firmware files** | WiFi-class chips need userspace firmware blobs; for the suspected MT7663: `mediatek/mt7663pr2h.bin` + `mt7663pr2h_rebb.bin` ship in [linux-firmware](https://archlinux.org/packages/core/any/linux-firmware-mediatek/files/) (Arch package file list, 2026-10 build) [V] — and even with firmware present, loading can fail (Debian bug [#1146149](https://lists.debian.org/debian-kernel/2026/08/msg00470.html), 2026-08: "Failed to get patch semaphore / failed to load mediatek/mt7663pr2h_rebb.bin") [V] |
| **Userspace glue** | pmOS user Halhadus: *"you can enable kernel configs to use USB Ethernet, Phosh working good"* — config + module + interface config all needed; another user on the same wiki could not get USB networking at all | pmOS wiki users section, cached, quoted in [06 §1.6](06-DROIDIAN-POSTMARKETOS.md) [V-cache] |

**Rule for every claim below:** "just enable X" means enable config **+ write DT node/pinctrl + provide firmware + wire userspace**. Any single layer missing = broken, exactly the pmOS-broken list.

---

## 1. State of the art (verified)

### 1.1 What the three mainline trees actually enable (defconfig evidence, fetched raw 2026-11-21)

All three in-tree `arch/arm64/configs/defconfig` files are near-identical, arm64-defconfig-derived (matches the pmOS APKBUILD note "config based on arch/arm64/configs/defconfig"):

| Tree / ref | File (raw fetch) | Size [V] |
|---|---|---|
| [Dinolek/mt6785-mainline](https://github.com/Dinolek/mt6785-mainline) branch `7.1` (tags 6.16.3-r0/6.16.4-r0/7.1-r0; base Linux 7.1.0 per [03 §4.1](03-KERNEL-HISTORY.md)) | [defconfig](https://raw.githubusercontent.com/Dinolek/mt6785-mainline/7.1/arch/arm64/configs/defconfig) | 48,532 B |
| same repo, branch `6.16` | [defconfig](https://raw.githubusercontent.com/Dinolek/mt6785-mainline/6.16/arch/arm64/configs/defconfig) | 43,393 B |
| [kalpakprod/mt6785-linux](https://github.com/kalpakprod/mt6785-linux) branch `main` (Linux 7.3.4, created 2026-11-15, per [03 §4.3](03-KERNEL-HISTORY.md)) | [defconfig](https://raw.githubusercontent.com/kalpakprod/mt6785-linux/main/arch/arm64/configs/defconfig) | 48,971 B |

Per-subsystem verdict vs the pmOS-broken list ([06 §1.5](06-DROIDIAN-POSTMARKETOS.md), [04](04-HARDWARE-DRIVERS.md)) — identical in **all three** configs [V]:

| pmOS-broken item | In-tree defconfig evidence | Verdict |
|---|---|---|
| Wi-Fi | `CFG80211/MAC80211` stacks only; **no `CONFIG_MT76*`, no `CONFIG_MT7663*`** (only `CONFIG_MT7921E=m` — PCIe, wrong bus for an SDIO combo) | **not enabled** — driver exists upstream (§1.3), needs config + DT + firmware |
| Bluetooth | no MT7663-family BT entry (kernel BT for such combos = `btmtkuart`-class UART/SDIO glue) | **not enabled** [I, medium] |
| Audio | `SND_SIMPLE_CARD=m` only; machine drivers present are for *other* SoCs (`MT8183/8188/8192/8195/8365 + MT6359` pairings); **no MT6785 AFE/machine driver** — Dinolek 7.1 [sound/soc/mediatek/Makefile](https://raw.githubusercontent.com/Dinolek/mt6785-mainline/7.1/sound/soc/mediatek/Makefile) has dirs `mt2701, mt6797, mt7986, mt8173, mt8183, mt8186, mt8188, mt8189, mt8192, mt8195, mt8365` [V] | **missing in-tree work** |
| Camera | Dinolek 6.16/7.1: media platform = jpeg/mdp/vcodec/vpu only ([04 §5](04-HARDWARE-DRIVERS.md) [V]); **kalpakprod adds `seninf/`, `camsv/`, `cam/`** ([Makefile](https://raw.githubusercontent.com/kalpakprod/mt6785-linux/main/drivers/media/platform/mediatek/Makefile), `obj-y` unconditional) [V] | **kalpakprod carries an ISP pipeline; Dinolek does not** |
| Modem | no `CONFIG_MTK_MODEM`-class option in any defconfig | **not enabled — no upstream driver exists** |
| Battery/charger | `CHARGER_MT6360=m`, `MFD_MT6360=y`, `TYPEC_MT6360=m`, `BATTERY_*` generic gauges — charger IC **is** mainline ([04 §13](04-HARDWARE-DRIVERS.md)) | **enabled in config**, yet pmOS battery broken → missing board glue (battery node, fuel-gauge wiring, userspace) — the owner's caveat in action |
| Working set (sanity check) | `DRM_PANEL_NOVATEK_NT36672A=m`, `DRM_PANFROST=m`, `NFC_NXP_NCI_I2C=m`, `USB_MTU3=y`, `RTC_DRV_MT6397=m`, `MTK_SCP/MTK_CMDQ/MTK_PMIC_WRAP` | matches pmOS works-list (screen/touch/GPU/NFC/OTG/haptics) [V] |

SoC-side MT6785 enablement (clocks, pinctrl, power domains, display) is carried as patches/in-tree SoC files in all three trees (per [03 §4](03-KERNEL-HISTORY.md)); the defconfig differences above are the *driver* deltas.

### 1.2 Linus master for MT6785-family today (re-confirmed)

- [arch/arm64/boot/dts/mediatek/Makefile](https://raw.githubusercontent.com/torvalds/linux/master/arch/arm64/boot/dts/mediatek/Makefile) on `master`, fetched 2026-11-21: **zero mt6785 lines** [V, re-confirms 03 §4]. Complete mt6xxx dtb list: `mt6755-evb`, `mt6779-evb`, `mt6795-evb`, `mt6795-sony-xperia-m5` (a **phone** dts), `mt6797-evb`, `mt6797-x20-dev` [V]. No G-series (mt6785/mt6789) and no Dimensity phone SoCs (mt6833/mt6853) — **there is no closer upstream generation than mt6779 (Helio P70/P90) and mt6797 (Helio X20)**; both are pre-G90 [V].
- Master [sound/soc/mediatek/Makefile](https://raw.githubusercontent.com/torvalds/linux/master/sound/soc/mediatek/Makefile): no mt6785 dir [V]; but **`mt6797/` machine dir exists upstream** — the closest template for an MT6785 AFE/machine driver [V].
- **MT6359 PMIC codec is already upstream**: [sound/soc/codecs/mt6359.c](https://raw.githubusercontent.com/torvalds/linux/master/sound/soc/codecs/mt6359.c) (88,336 B) and [mt6359-accdet.c](https://raw.githubusercontent.com/torvalds/linux/master/sound/soc/codecs/mt6359-accdet.c) (32,123 B, headset-jack detect) [V]. The audio gap is therefore **only** the MT6785 AFE DAI + machine driver + DTS sound card.
- Community SoC enablement precedent upstreamed: `drivers/clk/mediatek/clk-mt6735-*` files appear in mainline [MAINTAINERS](https://raw.githubusercontent.com/torvalds/linux/master/MAINTAINERS) F: lines [V] — the [mediatek-mainline org](https://github.com/mediatek-mainline)'s MT6735 (Helio P10) effort pushed clocks upstream.

### 1.3 WLAN driver & firmware status (for the suspected MT7663)

- Mainline mt76 **has MT7663 support**: [mt76/mt7615/Kconfig](https://raw.githubusercontent.com/torvalds/linux/master/drivers/net/wireless/mediatek/mt76/mt7615/Kconfig) on master defines `MT7663U` (USB), `MT7663S` (**SDIO** — the bus a phone combo would use), `MT7663_USB_SDIO_COMMON`, and `MT7615E` covering "MT7615E and MT7663E (PCIe)" [V]. kernel.org's driver page notes MT7613 is also handled as a mt7663 case (ChipID 0x7663) by the mt7615 driver ([wireless.docs.kernel.org — mediatek](https://wireless.docs.kernel.org/en/latest/en/users/drivers/mediatek.html)) [V].
- Firmware: `mediatek/mt7663pr2h.bin` + `mt7663pr2h_rebb.bin` are shipped by linux-firmware (Arch [linux-firmware-mediatek](https://archlinux.org/packages/core/any/linux-firmware-mediatek/files/) file list) [V].
- **Chip ID on begonia is still unknown** ([04 §8](04-HARDWARE-DRIVERS.md)); MT7663 is the owner's suspicion (REQUIREMENTS #31) and the standard MT6785-generation SDIO combo — on-device confirmation (Android: `cat /proc/net/wireless` + `/vendor/firmware/WIFI_RAM_CODE*` names, or SDIO VID/PID) is work-item C-1 below. Until then every MT7663 statement is conditional [I, medium].

---

## 2. The option tree (analysis — reasoned, not independently tested)

### Option A — Ubuntu Touch stays Halium-based (pragmatic UT path)

- Current: Halium 10.0, kernel 4.14.141, noble 24.04 — see [03 §3](03-KERNEL-HISTORY.md) and [05-UBUNTU-TOUCH.md](05-UBUNTU-TOUCH.md). Most phone features work; broken: mic (UT matrix), RTC, VoLTE-global, auto-brightness-global ([CONTEXT.md](_context/CONTEXT.md) device cache).
- **Newer Halium exists and the mapping is official**: [docs.ubports.com — Introduction to porting](https://docs.ubports.com/en/latest/porting/introduction/Intro.html) table (fetched 2026-11-21) [V]: Android 9→Halium 9.0, **10→10.0, 11→11.0, 12→12.0, 13→13.0**; "Since 20.04, Ubuntu Touch ports are normally based on Halium 9.0 or later. Older versions … deprecated." The Halium project is alive (GitHub org [Halium](https://api.github.com/orgs/Halium/repos): `libhybris` pushed 2026-10-27, `android` 2026-09-22, `android-headers` 2026-08-25 [V]).
- Begonia-specific raw material for a Halium-11 move already exists: [rubencarneiro/linux-android-begonia](https://github.com/rubencarneiro/linux-android-begonia) carries a **`halium-11` branch** (branch list verified in [06 §2.2](06-DROIDIAN-POSTMARKETOS.md)) and the Android-11-era kernel line exists in [AgentFabulous/begonia `android-11.0`](https://github.com/AgentFabulous/begonia) ([03 §2.1](03-KERNEL-HISTORY.md)); the vendor side would be the final MIUI 12.5 (Android 11) firmware — availability recorded in [02-FIRMWARE-HISTORY.md](02-FIRMWARE-HISTORY.md).
- **What it buys vs Halium-10:** newer vendor interface, potentially fixes Droidian-style gaps (mic contradiction [04 C4](04-HARDWARE-DRIVERS.md)), but nothing mainline; kernel stays 4.14/4.19 forever. Effort: **medium** (kernel rebase + device tree/vendor swap + retest ~10 items). No verified evidence anyone runs begonia UT on halium-11 today — not found (searched: UBports forum, GitLab porting group pages) [V-weak-negative].

### Option B — UT on a mainline kernel

- **Honest verdict: not viable today.** No modem in mainline MT6785 (no driver upstream, no pmOS calls/SMS/data — [04 §7](04-HARDWARE-DRIVERS.md)); audio needs the machine driver (§1.1); UT telephony stack (ofono/RIL glue) has no mainline-MTK path.
- Who has run UT-style stacks on mainline MTK: **nothing found for handsets** (searched 2026-11-21: "ubuntu touch mainline kernel mediatek", "halium mainline mediatek") [V-weak-negative]. Closest data points, all non-MTK: a Qualcomm experiment — *"Bringing native mainline Ubuntu Touch to the OnePlus 7T Pro"* ([r/UbuntuTouch](https://www.reddit.com/r/UbuntuTouch/comments/1vkj498/bringing_native_mainline_ubuntu_touch_to_the/), claims display/Adreno 640/touch/Wi-Fi working) [V-search, medium]; a promised Braxtech tablet with "UT on mainline" ([UBports forum topic 11905](https://forums.ubports.com/topic/11905/new-braxtech-tablet-or-laptop-with-ut-on-mainline-linux-kernel) — vaporware so far) [V-search, low]; historic note in [Halium docs — krillin (BQ Aquaris E4.5, MT6582)](https://docs.halium.org/en/latest/supplementary/devices/krillin.html): "There is no Mediatek MT-6582 device source tree present inside the mainline kernel yet" [V]. Long-term or never.

### Option C — pmOS-style mainline (best mainline story; ranked driver worklist)

Ordered by impact/effort ratio; every row = config **+ DT/pinctrl + firmware + userspace** (Section 0):

1. **Wi-Fi/BT (mt76 route)** — driver+firmware exist upstream (§1.3); unknowns: actual chip ID, SDIO node/pinctrl (board dtsi currently `no-sdio;`), power sequencing. Precedent for the whole move: pmOS sibling package [linux-postmarketos-mediatek-mt6768](https://pkgs.postmarketos.org/package/v24.06/postmarketos/aarch64/linux-postmarketos-mediatek-mt6768) (6.16.x, "early mainline port" family) [V]. Effort: **medium-high**.
2. **Audio (mt6359 present, mt6785 AFE/machine missing)** — port pattern from upstream `mt6797/` AFE + `mt8183-mt6358` machine driver; hardware facts in [04 §4](04-HARDWARE-DRIVERS.md). Effort: **high** (weeks; needs on-device iteration).
3. **Battery/charging** — charger/PMIC drivers already mainline+enabled (§1.1); missing board glue: battery node, fuel-gauge wiring, userspace upower. Effort: **medium**.
4. **Camera** — kalpakprod already carries `seninf/camsv/cam` in-tree (§1.1); needs begonia sensor nodes (currently none in DTS — [04 §5](04-HARDWARE-DRIVERS.md)) + a [Megapixels](https://gitlab.com/megapixels-org/Megapixels) device config (GTK4 camera app for V4L2 media-request pipelines [V]). Effort: **high**.
5. **Modem** — no upstream path; not realistic (see B).

### Option D — open-driver development plan (what is realistic to hand-port/RE)

| Component | Route | RE needed? |
|---|---|---|
| Touchscreen | solved — pmOS ships `firmware-xiaomi-begonia-touchscreen` + mainline `novatek-nvt-ts-spi` ([06 §1.3](06-DROIDIAN-POSTMARKETOS.md), [04 §2](04-HARDWARE-DRIVERS.md)) | none |
| Charger/USB-PD, NFC, sensors, display/touch/backlight | all mainline already ([04](04-HARDWARE-DRIVERS.md) §1–2, 9, 13, 15–16) | none |
| Wi-Fi/BT firmware | extract from vendor firmware partitions once chip confirmed (mt7663 blobs also in linux-firmware §1.3) | light (extraction, not Ghidra) |
| Audio machine driver | pure kernel work against MT6359 + AFE registers; vendor kernel source ([AgentFabulous/begonia](https://github.com/AgentFabulous/begonia)) is the reference | none (source available) |
| Camera sensors + ISP tuning | vendor sensor drivers + params live in vendor blobs; Ghidra-class RE of MTK camera HAL/params likely | **heavy** |
| Modem | inherited interface via AT/RPC to MediaTek firmware; no community precedent on this SoC | not attempted |

Cross-ref: blob/firmware provenance + RE entry points → `11-BLOBS-FIRMWARE-SOURCES.md` — **not yet present in the repo** (checked 2026-11-21); requirement registered as #27, deferred to assembler.

---

## 3. What the world already has

Other mainline-MTK handset/enablement efforts to learn from (all fetched or search-verified 2026-11-21):

1. [mediatek-mainline org (MT6735-mainline)](https://github.com/mediatek-mainline) — community mainline enablement for an MTK **handset** SoC (Helio P10): kernel repo (pushed 2023-11-02, branches `mt6735*`, `mt6735m-tablet`), u-boot, mtk-utils; GitLab mirror `gitlab.com/mt6735-mainline/linux` per repo description [V]. Its clock drivers got **upstreamed** (`clk-mt6735-*` in mainline MAINTAINERS F: lines §1.2) — the clearest template of "small team → upstream" for this SoC class. Status: dormant since 2023 [V-metadata].
2. [linux-postmarketos-mediatek-mt6768](https://pkgs.nura.eco/package/main/postmarketos/aarch64/linux-postmarketos-mediatek-mt6768) — pmOS mainline fork for the next-gen Helio G-series (6.16.0-r4 on Nura; upstream pmOS package exists too) [V].
3. `mt6795-sony-xperia-m5.dtb` in Linus master — proof an MTK **phone** board lives upstream ([master Makefile](https://raw.githubusercontent.com/torvalds/linux/master/arch/arm64/boot/dts/mediatek/Makefile)) [V].
4. [hexdump0815/linux-mainline-mediatek-mt81xx-kernel](https://github.com/hexdump0815/linux-mainline-mediatek-mt81xx-kernel) — long-running unified mainline kernels for MTK MT81xx Chromebook tablets (oak/kukui/corsola; v6.12.x releases) — mature mainline-MTK bring-up patterns [V-search].
5. [Megapixels](https://gitlab.com/megapixels-org/Megapixels) — the standard Linux-phone camera stack (GTK4, V4L2 media-request API; moved from postmarketOS org — old repo deprecated) [V].
6. [Ubuntu on MediaTek Genio](https://genio.mediatek.com/ubuntu) — Canonical+MTK mainline-kernel Ubuntu for Genio boards: *"Ubuntu can boot on Genio platforms with a mainline kernel, provided that the required hardware drivers are upstreamed"* — vendor cooperation exists upstream-side (SBCs, not handsets) [V-search].

**Upstream engagement points** (verified from mainline [MAINTAINERS](https://raw.githubusercontent.com/torvalds/linux/master/MAINTAINERS), 2026-11-21):

- Mailing list: [linux-mediatek](https://lore.kernel.org/linux-mediatek/) (`linux-mediatek@lists.infradead.org`) — the SoC section lists it plus maintainers **Matthias Brugger** (Google/`matthias.bgg`), **AngeloGioacchino Del Regno** (Collabora), and MediaTek's **Eddie Huang**, **Sean Wang** [V, high for names+addresses as printed].
- `mt76` wireless: section lists Felix Fietkau (`nbd@nbd.name`) et al. — my MAINTAINERS parse was noisy on this section; **medium confidence**, re-check the file before mailing [I].
- ASoC (sound/soc/mediatek): maintained under the ASoC tree (Mark Brown) — parsed section was mangled; **medium confidence**, verify in MAINTAINERS before first post [I].
- pmOS aports workflow: fork [gitlab.postmarketos.org/postmarketOS/pmaports](https://gitlab.postmarketos.org/postmarketOS/pmaports), device lives in `device/testing/`, merge request per device — begonia precedent MR !1909 ([06 §1.7](06-DROIDIAN-POSTMARKETOS.md)).

---

## 4. Recommended route for THIS owner

**Ranked: A now · C in parallel (WiFi first) · B long-term or never.** (Assessment — medium confidence.)

**Option A (keep UT usable, low risk) — first 3 work items:**
1. No action needed to *keep* what works: pin current noble 24.04; file/track mic + RTC against the UT stack (matrix rows in [CONTEXT.md](\_context/CONTEXT.md) cache; issue links in [04](04-HARDWARE-DRIVERS.md)).
2. Evaluate a Halium-11 move only if a concrete gain appears: test-tree = `rubencarneiro/linux-android-begonia` branch `halium-11` ([06 §2.2](06-DROIDIAN-POSTMARKETOS.md)) + Android-11 vendor from [02-FIRMWARE-HISTORY.md](02-FIRMWARE-HISTORY.md); budget a full 10-row feature retest.
3. Keep the UT kernel repo (`kernel-xiaomi-mt6785`, halium-10.0) as the known-good reference ([03 §3](03-KERNEL-HISTORY.md)); don't rebase what already ships stable.

**Option C (mainline, the actual upgrade) — first 3 work items:**
1. **Identify the WLAN/BT combo chip on-device** (Android SDIO VID/PID or `/vendor/firmware/WIFI_RAM_CODE*` names) — unblocks everything in §1.3; log result into [04 §8](04-HARDWARE-DRIVERS.md) (unknown today).
2. **WiFi bring-up spike on pmOS/Dinolek 6.16**: enable `CONFIG_MT7663S` (+ `MT76_SDIO`), add wlan DT node replacing `no-sdio;` on `mmc@11240000`, ship firmware via a pmOS `firmware-xiaomi-begonia` package (pattern: `firmware-xiaomi-begonia-touchscreen`, [06 §1.3](06-DROIDIAN-POSTMARKETOS.md)); expected failure modes per Section 0 (pinctrl, regulators, firmware load).
3. **Audio spike**: draft an MT6785 AFE/machine driver against upstream `mt6359` codec + `mt6797` AFE template; first milestone = `aplay` through `SND_SIMPLE_CARD`-style card registration on a pmOS rootfs. This is the longest pole; consider engaging linux-mediatek early (maintainers §3).

**Option B (UT on mainline) — gate, don't build:** revisit only after C delivers WiFi + audio + (hard) modem; no MTK precedent exists (§2-B).

**Unknowns to carry:** begonia WLAN chip ID (blocks C-1/C-2); whether kalpakprod's camera dirs actually function on mt6785 silicon; MT6785 AFE register map similarity to mt6797 (assumed close from shared-generation design, unverified); Halium-11 begonia port existence (none found).

## Limitations

- Halium "what ships today" was verified via the official UT porting-intro table + GitHub org activity; the Halium project's own docs pages returned 404s to plain fetches (docs.halium.org device pages render via JS/Sphinx paths differ) — treat "Halium 11/12/13 are valid current targets" as **high** (UT docs) and "Halium project healthy" as **high** (repo activity).
- MAINTAINERS section parse was noisy for `mt76` and ASoC maintainers (medium confidence, flagged inline).
- pmOS mt6768 APKBUILD raw fetch hit an Anubis bot-check on gitlab.postmarketos.org; cited from the package index pages instead [V-index].
- No live XDA consulted (blocked per [CONTEXT.md](\_context/CONTEXT.md)); not needed for this file.
- "Linux Edрота" (owner phrase, voice-input artifact) — interpretations logged in the session summary for owner confirmation; deliverable assumes it meant "a generic published Linux option" and covers all candidates (pmOS §2-C, generic mainline, EDK2/UEFI via Mu-Silicium per [03 §5](03-KERNEL-HISTORY.md) — Linux Boot ❔ in the only UEFI experiment).

## Sources (appended to sources.jsonl)

Defconfigs, Makefiles, master dts/mt76 Kconfig/MAINTAINERS, UT porting intro, Halium org API, mediatek-mainline org API, pmOS mt6768 package pages, Megapixels, wireless.docs.kernel.org, Arch linux-firmware-mediatek file list, Debian bug 1146149, UBports forum 11484/11905, r/UbuntuTouch OnePlus-7T-Pro thread, halium.org, Halium docs krillin page — all fetched 2026-11-21; per-record URLs in `sources.jsonl`.
