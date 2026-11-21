# W22 OUT — Injection patches: Anonym3310 originals + official Kali NetHunter patch sets + internal-TX search (2026-11-22)

Mission: `W22-INJECTION-PATCHES-MISSION.md`. Marks: **[V]** verified (read file/API/diff) · **[I]** inferred, not provable from source alone · **[NF]** not found.
Scope: TX/injection only (RX-monitor already closed in W20/W21). Owner constraint respected: **AkameKernel configs are pointers, not truth** — every choice re-derived from Kali/morrownr/aircrack-ng.

---

## Task 1 — Anonym3310 scan (github.com/Anonym3310, 41 repos)

### 1.1 Repo census **[V]**
41 public repos (GitHub API `users/Anonym3310/repos`, 2026-11-22). Relevant set:
| repo | branch(es) | what it is |
|---|---|---|
| **AkameKernel-begonia** | `Q-OSS-SLMK` (default, pushed 2023-03-02), `CFW` | kernel source; desc "NetHunter Kernel For Redmi Note 8 Pro" |
| **AkameKernels** | `master` | release-zip repo (AnyKernel zips + **`additional-drivers-pack.zip`** + headers .deb) for begonia/ginkgo/joyeuse/dumpling/lancelot/mido |
| **akame-configuration** | `master`, `add-license-1` | Kconfig-only repo (`NETHUNTER_SUPPORT` per-SoC menus), merged into kernel as `akame-configuration/` |
| AnyKernel3 (fork), others | — | build infra, not patches |

### 1.2 The patch collection found **[V]**
**CFW branch, top level** (verbatim files):
1. `0001-add-u32-mntr_flags-for-wifi-injection-patch.patch` — authored **Re4son** (Kali), 2017-06-07; adds `u32 mntr_flags` to `struct ieee80211_sub_if_data` union (`net/mac80211/ieee80211_i.h`).
2. `mac80211.compat08082009.wl_frag+ack_v1.patch` — the classic mac80211 injection patch (skip seq-renumber + NO_ACK for `IEEE80211_TX_CTL_INJECTED`); upstream original lives in the aircrack-ng repo: `aircrack-ng/aircrack-ng/patches/mac80211_2.6.28-rc4-wl_frag+ack_v2.patch` **[V]** (v1 = per-kernel adaptation of same change).

**Q-OSS-SLMK branch — patches applied as commits** (2022-03-14 block):
- `cb9c41e275` **"add wifi injection support"** — 5 files: `net/mac80211/cfg.c` (allow channel change with non-monitor vifs), `net/mac80211/tx.c` (injected-skip + NO_ACK, 4.14 form `u.mntr.flags`), `net/wireless/chan.c` (drop `cfg80211_has_monitors_only` gate), `drivers/net/wireless/zydas/zd1211rw/zd_mac.c` (sniffer RX filter = 0xFFFFFFFF + CR_SNIFFER_ON), `drivers/net/wireless/realtek/rtl818x/rtl8187/dev.c` (no MOREFRAG in monitor).
- `24b4616c78` **"fix ath9k naming conflict"** — renames `htc_connect_service/htc_start/htc_stop` → `*_hst` in `ath9k_htc` (6 files) to avoid symbol clash (needed when other HTC-based drivers coexist).
- `f2a490e67e` **"fix thread_info.h compile time errors"** — `-Og` constant-propagation workaround (build fix only).
- `3ea3a29a76` "Add akame defconfig" — adds `akame-configuration/` Kconfigs + `arch/arm64/configs/akame_defconfig` (5,794 lines).

### 1.3 Verbatim vs owner-modified **[V]**
Normalized diff (added-lines, order-sensitive) of `cb9c41e275` vs **Kali's official `add-wifi-injection-4.14.patch`**: **all 5 files IDENTICAL** — only hunk line offsets differ (owner's base tree differs). Same for `fix-ath9k-naming-conflict` (6/6 files identical incl. wmi.c) and `fix-thread_info.h`. **Verdict: the Q-OSS-SLMK injection stack is verbatim Kali kernel-builder patches; no owner modifications.** The CFW branch additionally carries the older standalone wl_frag+ack_v1 + mntr_flags pair (older-kernel style, same upstream lineage).

