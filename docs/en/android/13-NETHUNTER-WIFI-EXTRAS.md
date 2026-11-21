# 13 — NetHunter, Wi-Fi monitor mode & useful hacks/portables (begonia, 2026-11-21)

Dimension: security-research extras (REQUIREMENTS [#31](https://github.com/0-danielviktorovich-0/begonia-research/blob/main/_context/REQUIREMENTS.md) NetHunter/monitor-mode, [#32](https://github.com/0-danielviktorovich-0/begonia-research/blob/main/_context/REQUIREMENTS.md) hacks & portables) + merged [W13-ADDENDUM-USB-HID.md](https://github.com/0-danielviktorovich-0/begonia-research/blob/main/_context/W13-ADDENDUM-USB-HID.md) (REQUIREMENTS #33).
Research-only: nothing was flashed; no untrusted scripts executed. Conventions: **[V]** = verified directly against the cited source, **[I]** = inferred (reasoning stated), **[NF]** = not found (search list given). Confidence: high / medium / low. Wi-Fi chip & driver background: [04-HARDWARE-DRIVERS.md](https://github.com/0-danielviktorovich-0/begonia-research/blob/main/04-HARDWARE-DRIVERS.md) §8 (chip **unknown** there — §1 below is the W13 attempt to pin it); kernel line: [03-KERNEL-HISTORY.md](https://github.com/0-danielviktorovich-0/begonia-research/blob/main/03-KERNEL-HISTORY.md).

---

## 1. Wi-Fi chip & monitor mode

### 1.1 Chip identification — verdict: MT7663-family suspected, **not pinned to a part number**

Every reachable primary source names only the *driver family*, never the chip ID:

| Evidence | What it actually says | Verdict for chip ID |
|---|---|---|
| [AgentFabulous/begonia `begonia_user_defconfig`](https://github.com/AgentFabulous/begonia/blob/android-11.0/arch/arm64/configs/begonia_user_defconfig) (android-11.0, stock-derived 4.14) | `CONFIG_MTK_COMBO_WIFI=y`, `CONFIG_WLAN_DRV_BUILD_IN=y`, `CONFIG_MTK_DHCPV6C_WIFI=y` — no `*CHIP*` line [V] | Vendor **MTK combo (gen4m)** driver, built-in; chip not pinned in config |
| [MiCode/Xiaomi_Kernel_OpenSource `begonia-r-oss` defconfig](https://github.com/MiCode/Xiaomi_Kernel_OpenSource/blob/begonia-r-oss/arch/arm64/configs/begonia_user_defconfig) | same `CONFIG_MTK_COMBO_WIFI=y` lines, no chip ID [V] | same |
| [Anonym3310/AkameKernel-begonia `Q-OSS-SLMK` defconfig](https://github.com/Anonym3310/AkameKernel-begonia/blob/Q-OSS-SLMK/arch/arm64/configs/begonia_user_defconfig) | the only chip-menu line is `# CONFIG_MTK_COMBO_CHIP_MT7668 is not set`; **no** `CONFIG_MTK_COMBO_CHIP_MT7663=y` line [V] | Menu offers both; config alone does not decide |
| [connectivity `Kconfig`](https://github.com/AgentFabulous/begonia/blob/android-11.0/drivers/misc/mediatek/connectivity/Kconfig) | menu `Select Chip` with bools `MTK_COMBO_CHIP_MT7668`, `MTK_COMBO_CHIP_MT7663`, `MT6630`, `MT6632`, `CONSYS_6xxx`… each help text only says "this config is used to decided combo chip version in current platform is …" [V] | Chip selectable per platform; stock configs don't set it |
| [gen4m `Makefile`](https://github.com/AgentFabulous/begonia/blob/android-11.0/drivers/misc/mediatek/connectivity/wlan/core/gen4m/Makefile) | `WLAN_CHIP_LIST:=-UMT6620 -UMT6628 -UMT5931 -UMT6630 -UMT6632 -UMT7663 -UCONNAC -UCONNAC2X2 -UUT_TEST_MODE -UMT7915 -USOC3_0 -UMT7961`; if `MTK_COMBO_CHIP` unset → **default `MT6632`**; per-chip `-DMT7668` compile switches [V] | Build supports the whole list; runtime/detection decides on device |
| [Mainline DTS `mt6785-xiaomi-begonia-common.dtsi`](https://github.com/Dinolek/mt6785-mainline/blob/7.1/arch/arm64/boot/dts/mediatek/mt6785-xiaomi-begonia-common.dtsi) (Dinolek, branch `7.1`) | **no Wi-Fi/SDIO-combo node at all** (`no-sdio` appears only in `&mmc1` = the card-detect SD slot) [V] | mainline currently has nothing to bind a WLAN driver to |
| [Nura wiki SoC page "MediaTek Helio G90T/G95 (MT6785)"](https://wiki.nura.eco/wiki/MediaTek_Helio_G90T/G95_(MT6785)) | Wi-Fi/Bluetooth rows literally "Untested", no part number [V] | no help |
| [MediaTek Helio G90 series page](https://i.mediatek.com/g90series) | "Dual Wi-Fi Connections – Connects to two bands simultaneously" (DBDC marketing); no chip model [V] | 2x2 802.11ac class, unnamed |
| 4PDA caches (both threads, page-1 + rec2 extracts), GitHub issues (`AgentFabulous/begonia`, `Dinolek/mt6785-mainline`, `kalpakprod/mt6785-linux`) | zero mentions of 7663/7668 [V — absence] | no help |

**Bottom line [I, medium]**: begonia's Wi-Fi/BT rides the MTK **gen4m combo driver** (`CONFIG_MTK_COMBO_WIFI`), whose supported-chip list includes **MT7663, CONNAC, CONNAC2X2, MT7915, MT7961** — the MT7663 family suspicion from REQUIREMENTS #31 remains *consistent with all evidence but is not proven*; the gen4m Makefile default (MT6632) and the MT7668-only savedefconfig line show the config **cannot** be used to claim the part number. On-device `ls /vendor/firmware/WIFI_RAM_CODE*` / SDIO VID probing would settle it — **out of scope (no device access)**.

### 1.2 Mainline `mt76` coverage of that chip family (verified)

- [mt76 `mt7615/Kconfig` (torvalds/master)](https://github.com/torvalds/linux/blob/master/drivers/net/wireless/mediatek/mt76/mt7615/Kconfig): `MT7615E` = "MediaTek MT7615E and **MT7663E (PCIe)** support"; separate `MT7663U` = "**MediaTek MT7663U (USB) support**" and `MT7663S` = "**MediaTek MT7663S (SDIO) support**" (`select MT76_SDIO`, depends on MMC) [V, high].
- Kernel version: **Linux 5.9** introduced MT7663S — [kernelnewbies Linux_5.9](https://kernelnewbies.org/Linux_5.9) ("Introduce support for mt7663s devices") [V]; [lkddb CONFIG_MT7663S](https://cateee.net/lkddb/web-lkddb/MT7663S.html) lists "found in Linux kernels: 5.9–…, modules built: mt7663s" [V]. (Contradiction note: [kernelconfig.io](https://www.kernelconfig.io/CONFIG_MT7663S) says "since 5.1" — outvoted 2:1 by the two sources above; 5.9 taken.)
- Monitor mode: mt76 is a **mac80211** driver (Kconfig `depends on MAC80211`) → monitor interface support comes with the stack; community monitor-mode testing for the family is tracked in [morrownr/mt76 issue #18](https://github.com/morrownr/mt76/issues/18) [V, high] (about USB adapters, not phones).
- Firmware: `mt7663pr2hw.bin` **verified present** in [linux-firmware](https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/mt7663pr2hw.bin) (HTTP 200 via plain endpoint, 2026-11-21) [V, high].

### 1.3 Monitor mode on the internal Wi-Fi (Android) — **no public patch found**

Kali's own docs state the rule this project must live by: *"External wireless cards are necessary because Android devices do not support monitor mode on most devices apart from some Qualcomm chips used in modern Snapdragon SOC… only a specially modified version of Nexus 5 supports monitor mode for NetHunter."* — [Wireless Cards and NetHunter, kali.org](https://www.kali.org/docs/nethunter/wireless-cards/) [V, high].

For begonia specifically: **not found (searched:** web queries `MT7663 monitor mode patch github`, `mt7663 monitor mode injection github patch`, `begonia Redmi Note 8 Pro wifi monitor mode`, `nethunter mediatek mt67xx monitor mode kernel`, `MT7663 monitor mode patch`-family, GitHub issue searches `repo:AgentFabulous/begonia monitor mode` (0 hits), `repo:Dinolek/mt6785-mainline wifi` (0 hits), 4PDA cache grep for "monitor|7663"; grep.app rate-limited 429)**.** The only MTK-adjacent public repos are [kimocoder/qualcomm_android_monitor_mode](https://github.com/kimocoder/qualcomm_android_monitor_mode) (Qualcomm QCACLD only — not applicable to MT6785) and [vanhoefm/wifi-injection](https://github.com/vanhoefm/wifi-injection) (generic Linux-driver injection research). **The patches the owner once received privately could not be rediscovered publicly — stated explicitly.**

**The community's working path = external USB dongle over OTG** (OTG verified working on all OSes in [04 §15](https://github.com/0-danielviktorovich-0/begonia-research/blob/main/04-HARDWARE-DRIVERS.md)):

| Artifact | What it gives begonia | Source |
|---|---|---|
| [4PDA post "Модули к адаптерам на базе чипсетов Atheros: AR9271, AR7010" (p=105942017)](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=105942017) | Prebuilt **ath9k_htc** modules + firmware, "скомпилированны из исходников ядра Pixel Experience A11 Non-CFW… Версия ядра: 4.14.141-g1448309"; install: `ath9k_htc/` → `/system/etc/firmware/`, `*.ko` → `/vendor/lib/modules/`, insmod `ath9k_hw`→`ath9k_common`→`ath9k_htc`; "интерфейс адаптера скорее всего будет именоваться wlan2, при режиме мониторинга - wlan2mon"; ready script `ulan_ath9k_htc.sh` (enable adapter → switch to monitor → dump config), run from Termux via OTG [V-cache, high] | **begonia-specific, working monitor+injection recipe** |
| [4PDA "Инструкция по линковке внешних модулей к ядру" (p=105817890)](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=105817890) | How to link external modules into begonia kernels generally [V-cache/idx, high] | enables any dongle driver port |
| [AkameKernel additional-drivers-pack](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=97901817) | "Поддержка rtl8188eus rtl8188fu rtl8192eu rtl8812au rtl8814au (в additional-drivers-pack)" — the classic NetHunter injection adapters [V-cache, high] | same goal, Realtek branch |
| [Kali wireless-cards doc](https://www.kali.org/docs/nethunter/wireless-cards/) | Chipsets "supported by default in most, if not all, NetHunter kernels": Atheros ATH9K_HTC (**AR9271, AR7010**), ATH10K; Ralink RT73/RT2800USB/RT3070; Realtek RTL8188EUS…; MediaTek MT7601U/MT7610U/MT7612U; confirmed device: TP-Link TL-WN722N **v1** ("v2 & v3 have unsupported chipsets") [V, high] | shopping list |

### 1.4 pmOS / mainline angle — enabling `mt76` (ANALYSIS, not verified)

Verified inputs: pmOS 6.16 ships **no MediaTek WLAN driver** ([04 §8](https://github.com/0-danielviktorovich-0/begonia-research/blob/main/04-HARDWARE-DRIVERS.md), verified against the built 6.16.4 config) and my raw fetch of [`config-postmarketos-mediatek-mt6785.aarch64` on pmaports `main`](https://gitlab.nura.eco/nura/pmaports/-/raw/main/device/testing/linux-postmarketos-mediatek-mt6785/config-postmarketos-mediatek-mt6785.aarch64) returned only an 81-line fragment with **no** `MT76*`/`USB_ETH`/`CONFIGFS`/`RNDIS` entries [V, medium — fragment caveat].

**Analysis [I, low-medium]:** flipping on `CONFIG_MT7615E`/`CONFIG_MT7663S` (+ `MT76_CONNAC_LIB`, `MT7663_USB_SDIO_COMMON`, firmware `mt7663pr2hw.bin`) in the pmOS kernel package would *not by itself* give Wi-Fi, because (a) the mainline DTS has **no WLAN node** ([1.1](#11-chip-identification--verdict-mt7663-family-suspected-not-pinned-to-a-part-number)) — an SDIO/USB child node, regulators and (if the chip is the SoC-internal connsys rather than a discrete MT7663) possibly a different glue layer are missing; (b) if the silicon is `CONNAC2X2`-generation rather than discrete MT7663, mainline mt76 may not support it at all. If it ever binds, monitor mode would come free with mac80211/mt76 — that part is driver-true but **unproven for this board**. Net: "enable mt76 in the defconfig → Wi-Fi AND monitor" is **plausible-but-unverified**; nobody has published even a proof-of-branch (searched: Dinolek/mt6785-mainline issues+commits, kalpakprod/mt6785-linux — 0 Wi-Fi hits [V — absence]).

---

## 2. Kali NetHunter on begonia

### 2.1 Official support: **none**

[Kali NetHunter device-kernels index](https://nethunter.kali.org/device-kernels.html) (fetched 2026-11-21): the Xiaomi block lists *Redmi Note 8 (ginkgo)*, Mi 3/4, Mi 9 family, MiPad 1, Poco X3 NFC, Pocophone F1… — **`begonia` / "Redmi Note 8 Pro" appear nowhere in the page** (string check on fetched HTML: `begonia`→False, `note 8 pro`→False) [V, high]. Same for the [community kernel index](https://nethunter.kali.org/kernels.html) (no begonia row) [V, high]. Note the irony: official support exists for the *Snapdragon* sibling ginkgo, and a YouTube title even claims "[Nethunter Redmi note 8 ginko — Monitor mode working, no external adapter](https://www.youtube.com/watch?v=jWC8Bo-TWDs)" [V-title only, medium] — that is QCACLD territory, not reproducible on MT6785.

### 2.2 Community support: **AkameKernel (NetHunter)** — the one begonia NetHunter kernel

- Repo: [Anonym3310/AkameKernel-begonia](https://github.com/Anonym3310/AkameKernel-begonia) — description "NetHunter Kernel For Redmi Note 8 Pro [CFW] [NONCFW] [AOSP] [MIUI] [Q-OSS]", default branch `Q-OSS-SLMK` (+ `CFW`), **last push 2023-03-02** [V, high]. Listed in the CFW шапка under "**Ядра с поддержкой функционала NetHunter**" → [4PDA post p=97901817](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=97901817) [V-cache, high].
- Post content (verbatim features): "Включен весь возможный функционал для NetHunter" (all possible NetHunter functionality enabled); "Фиксация TTL" (TTL fix); **F2FS**; kernel headers; "AutoInsmodModules"; "Поддержка встроенной bluetooth карты (hci0)" (internal BT exposed as hci0 — NetHunter Bluetooth stack); chroot note `apt-get install firmware-ralink firmware-atheros firmware-realtek firmware-zd1211 firmware-ath9k-htc …`; external RTL8188EUS/FU, RTL8192EU, RTL8812AU/8814AU drivers in `additional-drivers-pack.zip` [V-cache, high].
- Defconfig cross-check [V, high]: `Q-OSS-SLMK` enables `CONFIG_USB_CONFIGFS_F_HID=y`, `CONFIG_USB_F_HID=y`, `USB_F_RNDIS`, `CONFIG_USB_CONFIGFS_F_FS` (functionfs), `F_ACC`, `F_AUDIO_SRC`, `F_MIDI`, `HIDRAW`, `UHID`; `CFW` defconfig (compact) keeps `MTK_COMBO_WIFI=y` + `CONFIGFS {SERIAL,ACM,RNDIS,MASS_STORAGE,F_HID}=y`.
- **Staleness**: targets MIUI-12.0/A10-era (Q-OSS) bases; current begonia ROMs run A16/17 on 4.19 kernels ([03 §2.4](https://github.com/0-danielviktorovich-0/begonia-research/blob/main/03-KERNEL-HISTORY.md)) → Akame is a historical/MIUI-path artifact, not a 2026 daily-driver kernel. Confidence high.

### 2.3 Install paths that apply today (from Kali docs, verified text)

Per [Installing NetHunter, kali.org](https://www.kali.org/docs/nethunter/installing-nethunter/): unsupported devices "can still use **Kali NetHunter Lite on any rooted device** with limited hardware features"; generic image "**Generic ARM64 Full installer: `kali-nethunter-20YY.X-generic-arm64-kalifs-full.zip`**"; "The preferred **custom recovery** for NetHunter is **TWRP**"; "The preferred software to **root** the device for NetHunter is **Magisk**"; the NetHunter image installs either via recovery (TWRP zip) or as a **Magisk module** [V, high]. Begonia mapping [I, medium-high]: TWRP is abundant ([10-GUIDE-INDEX §2](https://github.com/0-danielviktorovich-0/begonia-research/blob/main/10-GUIDE-INDEX.md): Unified TWRP 3.7.1 by wuxinG90 current), root paths Magisk/KernelSU/APatch/SukiSU all indexed there, so **NetHunter Lite via Magisk module works today; full NetHunter adds Akame-era kernel features (HID/BT-hci0/dongle drivers)**. Feature-by-feature kernel requirements: HID → already in AFB-based kernels (§3.4); Wi-Fi injection → external adapter only (§1.3); BT hci0 → Akame or equivalent patch [V/I as marked].



### 2.4 Community hub: the RU NetHunter thread on 4PDA (supplement, not replacement)

- [Kali NetHunter на ваши смартфоны | Вся информация по Nethunter — 4PDA t=952937](https://4pda.to/forum/index.php?showtopic=952937), first post by `l_cat_l` 2019-05-19 ([p=85416127](https://4pda.to/forum/index.php?showtopic=952937&view=findpost&p=85416127)), **511 pages, still active in Nov 2026** (recent posts discuss custom commands in the NetHunter manager) [V-cache 2026-11-21T13:10Z, high].
- What the шапка adds beyond kali.org: a curated RU link index — NetHunter builds (incl. **`nethunter-generic-arm64-kalifs-full/minimal-rolling`** mirrors of build.nethunter.com nightlies), install requirements, and RU-language support Q&A across 10k+ posts [V-cache, high]. For begonia the operative item is the **generic ARM64 installer** = the same "NetHunter Lite on any rooted device" path as [§2.3](#23-install-paths-that-apply-today-from-kali-docs-verified-text) — the thread is the RU walk-through of that path.
- Freshness caution: several шапка download links point to **2017-era rolling builds**; the current official artifacts remain kali.org / [images.kali.org](https://images.kali.org/nethunter/) — per REQUIREMENTS [#31](https://github.com/0-danielviktorovich-0/begonia-research/blob/main/_context/REQUIREMENTS.md) official sources stay primary, this thread is the community supplement (RU instructions, troubleshooting depth).
- Two verbatim rules from the шапка that *confirm* this file's analysis from the RU community side [V-cache, high]:
  - «**NetHunter не сможет работать с вашим встроенным Wi-Fi адаптером!**» — matches §1.3 (internal monitor mode: no public patch; external dongle is the working path);
  - «**Без ядра не будут работать некоторые функции NetHunter'а, но весь Kali Linux будет присутствовать и функционировать!**» — matches §2.3 (NetHunter Lite via Magisk module works kernel-less; HID/BT-hci0/dongle features need kernel support).
- Permalink policy: deep-dive answers should be cited as `showtopic=952937&view=findpost&p=<pid>` permalinks once a specific post is identified (page-377 sample: [custom NetHunter-manager commands Q&A, Nov 2026](https://4pda.to/forum/index.php?showtopic=952937&st=7520)) [V-cache, medium].

---

## 3. Useful hacks & portables — the begonia developer toolbox

### 3.1 Root / kernel-patching harnesses (reusable today)

| Harness | State | Source |
|---|---|---|
| Magisk v31.0 profile thread | active, 2026-09-05; also links KernelSU t=1067995, APatch t=1082492, SukiSU t=1108076 | [4PDA t=774072 post #1](https://4pda.to/forum/index.php?showtopic=774072&view=findpost&p=112985156) + [10-GUIDE-INDEX §2](https://github.com/0-danielviktorovich-0/begonia-research/blob/main/10-GUIDE-INDEX.md) |
| **KernelSU-Next + SUSFS** CI builder | [cvnertnc/Begonia-Kernel-Builder](https://github.com/cvnertnc/Begonia-Kernel-Builder) — "Automatically follow daily KernelSU-Next updates… built with KernelSU-Next and SUSFS"; **self-archived 2026-09-16** ("I'm archiving this project because I don't have much time anymore"); fork of [PhamtomK12/Android-Kernel-Builder](https://github.com/PhamtomK12/Android-Kernel-Builder) [V, high] → **reusable TODAY as a fork-and-run template** for KSU-Next/SUSFS begonia zips | [03 §2.3](https://github.com/0-danielviktorovich-0/begonia-research/blob/main/03-KERNEL-HISTORY.md) |
| Nova-Kernels | [Nova-Kernels/kernel_xiaomi_mt6785](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785) — active, 4.14.356, push 2026-10-03; commits "Enable XDP_SOCKETS", "zram: Set LZ4 as default" [V, high] | [03 §2.3] |
| Power kernel base | [Saikrishna1504/kernel_xiaomi_mt6785](https://github.com/Saikrishna1504/kernel_xiaomi_mt6785) (branches `main`, `kaeru`) [V, high] | [kernel-matrix.csv] |
| Suzaku Kernel V2 | 4PDA release 2026-08-07 by @WuxinG90; claims KernelSU 35053 + SUS-FS 2.2.0, AOSP Clang 21, "based on Power kernel"; **no public repo found** [V-quotes/NF-repo, medium]. Used by [EvolutionX 16.0](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=144852836) and Project Infinity X 3.12 (p=144878394) | [03 §2.3] |

### 3.2 Kernel zips with device-specific extras (historical→usable per base)

[Coconut Kernel](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=111452029) (MIUI 12.5, A11/12) · [PoWeR Kernel](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=137328276) · [UnicornHorn](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=106215865) · [QuantumKiller/Neutrino](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=99720504) · [Rave 1.8 (discontinued)](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=103603411) · [modified A9/MIUI-11 kernel](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=101609237) — all [V-cache, high] via the CFW шапка. **Hardware warning to preserve** (шапка, A10 non-CFW kernels section): "Если у вас фронтальная камера новой ревизии… вы можете лишиться работоспособности переднего модуля камеры и Google Camera" — newer-revision front camera units lose front cam + GCam on some custom kernels [V-cache, high].

### 3.3 External-Wi-Fi / injection adapter support — see §1.3 table (ath9k_htc AR9271/AR7010 recipe + RTL pack + module-linking guide).

### 3.4 USB gadget / HID attack surface (W13-ADDENDUM merged)

| Kernel | Configfs gadget options | NetHunter-HID meaning |
|---|---|---|
| [AFB `begonia_user_defconfig`](https://github.com/AgentFabulous/begonia/blob/android-11.0/arch/arm64/configs/begonia_user_defconfig) (addendum probe) | `USB_CONFIGFS {SERIAL, ACM, RNDIS, MASS_STORAGE, F_HID}=y` [V] | **HID keyboard attacks work without a kernel rebuild** on any AFB-based ROM kernel; USB-ethernet gadget (ECM/NCM) **not** enabled |
| [Akame Q-OSS-SLMK](https://github.com/Anonym3310/AkameKernel-begonia/blob/Q-OSS-SLMK/arch/arm64/configs/begonia_user_defconfig) | adds `F_FS` (functionfs), `F_ACC`, `F_AUDIO_SRC`, `F_MIDI`, `USB_F_RNDIS`; `NCM`/`ECM` = not set [V] | full NetHunter HID + DuckHunter-class functionfs paths |
| LOS kernel `lineage-24.0 begonia_defconfig` | addendum measured it at **29 chars** — a stub [V] | real LOS config lives under another name — unresolved lead (§4) |
| pmOS 6.16 config | no CONFIGFS/gadget functions in fetched fragment [V-fragment] | USB-HID on pmOS would need a kernel rebuild |

USB role switching/OTG dual-role is verified working ([04 §15](https://github.com/0-danielviktorovich-0/begonia-research/blob/main/04-HARDWARE-DRIVERS.md)), which is the host-mode prerequisite for both dongles (§1.3) and HID-target use. P4wnP1-style functionfs toolkit: nothing begonia-specific found (searched: `nethunter mediatek mt67xx`, `begonia HID gadget` via cache greps) [NF].

### 3.5 pmOS USB-Ethernet gadget (REQUIREMENTS #32 example)

Origin: wiki user **Halhadus** (begonia-linux org member): *"running pmOS, using as server, you can enable kernel configs to use USB Ethernet, Phosh working good"* — [Nura wiki device page](https://wiki.nura.eco/wiki/Xiaomi_Redmi_Note_8_Pro_(xiaomi-begonia)) "Users owning this device", cached 2026-11-21 [V-quote, medium]; contrast user **Letstry pmos**: "Haven´t suceeded in having Internet via USB" [V-quote]. Where the config lives: the kernel package `device/testing/linux-postmarketos-mediatek-mt6785` in [nura/pmaports](https://gitlab.nura.eco/nura/pmaports) — its `config-postmarketos-mediatek-mt6785.aarch64` currently has no `USB_ETH`/`USB_F_ECM`/`RNDIS`/`CONFIGFS` entries in my raw fetch [V-fragment] → enabling = edit that config (`CONFIG_USB_CONFIGFS=y` + `USB_F_ECM`/`USB_ETH_RNDIS` or `USB_ETH=y` with gadget-ethernet) and rebuild the kernel package. **ANALYSIS [I, medium]** — no published patch/build exists (searched: pmaports MRs/issues within tool budget; wiki notes only).

### 3.6 Magisk module ecosystem & misc mods

- Generic catalog: [4PDA "Каталог модулей для Magisk" t=915158](https://4pda.to/forum/index.php?showtopic=915158) [V-search, high] — the browse point for debloat/audio/perf modules.
- Audio: CFW шапка links "**ViPER4Android, не требующий root-прав и отключения SELinux**" (no-root, no-SELinux-off ViPER4Android) [V-cache quote; href truncated in extract → permalink pending in [10-GUIDE-INDEX](https://github.com/0-danielviktorovich-0/begonia-research/blob/main/10-GUIDE-INDEX.md) follow-up].
- Begonia-specific debloat list: **not found (searched:** `begonia magisk module debloat thermal audio 4pda`, cache greps for `Деблоат|debloat` — zero device-specific hits)**.**
- phh/GSI-era tweaks: covered by [02-FIRMWARE-HISTORY.md §2 (GSI era)](https://github.com/0-danielviktorovich-0/begonia-research/blob/main/02-FIRMWARE-HISTORY.md) — single-source rule: not re-researched here.

### 3.7 Sibling MT6785-family devices (portables)

- **rosemary** = Redmi Note 10S, Helio G95 (MT6785 family) — active trees: [Yukina-Supremacy/android_device_xiaomi_rosemary](https://github.com/Yukina-Supremacy/android_device_xiaomi_rosemary), [RedmiNote10S GitHub org](https://github.com/RedmiNote10S) [V-search, medium]; even XNU/iOS kernel experiments ran on rosemary ([r/hackios post](https://www.reddit.com/r/hackios/comments/1xc8yy7/ios_167_booted_xnu_kernel_on_redmi_note_10s/), 2026) [V-title, low] → MT6785-family kernel work is alive there; **no concrete begonia-portable optimization patch series located** (searched: `rosemary Redmi Note 10S mt6785 kernel optimization patch github` — trees only).
- **merlin** (Redmi Note 9) / **joyeuse** (Note 9 Pro): NetHunter kernels exist for siblings — [XDA "Kali Nethunter Kernel for Redmi Note 9" t=4643492](https://xdaforums.com/t/kali-nethunter-kernel-for-redmi-note-9.4643492/) (live XDA blocked for our tools; title verified via search), [dhiimr/nethunter_note9pro](https://github.com/dhiimr/nethunter_note9pro) [V-search, medium].
- **galahad**: not found (searched: none run specifically — flagged as open lead, see §4) [NF-honest].

---

## 4. What to search next / not found (ranked)

1. **Internal-Wi-Fi monitor patch for gen4m/MT7663-class on Android** — NF (searched: `MT7663 monitor mode patch github`; `mt7663 monitor mode injection github patch`; `nethunter mediatek mt67xx monitor mode kernel`; GitHub issues `AgentFabulous/begonia monitor mode`, `Dinolek/mt6785-mainline wifi`; 4PDA cache grep `monitor|7663`; grep.app rate-limited/429 — retry off-peak is the top lead).
2. **Exact combo part number** — NF; settle on-device (`ls /vendor/firmware/WIFI_RAM_CODE*`, `cat /sys/…/sdio/…/vendor,device`) or inside the gen4m detection tables (`drivers/misc/mediatek/connectivity/common/…` runtime chip-ID code).
3. **`mt7663 pca monitor`** (exact query from the mission) — not run verbatim; nearest equivalents (queries in #1) returned nothing; retry as-is.
4. **LOS `lineage-24.0` real defconfig** — addendum's 29-char `begonia_defconfig` is a stub; find the actual config filename in [LineageOS/android_kernel_xiaomi_mt6785](https://github.com/LineageOS/android_kernel_xiaomi_mt6785).
5. **Suzaku V2 public repo** — NF (searched: `suzaku kernel begonia github` family per [03]; only the 4PDA post exists).
6. **galahad as MT6785 sibling** — unsearched (budget); run `galahad mt6785 kernel` next.
7. **Begonia debloat list / thermal-profile mod** — NF (searched: `begonia magisk module debloat thermal audio 4pda`; only generic catalog t=915158).
8. **HYDRA kernel (viperkernels.com/devices/begonia, XDA t=4523225)** — site rendered empty (JS-only extract), live XDA blocked; features unknown → candidate monitor/HID claims unverified.
9. **ViPER4Android no-root permalink** — href truncated in cache extract; recover from `archive/rec2-cfw-*` HTML or re-extract with larger budget.

## 5. Limitations

- Live XDA blocked (bunny.net) per [CONTEXT.md](https://github.com/0-danielviktorovich-0/begonia-research/blob/main/_context/CONTEXT.md); only Wayback/search-title level used. 4PDA fetched via extractor (2 full posts re-fetched 2026-11-21).
- pmaports config raw file returned an 81-line fragment — possibly not the full built config; [04 §8](https://github.com/0-danielviktorovich-0/begonia-research/blob/main/04-HARDWARE-DRIVERS.md)'s verification stands as authoritative for "no MT76".
- grep.app code search unusable (HTTP 429); GitHub code search needs auth → chip-part-number search inside vendor trees incomplete.
- No device access: every on-device check (firmware file names, SDIO IDs, `iw list` monitor caps) is future work.
- Offline `archive/` snapshots for the pages newly fetched here are an orchestrator final-pass task (extracts live in `_cache/`).

## 6. Sources (full records in `sources.jsonl`)

Key URLs are inline above; primary new fetches 2026-11-21: AkameKernel repo+2 defconfigs, AFB/MiCode defconfigs, connectivity Kconfig, gen4m Makefile, torvalds mt7615 Kconfig, linux-firmware `mt7663pr2hw.bin`, pmaports config fragment, [nethunter.kali.org/device-kernels.html](https://nethunter.kali.org/device-kernels.html), [nethunter.kali.org/kernels.html](https://nethunter.kali.org/kernels.html), [kali wireless-cards](https://www.kali.org/docs/nethunter/wireless-cards/), [kali installing-nethunter](https://www.kali.org/docs/nethunter/installing-nethunter/), [lkddb MT7663S](https://cateee.net/lkddb/web-lkddb/MT7663S.html), [kernelnewbies Linux 5.9](https://kernelnewbies.org/Linux_5.9), 4PDA posts p=97901817 / p=105942017, [Nura SoC page](https://wiki.nura.eco/wiki/MediaTek_Helio_G90T/G95_(MT6785)), [MediaTek G90 page](https://i.mediatek.com/g90series).

## 1.5 Follow-up 2026-11-22 (owner-directed re-search; orchestrator)

Fresh web_search pass found two NEW leads beyond §1.3's NF verdict:
1. **XDA t=3591182** — "[Mediatek Wifi/BT/FM/GPS combo chips, hidden capabilities [MT6620/MT6628/MT6630]](https://xdaforums.com/t/mediatek-wifi-bt-fm-gps-combo-chips-hidden-capabilities-mt6620-mt6628-mt6630.3591182/)":
   monitor mode + FM TX unlocked by patches on the OLD MTK combo driver lineage (gen4m's ancestor).
   Action: capture the thread via the Brave lane (XDA is bunny-blocked for extractors) and check
   whether the unlock technique (debug/OID command path) survived into gen4m.
2. **gen4m source has RX radiotap plumbing** (verified in clones):
   `nic_rx.c` carries `MONITOR_RADIOTAP` fill code (nicRxFillRadiotapMCS/VHT), BUT
   `os/linux/gl_cfg80211.c` registers only STATION/ADHOC/AP — **NL80211_IFTYPE_MONITOR is not
   registered**. Dev target for our unified kernel: register IFTYPE_MONITOR + wire it to the
   internal capture path. Precedent for the vendor-driver approach:
   [kimocoder/qualcomm_android_monitor_mode](https://github.com/kimocoder/qualcomm_android_monitor_mode)
   (QCACLD: monitor flips on via `con_mode=4` sysfs, no patch, on modern kernels).
Both leads are registered as the unified-kernel dev track (skill `unified-kernel-build`).

## 1.6 RESEARCH WAVE RESULT 2026-11-22 (W20 source dive + W21 community sweep) — verdict FLIPPED

**Internal-WiFi monitor on begonia: FEASIBLE.** Two concrete paths, both rooted in verified facts:

### 1.6.1 Chip identity CORRECTED (supersedes §1.1 "MT7663-family suspected")
begonia's WiFi/BT = **SoC-internal connsys, NOT a discrete MT7663S**: build exports `MTK_COMBO_CHIP=CONNAC`,
`WLAN_CHIP_ID=6785`, `CONFIG_MTK_COMBO_WIFI_HIF=axi` (connectivity/Makefile:50-51, both clones) [V];
dts: `wifi@18000000` + `consys@18002000 ("mediatek,mt6785-consys")`, no SDIO child, no chip part number [V].
Implication: the mainline-mt76 route (§1.2, mt7663s) targets a DIFFERENT (discrete-SDIO) context —
still relevant for the far pmOS phase, but not the phone's connsys.

### 1.6.2 The capability already ships in gen4m [V — file:line evidence in W20-OUT]
`CFG_SUPPORT_SNIFFER=1` compile-on (config.h:1087 saikrishna / :1163 los); full RX monitor pipeline
(nicRxProcessMonitorPacket → radiotap%d netdev, ARPHRD_IEEE80211_RADIOTAP); armed by private command
**`"MONITOR <en> <chan> <width> <sco>"`** (gl_wext_priv.c:2869/9962, procfs `/proc/wlan/driver` too)
→ **FW command 0xFC CMD_ID_SET_MONITOR** (wsys_cmd_handler_fw.h:358). Kali's "unsupported" applies to
the missing NL80211 surface, not the capability.

### 1.6.3 Two implementation paths
- **Path A (SMALL, ~3 patches)**: register `BIT(NL80211_IFTYPE_MONITOR)` (gl_init.c:2411), add MONITOR
  branch in mtk_cfg80211_change_iface (gl_cfg80211.c:152-156 — currently -EINVAL), implement
  .set_monitor_channel mapping onto CMD_MONITOR_SET_INFO fields. Sketch: W20-OUT-GEN4M-FEASIBILITY.md Q3/Q5.
  Risk: FW-side 0xFC support unverifiable from source — test on device first via `/proc/wlan/driver`.
- **Path B (proven recipe, port)**: [TheThunderstormX/mt6789-wifi-monitor](https://github.com/TheThunderstormX/mt6789-wifi-monitor)
  (connac2, MT6789 emerald; verified on-device: 2.4 GHz capture 162 frames/6 APs/8 s) — kprobe on
  nicRxProcessDataPacket/MgmtPacket + RFCR register write via priv_driver_set_mcr → /proc/monx4 → radiotap pcap.
  All target symbols exist verbatim in begonia's gen4m [V]; RFCR address is connac2-empirical → relocate
  for begonia CONNAC (repo's REGISTERS.md documents the snapshot-differencing method) [I, medium].
- Both paths: **RX capture only** (radiotap0 has no ndo_start_xmit; monx is capture-only; WPA2 stays
  encrypted). Injection → external OTG adapters (§1.3 table) or future TX work.

### 1.6.4 Ledger updates (§4)
- HYDRA kernel: CLOSED [V] — browser-rendered viperkernels.com/devices/begonia: USB-HID/AIRSPY/HACKRF +
  dongle chipsets only, no internal monitor (A12/13, 2023-06 last build).
- `mt7663 pca monitor`: re-run → 0 hits [NF stays].
- Kali MTK row: still USB dongles only; new MTK NetHunter community kernel (Realme C15, mt6765) = dongle-only.
- PenMon (4PDA): Qualcomm-only [V].
Full evidence: _context/W20-OUT-GEN4M-FEASIBILITY.md, _context/W21-OUT-COMMUNITY-SWEEP.md (19-row table).

## 1.7 W19 addendum — XDA t=3591182 read fully + ATE TX lead (2026-11-22)

Full thread captured via **r.jina.ai live fetch** (bunny shield blocked the browser session AND zero
Wayback/archive.today captures existed — CDX checked; r.jina.ai is now the registered fallback-2 route
for bunny-walled pages, after live-browser and before giving up). Snapshot:
archive/jina-xda-3591182-p1-live-2026-11-22.md; full quotes: _context/W19-OUT-XDA-CAPABILITIES.md.

Thread verdict (ogurets 2017, MT6620/28/30 era): research log only, no patch links. Real packet TX
existed via the **hidden RF test mode** (`wifitesttool -t 0 -s 0 -R 11 …` + `RF_AT_FUNCID_PKTCONTENT`
payload hook) — ATE test frames, not 802.11 monitor [I high]; monitor mode itself was never achieved
in-thread. FM TX: MT6627/28 lack it; on begonia the MT6631 chip dir has zero TX ops → dead-end [I].

**gen4m cross-check [V high]** (both clones): the whole ATE stack is alive — `gl_qa_agent.c`,
`gl_ate_agent.c`, `rftest.h` with `RF_AT_FUNCID_PKTCONTENT` (L187), iwpriv
`SET_TEST_MODE`/`SET_TEST_CMD`/`ACCESS_MCR` handlers (gl_wext_priv.c:4763/4816);
`FM_IOCTL_TX_SUPPORT` byte-identical (fm_ioctl.h L54). The built-in `MONITOR` priv command (§1.6)
is confirmed in-thread-independent; **`kwefjkmqf/Monitor_mode_NetHunter`** documents the iwpriv
monitor method and cites a begonia-SoC tree — companion repo for our Path A/B.

**Injection angle for W22**: the alive ATE/test-mode TX path (custom payload TX) is a candidate
primitive for internal 802.11 TX injection — clunky (test-mode framing) but hardware-backed [I high].
FM TX: dead-end on begonia.

## 1.8 W19 follow-up: thread attachments CAPTURED (2026-11-22)

Orchestrator's playwright-Brave lane (real profile) passed bunny where browser_exec/CDP-harness got
challenged. Captured into archive/xda-3591182/: **wifitest.zip** (libwifitest source — the RF-test TX
tool from the thread: custom-payload packet TX via ATE), **firmwares.zip** (WIFI_RAM_CODE + _E6,
2014, MT6620-era), **something.dump** (4 MB, MCR dump per OP), **WIFI_RAM_CODE_6755** (2018, MT6755).
hint1.png pending (403 on the request-context path — page-context only). These document the
test-mode packet-TX technique referenced in §1.7 — historical MT6620/6755 generation, direct gen4m
lineage for the ATE TX-injection angle.

### §1.8.1 Artifact first-pass analysis (orchestrator, 2026-11-22)
- **wifitest/**: complete MTK ATE userspace toolchain (libwifitest wrapper over WIFI_TEST_set/RF_AT_FUNCID_*,
  main.c, wifi_hw_test_tool, nvram dir) + **testmode1.pcap** — the thread author's own ATE-mode capture.
  This documents the userspace→ATE→TX-engine API that ALSO exists in begonia's gen4m (rftest.h:187
  RF_AT_FUNCID_PKTCONTENT [V]); primary reference for the internal-TX-injection experiment.
- **something.dump**: NOT an MCR dump — 4 MB memory dump of the MT6582-era WiFi ROM/driver state
  (source paths wifi/ROM/wifi_authen_6582.c, hal_hif_rom.c, driver/hif.c visible) — an architecture map
  of the ROM-era stack (gen4m's ancestor).
- **WIFI_RAM_CODE_6755** (2018): connsys FW for MT6755, chip string "A-Die MT6625L" — connsys lineage
  datapoint (MT6625L is pre-CONNAC).
- Lane matrix vs bunny (final): playwright_brave PASS; browser_exec (default+isolated) challenge; curl 403;
  playwright standard (chrome-for-testing) not installed; Hermes desktop webview — no CDP port (driving it
  needs an app restart — not done without owner's go).
- Backlink pass on t=3591182: nothing new; bonus find — AOSP official gen3 wlan mirror (predecessor of gen4m).

## 1.9 W22 — injection patch stack verified (2026-11-22)

**Owner's Anonym3310 collection = verbatim Kali official patches [V]** (normalized diff: identical added
lines, offsets only): Q-OSS-SLMK carries Kali's `add-wifi-injection-4.14.patch` (5 files) +
`fix-ath9k-naming-conflict` + `fix-thread_info.h`; CFW branch has Re4son `u32-mntr_flags` + aircrack-ng
`mac80211.compat08082009.wl_frag+ack_v1`; `additional-drivers-pack.zip` = 6 prebuilt OOT Realtek .ko
(8188eu, 8192eu/8192fu, rtl8188fu, 88XXau, 8814au; vermagic 4.14.233-AkameKernel). The semi-amateur
kernel actually shipped the official NetHunter patch set — good news for trust in the technique, config
quality caveat still stands.

**Kali official builder** `kali-nethunter-kernel-builder@main/patches/4.14` [V]: 12 patches — core
injection; rtl8188eus→rtl8xxxu in-tree (yesimxev 2023); rtl88xxau 5.6.4.2 (Re4son 2020); rtw88-usb
backport (yesimxev 2026-04); **qcacld-3.0 internal TX injection (kimocoder 2025-10)**; BT/build fixes.
nethunter.kali.org/kernels.html: zero begonia entries [V].

**Internal gen4m TX injection: NF after 22 rotations** — no public gen4m/CONNAC TX artifact. Precedents:
qcacld-3.0 Kali patch (driver-layer, FW-dependent), hcxdumptool #531 raw-TX 0% ACKs ("firmware must
support it too"), nexmon (Broadcom-only). Engineering estimate from begonia clones [I]: TX chain
gl_init.c:1518 → gl_kal.c:2134 → wlan_lib.c:3951 → nic_tx.c:1126/1512 (TXD v2); monitor netdev lacks
xmit (gl_init.c:1841); ~600–1200 LOC hook feasible; **FW acceptance unverifiable = blocking risk**.
External adapters remain the injection path for the unified kernel; internal TX = research track after
RX-monitor lands (Path A/B of §1.6).

**Modern adapter stack for the unified kernel [V/I]** (W22-OUT full table): ath9k_htc,
rtl8188eus-via-in-tree-rtl8xxxu, rtl88xxau 5.6.4.2, rtw88-usb backport, mt76x2, rt2x00 (mt7921/7925
need ≥5.x — unreachable on 4.14/4.19). Ordered patch stack from official sources in W22-OUT §4.

## 1.10 W23 — ATE test-mode TX: ZERO-LOC injection experiment (2026-11-22)

The captured 2017 ATE toolchain maps VERBATIM onto begonia's gen4m [V — file:line in W23-OUT]:
PKTCONTENT=12 (rftest.h:187), transport byte-identical (ioctl +8/+9/+11, OIDs 0xFFA0C901/906/911,
magic key 2011, PRIV_CMD_OID=15). Three userspace shells exist: `iwpriv wlan0 set_test_cmd <idx> <data>`,
`/proc/wlan/driver` SET_TEST_CMD, and the ATE agent (`set ATE=TXFRAME`, ATEDA/ATESA). TX is
**firmware-generated** (CMD_ID_TEST_CTRL=0x01, passthrough — bypasses nic_tx/TXD entirely);
`testmode1.pcap` decoded: real on-air QoS-Data frames, NoAck, template MACs — custom payload is the
testable gap [I]. Experiment ladder E1 (template TX) → E2 (header control DA/SA/FC/seq) →
E3 (PKTCONTENT offset-chunking gate) is userspace-only, **ZERO kernel LOC**; W22's 600–1200 LOC LKM
stands only if E3 fails at the gate. nvram dependency satisfied on-device.
