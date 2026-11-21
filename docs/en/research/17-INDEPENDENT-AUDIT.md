# 17 — Independent source audit and corrections (2026-11-21)

> Independent read-only review of the first Hermes research wave, against repository snapshot `1435ee92c83c0d0223d87bc31ebb24a1278dc33c`. Observed on **2026-11-21** (exact observation clock time not recorded). No device was accessed, no images were downloaded or flashed, and no private forum login was used by this reviewer. This file is an **audit addendum**, not a wholesale certification of the 185-source corpus.

## Executive verdict

The repository is a useful working knowledge base: it separates MIUI/Android kernels, Halium Ubuntu Touch, Droidian and a developing mainline/postmarketOS effort; carries device-specific driver evidence; and stores forum extracts. **It should not yet be treated as a verified flashing manual or an exhaustive forum corpus.** The main shortcomings are provenance/coverage overclaims and recovery-version ambiguity, rather than lack of raw material.

Evidence markers: **V** = directly checked by this reviewer from current external page; **R** = observed in the private research repository/captured document; **I** = engineering inference; **U** = not independently verified.

## High-priority corrections

| ID / priority | Finding and exact evidence | Change needed |
|---|---|---|
| A01 / P0 | **OrangeFox is explicitly unmaintained** [V]. Its official [begonia page](https://orangefox.download/device/begonia) says the device is not currently maintained. Last listed image: **R11.0_0 Beta**, released **2020-07-26**, **“Use with CFW firmware only.”** | Correct [07](07-RECOVERY-SAFETY.md) §3.0 and [00](00-README.md) #10: an official *listing* is not current *maintained* recovery or general-purpose flash compatibility. Older/newer community OrangeFox builds are separate projects and must be checked individually. |
| A02 / P0 | **TWRP website update is not a new recovery image** [V]. Official [device page](https://twrp.me/xiaomi/xiaomiredminote8pro.html) is dated **2026-11-20** and calls support “Current”; official [download directory](https://dl.twrp.me/begonia/) lists newest binary **twrp-3.7.0_9-0-begonia.img**, dated **2022-10-06**. | In [07](07-RECOVERY-SAFETY.md) and [INDEX](INDEX.md), distinguish website date, support label, newest official **binary** date, and compatibility with a given ROM/vendor base. A 2022 image has **not** been validated for a 2026 Android 16 ROM by this listing. |
| A03 / P0 | **Strong brick-risk warning remains** [V]. Official [TWRP begonia notes](https://twrp.me/xiaomi/xiaomiredminote8pro.html) warn that this device can hard-brick and that data decryption can break after updates. [07](07-RECOVERY-SAFETY.md) accurately records BROM/mtkclient methods [R], but an exploit-based recovery *route* does not imply guaranteed success on any preloader, security patch or board failure [I]. | Replace any unconditional “easy to unbrick”, “only USB cable needed” claim with **conditional**: BROM entry, exploit support, compatible DA/preloader, intact hardware, trustworthy partition backups and matching ROM must all be validated on this particular unit. Official Xiaomi service recovery and community exploit recovery are different processes. |
| A04 / P1 | **Forum crawl is sampled, not exhaustive** [R]. [10-GUIDE-INDEX](10-GUIDE-INDEX.md) calls itself “every” guide and [00](00-README.md) #13 claims every instruction across threads with ~1,235 and ~1,110 pages. Yet repository archive contains selected first/middle/last-page snapshots plus specific linked posts, not full sequential copies of every forum page; [HUMAN-ASSISTS](_context/HUMAN-ASSISTS.md) records live XDA first-page capture as **40 posts on page 1**. | Rename the scope in README/INDEX/10 to **“guide index mined from pinned index, sampled pages, and individually discovered posts”** unless a complete page-range crawl with coverage manifest is later supplied. High confidence in linked posts does **not** establish completeness. |
| A05 / P1 | **Access-state documents disagree** [R]. [HUMAN-ASSISTS](_context/HUMAN-ASSISTS.md) marks live XDA megathread, two other XDA guides, both Nura pages, and key logged-in 4PDA spoiler posts **resolved 2026-11-21 using Brave/owner browser**; raw/markdown copies are in `archive/` and `_cache/`. However [00](00-README.md), [05](05-UBUNTU-TOUCH.md), [07](07-RECOVERY-SAFETY.md), [03](03-KERNEL-HISTORY.md), and [_context/CONTEXT](_context/CONTEXT.md) continue to describe some pages as inaccessible / Wayback-only. | Distinguish **“blocked in this reviewer's web fetch”** from **“previously captured successfully via Hermes Brave”**, and refresh stale limitations in the next editor pass. The captures may cover only a page; do not equate site access with a full crawl. |
| A06 / P1 | **“Last official MIUI” must be regional** [V]. [XM Firmware Updater's begonia table](https://xmfirmwareupdater.com/miui/begonia/) lists EEA stable `V12.5.15.0.RGGEUXM` (recovery 2022-09-16, fastboot 2022-08-26), Global stable `V12.5.1.0.RGGMIXM`, plus different Indonesia/Russia/China/India branches and stable-beta builds. | The EEA release is the latest **listed stable by date among those rows**, not a universal stock package to install on all SKUs. Never pick a firmware solely because its version/date is higher. Identify exact product/region/board before proposing a rollback baseline. |
| A07 / P1 | **Ubuntu Touch microphone is an audio-path question, not necessarily dead hardware** [V,R]. [Current official device matrix](https://devices.ubuntu-touch.io/device/begonia/) reports microphone unavailable, while the same matrix marks “Voice in calls” working. [Droidian adaptation](https://github.com/begonia-linux/adaptation-xiaomi-begonia) claims a working microphone [R, porter-maintained README]. | Separate voice-call uplink, voice recorder/capture, microphone permission and audio-route testing. Before binary RE, compare UT 2026-10 stock audio-policy + `quirks=-output_fast` changes with Droidian `/etc`, `/mnt/vendor`, audio policy and services. The status tables are maintainer reports, not on-device verification. |
| A08 / P2 | **Use “official” with a named authority** [R]. [00](00-README.md) #3 calls crDroid “the only OFFICIAL community ROM,” but [02](02-FIRMWARE-HISTORY.md) §3.6 calls AxionOS “OFFICIAL.” | Disambiguate “official crDroid download”, “official AxionOS team build”, “official LineageOS support”, and “stock Xiaomi”. These are not interchangeable scopes. |
| A09 / P1 | **Source completeness is different from source freshness** [R,I]. The inventory maps modern Android 16 ROMs, vendor trees and kernel forks, but dates on an Android ROM do not prove new MTK firmware/driver versions. [02](02-FIRMWARE-HISTORY.md) and [11](11-BLOBS-FIRMWARE-SOURCES.md) acknowledge this distinction. | Add extracted **SHA-256 + file version/build fingerprint + ELF SONAME/build-id + vendor partition origin + licensed reuse status** before claiming any blob is newest or compatible. This needs binaries from a trusted factory ROM and/or the actual device; it was not done in this browser-only review. |

## Direct independent web check: source-access results

| Original/derived URL | Direct fetch on 2026-11-21 | Reliable alternative |
|---|---|---|
| [4PDA 974421](https://4pda.to/forum/index.php?showtopic=974421) | HTTP **403** to this reviewer's web fetch [V] | Hermes/owner cached first/middle/last and individual posts in `archive/`, with logged-in spoiler saves [R]. |
| [4PDA 965629](https://4pda.to/forum/index.php?showtopic=965629) | This review did **not** independently direct-fetch it; prior accesses are recorded in repo [R] | Live extracts + owner spoiler saves in `archive/`. |
| [XDA 4056527](https://xdaforums.com/t/guide-info-psa-redmi-note-8-pro-megathread-cfw.4056527/) | HTTP **502** to this reviewer's web fetch [V] | Brave live snapshot `_cache/xda-megathread-live-2026-11-21.md` (first page, 40 posts); Wayback archive [R]. |
| [UBports begonia](https://devices.ubuntu-touch.io/device/begonia/) | **Accessible** and checked [V] | Official feature/release table. |
| [TWRP device](https://twrp.me/xiaomi/xiaomiredminote8pro.html) and [binaries](https://dl.twrp.me/begonia/) | **Accessible** and checked [V] | Official maintainer/download sources. |
| [OrangeFox device](https://orangefox.download/device/begonia) | **Accessible** and checked [V] | Official page with historical release and maintenance status. |
| [XM Firmware Updater](https://xmfirmwareupdater.com/miui/begonia/) | **Accessible** and checked [V] | Third-party index explicitly identifying untouched official MIUI archives; actual archive hashes still unverified. |

A browser overcoming an anti-bot interstitial is not proof that it saved *all* pages, thread posts, attachments, media, or downloadable ROM binaries. Keep a page-range coverage ledger. Never copy cookies/session tokens into source archives.

## Proposed evidence/compatibility contract for future port work

Record one row **per ROM + kernel branch + exact vendor/firmware base + tested board**, not “Android 16 supports this” as a single bucket:

- Device: codename, regional SKU, panel model/connector variant, storage and battery state, bootloader status; do not publish serial/IMEI/MAC or NVRAM dumps.
- Provenance: original archive URL, release date, exact checksum, upstream revision/commit or source tag, license and redistributability.
- Platform: Android userspace/API, vendor interface level, kernel `uname -r`, KMI/ABI, DTB/DTBO revision, boot header and AVB chain.
- Subsystems: display/panel, touch firmware, charging, suspend, GPU, Wi-Fi/BT chip **actually identified**, audio routes/recording, modem firmware/VoLTE per local carrier, camera, GPS, sensors, NFC.
- Test evidence: runtime kernel logs, full dmesg snippets stripped of identifiers, reproducible steps, expected/actual result, log timestamp, and rollback path.
- Failure levels: `not-tested` / `works-on-specified-build` / `regression` / `firmware-unknown` / `requires-closed-HAL`, never infer “works” from build success alone.

**Priority conclusion:** for a usable phone, stay on a reproducible existing Ubuntu Touch/Halium 10 baseline first and fix the recording path; treat Halium 11 as a separate experiment. For long-term upstream Linux, focus a *different* postmarketOS/mainline branch on DTS/regulators, charging, wireless and audio before attempting to remove the Android modem/camera dependencies. Do not transfer a newer Android blob into a different Halium ABI blindly.

## Proposed follow-up edits (for the next maintainer/editor pass, not performed here)

1. [07](07-RECOVERY-SAFETY.md) §3.0 + [00](00-README.md) #10: integrate A01/A02 with the official binary dates and CFW-only OrangeFox warning.
2. [10](10-GUIDE-INDEX.md) heading/intro + [00](00-README.md) #13: correct exhaustive-crawl overstatement; add `archive/crawl-coverage.csv` with per-page vs per-post evidence.
3. [_context/HUMAN-ASSISTS](_context/HUMAN-ASSISTS.md), [_context/CONTEXT](_context/CONTEXT.md), [05](05-UBUNTU-TOUCH.md), [07](07-RECOVERY-SAFETY.md): reconcile browser-access history with newly captured Brave sources.
4. [09](09-OPEN-QUESTIONS.md): add a question about **Android 16 recovery compatibility** and the OrangeFox 2020 CFW-only status.
5. [11](11-BLOBS-FIRMWARE-SOURCES.md): add a machine-readable checksum/ABI/provenance template (not guessed version numbers).
6. Perform a **privacy/credential scan** of HTML snapshots before any planned public release; **not performed** in this review.

## Scope and limitations

No device-in-hand testing; no claim to have read every page or verified every blob in the research repository. Independent checks here cover current UBports, TWRP/OrangeFox, official-MIUI mirror list, and the documented archive/metadata. Weak or unverified claims remain in the parent research files until their owners reconcile them. This addendum makes the correction queue explicit without modifying the concurrent Hermes-owned source-of-truth files.

Suggested next step: follow the **read-only on-device inventory** in [18-DEVICE-PREFLIGHT-READONLY.md](18-DEVICE-PREFLIGHT-READONLY.md), then record the exact firmware baseline, branch and rollback images before flashing anything.
