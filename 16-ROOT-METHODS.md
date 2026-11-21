# 16 — Root methods registry (begonia, 2026-11-21)

Dimension: REQUIREMENTS rows 25/31-adjacent (owner request 2026-11-21: «какие существуют способы
поставить рут: патч ядра, напрямую, Magisk, KernelSU…»). Conventions: **[V]** verified against the
cited source, **[I]** inferred (reasoning stated), **[NF]** not found (search list given);
confidence high/medium/low; observation stamps ISO 8601 UTC. Cross-refs:
[07-RECOVERY-SAFETY.md](07-RECOVERY-SAFETY.md) (unlock/AVB), [03-KERNEL-HISTORY.md](03-KERNEL-HISTORY.md) (§2.3 kernel zips),
[10-GUIDE-INDEX.md](10-GUIDE-INDEX.md) (§2 root threads), [13-NETHUNTER-WIFI-EXTRAS.md](13-NETHUNTER-WIFI-EXTRAS.md) (§2 NetHunter kernel needs).


> **2026-11-21 independent update:** [20-KERNEL-419-ROOT-ECOSYSTEM-RU.md](20-KERNEL-419-ROOT-ECOSYSTEM-RU.md) extends this registry with directly checked KSU-vs-Non-KSU NoVA defconfigs/build script, KernelSU-Next `legacy` submodule, a traced 4.19 source list, current official upstream compatibility constraints, and a source-of-patches map. Read [kernel-root-provenance.csv](kernel-root-provenance.csv) for verification status. Some broad compatibility language below (for example “all MIUI 9→17” and suggestions that root can be made undetectable) is **not sufficiently evidenced** and should not be taken as device-specific certification. Root != bootloader unlock; Android root frameworks are not required for native Linux/Ubuntu Touch porting.

---

## 1. Methods matrix

