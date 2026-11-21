# Xiaomi Redmi Note 8 Pro (`begonia`) — Firmware History
Dimension: firmware. Compiled 2026-11-21 (JST). Research-only; nothing was flashed or downloaded.
Evidence rules: exact URL + author/date + 4PDA permalink where applicable; `verified` = seen directly in a fetched source; `inferred` = derived (e.g. from pid ordering); confidence high/medium/low. Historical sections are marked **[HISTORICAL]**; current status is marked **[CURRENT]**.

Primary local evidence (cached, fetched by orchestrator):
- 4PDA custom-ROM thread `showtopic=974421` ("Redmi Note 8 Pro - Неофициальные прошивки", 1234 pages), pinned post #1 by **Xakep1993**, created **2019-12-01 12:50**, permalink https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=91427572 — pinned index last edited by sergrauber "Сегодня, 00:49" = **2026-11-21 00:49** (verified in cache).
- 4PDA MIUI firmware thread `showtopic=965629` ("Redmi Note 8 Pro - Прошивки MIUI", 1110 pages), pinned post by **SPIRITic**, created 2019-09-12, permalink https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=88821588.
- XM Firmware Updater live download table (fetched fresh 2026-11-21): https://xmfirmwareupdater.com/miui/begonia/

---

## 1. Official MIUI **[HISTORICAL — line ended 2022]**

### 1.1 Regions that actually shipped (verified)
The 4PDA MIUI pinned index and the XM Firmware Updater latest-table agree on six region variants; **Taiwan (TW) never appears in either source** — no `PGGTW`/`RGGTW`/TW build exists in any consulted source:

| Region | MIUI suffix | Verified evidence |
|---|---|---|
| China | `…CNXM` / weekly | 4PDA pinned (p=88821588); xmfwu table `V12.5.6.0.RGGCNXM` |
| Global | `…MIXM` | xmfwu `V12.5.1.0.RGGMIXM`, `V12.5.8.0.RGGMIXM` |
| EEA (Europe) | `…EUXM` | xmfwu `V12.5.15.0.RGGEUXM`, `V12.0.6.0.QGGEUXM` |
| Russia | `…RUXM` | xmfwu `V12.5.3.0.RGGRUXM`, `V12.5.5.0.RGGRUXM` |
| Indonesia | `…IDXM` | 4PDA zip URL `miui_BEGONIAIDGlobal_V11.0.1.0.PGGIDXM_…_9.0.zip`; xmfwu `V12.5.6.0.RGGIDXM` |
| India | `…INXM` (separate `begoniain` tree) | xmfwu path `/miui/begoniain/…V12.5.5.0.RGGINXM` |
| **Taiwan** | — | **absent from all consulted sources** (verified absence, high confidence) |

Android-base letter code (verified from actual filenames): `PGG` = Android 9, `QGG` = Android 10, `RGG` = Android 11 (e.g. `V11.0.1.0.PGGCNXM`, `V12.0.6.0.QGGEUXM`, `V12.5.15.0.RGGEUXM`).

### 1.2 Build timeline (verified build numbers/dates — no invented numbers)
**Android 9 era (MIUI 10 → MIUI 11)**
- China Developer weeklies from **9.9.25** (Sept 2019, `miui_BEGONIA_9.9.25_63b9ff3ba0_9.0.zip`, bigota link in 4PDA pinned) up to **9.12.26** — verified.
- **Global (EEA)**: MIUI 10 build `V10.4.5.0.PGGEUXM` is referenced in a 4PDA TWRP-install guide inside the MIUI pinned post (verified, quote: "для установки через TWRP на **Global V10.4.5.0.PGGEUXM**"). 
- MIUI 11 stable (A9): Global **V11.0.2.0 → V11.0.6.0** (last A9 Global); EEA **V11.0.1.0 → V11.0.3.0**; Russia **V11.0.1.0 → V11.0.3.0**; Indonesia **V11.0.1.0 (PGGIDXM) → V11.0.2.0**; China Stable **V11.0.1.0 (PGGCNXM) → V11.0.2.0**. All verified in 4PDA pinned (p=88821588) with bigota download URLs for ID/CN.
- ⚠️ **Contradiction on shipped MIUI**: Nura/pmOS wiki states "Original software: Android 9 (MIUI 11)" (wiki.nura.eco cache, verified), but the MIUI 10 `V10.4.5.0.PGGEUXM` reference above plus Sept-2019 China dev weeklies indicate the device shipped with **MIUI 10** (Android 9) in Sept 2019, receiving MIUI 11 around Nov 2019 (CN dev got 11 first — the "China Developer" section under "Android 9" lists 9.x builds). Resolution: shipped MIUI 10, updated to MIUI 11 within weeks — **medium confidence, inferred**; both claims recorded verbatim.

**Android 10 era (MIUI 12)**
- Global: **V12.0.0.4 → V12.0.8.0** (V12.0.8.0 = last A10 Global, Recovery/Fastboot, p=106868464); EEA: → **V12.0.6.0** (p=107679766; xmfwu classifies `V12.0.6.0.QGGEUXM` as "Stable Beta", Recovery 2021-06-25); Indonesia: → **V12.0.4.0**; Russia: → **V12.0.8.0** (p=106926264); India: → **V12.0.4.0**; China Stable: → **V12.0.5.0** (p=104104801); China MIUI 12 weeklies **V20.4.27 → V20.11.25**. All verified in 4PDA pinned.

**Android 11 era (MIUI 12.5) — final official line**
Verified in BOTH 4PDA pinned and the live xmfwu table:

| Region | Last build (xmfwu "latest" table, fetched 2026-11-21) | Date | Notes |
|---|---|---|---|
| **EEA** | **V12.5.15.0.RGGEUXM** (Recovery 2.4 GB; Fastboot 4.4 GB) | Recovery **2022-09-16** / Fastboot 2022-08-26 | **Last official MIUI build ever released for begonia (any region)** |
| India | V12.5.10.0.RGGINXM "Stable Beta" (Recovery) | 2022-07-07 | last non-beta: V12.5.5.0.RGGINXM 2021-10-22/16 |
| Russia | V12.5.5.0.RGGRUXM "Stable Beta" (Recovery) | 2022-07-20 | last stable: V12.5.3.0.RGGRUXM 2021-11-05/10-26 |
| Global | V12.5.8.0.RGGMIXM "Stable Beta" (Recovery) | 2022-06-06 | last true stable: V12.5.1.0.RGGMIXM 2021-07-08/06-29 |
| China | V12.5.6.0.RGGCNXM (Recovery + Fastboot) | 2022-06-13 / 06-02 | last weekly: **21.11.24** (2021-11-25) |
| Indonesia | V12.5.6.0.RGGIDXM (Recovery + Fastboot) | 2022-06-13 / 06-06 | |

