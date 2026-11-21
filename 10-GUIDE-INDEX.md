# 10-GUIDE-INDEX — every begonia (Redmi Note 8 Pro) guide/instruction post, indexed

Device: Xiaomi Redmi Note 8 Pro (`begonia`, MT6785/Helio G90T). Built 2026-11-21 by the indexer agent.
Scope: ALL guide posts from the two 4PDA threads (шапки fully mined: [custom-ROM thread 974421](https://4pda.to/forum/index.php?showtopic=974421), [MIUI thread 965629](https://4pda.to/forum/index.php?showtopic=965629)) + XDA (wayback) + Phase-C discoveries. Full outbound-link inventory with dispositions: `_context/OUTBOUND-LINKS.csv` (1083 unique URLs).

**Conventions.** Permalinks are `showtopic=<id>&view=findpost&p=<pid>`. Offline copies live in `archive/` (`4pda-*-extracted.html` = pandoc extracts of cached pages; `rec2-*.html` = snapshots made by this agent; `*-wayback.html` = Wayback saves). Confidence: high = title/pid read directly from cached шапка or fetched page; medium = inferred from anchor text/search. "Used-by" names the research file the entry feeds (02 firmware, 03 kernel, 05 UBports, 06 pmOS/Droidian, 07 recovery/safety).

Master threads: [CFW/custom-ROM thread t=974421](https://4pda.to/forum/index.php?showtopic=974421) — OP [Xakep1993](https://4pda.to/forum/index.php?showuser=2733256), 2019-12-01, [post #1 = шапка/guide index](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=91427572), 1235 pages — offline: `archive/4pda-cfw-p1-extracted.html` (+mid/last extracts).
[MIUI thread t=965629](https://4pda.to/forum/index.php?showtopic=965629) — OP [SPIRITic](https://4pda.to/forum/index.php?showuser=349568), 2019-09-12, [post #1 = шапка](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=88821588), 1110 pages — offline: `archive/4pda-miui-p1-extracted.html` (+last-page extract).

---

## 1) Bootloader unlock

| Entry | Source | Permalink | Offline | Conf | Used-by |
|---|---|---|---|---|---|
| «Разблокировка загрузчиков XIAOMI» — profile thread for ALL Xiaomi (MTK+Qualcomm), 4700 pages, curator varalex | 4PDA t=721838, OP varalex 2016-01-29, post #1 | [thread / post #1](https://4pda.to/forum/index.php?showtopic=721838&view=findpost&p=46637079) | `archive/rec2-unlock-721838.html` | high | 07 |
| BL rules for begonia in MIUI шапка: region-locked flashing, never relock cross-region, all data wiped on lock/unlock, "100% hardbrick only via service account" (see Contradiction C1), **ARB absent on begonia** (source: [mi-faq.ru anti-rollback](https://4pda.to/stat/go?url=https%3A%2F%2Fmi-faq.ru%2Fanti-rollback.html&e=88821588), medium conf) | 4PDA t=965629 post #1, SPIRITic 2019-09-12 | [post #1](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=88821588) | `archive/4pda-miui-p1-extracted.html` | high (ARB claim: medium) | 07 |
| mtkclient unlock path: `mtk da seccfg unlock` via BROM exploit (no Mi account/wait) | Nura/pmOS wiki device page | [wiki section](https://wiki.nura.eco/wiki/Xiaomi_Redmi_Note_8_Pro_(xiaomi-begonia)) | `archive/pmos-wiki-begonia-extracted.html` | high | 06, 07 |
| mtkclient discussion: "Redmi Note 8 Pro (MT6785) — Bootloader Unlock Without Mi account" | GitHub bkerler/mtkclient discussion #412 | [discussion](https://github.com/bkerler/mtkclient/discussions/412) | — | high | 07 |
| XDA: "MTK client Bootloader unlock" — many begonia confirmations | XDA t=4428577 | [thread](https://xdaforums.com/t/mtk-client-bootloader-unlock.4428577/) | — (live XDA blocked; no snapshot) | medium | 07 |

## 2) Recovery / TWRP / root / Magisk

Recovery builds (CFW шапка «Рекавери» unless noted):

| Entry | Source | Permalink | Offline | Conf | Used-by |
|---|---|---|---|---|---|
| Unified TWRP 3.7.1 by wuxinG90 (current unified recovery) | 4PDA t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=144354114) | `archive/rec2-cfw-twrp-unified-144354114.html` | high | 07 |
| TWRP 3.7.0_12 for A12–14 custom ROMs | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=125972431) | — | high | 07 |
| PitchBlack 4.0 (A12+) | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=126123733) | — | high | 07 |
| PitchBlack Recovery Project 4.1 | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=136151364) | — | high | 07 |
| OrangeFox (A12+) | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=122362174) | — | high | 07 |
| TWRP 3.7.0 by timjosten (A12+) | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=122291401) | — | high | 07 |
| TWRP v3.6.2_12-4 (only A12.1/13 ROMs) | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=118192304) | — | high | 07 |
| TWRP for Non-CFW/GSI on MIUI 12.5 base (A11/12) | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=107899317) | `archive/rec2-miui-twrp-miui125-107899317.html` | high | 07 |
| TWRP for Non-CFW/GSI on MIUI 12.0 base (A10) — "BLACK TWRP 3.5.1 V2 UNIFIED" in MIUI шапка | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=105380152) | — | high | 07 |
| TWRP 3.5.2 v3 Android 11 | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=111411942) | — | high | 07 |
| PBRP-begonia-2.9.1 | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=98521479) | — | high | 07 |
| OrangeFox R10.1 Stable (MIUI 11/12, A10 only), by Xakep1993 | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=96101925) | — | high | 07 |
| OrangeFox-R10.1 (Android 9) | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=94367993) | — | high | 07 |
| TWRP android 9 + RU lang | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=101504220) | — | high | 07 |
| TWRP android 10 + RU lang | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=101507229) | — | high | 07 |
| Install-TWRP guide for A11 ROMs | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=110723127) | — | high | 07 |
| Install TWRP on Android 10 | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=94929391) | — | high | 07 |
| Fastboot-flash TWRP on A11 (short guide) | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=109606933) | — | high | 07 |
| Bootloop-after-reset warning + first-aid post ("don't flash random recoveries") | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=94388409) | — | high | 07 |
| TWRP/backup problems: [general](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=109993921) and [backup-specific](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=97321551) | t=965629 | see left | — | high | 07 |
| Official TWRP page for begonia (install doc) | twrp.me | [page](https://twrp.me/xiaomi/xiaomiredminote8pro.html) | — | high | 07 |
| XDA unofficial TWRP thread (fastboot install steps) | XDA t=3972573 | [thread](https://xdaforums.com/t/recovery-begonia-unofficial-twrp-recovery-for-redmi-note-8-pro.3972573/) | `archive/rec2-xda-twrp-3972573.html` (wayback, curl) | high | 07 |

Root / Magisk:

| Entry | Source | Permalink | Offline | Conf | Used-by |
|---|---|---|---|---|---|
| Magisk profile thread — **v31.0**, updated 2026-09-05; links Magisk-FAQ t=1071490, KernelSU t=1067995, APatch t=1082492, SukiSU t=1108076 | 4PDA t=774072, OP Washerron 2022-02-04, post #1 p=112985156 | [post #1](https://4pda.to/forum/index.php?showtopic=774072&view=findpost&p=112985156) | `archive/rec2-magisk-774072.html` | high | 07 |
| Root MIUI 12.5 guide | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=107898228) | — | high | 07 |
| TWRP+ROOT+GPay on Global device | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=90018812) | — | high | 07 |
| ROOT+GPay on China device | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=90550520) | — | high | 07 |
| ROOT+GPay on China device w/ Indonesian ROM (A9) | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=102227437) | — | high | 07 |
| "If you can't get ROOT" troubleshooting | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=93336734) | — | high | 07 |
| Patched vbmeta.img (disables image verification — needed before custom recovery/GSI) | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=93523562) | — | high | 07 |
| SafetyNet/Play-Integrity & root-hiding topic | t=826244 | [topic](https://4pda.to/forum/index.php?showtopic=826244) | — | medium | 07 |

## 3) ROM installation

### 3a. GSI era (2019–2021)

| Entry | Source | Permalink | Offline | Conf | Used-by |
|---|---|---|---|---|---|
| CFW-thread F.A.Q. (mandatory reading per шапка) | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=95638880) | `archive/rec2-cfw-faq-95638880.html` | high | 02, 07 |
| "How do ROM types differ?" (CFW vs Non-CFW vs GSI) | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=104220383) | — | high | 02 |
| Enable/disable forced data encryption | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=93529098) | — | high | 07 |
| GSI vendor patch: restore network | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=95251749) | — | high | 02 |
| GSI patch: restore audio/video | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=95162709) | — | high | 02 |
| GSI: fix call recording | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=95198486) | — | high | 02 |
| GSI: fix BT-headset echo | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=101430602) | — | high | 02 |
| GSI: scroll smoothness | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=94973835) | — | high | 02 |
| GSI: fix stuck LED | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=102044482) | — | high | 02 |
| GSI: alternative wake-up method | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=95325446) | — | high | 02 |
| Official GSI documentation (flash procedure incl. vbmeta) | developer.android.com | [page](https://developer.android.com/topic/generic-system-image) | — | high | 02 |

### 3b. Native ROM era (Non-CFW / CFW releases — full list in `firmware-matrix.csv`, 320 release permalinks in OUTBOUND-LINKS.csv)

| Entry | Source | Permalink | Offline | Conf | Used-by |
|---|---|---|---|---|---|
| Unified MIUI flashing instruction | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=109320447) | — | high | 02 |
| Fastboot flash from PC (simplest method) | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=111315214) | — | high | 02 |
| SP Flash Tool flashing without service account (current) | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=111347904) | `archive/rec2-miui-unbrick-new-111347904.html` | high | 02, 07 |
| SP Flash Tool without service account (old variant) | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=103570746) | `archive/rec2-miui-unbrick-old-103570746.html` | high | 02, 07 |
| Install ROM via TWRP | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=97183901) | — | high | 02 |
| Reflash via TWRP | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=102378978) | — | high | 02 |
| Update stock while keeping TWRP/root | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=109311334) | — | high | 02 |
| Update stock ROM when TWRP/Magisk present | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=101237489) | — | high | 02 |
| OTA "three dots" manual update on locked BL | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=92899852) | — | high | 02 |
| Xiaomi.eu + TWRP + Magisk short guide | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=91862316) | — | high | 02 |
| China Weekly/Nightly flashing (works for Global Stable too) | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=107611141) | — | high | 02 |
| China beta flashing guide | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=103326447) | — | high | 02 |
| Clean install Global MIUI 12 (wipe) | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=98613041) | — | high | 02 |
| Global 12.5.5.0 + Play certification + SafetyNet | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=110646530) | — | high | 02 |
| Region switch: Global→Indonesia keeping data | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=93699767) | — | high | 02 |
| Region switch: RU/MI/EU→Indonesia (BL unlocked during) | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=91182189) | — | high | 02 |
| Global→Indonesia (device discussion thread) | t=963868 | [post](https://4pda.to/forum/index.php?showtopic=963868&view=findpost&p=100452107) | — | high | 02 |
| Easiest PC flash method | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=94970447) | — | high | 02 |
| Flash via ADB (Lyelik74) | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=90022165) | — | high | 02 |
| Flash without PC (fastboot+adb on-device) | t=838678 | [post](https://4pda.to/forum/index.php?showtopic=838678&view=findpost&p=72982671) | — | high | 02 |
| XiaoMiTool V2 reflash guide | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=89739718) | — | high | 02 |
| All stock firmware in one post (+ firmware decode post [p=94473664](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=94473664)) | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=89799763) | — | high | 02 |
| Firmware & vendor archives for begonia (third-party index) | xmfirmwareupdater.com | [firmware](https://xmfirmwareupdater.com/firmware/begonia/), [vendor](https://xmfirmwareupdater.com/vendor/begonia/) (via [шапка](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=88821588)) | — | high | 02 |
| Linux builds: [Ubuntu Touch 24.04](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=146080111) and [postmarketOS](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=145567744) | t=974421 шапка | see left | — | high | 05, 06 |
| UEFI & WinPE for begonia | t=974421 шапка | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=146118602) | — | high | 06 |