### 1.4 additional-drivers-pack.zip (AkameKernels, begonia/NONCFW/Q-OSS/02.06.21) **[V]**
Downloaded + inspected: 6 prebuilt **out-of-tree Realtek .ko modules**, all `vermagic=4.14.233-AkameKernel … modversions aarch64`, "Realtek Wireless Lan Driver":
`8188eu.ko`, `8192eu.ko`, `8192fu.ko`, `rtl8188fu.ko`, `88XXau.ko`, `8814au.ko`.
Originals (chipset → upstream source): rtl8188eus → `aircrack-ng/rtl8188eus` (v5.7.6.1, ≤5.4+); rtl8188fu/rtl8192fu → `kelebek333/rtl8188fu` (+Realtek 8192fu family); rtl8812au/8814au → `aircrack-ng/rtl8812au` v5.6.4.2; rtl8192eu → Realtek-derived OOT driver family. Exact srcversion matching not possible without building each upstream at the same toolchain — **[I]** attribution by module name + chipset family.

### 1.5 akame_defconfig pointer values **[V]** (not truth)
In-tree: `CONFIG_ATH9K_HTC=y`, `ATH10K=y` + `ATH10K_USB=y`, `RTL8187=y`, `RTL8192CU/RTLWIFI=y`, `RTL8XXXU=y` + `_UNTESTED=y`, `USB_NET_RNDIS_WLAN=y`, `MAC80211=y/MESH=y`. Not in defconfig: rtl8812au/8814au/8188eu/8188fu/8192fu — shipped as the OOT `.ko` pack instead. No `rtl8188eus`-in-rtl8xxxu patch was applied by owner (that Kali patch post-dates their build, 2023-02).

---

## Task 2 — Official Kali NetHunter kernel patch sets **[V]**

### 2.1 Where they live
Official builder: **`gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-kernel-builder`** (default branch `main`, last activity 2026-10-27). Patches are version-bucketed: `patches/3.04 … 3.18, 4.04, 4.09, 4.14, 4.19, 5.4`. `build.sh` applies them **interactively/manually** per device (`patch -d${KDIR} -p1`, menu item "4. Apply NetHunter kernel patches"; `config` expects a per-device `nethunter_defconfig`). Unofficial 1:1 mirror also exists (github `wumingzhinu/kali-nethunter-kernel-patches`, for 4.4→6.6) — not authoritative.