⚠️ **Contradictions 4PDA-index vs xmfwu (both recorded, high confidence each source is accurately quoted):**
1. **Global**: 4PDA pinned lists V12.5.8.0 under "**Global Stable**" (p=115441197); xmfwu classifies the same build as "**Stable Beta**" and shows V12.5.1.0 as the last Global *Stable*.
2. **Russia**: 4PDA pinned lists **V12.5.4.0 - Recovery** (p=114131518) as the last RU 12.5 entry; xmfwu shows RU stable ending at V12.5.3.0 + a "Stable Beta" V12.5.5.0 — V12.5.4.0 does not appear in xmfwu's latest table (may exist in the archive, not fetched).
3. **China weekly**: 4PDA pinned's last weekly is **V21.10.15** (p=110228918); xmfwu shows **21.11.24** (2021-11-25) — the 4PDA index appears stale/incomplete for CN weeklies.

**Modem/baseband firmware**: no consulted source states begonia baseband/modem versions. Non-vendor firmware images (modem/NVRAM packs) exist as downloads at https://xmfirmwareupdater.com/firmware/begonia/ (linked from the 4PDA pinned "FirmWare, Vendor" section, verified), but version numbers were not extracted. Recorded as a limitation, not invented.

**ARB (Anti-Rollback)**: 4PDA MIUI pinned states verbatim "В данной модели ARB (Anti-RollBack) отсутствует !!!" — this model has **no ARB** (verified; source mi-faq.ru via 4PDA). Region cross-flashing is impossible without unlocked bootloader ("China-производства не могут быть прошиты Global-прошивками" etc.), and MIUI 10 vs MIUI 11 boot/recovery images must never be mixed ("Нельзя ставить на MIUI 10 файлы BOOT и RECOVERY от MIUI 11 и наоборот!" — 100% hardbrick risk).

### 1.3 Vendor partition — what custom ROMs ride on **[CURRENT]**
- The 4PDA CFW pinned kernel section states (verified quote): "Ядра, указанные ниже, совместимы только с прошивками, основанными на образах **MIUI 12.5.x** (Android 11/12+)" — i.e. **current custom ROMs and kernels are built on the MIUI 12.5 vendor images** (the final RGG builds, §1.2). The two earlier vendor generations (MIUI 12.0 A10, MIUI 12.5 A11/12) are also reflected in dedicated TWRP builds: "TWRP для Non-CFW/GSI прошивок, основанных на образах MIUI 12.5 (Android 11/12)" (p=107899317) and "…MIUI 12.0 (Android 10)" (p=105380152) — verified.
- Per-region vendor/firmware packs are published at https://xmfirmwareupdater.com/vendor/begonia/ and https://xmfirmwareupdater.com/firmware/begonia/ (links verified in 4PDA MIUI pinned; pages not individually fetched).
- Inference (medium confidence): the newest A15–A17 ROMs (§3) still boot on this Android 11-era MIUI 12.5 vendor + 4.14 kernel (stock 4.14.141 per devices.ubuntu-touch.io; AgentFabulous kernel repo `android-11.0` default branch, last push 2022-06-23 per shared context) — see §4.

---

## 2. GSI era (Dec 2019 – 2020) **[HISTORICAL]**
Thread origin: the 4PDA custom-ROM thread was created **2019-12-01** by Xakep1993 as a **GSI-flash thread** (post #1, p=91427572: "Гайд по установке напишу в течении 1-2 часа" — guide promised within 1–2 hours; edit log 01.12.19 14:24).

**Pinned GSI guide chain (all permalinks verified in page-1 cache):**
- Post #3, 2019-12-01 15:12 (edited 18:33), p=91432197 — install guide: download archive → unpack to bare IMG → verify **md5** ("не забывайте md5 проверять, у меня с первые два раза не сошлось") → TWRP backup first; verbatim warning: "**Нивкоем случае не трогать BOOT файл** - даже восстановление из бекапа (при помощи TWRP)! За кирпичи связанные с BOOT файлом не отвечаю!" (never touch the BOOT image — brick warning).
- Post #20, 2019-12-01 21:19, p=91444631 — points to the general MTK GSI guide "Установка GSI-прошивок (Пост Ctarchik #87789849)" in topic 892755.
- Pinned index also links "Альтернативный способ пробуждения экрана устройства (для некоторых GSI)" (p=95325446) — wake-screen workaround for GSIs.
- Unlock prerequisite (from Nura wiki, verified): Mi Unlock tool (7-day wait) or **mtkclient BROM exploit** `mtk da seccfg unlock` (5 minutes).

**Early bug reports (day-one GSI experience, Dec 1, 2019):**
- **Post #11** (StegroNN, 01.12.19 18:56, p=91439510), tested "PE и AOSP от phh" (Pixel Experience + phh's AOSP GSI), verbatim: "связь не работает на PE. На всех прошивках что я тестил, **не работал звук** ни уведомления ни мультимедиа, только разговорный динамик. **Не работает анимация нормально**, анимация прокручивания списка дёргается часто, а анимации связанные красивыми загрузками различных приложений, неадекватно себя ведут." → PE: no cellular; on all tested GSIs: no notification/media audio (earpiece only), broken/jerky animations.
- **Post #18** (StegroNN, 01.12.19 20:27, p=91442761), verbatim: "пока все сырое, там конечно есть **костыли для регулировки яркости** и анимацию вроде можно пофиксить, но **звука нет** и поэтому не остался" → everything still raw; brightness only via crutches, animations fixable, **no audio** — user reverted.
- Xakep1993's own reply in #17-thread context: "9ку не ставил, откатился на миюай 11 европейку" (didn't stay on the GSI, went back to MIUI 11 EEA) — verified.