## 4) Kernel / dev guides

Custom kernels (compat: A11+ kernels need MIUI 12.5-based ROMs; A10 kernels need MIUI 11/12-based):

| Entry | Source | Permalink | Offline | Conf | Used-by |
|---|---|---|---|---|---|
| Power Kernel (A11–16), updated 2026-10-21 | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=145668901) | — | high | 03 |
| Suzaku Kernel V2 | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=144852836) | — | high | 03 |
| PoWeR Kernel (A11–16) | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=140587695) | — | high | 03 |
| NoVA Kernel (A11–16) | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=140587177) | — | high | 03 |
| PoWeR Kernel (A11–14) | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=129924406) | — | high | 03 |
| Nova Kernel (A11–13) | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=123613321) | — | high | 03 |
| Coconut Kernel | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=123608360) | — | high | 03 |
| Hydra Kernel | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=122292944) | — | high | 03 |
| QuantumKiller / Neutrino (ZyCromerZ) [Q-OSS] | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=99720504) | — | high | 03 |
| Rave 1.8 (Peppe289, discontinued) [Q-OSS] | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=103603411) | — | high | 03 |
| UnicornHorn (TheMalachite) [Q-OSS] | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=106215865) | — | high | 03 |
| AkameKernel (NetHunter support), by Anonym3310@localhost [Q-OSS] | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=97901817) | — | high | 03 |