### 2.2 The official 4.14 set (12 patches) — what each enables
Permalink prefix: `https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-kernel-builder/-/blob/main/patches/4.14/`
| patch (author, date) | enables |
|---|---|
| `add-wifi-injection-4.14.patch` | core mac80211/cfg80211 injection: channel-change with non-mon vifs (cfg.c), NO_ACK + no seq renumber for injected frames (tx.c), remove monitors-only gate (chan.c), zd1211rw sniffer filter, rtl8187 MOREFRAG fix |
| `add-rtl8188eus-to-rtl8xxxu-drivers-4.14.patch` (yesimxev, 2023-02-15) | adds **RTL8188EUS into in-tree rtl8xxxu** (new `rtl8xxxu_8188e.c`, +2,525 lines) — monitor+injection via mac80211, no OOT driver |
| `add-rtl88xxau-5.6.4.2-drivers.patch` (Re4son, 2020-03-15) | full **aircrack-ng rtl8812au v5.6.4.2** driver in-tree as `realtek/rtl8812au` (607 files) — RTL8812AU/21AU/14AU |
| `add-rtw88-drivers-4.14.patch` (yesimxev, 2026-04-25) | **rtw88 + rtw88-usb backport for 4.14** (128 files) — modern mac80211 path for 8821CU/8822BU/CU… |
| `add-qcacld-3.0-injection-4.14.patch` (kimocoder/aircrack-ng + Loukious, 2025-10-25) | **INTERNAL Qualcomm WiFi TX injection**: `wlan_hdd_frame_inject.c` (+1,807 lines), monitor-mode TX via `ndo_start_xmit`, WMA injection queue + FW TX completion, radiotap parse/validate, `CONFIG_FEATURE_FRAME_INJECTION_SUPPORT`, mac80211/cfg80211 channel fixes |
| `fix-ath9k-naming-conflict.patch` | ath9k_htc `htc_*` → `htc_*_hst` symbol collision fix (same as owner's commit) |
| `add-rtl8188eus-to-rtl8xxxu-drivers.patch` | same as -4.14 variant for the next bucket |
| `add-ub500-to-btusb.patch` | 32-byte stub → `../4.04/add-ub500-to-btusb.patch` (Intel/Realtek UB500 BT USB ID) |
| `fix-hciconfig-samsung-oneui{,-5.x}.patch` | Samsung OneUI BT vendor fixes |
| `fix-thread_info.h-compile-time-errors.patch`, `fix-yylloc.dtc-lexer.lex.c_shipped.patch` | build fixes |

ath9k_htc itself needs **no injection patch** — mainline mac80211 driver (AR9271/AR7010), monitor+injection native; only the naming fix is kernel-version-specific. **[V]**

### 2.3 Kali docs on external cards (kali.org/docs/nethunter/wireless-cards/, updated 2025-06-18, author re4son) **[V]**
> "External wireless cards are necessary because Android devices do not support monitor mode on most devices apart from some Qualcomm chips used in modern Snapdragon SOC. There are some devices that can support monitor mode with a modified firmware and kernel such as the Nexus 5, 7 (2012), and Nexus 6P. Right now, only a specially modified version of Nexus 5 supports monitor mode for Nethunter."

Default-supported chipset list in the same doc: Atheros **ATH9K_HTC (AR9271, AR7010)**, ATH10K; Ralink RT73/RT2800USB/RT3070; Realtek **RTL8188EUS**, 8188CU/RU, 8192CU, 8192EU, 8723AU, 8811AU, **8812AU**, 8814AU, 8821AU, RTW88-USB; MediaTek MT7601U/7610U/7612U. Confirmed-working devices: TL-WN722N **v1 only** (v2/v3 "may be supported using RTL8188EUS/RTL8XXXU drivers"), TL-WN822N v1–v4, Alfa AWUS036ACH/NEH/NHA/NH, Panda PAU05.

### 2.4 NetHunter kernels page (nethunter.kali.org/kernels.html) **[V]**
~264 device kernel entries; 235 "Injection" feature tags. **Zero entries for `begonia`** (Redmi Note 8 Pro); Redmi Note 8 `ginkgo` has 4 entries (ikteach: ATH9K_HTC, RTL8188EUS, MT76, RTL8814AU/88XXAU/88X2BU, QCACLD-3.0 injection…). AkameKernel remains the only NetHunter-style kernel ever published for begonia.

---

## Task 3 — Internal (gen4m) TX injection search

### 3.1 Query log — all rotations (ENGLISH; 22 passes, no early quit) **[V]**
Pass set A: `gen4m wifi driver injection monitor mode mediatek` · `mediatek connac wifi TX injection monitor mode android kernel` · `wlan_drv_gen4m monitor mode injection` · `MT6785 OR MT6789 wifi packet injection android` · `mediatek wifi radiotap TX injection ndo_start_xmit` · `site:github.com mediatek gen4m injection monitor` · `mediatek monx monitor injection wifi` · `xda mediatek wifi injection monitor mode internal chipset`.
Pass set B: `mediatek connsys wifi packet injection firmware patch` · `"gen4m" TX OR transmit injection site:github.com` (0 results) · `mediatek wifi driver "monitor mode" TX "start_xmit" patch android` · `MediaTek smartphone internal wifi injection nexmon-like firmware hack` · `kalSendPacket gen4m OR connac monitor TX frame` · `"CONFIG_MTK_COMBO_WIFI" injection OR monitor TX` · `mediatek gen4m "TX monitor" OR "packet injection" driver source` · `android kernel MTK wifi injection aireplay impossible OR feasible`.
Pass set C (provenance): `"mac80211.compat08082009.wl_frag+ack_v1.patch" …` · `"add u32 mntr_flags for wifi injection" …` · `aircrack-ng "wl_frag+ack" patch origin 2009 …`.

### 3.2 Artifacts examined
1. **kwefjkmqf/Monitor_mode_NetHunter** (GitHub, pushed 2024-05-02, single README) **[V]** — documents MTK monitor enable via `iwpriv wlan0 driver monitor <en> <chan> <width> <sco>`, `CFG_SUPPORT_SNIFFER` in `include/config.h:1087` (points at the very same Saikrishna mt6785 tree we use), and Coconutat/ruby_exp variant (`CONFIG_MTK_WIFI_SNIFFER_RADIOTAP` in gen4m Makefile, disabled there at :225). **Monitor (RX) only; no TX-injection patch shipped; "maybe with injections" is hedged.** Corroborates W20; not a TX artifact.
2. **ZerBea/hcxdumptool discussion #531** (2025-11-27/28, qcacld-3.0 on SM8750) **[V]** — ZerBea: "Neither Linux drivers >= ath10k nor the qcacld-3.0 driver support full packet injection"; user `brokestar233` hand-patched driver-layer raw TX (`dp_tx_send`, radiotap stripped): logs say success, radio shows **0 % ACKs / no emission**; ZerBea: "It's not enough to patch the driver. The firmware must support full monitor mode and full frame injection, too!"; qcacld-**2.0** "partly supports frame injection for a few devices".
3. **Kali `add-qcacld-3.0-injection-4.14.patch`** (kimocoder, 2025-10) **[V]** — the only official patch set shipping SoC-internal TX injection (Qualcomm only): full HDD frame-inject framework + monitor `ndo_start_xmit` + FW TX-completion handling. Proves internal TX is buildable at the driver layer **when the FW cooperates**.
4. **Nexmon** (seemoo-lab) — Broadcom-only firmware-patching framework (Nexus 5 etc.); no MTK equivalent exists. **[V]**
5. Reddit/Quora/Facebook hits — generic "buy an external adapter" advice; no MTK internal TX artifact.

### 3.3 Verdict per subtopic
- Public gen4m/CONNAC TX-injection patch or project: **[NF]** across all 22 rotations (incl. site:github.com variants).
- QC-side internal injection: exists as (a) Kali official patch, (b) qcacld-2.0 partial, (c) failed SM8750 driver-layer attempt — FW acceptance is the standing blocker. **[V]**
- MTK-side: nothing like nexmon/qcacld patch. **[NF]**

### 3.4 Engineering estimate from local clones (what internal gen4m TX would require)
Evidence (saikrishna-4.14.357, `drivers/misc/mediatek/connectivity/wlan/core/gen4m/`):
- `rg -i inject` over gen4m → **0 hits** (no injection concept in driver). **[V]**
- Mon netdev stays TX-less: `os/linux/gl_init.c:1841-1844` `wlan_mon_netdev_ops` = ndo_open/stop only; `:1880` `netif_tx_stop_all_queues(prMonDevHandler)`. **[V]**
- Normal TX chain: `gl_init.c:1518` `wlanHardStartXmit()` → `os/linux/gl_kal.c:2134` `kalHardStartXmit()` → `:2207` `wlanProcessTxFrame()` (core entry, `common/wlan_lib.c:3951`) → per-BSS/TC pending queues (`prGlueInfo->ai4TxPendingFrameNumPerQueue[ucBssIndex][u2QueueIdx]`, gl_kal.c:2244-2255) or TX-direct shortcut `:2275-2276` `nicTxDirectStartXmit()` (`nic/nic_tx.c:4599/4613` `nicTxDirectStartXmitMain()`) → `nic/nic_tx.c:1126` `nicTxMsduInfoList()` → TXD v2 (`nic/nic_txd_v2.c`) + `:1512` `halTxRingDataSelect()` → PLE-page/queue FW path (`:446` `nicTxAcquireResourcePLE`, `:2300` `halTxIsDataBufEnough`, `:3725` `halTxGetPageCount`). **[V]**
- Monitor channel is already FW-commanded (W20: OID `wlanoidSetMonitor` → FW cmd 0xFC), so channel control for TX exists. **[V]**
- Driver is **wext-based, not mac80211** — there is no `ieee80211_parse_tx_radiotap` equivalent anywhere; a radiotap-TX parser must be written. **[V]**
- Note: the mission's guessed symbol `P_MBSS` does not exist in this 4.14 tree (only `ELEM_EXT_CAP_MBSSID_BIT`, `include/nic/mac.h:1254`) — TX queuing here is BSS-index/TC-based, not P_MBSS. **[V]**

**Estimate (documented hypothesis, not a claim):** a monitor-TX hook = add `ndo_start_xmit` to `wlan_mon_netdev_ops` (gl_init.c:1841) that (1) parses/strips the radiotap header (rate, TX flags), (2) builds a raw 802.11 skb, (3) pushes it through a dedicated no-BSS TX path — the TX-direct shortcut (`nicTxDirectStartXmit`) plus a hand-built TXD (nic_txd_v2.c) with a synthetic BSS index, no encryption, no A-MPDU aggregation, no-ACK, fixed rate — mirroring what Kali's qcacld patch does for HDD. Skeleton ≈ 600–1,200 LOC across `os/linux/gl_init.c`, `os/linux/gl_kal.c`, `nic/nic_tx.c`, new `radiotap-tx.c` — **medium driver work (weeks)**. The **blocking unknown is firmware acceptance** [I]: the CONNAC FW may drop raw data frames from a non-associated context exactly as qcacld-3.0 FW does (hcxdumptool #531 shows that failure mode; MTK FW internals are closed). Mgmt frames have better odds — FW already TX-probes on command during scan [I]. Honest label: **feasible to prototype, unverifiable from source, real risk of qcacld-style silent-drops; external adapters remain the only proven injection path for begonia.** Priority: LOW vs external-adapter path.

---

## Task 4 — Modern external-adapter chipset list (unified kernel driver-pack decision)

### 4.1 Table — current (2025/2026) recommended chipsets for monitor+injection on NetHunter
| chipset | USB adapters (examples) | driver source modern-best | monitor/injection | kernel options for our 4.14 unified kernel |
|---|---|---|---|---|
| **AR9271** (ath9k_htc) | TL-WN722N **v1**, AWUS036NHA/NEH | mainline `ath9k_htc` (mac80211) | native both **[V]** | `ATH_COMMON/ATH9K_HW/ATH9K_COMMON/ATH9K_HTC=y` (+naming-conflict fix patch) |
| **RTL8812AU/21AU/14AU** | AWUS036ACH/ACS/1900 | **rtw88 (lwfinger)** on ≥6.13/6.16; on 4.14 = aircrack-ng rtl8812au v5.6.4.2 (aircrack-ng README: monitor+injection working, but "THESE DRIVERS IS DEPRECATED") **[V]** | yes (aircrack driver) | Kali in-tree patch `add-rtl88xxau-5.6.4.2` **or** OOT module `88XXau.ko/8814au.ko` |
| **RTL8188EUS** | TL-WN722N v2/v3, cheap dongles | in-kernel `rtl8xxxu` **with Kali 8188e extension**; OOT aircrack-ng rtl8188eus v5.7.6.1 (≤5.4+) **[V]** | yes | Kali patch `add-rtl8188eus-to-rtl8xxxu-4.14` (preferred: in-tree, mac80211) |
| **RTL8188FU/8192FU** | various nano dongles | `kelebek333/rtl8188fu` (4.15+; note: mainline rtl8xxxu got 8188fu in 6.2 — not our 4.14) **[V]** | monitor yes; injection = Realtek driver path (aircrack family) **[I]** | OOT module `rtl8188fu.ko` (as owner's pack did) |
| **RTL8821CU/8822BU/CU** | many budget AC dongles | **rtw88-usb** — Kali backport patch for 4.14 exists (`add-rtw88-drivers-4.14`, yesimxev 2026-04) **[V]** | rtw88 = monitor+injection **[V]** (morrownr) | Kali rtw88 backport patch (modern replacement for 8192eu-class OOT modules) |
| **MT7610U/7612U** | AWUS036ACHM/ACM, Panda PAU0B/PAU0D | mainline **mt76** (morrownr: monitor, injection, VIF, active monitor — the best-behaved family) **[V]** | yes | `MT76_CORE/MT76x2U` etc. — mainline 4.14 has mt76, verify USB IDs |
| **MT7921au/7925u** | AXE3000 / WiFi 7 dongles | mainline mt7921u/mt7925u (much newer than 4.14) **[V]** | yes (active monitor quirk pre-6.12) | **not feasible on 4.14** — needs ≥5.18/6.x [I] |
| RTL8192EU/8192CU/8187 | legacy list (Kali doc) | rtlwifi/rtl8xxxu in-tree; aircrack family OOT | legacy yes | already in-tree (`RTL8XXXU=y`, `RTL8192CU`, `RTL8187` — owner defconfig matches) |
| MT7601U | budget N dongles | mainline mt76 | monitor+injection | `MT76x0U` (mainline) |
| Ralink RT3070/2800USB/RT73 | TL-WN722N-era classic | mainline rt2x00 | monitor+injection | `RT2800USB` + RT2X00 options (absent in owner defconfig — owner skipped Ralink) |

Sources: Kali wireless-cards doc (2025-06-18) **[V]**; morrownr `Recommended_Adapters_for_Kali_Linux.md` (2025-12-14: mt76 = "monitor mode, packet injection, VIF and active monitor", rtw88 = "monitor mode and packet injection"; rtl8812au merged to kernel 6.13/6.14, rtl8814au 6.15/6.16; OOT Realtek drivers "deprecated… never did a good job with monitor mode") **[V]**; aircrack-ng repo READMEs **[V]**; kelebek333 README **[V]**.

### 4.2 What this changes vs AkameKernel-derived choices
- Owner's OOT `.ko` pack (6 modules) ≈ Kali's 2020-2023 patch approach. Modern-guide preference for a 4.14 target: **in-tree Kali patches for rtl8188eus (rtl8xxxu ext) + rtl88xxau 5.6.4.2** [V-approach], keep **ath9k_htc in-tree** (owner already has it right), **add rtw88-usb backport** for 8821CU/8822BU-class, keep `RTL8XXXU_UNTESTED`, **add Ralink rt2x00 USB** (Kali-default list, owner omitted), keep `USB_NET_RNDIS_WLAN`. rtl8188fu stays OOT (no Kali/mainline 4.14 path). MT7921/7925 (morrownr "best") is unreachable on 4.14 — flag for a future 5.x/6.x unified kernel.

---

## Unified kernel patch-stack proposal (saikrishna-4.14.357)

Apply in this order, all from official `kali-nethunter-kernel-builder@main/patches/4.14/` (owner's begonia commits prove they apply cleanly to this lineage) **[V]**:
1. `add-wifi-injection-4.14.patch` — core mac80211/cfg80211 injection (needed by every mac80211 external adapter).
2. `fix-ath9k-naming-conflict.patch` — must precede/enable ath9k_htc coexistence.
3. `add-rtl8188eus-to-rtl8xxxu-drivers-4.14.patch` — 8188EUS without OOT module.
4. `add-rtl88xxau-5.6.4.2-drivers.patch` — 8812/21/14AU (or OOT modules; in-tree preferred for the unified kernel).
5. `add-rtw88-drivers-4.14.patch` — modern USB Realtek (optional but recommended).
6. `fix-thread_info.h-compile-time-errors.patch`, `fix-yylloc.dtc-lexer.lex.c_shipped.patch` — as needed by toolchain.
7. defconfig additions on top of begonia_user_defconfig: `ATH9K_HTC=y`, `RTL8XXXU(_UNTESTED)=y`, rt2x00 USB, `MAC80211(+MESH)=y`, `USB_NET_RNDIS_WLAN=y` (verify per build; owner's akame_defconfig is the pointer list, not truth).
**Not proposed:** qcacld-3.0 injection patch (Qualcomm-only, N/A on MT6785) and any internal gen4m TX patch (nothing upstream exists; estimate in 3.4; W20 radiotap0 RX-first plan unchanged).

---

## Not-found register (exact queries)
gen4m/CONNAC TX injection: all 22 rotations of §3.1 (incl. `site:github.com` variants, `wlan_drv_gen4m`, `monx`, `connsys`, `P_MBSS`-adjacent, `kalSendPacket`) → no artifact; strongest related: kwefjkmqf README (RX-only), hcxdumptool #531 (qcacld), Kali qcacld-3.0 patch (QC-only). Owner-side: no additional patch dirs beyond §1.2 (top-level trees of both branches enumerated; AkameKernels = zips only; akame-configuration = Kconfigs only).
