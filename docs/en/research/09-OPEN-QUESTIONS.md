# 09 — Open questions, contradictions & not-found ledger (begonia, Redmi Note 8 Pro)

Everything this research could **not** resolve as of 2026-11-21, with what would settle each item. Cross-references: contradictions flagged in [04 §18](../kernels/04-HARDWARE-DRIVERS.md), [02 §6](../android/02-FIRMWARE-HISTORY.md), [03 §6](../kernels/03-KERNEL-HISTORY.md), [07 §8](../recovery/07-RECOVERY-SAFETY.md), [10-GUIDE-INDEX.md](../android/10-GUIDE-INDEX.md).

---

## 1. Unresolved contradictions (kept, dated — not silenced)

| # | Contradiction | Sources / status | What would settle it |
|---|---|---|---|
| 1 | **Hard-brick era vs mtkclient era**: official TWRP page (updated 2026-11-20) warns *"This device hard bricks really easily… Restoring device without spending real money is impossible as of now."*; pmOS wiki (mtkclient era) says *"it's easy to unbrick the device"* | [07 §3](../recovery/07-RECOVERY-SAFETY.md) / [07 §6](../recovery/07-RECOVERY-SAFETY.md) | Different eras/assumptions (paid Mi-Authorized-Account service vs local BROM exploit). A test on current TWRP builds + a dated statement from the TWRP maintainer would close it |
| 2 | **Which TWRP for which Android base**: unified community 3.7.1 (wuxinG90, A12+ era) vs base-specific builds (3.7.0_12 A12–14, 3.6.2_12-4 A12.1/13, 3.5.2 v3 A11, MIUI-12.5-base TWRP, BLACK TWRP 3.5.1 V2 for A10) | [10-GUIDE-INDEX §2](../android/10-GUIDE-INDEX.md) | A compatibility table read off each build's post body (human-browser or per-post fetch) |
| 3 | **Anti-rollback (ARB) absent on begonia** — single source, [mi-faq.ru via 4PDA](https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=88821588), low confidence | [10-GUIDE-INDEX §1](../android/10-GUIDE-INDEX.md) | One primary confirmation (firmware changelog, XDA megathread body, or an actual `fastboot oem` ARB query) |
| 4 | **vbmeta handling for GSI**: 4PDA-recommended *patched vbmeta.img* ([p=93523562](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=93523562)) vs generic `fastboot --disable-verification flash vbmeta` | [10-GUIDE-INDEX.md](../android/10-GUIDE-INDEX.md), [07 §2/§6](../recovery/07-RECOVERY-SAFETY.md) | Hash-compare the patched image vs stock + one controlled boot test per method |
| 5 | **Microphone**: broken on UT 24.04 vs **works on Droidian** (same Halium-10 vendor base, different audio stacks) | [05 §feature](../linux/05-UBUNTU-TOUCH.md) vs [06](../linux/06-DROIDIAN-POSTMARKETOS.md) | Diff Droidian `adaptation-xiaomi-begonia` audio policy vs UT's; port the delta (also the [08 P0](../linux/08-DEVELOPMENT-ROADMAP.md) lever) |
| 6 | **Accelerometer BMI120**: pmOS wiki says *works*, but the pmOS 6.16.4 kernel config has **no BMI120 driver** (only BMI160 / HID_SENSOR_ACCEL_3D) | [04](../kernels/04-HARDWARE-DRIVERS.md) (flagged there) | On-device check (`/sys/bus/iio` device list on a pmOS boot) or a defconfig diff against the running kernel |
| 7 | **Charger IC duty split**: MT6360 vs SMB1351 responsibilities (which part does what in the charging path) | [04 §13](../kernels/04-HARDWARE-DRIVERS.md) | Mainline DTS probe + charging driver docs for MT6785 platforms |
| 8 | **Shipped MIUI at launch**: MIUI 10 vs MIUI 11 (pmOS/Nura wiki says shipped Android 9 / MIUI 11; launch-era forum history suggests MIUI 10-era builds in Sept 2019) | [_context/CONTEXT.md](../../../_context/CONTEXT.md) vs 4PDA MIUI thread history | Read the first-post changelogs of the MIUI thread (t=965629, Sept 2019 pages) |
| 9 | **Regional last-build mismatches**: EEA V12.5.15.0 (2022-09-16) vs Global/RU/CN dates differing by weeks across mirrors | [02 §1](../android/02-FIRMWARE-HISTORY.md), [_context/SOURCE-CENSUS.md](../../../_context/SOURCE-CENSUS.md) | Cross-check two mirror classes per region (xiaomirom + xmfirmwareupdater already agree for EEA) |
| 10 | **twrp.me index vs device page**: the [index](https://twrp.me/xiaomi/) showed zero "begonia" matches the same day the [device page](https://twrp.me/xiaomi/xiaomiredminote8pro.html) existed, fresh (2026-11-20) | [07 §3](../recovery/07-RECOVERY-SAFETY.md) | Re-grep the index + device page after a few weeks; if still unlisted, the device page is simply unlinked from the index |

## 2. Not-found ledger (explicit "searched, absent" markers — never guessed)

- **Per-ROM source trees for closed ports**: per-build device/vendor/manifest trees absent for the closed zip-only ports (Bliss GSI, RR GSI, PE GSI, crDroid GSIs, OEM ports) — searched: the exact 4PDA posts + GitHub ([02 §7.15](../android/02-FIRMWARE-HISTORY.md)).
- **Xiaomi device tree never published** for begonia (only kernel sources P/Q/R on MiCode) — searched: MiCode mirrors + repos ([02 §7](../android/02-FIRMWARE-HISTORY.md)).
- **UART pinout**: no begonia-specific UART pad/console source (only SoC-level BROM UART base 0x11002000 from mtkclient config) — searched: web + all 10 cached 4PDA pages, 0 hits ([07 §4](../recovery/07-RECOVERY-SAFETY.md)).
- **LK verified-partition list**: pmOS wiki itself marks it TODO ([07 §5](../recovery/07-RECOVERY-SAFETY.md)).
- **Suzaku V2 kernel**: Linux base version unstated, **no public repo found** ([03 §2.3](../kernels/03-KERNEL-HISTORY.md)).
- **HYDRA PLUS kernel**: no public source tree; toolchain evidence only ("Ubuntu Pure Linux Clang 14.0.1", [t.me/begoniaupdateindonesia](https://t.me/s/begoniaupdateindonesia)) ([03 §6](../kernels/03-KERNEL-HISTORY.md)).
- **No mt6785 DTS in Linus master; no lore.kernel.org patch trail** — mainlining is fork-only ([03 §4](../kernels/03-KERNEL-HISTORY.md), [_context/SOURCE-CENSUS.md](../../../_context/SOURCE-CENSUS.md)).
- **Battery model**: PARTIALLY RESOLVED 2026-11-21 — device-tree READMEs state Non-removable Li-Po **4500 mAh** ([TTTT555/device_xiaomi_begonia](https://github.com/TTTT555/device_xiaomi_begonia) et al., found via plain web search) [V-README, medium]. Still open: health-check procedure + replacement-cost sources (row 25).
- **Live XDA megathread newer posts** (post-2026-04-15): unverifiable by our tools (Wayback snapshot is the ceiling) — see §3.
- **4PDA SP-Flash-Tool-dedicated unbrick guide**: not found (searched: all cached pages for кирпич/unbrick/SP Flash/тест-по patterns) ([07 §7](../recovery/07-RECOVERY-SAFETY.md)).

## 3. Pending human-browser checks

All rows with instructions live in [_context/HUMAN-ASSISTS.md](../../../_context/HUMAN-ASSISTS.md) (7 rows): nura/pmaports MR 1909 + device dir (Anubis wall), live XDA megathread + unlock guide + DT-sources thread + MTK-unlock thread + optional TWRP thread (bunny.net wall). One browser sitting covers all of them; dropped files land in `archive/human/` and get indexed at the final pass. Additionally: **auth-walled downloads** (4PDA attachments, XDA downloads) are cited by URL only, per the no-registration rule (REQUIREMENTS row 23).

## 4. What a continuation agent should do first (ranked)

1. **Onboard in one hop**: [00-README.md](00-README.md) → [_context/CONTEXT.md](../../../_context/CONTEXT.md) → [_context/REQUIREMENTS.md](../../../_context/REQUIREMENTS.md) → [08](../linux/08-DEVELOPMENT-ROADMAP.md)/[09](09-OPEN-QUESTIONS.md) (this file). Do not re-research what is already cited; extend, don't fork.
2. **Assembler pass** (owns: `01-SOURCES.md`, `INDEX.md`, `index.json`, `sources.json` from the `sources.jsonl` log, CSV refresh — **add the flagged Bliss OS 16.9 row** to `firmware-matrix.csv`, [02 §3.11](../android/02-FIRMWARE-HISTORY.md)) + `archive/index.html` regeneration + LICENSE decision + privacy scan (REQUIREMENTS rows 4, 15; `begonia-research.zip` dropped per the row-4 amendment 2026-11-21 — the repo itself is the distribution medium).
3. **Run the human-assist saves** ([_context/HUMAN-ASSISTS.md](../../../_context/HUMAN-ASSISTS.md)), then re-mine the **live** XDA megathread (newer than the 2026-04-15 Wayback ceiling) for 2026 ROM/kernel links and update [10-GUIDE-INDEX.md](../android/10-GUIDE-INDEX.md).
4. **Verify current recovery builds**: pull version numbers from [dl.twrp.me/begonia](https://dl.twrp.me/begonia) and the [OrangeFox release listing](https://orangefox.download/device/begonia), snapshot both pages into `archive/` (OrangeFox has no offline copy yet), and update [07 §3](../recovery/07-RECOVERY-SAFETY.md) statuses.
5. **Battery-repair pass** (REQUIREMENTS row 25): establish the battery model from software, register health-check + replacement-cost sources into [08](../linux/08-DEVELOPMENT-ROADMAP.md) §Device-repair; then, at packaging, execute REQUIREMENTS row 16 (move the repo into `~/AI-OS/begonia-research`).

*Written by the editor-in-chief pass, 2026-11-21 (JST).*
