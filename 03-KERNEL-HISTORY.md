# Begonia (Xiaomi Redmi Note 8 Pro, MT6785) — Kernel History

Research date: 2026-11-21 (JST). Dimension: kernels. Method: GitHub/GitLab APIs (curl/urllib), raw.githubusercontent Makefile heads, kernel.org cgit, Wayback snapshot of XDA megathread, cached 4PDA pages. No git commands; research-only.
Legend: **[V]** = verified directly (API/page/file fetched by this task, with URL+ref); **[I]** = inferred (marked with basis); confidence given per claim (high/medium/low).

---

## 1. Stock kernel (Xiaomi/MIUI)

Xiaomi published three OSS kernel drops for begonia in [MiCode/Xiaomi_Kernel_OpenSource](https://github.com/MiCode/Xiaomi_Kernel_OpenSource) (branches found via GitHub API `git/matching-refs/heads/begonia` [V]):

| Branch | Linux base (Makefile [V]) | Android/MIUI era | Last commit (GitHub API [V]) | HEAD SHA |
|---|---|---|---|---|
| `begonia-p-oss` | **4.14.94** | Android 9 (P) — the shipping MIUI 11 base | 2019-09-04 "Kernel: Xiaomi kernel changes for Redmi Note 8 Pro Android P" | `03ffbf50810a` |
| `begonia-q-oss` | **4.14.141** | Android 10 (Q) / MIUI 12 updates | 2020-04-16 "Kernel: Xiaomi kernel Opensource changes for Redmi Note 8 Pro Android Q" | `4e3bb1fabfa8` |
| `begonia-r-oss` | **4.14.186** | Android 11 (R) / MIUI 12.5 era — final OEM drop | 2021-07-23 "Kernel: Xiaomi kernel changes for Redmi Note 8 Pro Android R" | `777ef5dfc3c9` |

- The widely-cited "stock kernel 4.14.141" (UBports device page, cached: "Kernel version on the device is 4.14.141", https://devices.ubuntu-touch.io/device/xiaomi-begonia/ [V-cache]) corresponds to the **Q-drop sublevel**; the device actually shipped on a 4.14.94-era (P) kernel. Sublevels on retail OTA builds may differ from OSS drops — not verifiable from sources alone [I, medium].
- OEM kernel support ended with the R drop (2021-07-23) [V: last commit date]. All stock trees are Linux 4.14 LTS, aarch64.
- Boot chain context (from cached pmOS/Nura wiki, oldid=109575): BROM→PL→LK→Linux; the LK/preloader constrains kernel choice (see §2 a10-rebase).

## 2. Android kernel forks

### 2.1 AgentFabulous/begonia (the community base, 2020–2022)

https://github.com/AgentFabulous/begonia — "Linux kernel source tree for the Redmi Note 8 Pro (xiaomi-mt6785)", 37★/45 forks, default branch `android-11.0`, **repo last push 2022-06-23T06:47:15Z** [V, matches context pack]. 12 branches, **all Linux 4.14.x** (GitHub API `branches/<name>` [V]; sublevels from Makefile heads on `a10-rebase`, `android-11.0`, `android-12.0` [V] or merge-commit messages [V]):

| Branch | HEAD SHA | Last commit (UTC) | Linux 4.14 sublevel | Android base | Role / used by |
|---|---|---|---|---|---|
| android-9.0 | `ff0b71e56b65` | 2020-03-08 | ≥151 (merge tag v4.14.151) [V-msg] | 9 | early AOSP/GSI-era ROMs [I] |
| android-10.0-orig | `3a37ea505cbe` | 2020-06-02 | 4.14.x | 10 | experimental A10 base [I] |
| staging | `186e9186f6fc` | 2020-06-18 | ≥184 (merge 4.14.184) [V-msg] | n/a | scratch [I] |
| mali-merge | `12bb2a97bf7e` | 2020-05-21 | 4.14.x | n/a | Mali GPU driver merge experiment [I, name+msg "makefile"] |
| android-10.0-staging | `d66a5f3cff67` | 2020-07-01 | ≥187 (merge 4.14.187) [V-msg] | 10 | staging [I] |
| android-10.0 | `7af84a8219ed` | 2020-08-22 | 4.14.x | 10 | A10 ROMs [I] |
| a10-rebase | `b53d72147672` | 2021-01-27 | **4.14.141** (Makefile [V]) | 10 | Agent_fabulous's A10 ROM line — see below [V] |
| android-11.0-cfw | `78b3211ba301` | 2021-01-31 | ≥218 (merge 4.14.218) [V-msg] | 11 | CFW (custom-firmware) builds [I, name] |
| android-11.0-old | `bb856f0cd8b0` | 2021-07-05 | 4.14.x | 11 | superseded A11 line [I] |
| android-11.0-staging | `c05b8353e2cb` | 2021-09-02 | 4.14.x | 11 | staging [I] |
| android-11.0 (default) | `d7a53936ff22` | 2021-10-31 | **4.14.253** (Makefile [V]) | 11 | A11 ROMs, e.g. LOS 18.1-era [I] |
| android-12.0 | `143df718861d` | 2022-06-23 | **4.14.284** (Makefile [V]) | 12 | A12-era ROMs — the tree's final push [I] |

**a10-rebase rationale** (Agent_fabulous's own post, XDA megathread, Wayback capture 2026-04-15 [V-Wayback]):
> "the A10 kernel source released by Xiaomi does not work with the factory bootloader/preloader, which was the reason I worked on a new kernel source based on Android 9 (A9) with several Android 10 (A10) drivers to work nicely with the A10 blobs."

Same thread (post by Agent_fabulous, ROM created 2020-02-24, updated 2020-10-26) lists for his A10 ROM: "Device Tree - branch android-10, Vendor Tree - branch android-10, Kernel - branch master … ROM Kernel: Linux 4.x" [V-Wayback] — i.e. the ROMs used the AF tree (branch names evolved: master → a10-rebase/android-10.x/android-11.x lines) [I for exact branch↔ROM pairing].
The pmOS/Nura wiki's "Kernel sources" link also points to AgentFabulous/begonia (cached wiki, oldid=109575) [V-cache].

After 2022-06-23 the AF tree went dormant; Android ROM work continued on other 4.14 forks (below).

### 2.2 LineageOS kernel repo (2020–2026, active)

https://github.com/LineageOS/android_kernel_xiaomi_mt6785 [V] — 7 branches, SHAs via API [V], Linux bases from Makefile heads [V raw]:

| Branch | Linux base | LOS/Android era |
|---|---|---|
| lineage-17.1 | 4.14.194 | LOS 17.1 (A10) |
| lineage-20 | 4.14.326 | LOS 20 (A13) |
| lineage-21 | 4.14.340-openela | LOS 21 (A14) |
| lineage-22.2 | 4.14.356-openela-rc1 | LOS 22.2 (A15) |
| lineage-23.0 | 4.14.356-openela-rc1 | LOS 23.0 |
| lineage-23.2 | **4.19.325** | LOS 23.2 — moved begonia to 4.19 |
| lineage-24.0 (default) | **4.19.325** | LOS 24.0 (A16-era); repo last push **2026-10-31** [V] |

("openela" = OpenELA LTS-continuation rebrand of stable sublevels [I].) Per-branch tip commit dates and the device-repo branch list could not be fetched — GitHub API rate limit hit mid-task (see Limitations); branch SHAs: lineage-17.1 `a48fdea8`, lineage-20 `81a4186a`, lineage-21 `b46a1098`, lineage-22.2 `262ad067`, lineage-23.0 `2e1ddbd7`, lineage-23.2 `b74ec728`, lineage-24.0 `30485853` [V].
Cross-link: the UBports kernel repo's `lineage-17.1` branch tip `a48fdea8` is the **identical commit** to LOS `lineage-17.1` tip `a48fdea87dcf` [V — SHA equality].

### 2.3 Other active 4.14 forks and kernel-zip builders

- **Nova-Kernels/kernel_xiaomi_mt6785** — "Kernels for Redmi Note 8 Pro (Begonia)", default `main`, Linux **4.14.356** (Makefile [V]), last push 2026-10-03 [V], recent commits: "arm64: configs: Enable XDP_SOCKETS", "drivers: block: zram: Set LZ4 as default" [V]. Active custom-kernel tree.
- **cvnertnc/Begonia-Kernel-Builder** — CI builder "Automatically follow daily KernelSU-Next updates and build the android kernel for Xiaomi Redmi Note 8 Pro(begonia)… built with KernelSU-Next and SUSFS"; self-archived: "I'm archiving this project because I don't have much time anymore."; last push 2026-09-16 [V]; original project: PhamtomK12/Android-Kernel-Builder [V-README]. Base kernel version not stated in fetched README [unknown].
- **Suzaku Kernel V2** (community, 4PDA) — post https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=144852836 [V-cache-fresh]: release 2026-08-07 by @WuxinG90 (base kernel credit @Saikrishna1504; 4PDA post by Arrue, edited 2026-08-29). Claims: supports "Android 11 - 17" incl. **Android 17 QPR0** and HyperOS 2+ components; built with **AOSP Clang 21**; KernelSU 35053 + SUS-FS 2.2.0; "PSI обновлен до состояния версии 4.19"; "Binder обновлен до версии 5.10 LTS"; "Основано на ядре Power kernel" ("based on Power kernel") [V-quotes]. **Linux base version not stated** in the post; binder-5.10/PSI-4.19 backports are typical of a 4.14/4.19 base [I, low-medium]. No public repo identified [unknown].
- **Power kernel** — referenced only as Suzaku's base [V-mention]; repo/base version unknown.

### 2.4 Which kernel do the newest 2026 ROMs actually run? (explicit answer)

An Android 16/17-era ROM label does **not** imply a modern kernel — verified:

- **LineageOS** (newest generation, kernel repo pushed 2026-10-31 [V]): LOS 23.2/24.0 (A16-era) run **Linux 4.19.325**; older LOS 20–23.0 ran 4.14.3xx (Makefile-verified [V]).
- **EvolutionX "16.0"** (Android 16, `EvolutionX-16.0-20260525-begonia-11.7-Unofficial.zip`, posted 2026 on 4PDA [V-cache]) links its "Kernel" to the **Suzaku Kernel V2** post (p=144852836) [V].
- **Project Infinity X 3.12** (Android 16, released 2026-08-25, post p=144878394): changelog item 12 — "Осуществлен переход на новейшее ядро Suzaku" ("moved to the newest Suzaku kernel") [V-cache-fresh].
- **DerpFest 16.2** (Android 16, build 2026-04-03, post p=144870980, by @rabbiraihan789, begonia tree credits @Saikrishna1504/@WuxinG90): install flow says "Flash KSU kernel OR Magisk" — a 4.x custom kernel zip [V-cache-fresh]; exact base unverified [I].
- Highest verified Linux base in any Android kernel tree for begonia: **4.19.325** (LOS 23.2/24.0). No begonia Android ROM or kernel tree runs 5.x/6.x/7.x [V-absence across all trees surveyed; high confidence]. Modern bases exist only for Linux-distro kernels (§4).

## 3. Halium kernel (Ubuntu Touch)

Repo: https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/kernel-xiaomi-mt6785 (project id 23877901) [V].

- **Base: Linux 4.14.141** (Makefile head on `halium-10.0` [V]) — the exact stock Q-drop sublevel; Halium 10.0 = Android 10 vendor blobs.
- Branches [V, GitLab API]: `halium-10.0` (tip `4c74d0e8`, commit dated 2026-07-09T02:08:14+03:00 = 2026-07-08 UTC), `halium-10.0-cfw` (tip `d695e57f`, 2021-04-02, dormant), `lineage-17.1` (tip `a48fdea8`, 2020-12-31, dormant — identical commit to LOS lineage-17.1 tip [V]).
- Last 10 commits on `halium-10.0` [V, GitLab API `repository/commits?ref_name=halium-10.0&per_page=10`]:
  - 2026-07-08 TheKit — "scripts/dtc: add -fcommon to fix multiple definition of yylloc" (build fix)
  - 2023-12-03 TheKit — "(halium) begonia_user_defconfig: enable CONFIG_CGROUP_DEVICE"
  - 2023-12-02 TheKit — "(halium) begonia_user_defconfig: enable extra squashfs compression methods"
  - 2023-05-09 TheKit — "(halium) begonia_user_defconfig: enable CONFIG_BINFMT_MISC"
  - 2022-08-02 TheKit — "(halium) flashlights-mt6360: fix enabling torchlight from indicator-power"
  - 2022-07-01 TheKit — "(halium) begonia_user_defconfig: enable RFKill"
  - 2022-04-01 Rúben Carneiro — merge
  - 2022-02-22 Rúben Carneiro — "Configurable global PID lookups" (binder, crediting Alfred Neumayer)
  - 2022-02-22 Rúben Carneiro — "# wireguard fixed"
  - 2022-02-03 Rúben Carneiro — defconfig wireguard debug
- Activity profile: one 2026 build fix on top of a 2021-era Halium tree; defconfig is `begonia_user_defconfig` [V]. Maintainers per commits + device page: **TheKit** (kernel/device), Rúben Carneiro (device dev) [V].
- Used by: Ubuntu Touch noble 24.04 (stable 24.04-1.4, 2026-07-13 — cached device page [V-cache]).

## 4. Mainline effort (Linux on MT6785)

**Upstream status: MT6785 is NOT in mainline.** Verified twice: (a) torvalds/linux GitHub mirror `arch/arm64/boot/dts/mediatek` = 192 files, **zero** `mt6785*` [V, API 2026-11-21]; (b) kernel.org cgit plain `arch/arm64/boot/dts/mediatek/Makefile?h=master` — no mt6785 lines [V]. So **no mainline kernel version has introduced an mt6785 DTS upstream** as of 2026-11-21; "mainline" for begonia means *mainline-based forks carrying out-of-tree SoC/board support*.

### 4.1 Dinolek/mt6785-mainline (github)

https://github.com/Dinolek/mt6785-mainline — created 2025-09-10, default branch `7.1`, **last push 2026-06-17T19:55:54Z** (matches context), 11★, not a fork [V].
- Branches [V]: `6.16` (`203a993f86cd`), `7.1` (`811c3c80dac3`), `battery-downstream` (`fad73078be1b`). Tags [V]: `6.16.3-r0`, `6.16.4-r0`, `7.1-r0`.
- **Kernel base: Linux 7.1.0** on `7.1` (Makefile [V]); `6.16` line tagged 6.16.4-r0.
- No project README (only the stock kernel README) [V].
- Recent commits (2026-06-17, `7.1`) [V]: "arm64: dts: mediatek: mt6785: Add resets to ovl0/ovl_2l0"; "drm/mediatek: ovl: Add optional reset support"; "soc: mediatek: mmsys: mt6785: clear routes left by bootloader"; "drm/mediatek: dsi: Clear DSI_INTSTA before requesting irq"; "arm64: dts: mediatek: mt6785-xiaomi-begonia: Add nodes required by lk" (LK-bootloader interplay).
- Relationship to pmOS: its tags **are** the pmOS package sources (§4.2) [V]; Dinolek is the Nura/pmOS begonia maintainer (context pack) [V-context].

### 4.2 pmOS/Nura kernel package

`device/testing/linux-postmarketos-mediatek-mt6785` in https://gitlab.nura.eco/nura/pmaports (branch `main`; APKBUILD fetched raw [V]):
- **pkgver 6.16.4-r0** (expected 6.16.x ✓), pkgdesc "Mainline kernel fork for MT6785", maintainer "Dinolek <git@dinolek.me>".
- **Source URL (upstream it clones):** `https://gitlab.postmarketos.org/mt6785-mainline/linux/-/archive/6.16.4-r0/linux-6.16.4-r0.tar.gz` — a GitLab mirror of the Dinolek tree (GitHub mirror also exists: external-mirrors/mt6785-mainline-linux, pushed 2026-06-19 [V]).
- **Patches list: none in the APKBUILD** — `source=` contains only the kernel tarball + config; all MT6785 work lives **in-tree** in the fork [V].
- **Config:** single `config-postmarketos-mediatek-mt6785.aarch64`, header comment "Kernel config based on: arch/arm64/configs/defconfig"; no config fragments [V].
- Device package `device-xiaomi-begonia` (pkgver 6) [V]: depends on `linux-postmarketos-mediatek-mt6785`, `firmware-xiaomi-begonia-touchscreen`, `mesa-vulkan-panfrost`, `mkbootimg`; builds an **empty DTB packaged as dtbo** — comment: "begonia bootloader needs empty dtbo, build it and add as recovery_dtbo to final image" [V-quote].
- pmOS wiki's "kernel 6.16.4, mainline=yes" (cached wiki [V-cache]) therefore means *mainline-based fork*, not upstreamed mainline code.

### 4.3 kalpakprod/mt6785-linux (new, Nov 2026)

https://github.com/kalpakprod/mt6785-linux — created 2026-11-15, pushed **2026-11-20**, not a GitHub fork [V].
- **Mainline Linux 7.3.4** (Makefile [V]); README [V]: "Mainline Linux 7.3.4 for phones on the MediaTek MT6785 (Helio G90T / Helio G95)".
- Design: "The chip support (clocks, pinctrl, power domains, display pipeline, audio, Wi-Fi/Bluetooth/GPS, modem, camera blocks) is written for the SoC and kept apart from the board files"; tested board = **rosemary** (POCO M5s / Redmi Note 10S); "The Redmi Note 8 Pro (`begonia`) device trees from the base are carried along"; 44 MT6785 phone models listed [V-quotes].
- Relationship to Dinolek's tree: begonia DTS "from the base" — likely carried from Dinolek's tree [I, medium]. Branch `main`, work merged as "exp/rel/v0.2.1" [V].
- rosemary status table: boot/UFS/USB-networking work; battery partial [V-README].

### 4.4 Other / upstreaming status

- Screaming-Bird/mt6785-mainline — created & last pushed 2025-06-05, no description; dormant early tree, role unclear [V-metadata; low confidence on purpose].
- Upstream/lore: an `site:lore.kernel.org mt6785` web search returned no results [V-weak-negative]; linux-next could not be checked (cgit path 404 — see Limitations). Verdict: **MT6785 mainline support remains out-of-tree; whether patch series are on the mailing lists is unknown** (commit-subject style of Dinolek's tree is mainline-track [I]).

## 5. Mu-Silicium (UEFI firmware — NOT a kernel)

- **What it is:** [Project-Silicium/Mu-Silicium](https://github.com/Project-Silicium/Mu-Silicium) — "Project Mu UEFI Ports for ARM64-Based Devices", 633★, last push 2026-11-20 [V]. It is UEFI firmware (Project Mu), used by community projects to boot Windows/other OSes on ARM64 phones; it is **not** a Linux kernel and not a ROM.
- **Begonia support:** none published. A 4PDA CFW-thread attempt exists — post #24679 by KiryxaTipa (KiryxaMeow), 2026-11-20, https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=146118602 [V-cache]: "UEFI (Mu-Silicium)" + "WinPE 11" for begonia, installed via `fastboot flash boot UEFI.img`. Reported: Display ✅, Side Buttons ✅, SD Card ✅, Internal Storage partial, "Windows Boot ✅ (PE only)", "Linux Boot ❔"; USB host/device/PD ❌; in WinPE everything else ❌ (touch, battery, WLAN, BT, GPU, camera…), CPU ⚠️. Quotes: "запуск полноценной Windows 10/11 невозможен. только PE-версия"; "результат тот же что и на lancelot: работает только дисплей и частично процессор… исходники выложу на Github Mu-Silicium" (sources *promised*, future tense).
- Verified as of 2026-11-21: the Project-Silicium org has 5 repos, **no begonia/mt6785 repo** [V, org repo list]. Related ecosystem (UniXNU/DarwinBoot iOS-on-Android experiments) is peripheral; multiple Mu-Silicium device ports exist for other SoCs (SM8250 lmi/umi, SDM845 polaris, etc.) [V-search].

## 6. Toolchains / maintainers per tree

| Tree | Toolchain (as evidenced) | Maintainer(s) |
|---|---|---|
| pmOS linux-postmarketos-mediatek-mt6785 | **clang/llvm/lld, `LLVM=1`, `HOSTLDFLAGS="-fuse-ld=lld"`** + bison, flex, openssl-dev, pahole, zstd; `pmb:kconfigcheck-community` [V-APKBUILD] | Dinolek <git@dinolek.me> [V] |
| Suzaku Kernel V2 (4PDA) | **AOSP Clang 21** [V-post] | WuxinG90 (base: Saikrishna1504) [V] |
| LineageOS android_kernel_xiaomi_mt6785 | built by LOS with its Android clang toolchain; no toolchain manifest in repo [I] | LineageOS team [V-repo] |
| AgentFabulous/begonia | Android ROM builds 2020–22; toolchain unspecified in repo [unknown] | Agent_fabulous [V-XDA] |
| UBports kernel-xiaomi-mt6785 | GCC-based Halium/UT build (2026 commit adds `-fcommon` for host dtc — GCC symptom) [I, low-medium] | TheKit, Rúben Carneiro [V-commits] |
| cvnertnc builder | GitHub Actions CI (badge) [V-README]; details unread [unknown] | cvnertnc [V] |
| kalpakprod/mt6785-linux | "README, build config: as of the latest test kernel" — configs in repo [V-commit]; specifics unread [unknown] | kalpakprod [V] |
| MiCode stock drops | Unpublished (OEM) [unknown] | Xiaomi [V] |

## 7. Limitations

- **XDA live blocked** (bunny.net challenge; per context pack) — used Wayback snapshot `web.archive.org/web/20260415164458/` of the megathread (fetched fresh, 337,017 bytes, parsed) [V-Wayback]. Other XDA pages not consulted.
- **GitHub API rate limit exhausted** (shared unauthenticated pool) partway through: per-branch tip commit *dates* for the LOS kernel repo, LOS device-repo branch list, and kalpakprod/LOS latest-commit dates were not fetched (SHAs + Makefile heads were obtained before the limit). Repo-level `pushed_at` values are verified.
- **linux-next** cgit path returned 404 → MT6785 status in linux-next unverified.
- **lore.kernel.org**: backend search returned no mt6785 hits (weak negative only — not proof of absence on the lists).
- **ishan-parihar/begonia_kernel_dev**: surfaced by web search but GitHub API returns 404 → repo deleted/private; contents unknown.
- **Suzaku/Power kernel**: no public repo found; Linux base version unstated; kernel-zip downloads (pixeldrain) not fetched per research-only rule. Exact base = "pending human-browser check".
- **Retail MIUI OTA kernel sublevels** cannot be verified from OSS drops alone.
- 4PDA per-ROM topics beyond the cached pages were not fetched; EvolutionX/DerpFest/Infinity X kernel *runtime versions* rest on the changelog/kernel-post links cited, not on build manifests.

## Contradictions / refinements found

1. "Stock kernel 4.14.141" (UBports page) vs MiCode drops: 4.14.141 is the **Q-drop** sublevel; the shipping A9 device was 4.14.94-era and the final OEM drop was 4.14.186. Refinement, not a contradiction [V].
2. pmOS wiki "mainline=yes" vs "no mt6785 in Linus master": both true — pmOS means *mainline-based fork with out-of-tree MT6785 support* [V].
3. Context-pack "kernel-xiaomi-mt6785 last 2026-07-08" ✓ consistent with API (tip commit 2026-07-09T02:08+03:00 = 2026-07-08 UTC) [V].