**GSI-based ROMs catalogued in the pinned index ("Другое" section — "Прошивки, имеющие в основе GSI и подобное"):**
| Base | ROM (author) | Permalink |
|---|---|---|
| A10 | BlissROM (GSI) — rvtom1970 | …974421&view=findpost&p=107855537 |
| A10 | Resurrection Remix (GSI) — rvtom1970 | …p=102565322 |
| A11 | LineageOS 18.1 (GSI-based) — bugreporter | …p=106451290 |
| A11 | crDroid 7.xx Mod (GSI) — User-_-Name | …p=110287291 |
| A12 | Bliss — (GSI) | …p=114061722 |
| A12 | Evolution X — timjosten (GSI) | …p=112878843 |
| A13 | crDroid 9.x — timjosten (unofficial, closed code) | …p=121096835 |
| A13 | MagicOS 7.1 Beta | …p=145549738 |
| A12 | HarmonyOS 4.0.0.112 (port) | …p=145551659 |
(all topic 974421; verified from pinned index)

Era assessment: GSIs were the only custom option from Dec 2019; the pinned guide rates them "все сырое" (all raw). Native ROMs began appearing while GSIs were still current (first native build listed under "Non-CFW Android 10": **crDroid 6.27 FINAL by TTTT555**, p=97822397 — date inferred early-2020 from pid ordering, medium confidence); fully native A11 builds by ~spring 2020 (AOSP ZIDAN44 p=101209196, crDroid 7.2 p=101340561 — inferred from pid ordering vs known MIUI build dates).

**GSI vendor-base data point (added at synthesis pass 2026-11-21, C4):** Erfan's treble GSI builds for begonia shipped a vendor image tagged **`begonia-user 10/QP1A.190711.020/20.5.14` (2.66 GiB)** — an Android-10-era vendor base (Android build fingerprint `QP1A.190711.020`, MIUI build stamp `20.5.14`) for the early treble wave. Source class: public Telegram channel log via [t.me/s/ProjectTreble_Updates](https://t.me/s/ProjectTreble_Updates) web preview (community signal — citable as evidence of what existed, not as primary docs; census 2026-11-21, medium).

---

## 3. Native custom-ROM catalog **[CURRENT state as of 2026-11-21; first-release dates historical]**
The pinned index (edited 2026-11-21 00:49) is organized Non-CFW (native) / Другое (GSI-based) / CFW (deprecated) / Linux / UEFI, and states: "В настоящее время актуальны прошивки из раздела **Non-CFW** и **Другое**" (currently relevant: Non-CFW and Other). ~60 native builds A10→A17 are indexed; the notable ones:

### 3.1 crDroid — **OFFICIAL** (verified: https://crdroid.net/begonia listed on crdroid.net/downloads, fetched 2026-11-21)
- Official versions listed: **crDroid 6 (A10) → 10 (A14)**; page states "**Last build: 2024-07-17**". Maintainers per 4PDA: TTTT555 (6.x A10, p=97822397; 7.2/7.x A11, p=101340561 & p=114818456), Simone Esposito (8.x A12, p=112425228), DarkJoker360dev (9.x A13, p=126542230 — "OFFICIAL by DarkJoker360dev"). Status: **official support ended 2024-07-17 (A14)**; unofficial line continues (crDroid **v12.11** UNOFFICIAL A16, p=143929573; v12.7 p=141907803; v11.x A15 p=141749053). High confidence.
- Related GitHub hit (search, verified): `MaloyBegonia/android_device_redmi_begonia_crDroid`, pushed 2024-01-17.

### 3.2 LineageOS — **NOT official** (verified: https://wiki.lineageos.org/devices/begonia/ returns 404 "Page Not Found", fetched 2026-11-21)
All begonia LineageOS builds are **unofficial** (4PDA labels each "UNOFFICIAL"):
- LOS 20 (A13) p=118200298; LOS 20 for microG p=120005877; LOS 22.2 Stable **by wuxinG90** (A15) p=145635495; LOS 22.2-QPR2 p=136393297; LOS 23.0 p=140587004; **LOS 23.1 p=145618622; LOS 23.2 p=145712732** (A16, newest LOS listed, both UNOFFICIAL, indexed in the 2026-11-21 pinned edit). Dates of individual posts not extractable from the index (pids only) — medium confidence on ordering, high on existence.
- Unofficial kernel-side lineage: `github.com/AgentFabulous/begonia` ("Linux kernel source tree for the Redmi Note 8 Pro"), default branch `android-11.0`, last push 2022-06-23, branches a9→a12 (verified in shared context).

### 3.3 PixelExperience / PixelOS — unofficial
- PE A12 p=112628231; **PE 13** p=118140083 & PE Plus 13 p=118676391 (A13); PE UNOFFICIAL A14 p=129921932; successor-brand **PixelOS 16.2 UNOFFICIAL by @wuxinG90** p=144357321 (also p=142245568, p=140904812 for 16.1). Official PixelExperience status for begonia not verifiable (site not fetched) — medium confidence that all were unofficial.

### 3.4 ArrowOS — unofficial
- ArrowOS A11 by Santoshhh000 p=102841984 (indexed under Non-CFW A11); "Arrow OS - Unofficial **by isegorka**" A12 p=116619121. No official ArrowOS begonia page consulted — status: unofficial, last indexed A12 (dead on begonia since ~2022, inferred).

### 3.5 Evolution X — official→unofficial lineage
- First A11 build by TheMalachite p=111369873 (Non-CFW A11 index); **"Evolution X Official"** A14 p=126147449 (the only begonia EX build the index labels Official); then A16 line: 11.0 p=138215195/p=138251566, 11.4.1 p=140587298, 11.6.3 p=143064325, **EvolutionX 11.7 UNOFFICIAL p=146098392 — highest pid in the entire pinned index → newest ROM build for begonia as of 2026-11-21** (release date not shown in index; high confidence it is the newest listed).

### 3.6 AxionAOSP / AxionOS — OFFICIAL, Android 16, daily-driven
- AxionOS v1.2 OFFICIAL (A15) p=136333822 → v2.2.1 OFFICIAL p=140587508 → **AxionAOSP v2.4 OFFICIAL Gapps p=141675626 (+Vanilla p=141675834)** → axion os 2.7 p=143770022 → **AxionOS 2.9 Noesis OFFICIAL (A16) p=145668812**. The "AXION AOSP 16" daily-driver claim is verified on the Nura wiki user list (wiki.nura.eco cache, verified): "[Core6quad] (Notes: **Daily driver, AXION AOSP 16**)". Same wiki records other current users: Michaelskyf "Daily driver - LineageOS 19.0", Sohrabbehdani "running CrDroid". High confidence.