Dev guides & sources:

| Entry | Source | Permalink | Offline | Conf | Used-by |
|---|---|---|---|---|---|
| Official Xiaomi kernel source, A11: begonia-r-oss (MiCode) | GitHub | [repo/branch](https://github.com/MiCode/Xiaomi_Kernel_OpenSource/tree/begonia-r-oss) (via [шапка link](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=91427572)) | — | high | 03 |
| Linking external modules to the kernel | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=105817890) | — | high | 03 |
| Atheros USB-WiFi modules (AR9271/AR7010) build | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=105942017) | — | high | 03 |
| Unpacking `*.img` images | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=95104123) | — | high | 03 |
| Goodix fingerprint patch for service preloader | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=98459789) | — | high | 03 |
| Patched-kernel installer for TWRP | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=101695089) | — | high | 03 |
| Community kernel tree (AgentFabulous, android-11.0) | GitHub | [repo](https://github.com/AgentFabulous/begonia) | `archive/github-agentfabulous-begonia.html` | high | 03 |
| pmOS maintainer Dinolek: mt6785-mainline kernel | GitHub | [repo](https://github.com/Dinolek/mt6785-mainline) | `archive/github-dinolek-mt6785-mainline.html` | high | 03, 06 |
| MemeTek org: [kernel mt6785](https://github.com/xiaomi-begonia-dev/android_kernel_xiaomi_mt6785), [+12 repos](https://github.com/xiaomi-begonia-dev) | GitHub (Phase-C) | see left | — | high | 03 |
| Device tree: [MT6785-dev/device_redmi_begonia](https://github.com/MT6785-dev/device_redmi_begonia); AOSP trees: [mt6785-wahid org](https://github.com/mt6785-wahid); custom: [pox-kernel-begonia](https://github.com/txorav/pox-kernel-begonia) | GitHub (Phase-C) | see left | — | medium | 03 |
| Official LineageOS tree for begoniain (India variant of begonia) | GitHub (Phase-C) | [repo](https://github.com/LineageOS/android_device_xiaomi_begoniain) | — | high | 03 |

## 5) Unbrick / rescue / test-points

| Entry | Source | Permalink | Offline | Conf | Used-by |
|---|---|---|---|---|---|
| Restore & flash via SP Flash Tool WITHOUT authorized Xiaomi service account — current method | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=111347904) | `archive/rec2-miui-unbrick-new-111347904.html` | high | 07 |
| Same, old variant (the one referenced by CFW шапка as «Метод») | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=103570746) | `archive/rec2-miui-unbrick-old-103570746.html` | high | 07 |
| Full NVRAM partition restore | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=122476275) | — | high | 07 |
| NVRAM+IMEI restore (MIUI thread version) | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=94524985) | — | high | 07 |
| Fix "NVRAM WARNING: Err=0x10" in WiFi list | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=101867024) | — | high | 07 |
| Bluetooth broken after some ROMs — fix | t=974421 | [post](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=113702662) | — | high | 07 |
| IMEI restore step-by-step | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=105685212) | — | high | 07 |
| MauiMETA for IMEI/NVRAM | t=678449 | [topic](https://4pda.to/forum/index.php?showtopic=678449) | — | high | 07 |
| Stock modems collection (all MIUI versions) | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=99355057) | — | high | 07 |
| FRP (Google account) removal: [main](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=101883357), [alternative bypass](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=136982282) | t=965629 | see left | — | high | 07 |
| Exit fastboot mode | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=132345475) | — | high | 07 |
| Fastboot-flash problem solving | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=93553248) | — | high | 07 |
| SP Flash Tool "Download DA 100%" error fix | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=94626014) | — | high | 07 |
| Patched bootloader — prevents common bricks (MIUI 10/11, A9 only, device must be alive) | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=94143159) | — | high | 07 |
| XDA: unbrick when stuck on preloader mode (begonia/begoniain) | XDA t=4000433 | [thread (wayback)](https://web.archive.org/web/2024/https://xdaforums.com/t/guide-begonia-begoniain-how-to-unbrick-when-stuck-on-preloader-mode.4000433/) | `archive/rec2-xda-unbrick-preloader-4000433.html` | high | 07 |
| /e/OS build thread — includes mtkclient + SPFT + Android 9 rescue recipe | /e/ community | [thread](https://community.e.foundation/t/unofficial-build-redmi-note-8-pro-begonia-for-e-os-t/54371) | — | high | 07 |

## 6) Tools (mtkclient, SP Flash Tool, bypass utilities)

| Entry | Source | Permalink | Offline | Conf | Used-by |
|---|---|---|---|---|---|
| SP Flash Tool thread — v5.2404/v6.2404 (v5.2228/v6.2228), updated 2024-12-27 | 4PDA t=469340, OP wexxxx 2013-06-05, post #1 p=22556656 | [post #1](https://4pda.to/forum/index.php?showtopic=469340&view=findpost&p=22556656) | `archive/rec2-spflash-469340.html` | high | 07 |
| MTKClient thread (4PDA) — referenced from SPFT шапка | t=1077289 | [topic](https://4pda.to/forum/index.php?showtopic=1077289) | — | high | 07 |
| mtkclient GitHub (BROM exploit tool) | GitHub bkerler | [repo](https://github.com/bkerler/mtkclient) | — | high | 06, 07 |
| WwR MTK (MTK tool) | t=813767 | [topic](https://4pda.to/forum/index.php?showtopic=813767) | — | high | 07 |
| ADB / fastboot usage | t=383300 | [topic](https://4pda.to/forum/index.php?showtopic=383300) | — | high | 07 |
| MiFlashPro | t=889822 | [topic](https://4pda.to/forum/index.php?showtopic=889822) | — | high | 07 |
| Universal MTK driver installer | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=90606164) | — | high | 07 |
| Magisk official repo (topjohnwu) | GitHub | [repo](https://github.com/topjohnwu/Magisk) (via [thread](https://4pda.to/forum/index.php?showtopic=774072&view=findpost&p=112985156)) | — | high | 07 |
| Fastboot flasher for begonia (dedicated tool post) | t=965629 | [post](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=101067763) | — | high | 07 |

## 7) XDA-only guides

| Entry | Source | Permalink | Offline | Conf | Used-by |
|---|---|---|---|---|---|
| [GUIDE][INFO][PSA] Redmi Note 8 Pro — Megathread + CFW (guide index post #1) | XDA t=4056527 | [wayback 2026-04-15](http://web.archive.org/web/20260415164458/https://xdaforums.com/t/guide-info-psa-redmi-note-8-pro-megathread-cfw.4056527/) | `archive/xda-megathread-wayback.html` | high | 02, 07 |
| [GUIDE][BEGONIA] Unlock Bootloader, Flash TWRP and Root [PROPER] | XDA t=3995919 | [wayback 2023-03-16](http://web.archive.org/web/20230316035523/https://forum.xda-developers.com/t/guide-begonia-unlock-bootloader-flash-twrp-and-root-proper.3995919/) | `archive/xda-unlock-guide-wayback.html` | high | 07 |
| [GUIDE] begonia/begoniain: how to UNBRICK when stuck on preloader mode | XDA t=4000433 | [wayback](https://web.archive.org/web/2024/https://xdaforums.com/t/guide-begonia-begoniain-how-to-unbrick-when-stuck-on-preloader-mode.4000433/) | `archive/rec2-xda-unbrick-preloader-4000433.html` | high | 07 |
| [RECOVERY][begonia][UNOFFICIAL] TWRP recovery | XDA t=3972573 | [wayback](https://web.archive.org/web/2024/https://xdaforums.com/t/recovery-begonia-unofficial-twrp-recovery-for-redmi-note-8-pro.3972573/) | `archive/rec2-xda-twrp-3972573.html` | high | 07 |
| [RESOURCES] Device tree for Redmi Note 8 Pro | XDA t=3999013 | [thread](https://xdaforums.com/t/resources-device-tree-for-redme-note-8-pro.3999013/) | — (blocked; no snapshot) | medium | 03 |
| MTK client bootloader unlock (begonia confirmations) | XDA t=4428577 | [thread](https://xdaforums.com/t/mtk-client-bootloader-unlock.4428577/) | — (blocked; no snapshot) | medium | 07 |

---

## Contradictions (feeds the verification pass)

- **C1 — Hardbrick recoverability.** MIUI шапка (t=965629 [post #1](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=88821588)): «100% HARDBRICK восстанавливается только через сервисный аккаунт» vs CFW шапка (t=974421 [post #1](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=91427572)) + [SPFT-without-account methods](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=111347904): unbrick possible since ~2021 without authorized account (BROM exploit). Resolution: MIUI statement predates the method; SPFT-without-auth is current.
- **C2 — Which TWRP.** [Unified TWRP 3.7.1](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=144354114) is presented as the current one, while шапка simultaneously lists base-specific builds ([A12–14](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=125972431), [A12.1/13-only 3.6.2](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=118192304), [MIUI-12.5-base](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=107899317), [MIUI-12.0-base](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=105380152)). The "right" TWRP depends on ROM base — unified claim not cross-verified.
- **C3 — Unlock procedure.** Official Xiaomi unlock ([t=721838](https://4pda.to/forum/index.php?showtopic=721838&view=findpost&p=46637079), Mi-account wait) vs instant mtkclient unlock ([wiki](https://wiki.nura.eco/wiki/Xiaomi_Redmi_Note_8_Pro_(xiaomi-begonia)), [discussion](https://github.com/bkerler/mtkclient/discussions/412)). Both wipe data; risk profiles differ (BROM exploit vs official tool).
- **C4 — ARB.** [MIUI шапка](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=88821588) states ARB (anti-rollбack) is ABSENT on begonia, citing [mi-faq.ru](https://4pda.to/stat/go?url=https%3A%2F%2Fmi-faq.ru%2Fanti-rollback.html&e=88821588) — low-confidence source, unverified against stock preloader behavior.
- **C5 — vbmeta handling for GSI.** Patched vbmeta.img post ([p=93523562](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=93523562)) vs generic `fastboot --disable-verification flash vbmeta` advice ([Android docs](https://developer.android.com/topic/generic-system-image)). begonia-specific patched image is the 4PDA-recommended path.

## Limitations

- Live xdaforums.com blocked (bunny.net challenge) for all fetchers; XDA content above comes from Wayback snapshots only. XDA t=3999013 and t=4428577 have **no snapshot** (pending human-browser check).
- web.archive.org is blocked by the sandboxed fetcher (`web_extract`); the two new XDA wayback copies were made with `curl` (full HTML, clickable).
- 4PDA guide posts live in 1110–1235-page threads; only pages listed in `archive/` are snapshotted. Uncached permalink targets are reachable via the permalinks above (4PDA allows guest read).
- Attachment/file-host links (androidfilehost) may be dead — marked in CSV; no binaries archived per repo policy.
- YouTube unbrick/TWRP videos exist (see CSV) but are video-only — not text-indexable, not archived.