| Method | What it patches | Needs | Works on begonia bases | Status (observed 2026-11-21) | Risks | Primary sources |
|---|---|---|---|---|---|---|
| **Magisk (boot.img patch)** | `boot.img` (ramdisk patch via magiskboot) | unlocked BL; stock boot.img **of the exact firmware**; TWRP or app-patch + fastboot flash | all (MIUI 9→17, all custom ROMs); historically the default | **Alive: v31.1 (2026-10-25)**, active commits to 2026-11-10 incl. "sepolicy: support domain updates in Android 17" [V, high] | per-firmware boot discipline — wrong boot.img = hard brick on MIUI10/11 era [V-verbatim]; AVB: Close AVB2.0 in TWRP [V]; detection pressure grows (Play Integrity) | [topjohnwu releases](https://github.com/topjohnwu/Magisk/releases) (v31.1), [4PDA Magisk t=774072](https://4pda.to/forum/index.php?showtopic=774072) (RU hub, v31.0+ profile), [begonia guide p=90018812](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=90018812) [V-cache] |
| **KernelSU / KernelSU-Next (+ SUSFS)** | kernel (integrated or LKM) + manager APK; SUSFS hides mounts | a kernel **built with KSU** (GKI/LKM variants exist for some kernels) or patched source; unlocked BL | needs a KSU-enabled begonia kernel; proven datapoint: Evolution X 11.6.2 ships root via dedicated kernel + KSU manager | **Alive: KSU-Next v3.4.2 (2026-10-13)**, SUSFS LKM integration 2026-10-12, commits 2026-11-17 [V, high]; Android 17 (zygote_next, GKI 6.18) implications tracked by community [V, medium] | kernel rebuild/flash; mismatched kernel = brick risk same as any boot flash; SUSFS adds hide-ability but needs matching kernel source | [KernelSU-Next repo](https://github.com/KernelSU-Next/KernelSU-Next) (v3.4.2, SUSFS LKM commit), [Evolution X recipe t.me/RedmiNote8ProUpdates/1613](https://t.me/RedmiNote8ProUpdates/1613) ("flash this kernel and use this manager": kernel + [KernelSU_v3.0.0-30-legacy APK](https://github.com/rsuntk/KernelSU/releases/download/v3.0.0-30-legacy/KernelSU_v3.0.0-30-legacy_32334-release.apk)) [V-quote] |
| **APatch** | kernel image patch (KernelPatch core) — root at kernel level | boot.img patch via APatch app (no TWRP needed), ARM64 only | architecture-independent in principle; **no begonia-specific APatch guide found** [NF, searched list §5] | active project [V, high]; ARM64 ✓ (begonia is aarch64) [V] | kpatch on MTK 4.14 kernels unproven for begonia — treat as experimental until a device datapoint appears | [bmax121/APatch](https://github.com/bmax121/APatch), [4PDA APatch t=1082492](https://4pda.to/forum/index.php?showtopic=1082492) |
| **SukiSU-Ultra** | kernel-level root, KPM modules (ported from APatch) | kernel with SukiSU integration or GKI/LKM path | same as KSU — kernel-dependent; begonia datapoint not found [NF] | active ("SukiSU Nova" site, KPM support) [V, medium] | same kernel-match risks | [sukisu.org](https://sukisu.org/), [XDA comparison thread](https://xdaforums.com/t/comparison-kernelsu-vs-magisk-vs-apatch-which-root-solution-is-best-in-2025.4752338/), [4PDA SukiSU t=1108076](https://4pda.to/forum/index.php?showtopic=1108076) |
| **Custom kernels with root features** | whole kernel (prebuilt zip via TWRP/AnyKernel) | matching ROM base + firmware; unlocked BL | MIUI 12.0/A10-era (Akame), A11/12 (Coconut), A16 (Suzaku-based ROMs) | see [03 §2.3](03-KERNEL-HISTORY.md); **Suzaku V2**: "KernelSU 35053 + SUS-FS 2.2.0" claims [V-quotes, medium — repo not public [NF]]; **AkameKernel**: NetHunter feature set, stale (2023-03) [V, high] | kernel/ROM/base mismatch; front-camera-revision warning on some non-CFW A10 kernels [V-verbatim in 03 §3.2] | [03 §2.3 kernel zips table](03-KERNEL-HISTORY.md), [AkameKernel](https://github.com/Anonym3310/AkameKernel-begonia), [cvnertnc/Begonia-Kernel-Builder](https://github.com/cvnertnc/Begonia-Kernel-Builder) (KSU-Next+SUSFS CI, self-archived 2026-09-16 — fork-and-run template [V, high]) |
| **mtkclient-assisted (direct)** | N/A for root itself — this is the **prerequisite chain**: BROM-mode BL unlock (`mtk da seccfg unlock`) without Xiaomi wait-time | Linux/macOS host, USB-C cable; no testpoint needed on begonia | all bases (bootloader unlock is ROM-independent) | verified path per [pmOS wiki + 07](07-RECOVERY-SAFETY.md) [V, high]; no public MT6785 exploit-root (mtk-su targets older MTK chips) [NF — searched: 'mtk-su MT6785', 'mediatek mt6785 exploit root'] | unlock wipes data; seccfg corruption risk handled by mtkclient backups | [mtkclient README-USAGE](https://github.com/bkerler/mtkclient/blob/main/README-USAGE.md#unlock-bootloader), [07 §unlock](07-RECOVERY-SAFETY.md) |

---

## 2. Method details (begonia-specific)

### 2.1 Magisk — the historical default, still first-line
- **The verbatim begonia recipe** (captured full-text 2026-11-21 with owner login, [archive/human-4pda-90018812-spoilers-full.html](archive/human-4pda-90018812-spoilers-full.html), [07 §N.1](07-RECOVERY-SAFETY.md)):
  MIUI10/11-era flow — MTK drivers → fastboot → `fastboot flash recovery recovery.img` (TWRP 3.3.1-9)
  → in TWRP: mount data/system/vendor/nvdata → **delete `system_root/system/recovery_fromboot.p`**
  → **flash Close AVB2.0** → flash `SuperSu_installer.zip` (contains **Magisk 19.4**, patches boot) →
  "ROOT ПОЛУЧЕН". Rescue path: re-flash stock boot.img + recovery of **the exact firmware** —
  "Стоковый boot.img от MIUI10 EU, прошивка этого файла на MIUI11 превращает телефон в КИРПИЧ" [V-verbatim].
  Modern mapping [I, high]: same skeleton, Magisk 19.4 → current **v31.1** app-based "Install to inactive
  slot/boot" or TWRP flash; Magisk Hide → Zygisk + DenyList/PlayIntegrityFix modules (module ecosystem
  catalog: [4PDA t=915158](https://4pda.to/forum/index.php?showtopic=915158)).
- **Status answer to "Magisk лиустред/убит?"**: no — v31.1 released 2026-10-25 with commits through
  2026-11-10 including Android 17 sepolicy support [V, high].

### 2.2 KernelSU family — where begonia actually has datapoints
- **Evolution X 11.6.2 (A16) official root path** (channel post, [t.me/RedmiNote8ProUpdates/1613](https://t.me/RedmiNote8ProUpdates/1613), 2026-03-23):
  "If you need root, please flash [this kernel](https://pixeldrain.com/u/oAdsLaJq) and use this
  [manager](https://github.com/rsuntk/KernelSU/releases/download/v3.0.0-30-legacy/KernelSU_v3.0.0-30-legacy_32334-release.apk)"
  [V-quote, high] — i.e. kernel-swap + legacy-KSU manager, **no TWRP root-zip involved**.
- **Suzaku V2 kernel** (2026-08-07, @WuxinG90): "KernelSU 35053 + SUS-FS 2.2.0", AOSP Clang 21,
  "based on Power kernel" [V-quotes, medium]; used by [EvolutionX 16.0](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=144852836)
  and Project Infinity X 3.12 (p=144878394); public repo **not found** (searched: web
  'Suzaku kernel begonia github', 'TTTT555/Suzaku', cache greps — TTTT555 search instead surfaced
  [device trees](https://github.com/TTTT555/device_xiaomi_begonia)) [NF, medium].
- **cvnertnc/Begonia-Kernel-Builder**: KSU-Next+SUSFS daily CI for begonia; **self-archived 2026-09-16**
  ("I don't have much time anymore") — reusable as fork-and-run template [V, high].
- **Nova-Kernels** ([Nova-Kernels/kernel_xiaomi_mt6785](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785),
  4.14.356, push 2026-10-03): active tree; KSU-Next integration status **unverified** (checked commits
  list only; search 'Nova-Kernels kernelsu' not yet run — registered as open follow-up).
- Community context: Android 17's `zygote_next`/GKI 6.18 changes are being tracked by the KSU/SUSFS
  ecosystem ([privacyportal analysis, 2026-08-28](https://www.privacyportal.co.uk/blogs/free-rooting-tips-and-tricks/android-17-zygote-next-implications-for-kernelsu-susfs-and-module)) [V, medium]; begonia's 4.14 non-GKI kernels are unaffected by GKI specifics but
  SUSFS/manager compatibility still applies [I, medium].

### 2.3 APatch / SukiSU on begonia — honest gap
- Both are active kernel-level projects (ARM64-only for APatch [V]); both patch boot images or need
  kernel integration. **No begonia-specific build/guide found for either** (searched: web
  'APatch begonia', 'SukiSU begonia MT6785', 4PDA cache greps 'apatch|sukisu' — the RU threads
  [t=1082492](https://4pda.to/forum/index.php?showtopic=1082492), [t=1108076](https://4pda.to/forum/index.php?showtopic=1108076)
  are generic-device hubs) [NF, medium].
- Plausible route [I, low-medium]: APatch patches stock boot.img directly (no TWRP), which suits
  begonia's per-firmware boot discipline; KernelPatch's MTK 4.14 support is the open question —
  would need one device datapoint or a kernel-source check before claiming anything.

### 2.4 Direct/exploit methods
- **No public exploit-root for MT6785** [NF, medium-high] (searched: 'mtk-su MT6785', 'mediatek
  mt6785 exploit root 2026', cache greps). mtkclient's role is the unlock prerequisite, not root:
  [mtk da seccfg unlock](https://github.com/bkerler/mtkclient/blob/main/README-USAGE.md#unlock-bootloader) —
  no Xiaomi wait-time, works cable-only ([07 §unbrick/unlock](07-RECOVERY-SAFETY.md)) [V, high].
- Old SuperSU-era zips: the captured guide's `SuperSu_installer.zip` actually carried **Magisk 19.4**
  [V-cache]; plain SuperSU is obsolete — do not use on modern ROMs [I, high].

---

## 3. Telegram channels (root/ROM intel for begonia)

| Channel | What it publishes | Freshness (observed 2026-11-21) |
|---|---|---|
| [@RedmiNote8ProUpdates](https://t.me/RedmiNote8ProUpdates) | ROM releases (Evolution X, Lunaris, MistOS, LOS 23.2) **+ root recipes** (the KSU kernel+manager recipe) | latest visible post 2026-11-17 [V] |
| [@RedmiNote8ProOfficial](https://t.me/RedmiNote8ProOfficial) | device chat (support) | linked from the hub [V] |
| [@wuxinboys](https://t.me/wuxinboys) | wuxinG90 builds, **Unified-TWRP** posts (t=1002), kernel uploads | active [V — linked in release posts] |
| [@begoniadump](https://t.me/begoniadump) | support + SourceForge mirrors (begoniadump project) | active [V — linked] |
| [@danascapeprojects](https://t.me/danascapeprojects) | LOS 23.2 support by @danascape | linked [V] |
| [@Saikrishna1504](https://t.me/Saikrishna1504) | maintainer personal: v4.19 kernel port testing ([post 1657](https://t.me/RedmiNote8ProUpdates/1657)) | 2026-11-17 [V] |

Web preview note: `t.me/s/<channel>` is readable as guest — no joining required
(snapshot: [archive/human-tg-redminote8proupdates-preview.html](archive/human-tg-redminote8proupdates-preview.html)).

---

## 4. Recommendation snapshot [I, high]

- **Stock MIUI / simple custom ROM** → Magisk v31.1 via boot patch (per-firmware boot.img discipline!)
  or via the ROM's own instructions.
- **Modern A16 custom ROMs** → the ROM's bundled kernel root path (Evolution X-style: KSU-enabled
  kernel + matching manager); do NOT mix kernels across ROM bases.
- **Undetectability needs (banking)** → kernel-level (KSU-Next+SUSFS or APatch-class) with a matching
  kernel build — on begonia today that means Suzaku-based ROMs or a self-built kernel from
  Nova-Kernels/cvnertnc template; no turnkey APatch/SukiSU guide exists for this device yet.
- **Never** flash boot.img/recovery from a different firmware generation (MIUI10↔11 hard-brick rule) [V-verbatim].

## 5. Not-found ledger (searched, 2026-11-21)

- Suzaku V2 public repo: web ('Suzaku kernel begonia github', 'TTTT555/Suzaku'), 4PDA cache greps →
  only 4PDA release posts [NF].
- APatch/SukiSU begonia builds or guides: web + 4PDA cache → none [NF].
- MT6785 exploit-root (mtk-su-class): web → none [NF].
- Nova-Kernels KSU-Next integration: commit list only; deeper search pending (next session follow-up).