### 3.7 MIUI/other-OEM ports (the "port" sub-scene, alive in 2026)
ColorOS 16 ports (16.0.9.402 p=144433439; REPACK p=144473382; PLF100_16.0.10.501 p=145345569) and **ColorOS 17 - Stable Revision 17 (Android 17!) p=146083465** + Revision 13 UNOFFICIAL p=146061439; **AviumUI 16.2.1 OFFICIAL p=146024411**; OriginOS 6 Port by tuser, Stable Release 3 - Revision v22 p=145985251; OriginOS 4 R1/R2 p=131543971/p=134414587; OriginOS 3.1 Beta2 p=143563437; OriginOS Ocean 22.1.14 PORT p=112676744; Flyme 10.3.0.0A port p=143523197; EMUI 14.2.0 Beta p=145406321; ROGUI 14.0-R1 (ROG Phone 6D port) p=141706486; PixelUI Pixel 6 Pro port p=136241130. All verified in pinned index.

### 3.8 Other active A14–A17 native ROMs (pinned index, abridged)
DerpFest 16.2 p=144870980 (and DerpFest A13 p=128191141, Derpfest Tango p=118140323); Project Infinity X 3.12 p=144878394 (OFFICIAL up to 3.8 p=142411724); VoltageOS 5.11-EOL p=144980405; Lunaris-AOSP 3.12 EOL p=145131057; MistOS 4.6 p=142862082 (Sunshine OFFICIAL p=138203843); RisingOS-Revived 8.1.1-Arete p=140587231; CherishOS v6.3 OFFICIAL p=140991383; Project Elixir 4.2 OFFICIAL p=129792004; YAAP Homemade p=137652577; Halcyon p=133667888/p=129274364; Styx Project 4.0.0+alpha1 p=132325074; AlphaDroid p=129916721; OctaviOS V5.0 p=128191584; Project Sakura 9.0 p=130055523; plus the A10–A12 graveyard (POSP, Nusantara, Corvus, Havoc-OS p=104933535, SuperiorOS, CesiumOS, PixysOS, LegionOS, Spark OS, RiceDroid, KomodoOS, Fluid, Ancient, dotOS p=142195743/p=104328069, Syberia p=118344953, Ten-X, ExTHmUI, HyconOS, LegionOS, Pixel Extended p=102952720, AOSP Extended…). All verified as index entries.

### 3.9 "Mu-Silicium" — **NOT an Android ROM** (resolved)
- Identity (verified via GitHub API, fetched 2026-11-21): **github.com/Project-Silicium/Mu-Silicium** — "Project **Mu UEFI** Ports for ARM64-Based Devices"; created 2022-12-24, last push 2026-11-20, 633 stars. It is a Project-Mu (Microsoft UEFI) firmware project for ARM64 phones — a way to boot PC OSes, **not** a mainline-Linux Android ROM for MTK.
- The 4PDA CFW last-page mention (verified, cache of page 1234): post "**UEFI & WinPE**" (pinned-index link p=146118602) by **KiryxaMeow**, with screenshots dated **2026-11-20**: "UEFI (Mu-Silicium) + WinPE 11" begonia port. Verbatim status: "в нынешних реалиях запуск полноценной Windows 10/11 невозможен. только PE-версия" (full Windows 10/11 boot impossible; PE only). Install: `fastboot flash boot UEFI.img`; WinPE 11 boots from a GPT/FAT32 SD card (5–60 min wait). Feature matrix: Display ✅, Side buttons ✅, SD ✅, Windows-Boot ✅ (PE only); internal storage partial (❔); USB host/device/PD ❌, touch ❌, all sensors/audio/GPU/camera ❌, "Linux Boot - ❔". Quote: "исходники выложу на Github Mu-Silicium" (sources promised on GitHub Mu-Silicium; begonia device folder in that repo not yet verified by me — medium confidence the begonia port source is public).
- So the correct 2026 statement: begonia's newest non-Android experiment is a **Mu-Silicium UEFI + WinPE 11 ARM64 boot image** (Nov 2026), unrelated to Android ROMs; the 4PDA pinned has a dedicated "UEFI" section for it.

### 3.10 Linux/UEFI on the pinned index (cross-reference)
Pinned "Linux" section links Ubuntu Touch 24.04 (p=146080111) and postmarketOS (p=145567744) — matching the other dimension's findings (UT stable 24.04-1.4 2026-07-13; pmOS mainline 6.16.4, maintainer Dinolek).

---

### 3.11 Bliss OS 16.9 — unofficial native build, 2023 (catalog gap closed at synthesis pass, C2)

- **Artifact:** `Bliss-v16.9-begonia-UNOFFICIAL-vanilla-20230808.zip` (+ sibling build `…20230809.zip`) in the [AndroidFileHost begonia folder, flid=339073](https://www.androidfilehost.com/?w=files&flid=339073) — an Android-13-era unofficial **native** Bliss OS build for begonia. It was absent from the pinned-index-derived catalog above, which lists only Bliss *GSIs* (§2).
- **Classification:** community mirror, **hash-unverified** (research-only policy: not downloaded); provenance/maintainer of the 2023 build not verified (medium, census 2026-11-21).
- **Status:** historical (Aug 2023); no current Bliss thread or maintainer verified for begonia — treat as "exists on mirrors, unverified provenance".
- **CSV flag:** a matching `firmware-matrix.csv` row is left to the assembler agent (category `custom-rom`, status `unofficial-historical`, source `androidfilehost.com/?w=files&flid=339073`) — CSVs are outside this file's write scope.

## 4. Latest-by-date vs latest-driver-base **[CURRENT — explicit separation]**
- **Latest by release date (verified, Nov 2026):** custom ROMs up to **Android 16/17** — EvolutionX 11.7 UNOFFICIAL (highest pid, p=146098392), ColorOS 17 Rev 17 (p=146083465), LineageOS 23.2 UNOFFICIAL (p=145712732), AxionOS 2.9 Noesis OFFICIAL (p=145668812), crDroid v12.11 UNOFFICIAL (p=143929573), AviumUI 16.2.1 OFFICIAL (p=146024411). Thread itself is active (last-page timestamps 19–21.11.26). Linux-side newest: UT noble stable 24.04-1.4 (2026-07-13), pmOS mainline 6.16.4, Mu-Silicium UEFI/WinPE port (2026-11-20).
- **Latest underlying driver/firmware base (verified):** all of those Android ROMs still ride the **Android 11-era vendor**: MIUI 12.5.x vendor blobs (final builds V12.5.6.0–V12.5.15.0.RGG…, §1.2–1.3) + the **4.14 kernel** line (stock 4.14.141; AgentFabulous kernel `android-11.0`, last push 2022-06-23). The pinned kernel section is explicit that A11+ kernels (Power Kernel A11–16 updated **21.10.26**, Suzaku V2, NoVA, Coconut, Hydra — p=145668901 etc.) require "прошивки, основанными на образах MIUI 12.5.x". UBports uses Halium 10.0 (Android 10 base). **pmOS is the only stack that abandons this base** (mainline kernel 6.16.4 — but then audio/camera/wifi/bt/gps/modem are broken per Nura wiki). Inference: "newest ROM" ≠ "newest drivers" on begonia; nothing newer than A11 vendor blobs exists to build on. Confidence: high for the compat statements (quoted), medium for the generalization across all ROMs.

---

## 5. Limitations
- **Live XDA blocked**: xdaforums.com returns a bunny.net challenge for both web_extract and the headless browser (3× tested per shared context). The megathread https://xdaforums.com/t/guide-info-psa-redmi-note-8-pro-megathread-cfw.4056527/ was therefore consulted **only via the pre-verified Wayback snapshot** listed in CONTEXT (http://web.archive.org/web/20260415164458/...); no additional XDA pages were fetched within budget. Anything obtainable only from live XDA is **pending human-browser check**.
- **xmfirmwareupdater.com/device/begonia/ → HTTP 404** (verified). The working paths are `/miui/begonia/`, `/firmware/begonia/`, `/vendor/begonia/`, and an archive at `/archive/miui/begonia/` (not fetched — call budget); the "latest" table shows only the final 17 entries, so the full per-region MIUI history relies on the 4PDA pinned index.
- **wiki.lineageos.org/devices/begonia/ → HTTP 404** (verified) — basis for "LineageOS unofficial" claim.
- **Exact dates of most unofficial ROM releases** are not extractable from the pinned index (permalinks only); dating by pid ordering is marked inferred. Per-post fetches were out of budget.
- **Baseband/modem firmware versions**: no consulted source states them (xmfwu firmware page exists but unfetched).
- **Evolution X / PixelExperience official-site status** (evolutionx.rocks, pixelexperience.net) not fetched; "official" labels rest on 4PDA index wording.
- **Mu-Silicium begonia port sources**: promised on GitHub ("исходники выложу на Github Mu-Silicium"); the repo exists and is active, but its begonia device folder was not individually verified.

## 6. Contradictions found (summary)
1. Shipped MIUI: Nura wiki "Android 9 (MIUI 11)" vs 4PDA-era MIUI 10 `V10.4.5.0.PGGEUXM` + Sept-2019 CN weeklies → likely shipped MIUI 10 (inferred, medium).
2. Global last 12.5: "Stable" (4PDA V12.5.8.0) vs "Stable Beta" + stable V12.5.1.0 (xmfwu).
3. Russia last 12.5: V12.5.4.0 (4PDA) vs V12.5.3.0 stable / V12.5.5.0 stable-beta (xmfwu).
4. CN weekly last: V21.10.15 (4PDA) vs 21.11.24 (xmfwu).

---

## 7. Per-ROM source inventory (appended 2026-11-21; user-mandated)

Method: GitHub API NOT used (shared quota exhausted). Verification = `git ls-remote --symref` branch listings + raw.githubusercontent.com file fetches + github.com topics/tree HTML + web_search, all executed 2026-11-21. `verified-direct` = seen by this pass; `seed` = orchestrator-verified 2026-11-21; `inferred` = derived. Kernel deep-dive per kernel lives in 03-KERNEL-HISTORY.md (not duplicated). Ready-build links remain in §1–§3; this section adds development sources.

⚠️ **Seed correction (verified-direct, high confidence):** orchestrator seeds attributed lineage-* kernel branches (lineage-17.1/21/22.2/23.0/24.0) to `AgentFabulous/begonia`. Live branch listing shows `AgentFabulous/begonia` has exactly **12 branches** (a10-rebase, android-9.0, android-10.0/-orig/-staging, android-11.0/-cfw/-old/-staging, android-12.0, mali-merge, staging; default `android-11.0`) and **no lineage-\* branches**. The lineage-* branches live in **`LineageOS/android_kernel_xiaomi_mt6785`** (lineage-17.1, lineage-20, lineage-21, lineage-22.2, lineage-23.0, lineage-23.2, lineage-24.0; default lineage-24.0). The seed's kernel-version claims (4.14.194/340-openela/356/356-openela-rc1, 4.19.325) stand, re-attributed to this repo.

### 7.1 Official MIUI (all §1 rows; CSV rows 2–22)

| component | URL | branch/ref | verified | confidence |
|---|---|---|---|---|
| kernel (A9 / PGG builds) | https://github.com/MiCode/Xiaomi_Kernel_OpenSource | `begonia-p-oss` @03ffbf5 (seed) | ls-remote 2026-11-21 + seed | high |
| kernel (A10 / QGG builds) | https://github.com/MiCode/Xiaomi_Kernel_OpenSource | `begonia-q-oss` @4e3bb1f (seed) | ls-remote + seed | high |
| kernel (A11 / RGG builds) | https://github.com/MiCode/Xiaomi_Kernel_OpenSource | `begonia-r-oss` @777ef5d (seed) | ls-remote + seed | high |
| device tree | not found — Xiaomi publishes kernel source only; no begonia device tree in MiCode org | — | searched: MiCode org | high (absence) |
| vendor | binaries only: https://xmfirmwareupdater.com/vendor/begonia/ + /firmware/begonia/; source-level community dumps: https://github.com/ZIDAN44/redmi_begonia_dump (15 branches, V11.0.4→V12.5.7 Global/CN/weeklies) and https://github.com/ZyCromerZ/redmi_begonia_dump (24 branches, A9 PGG → A11 RGG, IDXM/EUXM/RUXM/MIXM) | dump branches named per MIUI build | ls-remote | high |
| manifest | n/a — prebuilt zips; install docs: 4PDA MIUI pinned p=88821588 | — | cached | high |

### 7.2 Kernel / vendor base bundles (CSV rows 23–26)

| entry | source | branch/ref | verified | confidence |
|---|---|---|---|---|
| MIUI 12.5 vendor base | MiCode `begonia-r-oss` @777ef5d + xmfwu vendor page | seed + ls-remote | verified-direct + seed | high |
| Stock kernel 4.14.141 | MiCode `begonia-p-oss`/`begonia-q-oss` (4.14 line) | ls-remote; sublevel per devices.ubuntu-touch.io | verified-direct | high |
| AgentFabulous kernel | https://github.com/AgentFabulous/begonia | 12 branches, see §7 intro; default android-11.0; Makefile VERSION=4 (raw) | verified-direct | high |
| Power Kernel | https://github.com/Saikrishna1504/kernel_xiaomi_mt6785 | `main` (default), `kaeru` | ls-remote + pointer in cvnertnc/Begonia-Kernel-Builder README (raw-fetched) | high |
| AkameKernel | https://github.com/Anonym3310/AkameKernel-begonia | `Q-OSS-SLMK` (default), `CFW` | ls-remote | high |
| Pox Kernel | https://github.com/txorav/pox-kernel-begonia | `main`, `onyx` (Rock Editions Granite/Obsidian/Onyx per topics page) | ls-remote | high |
| Kernel CI builder | https://github.com/cvnertnc/Begonia-Kernel-Builder (KernelSU-Next+SUSFS, archived) ← fork of https://github.com/PhamtomK12/Android-Kernel-Builder | main | raw README | high |
| TWRP trees | https://github.com/HyperTeam/android_device_redmi_begonia-TWRP (`android-9.0`); https://github.com/BitsAndBytes-dev/twrp_device_redmi_begonia (`11`) | ls-remote | verified-direct | high |

### 7.3 GSI rows (§2; CSV rows 27–37)

| component | URL | branch/ref | verified | confidence |
|---|---|---|---|---|
| GSI framework (A10 era) | https://github.com/phhusson/treble_experimentations | master | ls-remote | high |
| GSI framework (TrebleDroid, current) | https://github.com/TrebleDroid/treble_experimentations | master | ls-remote | high |
| begonia GSI adaptation | https://github.com/reddxae/begonia-gsi-adaptation | main | ls-remote | high |
| kernel/vendor under GSIs | stock MIUI vendor+kernel (§7.1–7.2) — GSI replaces system only | per base: q-oss/r-oss | inferred | high |
| per-build sources (Bliss GSI, RR GSI, PE GSI, crDroid GSI by rvtom1970/timjosten/User-_-Name/bugreporter) | not found (searched: 4PDA posts p=107855537, 102565322, 112878843, 114061722, 121096835, 106451290, 110287291; GitHub) | — | — | — |
| HarmonyOS 4.0.0.112 / MagicOS 7.1 Beta ports | not found (closed ports; searched: 4PDA p=145551659 / p=145549738, GitHub) | — | — | — |

### 7.4 crDroid (§3.1)

| ROM (CSV row) | kernel | device tree | vendor | manifest | verification |
|---|---|---|---|---|---|
| crDroid 6.27 FINAL A10 (38) | AgentFabulous/begonia @android-10.0 (inferred) | not found (crdroidandroid org starts at 12.0; searched: crdroidandroid org, GitHub, 4PDA p=97822397) | not found for A10 (crdroid vendor org starts 12.0) | https://github.com/crdroidandroid/android @10.0 (branch verified) | mixed |
| crDroid 7.2/7.x A11 (39) | https://github.com/AgentFabulous/begonia @android-11.0 — **verified** via MaloyBegonia tree `lineage.dependencies` | https://github.com/MaloyBegonia/android_device_redmi_begonia_crDroid @11.0 (verified) | referenced as `vendor_redmi_begonia` in deps; MaloyBegonia/vendor_redmi_begonia **not found** (searched: GitHub) | https://github.com/crdroidandroid/android @11.0 (branch verified) | verified-direct |
| crDroid 8.x A12 (40) | https://github.com/crdroidandroid/android_kernel_xiaomi_mt6785 @12.1 (org kernel branches 12.1/13.0/14.0; pairing to 12.0 inferred) | https://github.com/crdroidandroid/android_device_redmi_begonia @12.0 (verified; crdroid.dependencies 404 for 12.0) | https://github.com/crdroidandroid/android_vendor_redmi_begonia @12.0 + android_vendor_redmi_begonia-ims @12.0 (verified) | https://github.com/crdroidandroid/android @12.0 (verified) | verified-direct |
| crDroid 9.x A13 (41) | crdroidandroid/android_kernel_xiaomi_mt6785 @13.0 (**verified** via crdroid.dependencies @13.0) | android_device_redmi_begonia @13.0 (verified) | android_vendor_redmi_begonia @13.0 + -ims @13.0 (verified) | crdroidandroid/android @13.0 (verified) | verified-direct |
| crDroid 10 A14 (42) | crdroidandroid/android_kernel_xiaomi_mt6785 @14.0 (**verified** via crdroid.dependencies @14.0; deps also pull begonia-dev/android_packages_apps_RevampedFMRadio) | android_device_redmi_begonia @14.0 (verified) | android_vendor_redmi_begonia @14.0 (verified; -ims latest is 13.0) | crdroidandroid/android @14.0 (verified) | verified-direct |
| crDroid v12.11 UNOFFICIAL A16 (43) | not found (crdroidandroid kernel max 14.0; LineageOS kernel lineage-23.x/24.0 pairing unconfirmed; searched: crdroidandroid org, LineageOS org, begonia-dev, GitHub, 4PDA p=143929573) | not found (crdroidandroid org max 14.0; searched: orgs, GitHub) | not found (no 15/16 vendor branches) | not found (unofficial; searched: GitHub) | not found |

### 7.5 LineageOS (§3.2)

| component | URL | branch/ref | verified | confidence |
|---|---|---|---|---|
| kernel for all LOS-based builds | https://github.com/LineageOS/android_kernel_xiaomi_mt6785 | lineage-17.1, lineage-20, lineage-21, lineage-22.2, lineage-23.0, lineage-23.2, lineage-24.0 (7 branches, default lineage-24.0) | ls-remote | high |
| LOS org device tree | https://github.com/LineageOS/android_device_xiaomi_begonia + https://github.com/LineageOS/android_device_xiaomi_mt6785-common | lineage-17.1 only (deps → mt6785-common) | ls-remote + lineage.dependencies | high |
| per-build trees (LOS 20 / 22.2 / 23.x unofficial) | not found (searched: LineageOS org — only 17.1; begonia-dev, xiaomi-begonia-dev, WuXing90 [avium-only], GitHub, 4PDA p=118200298, p=145635495, p=145712732) | — | — | — |

### 7.6 PixelExperience / PixelOS (§3.3)

| ROM | kernel | device tree | vendor | manifest |
|---|---|---|---|---|
| PE 11–14 (47) | https://github.com/PixelExperience-Devices/kernel_xiaomi_begonia — branches ten, eleven(+cfw/old), twelve(+old), thirteen, fourteen, q-oss (verified; default fourteen) | https://github.com/PixelExperience-Devices/device_xiaomi_begonia — ten…thirteen-plus (+wip/cfw) (verified) | not found (PixelExperience-Devices/vendor_xiaomi_begonia absent; searched: GitHub) | https://github.com/PixelExperience/manifest — ten…fourteen (+plus) (verified) |
| PixelOS 16.2 (48) | not found (searched: PixelOS-AOSP org, GitHub, 4PDA p=144357321) | not found (PixelOS-AOSP/android_device_xiaomi_begonia absent; searched: GitHub) | not found | https://github.com/PixelOS-AOSP/manifest — eleven…sixteen (verified) |

### 7.7 Evolution X (§3.5; CSV 51–53)

| component | URL | branch/ref | verified |
|---|---|---|---|
| device tree | https://github.com/Evolution-X-Devices/device_redmi_begonia (org renamed → Evolution-XYZ-Devices; both URLs resolve) | `ten`, `ten-retrofit`, `elle` (default ten) — A10-era only | ls-remote |
| vendor | https://github.com/Evolution-XYZ-Devices/vendor_redmi_begonia | `ten`, `elle` | ls-remote |
| kernel | not found in EX org (searched: Evolution-X-Devices, Evolution-XYZ-Devices, GitHub); LOS-org kernel lineage-21/23.x is the likely base for A14/A16 builds (inferred, low) | — | — |
| manifest | not found (EvolutionX/manifest, EvolutionX-Devices/manifest, EvolutionX/platform_manifest all absent; searched: GitHub) | — | — |

A11/A14/A16 EX builds ride the same org repos only for the ten-era; newer per-build trees not found.

### 7.8 AxionAOSP (§3.6; CSV 54–55)

| component | URL | branch/ref | verified |
|---|---|---|---|
| device tree | https://github.com/AxionAOSP-devices/android_device_redmi_begonia | `axion` (default), `bka`, `vic` | ls-remote |
| kernel | likely https://github.com/WuXing90/kernel_xiaomi_mt6785 @`bka` (branch-name match with device tree; pairing unverified) | bka, erofs | inferred (medium) |
| vendor | not found (AxionAOSP-devices/vendor_redmi_begonia absent; searched: GitHub) | — | — |
| manifest / build docs | manifest not found (AxionAOSP/manifest absent); install guide: https://github.com/AxionAOSP/official_devices @main `Wiki/begonia.md` (raw-fetched, verified) | — | mixed |

### 7.9 AviumUI / WuXing90 MIUI-class ports (CSV 65)

| component | URL | branch/ref | verified |
|---|---|---|---|
| device tree | https://github.com/WuXing90/device_redmi_begonia | `avium-16`, `avium-16.2` (default), `avium-17` | ls-remote |
| kernel | not found per-build (searched: GitHub, 4PDA p=146024411) | — | — |
| vendor / manifest | not found (searched: GitHub) | — | — |

### 7.10 Other OEM ports (CSV 66–71: ColorOS 16/17, OriginOS 4/6/Ocean/3.1, EMUI 14.2, Flyme 10, ROGUI 14)
All components **not found** (closed zip-only ports; searched: 4PDA posts p=144433439, 144473382, 145345569, 146083465, 146061439, 145985251, 131543971, 134414587, 143563437, 112676744, 143523197, 145406321, 141706486; GitHub). They repack the MIUI 12.5 vendor base (§1.3, §7.1–7.2).

### 7.11 Long-tail AOSP ROMs (§3.8; CSV 49–50, 56–64)

Shared, ls-remote-verified community infrastructure (per-ROM mapping not established):

| org / repo | covers | branches |
|---|---|---|
| begonia-dev: android_kernel_xiaomi_mt6785 / android_device_redmi_begonia / android_vendor_redmi_begonia | A11–A14 kernel+device+vendor trio | 11.0, 12.0, 12.1, 13.0, 14.0 (kernel adds -bak/-staging/-data) |
| xiaomi-begonia-dev: android_device_redmi_begonia (≡ android_device_xiaomi_begonia) / android_vendor_xiaomi_begonia | A13/A14 device+vendor (incl. Halcyon) | aosp-13, fourteen (default), halcyon, wip / aosp-13, fourteen, tmp |
| Trinity-ROMS: android_device_redmi_begonia / android_vendor_redmi_begonia / android_vendor_redmi_begonia-ims | A13/A14/A16 | device 13, 14; vendor 13, 14, 16 (default) |
| BitsAndBytes-dev: android_device_redmi_begonia | A11/A12 (incl. Spark OS) | eleven, spark, twelve (default) |
| BlissRoms-Devices: android_device_xiaomi_begonia | Bliss A10/A13-era | q, typhoon (default) |
| PotatoDevices: device_redmi_begonia | Potato releases | croquette/dumaloo/frico/gnocchi -release/-staging (default frico_mr1-release) |
| theimpulson: android_device_xiaomi_begonia (+android_device_xiaomi_mt6785-common) | early LOS 17.1 dev | lineage-17.1(+parts/_final), rebase-final |
| crdroidandroid: android_vendor_redmi_begonia-ims | A12–A13 IMS blobs | 12.0, 12.1, 13.0 |
| blobs mirror: AndroidBlobs/vendor_redmi_begonia | vendor blobs dump | (search hit, not branch-listed this pass) |

Per-ROM kernel (inferred): begonia-dev kernel @matching 11.0–14.0 branch for A11–A14; LineageOS kernel @lineage-22.2/23.x/24.0 for A15/A16 (branches verified, pairing inferred). Device/vendor/manifest per individual ROM: **not found** (searched: GitHub org naming per ROM, github.com/topics/begonia index, 4PDA posts).

### 7.12 Ubuntu Touch (CSV 73)

| component | URL | branch/ref | verified |
|---|---|---|---|
| kernel | https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/kernel-xiaomi-mt6785 | halium-10.0 | GitLab API tree fetch 2026-11-21 + shared context |
| device/Halium config | https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia | master (overlay/, ramdisk-overlay/, ramdisk-recovery-overlay/) | GitLab API tree fetch |
| vendor | stock MIUI vendor via Halium — no separate repo found (searched: UBports porting group) | — | — |
| manifest | not found (UBports halium tooling; no per-device local_manifest located) | — | — |

### 7.13 postmarketOS (CSV 74)

| component | URL | branch/ref | verified |
|---|---|---|---|
| mainline kernel | https://github.com/Dinolek/mt6785-mainline | 6.16, 7.1 (default), battery-downstream | ls-remote |
| device package | gitlab.nura.eco/nura/pmaports → device/testing/device-xiaomi-begonia | main | context-verified; raw+API fetch blocked by Anubis bot-check this pass |
| kernel package | gitlab.nura.eco/nura/pmaports → device/testing/linux-postmarketos-mediatek-mt6785 | main | same |
| manifest | pmaports repo itself; initial MR https://gitlab.nura.eco/nura/pmaports/-/merge_requests/1909 | — | context |
| vendor | n/a (mainline; no vendor blobs) | — | — |

### 7.14 Mu-Silicium UEFI (CSV 72)

| component | URL | branch/ref | verified |
|---|---|---|---|
| UEFI firmware source | https://github.com/Project-Silicium/Mu-Silicium | main (BootShim/Common/Platforms/Silicon tree verified) | ls-remote + tree HTML |
| begonia device package | **not found** — searched Platforms/Xiaomi: 36 device packages (aliothPkg…willowPkg), **no begoniaPkg** → KiryxaMeow's begonia port sources not yet published in the main repo (matches §3.9 caveat, now verified absence) | — | verified absence |
| build/install | 4PDA p=146118602 (KiryxaMeow: `fastboot flash boot UEFI.img`, WinPE from SD) | — | cached |

### 7.15 Source-inventory contradictions & limitations
1. Seed correction: lineage-* kernel branches are on `LineageOS/android_kernel_xiaomi_mt6785`, not `AgentFabulous/begonia` (§7 intro).
2. crdroidandroid kernel/device/vendor branches start at 12.0/12.1 — official crDroid 6/7 (A10/A11) trees are not in the org (A11-era MaloyBegonia fork verified instead; TTTT555 originals not found).
3. crdroidandroid/android_vendor_redmi_begonia-ims has no 14.0 branch although crdroid.dependencies@14.0 references it (repo default 13.0).
4. gitlab.nura.eco (raw + API) behind Anubis bot-check for this toolset — pmaports file-level verification pending human browser; facts cited from orchestrator-verified context.
5. Evolution X org renamed Evolution-X-Devices → Evolution-XYZ-Devices; only A10-era (`ten`) begonia trees present.
6. web_extract refused github.com this session ("private or internal network address" — false positive); ls-remote/raw/HTML-curl used instead.
7. `MaloyBegonia` crDroid tree references vendor repo `vendor_redmi_begonia` without owner; not found under that owner on GitHub.


### 7.16 Telegram ROM-updates hub (freshness source, 2026-11-21T14:05Z)

[@RedmiNote8ProUpdates](https://t.me/RedmiNote8ProUpdates) is the live release hub; web-preview `t.me/s/` readable as guest (snapshot: [archive/human-tg-redminote8proupdates-preview.html](archive/human-tg-redminote8proupdates-preview.html)). Releases visible there that post-date parts of this file: [Evolution X 11.6.2 A16 QPR2 (2026-03-23)](https://t.me/RedmiNote8ProUpdates/1613), [Lunaris-AOSP 3.8→3.12 EOL (2026-09-18)](https://t.me/RedmiNote8ProUpdates/1656), [LineageOS v23.2 A16 UNOFFICIAL (2026-03-30; XDA t=4783655)](https://t.me/RedmiNote8ProUpdates/1616), [MistOS 4.5 A16 (2026-04-07)](https://t.me/RedmiNote8ProUpdates/1617). Related channels: [@RedmiNote8ProOfficial](https://t.me/RedmiNote8ProOfficial) (chat), [@wuxinboys](https://t.me/wuxinboys) (wuxinG90 builds + Unified-TWRP), [@begoniadump](https://t.me/begoniadump) (support/SourceForge), [@danascapeprojects](https://t.me/danascapeprojects) (LOS support). For anything newer than this file's rows, the channel posts are the primary release notes.


### 7.17 Device-tree repos found via plain web search (2026-11-21T15:10Z)

Owner correction applied: previous 'not found' verdicts must be re-checked with a plain web search. Immediately found and previously unindexed: [TTTT555/device_xiaomi_begonia](https://github.com/TTTT555/device_xiaomi_begonia), [begonia-dev-space/android_device_redmi_begonia](https://github.com/begonia-dev-space/android_device_redmi_begonia), [xiaomi-begonia-dev/android_device_redmi_begonia](https://github.com/xiaomi-begonia-dev/android_device_redmi_begonia) — A9-era device trees whose READMEs also state the battery: **Non-removable Li-Po 4500 mAh** [V-README, medium] — resolves part of [09-OPEN-QUESTIONS.md](09-OPEN-QUESTIONS.md) (battery model); replacement-cost docs remain open.
