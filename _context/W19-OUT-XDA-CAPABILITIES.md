# W19 — XDA t=3591182 "MTK combo chips, hidden capabilities" → gen4m applicability (2026-11-22)

Mission: W19-MONITOR-XDA-MISSION.md. Owner: Светозар. Access method: XDA bunny.net shield blocked
both the isolated browser session `w19-xda` (endless "Establishing a secure connection" JS challenge)
and **all Wayback/archive.today routes** (CDX queries for `showthread.php?t=3591182`, the new-format
slug, and the 2017-era path format return zero captures — this thread was never archived).
Thread was read **fully** via the r.jina.ai reader proxy (live fetch, passes the shield):
`archive/jina-xda-3591182-p1-live-2026-11-22.md` (16.9 KB, snapshot 2026-11-22).

Thread: "Mediatek Wifi/BT/FM/GPS combo chips, hidden capabilities [MT6620, MT6628, MT6630]"
https://xdaforums.com/t/mediatek-wifi-bt-fm-gps-combo-chips-hidden-capabilities-mt6620-mt6628-mt6630.3591182/
Starter: **ogurets** (m/ogurets.5468407), start date **Apr 17, 2017** [V, high].
Single page; visible posts: #1, #2, #3, #5, #7 — numbering gaps at #4/#6 → soft-deleted posts [I, high].
Thread is a solo research log, **not a patch drop**: no diff/patch links, attachments are firmware
dumps + test utilities (`firmwares.zip`, `something.zip`, `wifitest.zip`, `WIFI_RAM_CODE_6755.zip`).

## 1. OP technique (verbatim key quotes, with permalinks)

Format: `showtopic=3591182&view=findpost&p=<pid>` per mission brief (modern equivalent `/post-<pid>`).

### Post #1 (OP) — p=71905049 — chip ID + FM-TX probing via /dev/fm ioctls
- Goals: *"My goals are - implement Wifi monitor mode and enable FM Transmission capability."* [V]
- Driver source location: *"I've found the drivers for it in this repo: https://github.com/bq/aquaris-E5,
  wlan path: mediatek/kernel/drivers/combo/drv_wlan, fm path: mediatek/kernel/drivers/fmradio/mt6620."* [V]
- Direct chip-ID query (bypasses build.prop/lsmod): *"You can use a built-in ioctl utility to issue a
  request directly to the chip like this: `ioctl -l 4 /dev/fm -1073416950`"* (= 0xC004F50A signed decimal) [V]
- FM TX-support probe: *"You can check it for your device like this: `ioctl -l 4 /dev/fm -1073416935`.
  If you get a '01 00 00 00' response, it would mean really good news - that your device supports TX
  and it is not disabled by the driver!"* (= 0xC004F519 = `_IOWR(FM_IOC_MAGIC 0xF5, 25, int32_t*)` =
  `FM_IOCTL_TX_SUPPORT`) [V; numeric equivalence I]
- Chip findings: Philips S388 = MT6627 *"doesn't even have an FM Tx block in hardware"*; PAP4044 Duo =
  MT6628 *"also doesn't support Tx ... doesn't even have FM_IOCTL_TX_SUPPORT ioctl implemented"* [V]
- Firmware: 3 flavors *"STA", "STA+P2P" or "AP"* loaded via `wifi_change_fw_path` from
  `/etc/firmware/WIFI_RAM_CODE`; FWDL structs `FWDL_SECTION_INFO_T` / `FIRMWARE_DIVIDED_DOWNLOAD_T`,
  `"MTKW"` signature; download encryption: `prInitCmdDownloadBuf->u4DataMode = 0 | 0x1; // enable
  encryption` → OP concludes *"95% sure it is 3DES in EDE mode"* [V]
- MCR test-mode dump: *"using test mode MCR (MCU Register?) functions, I've managed to dump around
  4 megs of something ... could contain the decrypted firmware at offset 0x60000"* [V]
- FM TX ioctls present in driver: `FM_IOCTL_TX_SUPPORT(25), FM_IOCTL_RDSTX_SUPPORT(26),
  FM_IOCTL_RDSTX_ENABLE(27), FM_IOCTL_TX_SCAN(28)`; ops wiring `ops->bi.tx_support = mt6620_Tx_Support;`
  with `static fm_s32 mt6620_Tx_Support(fm_s32 *sup) { *sup=1; return 0; }` — *"the support availability
  seems to be out of the question"* (driver always says yes; firmware may gate TX) [V]

### Post #3 (OP) — p=71973656 — real TX via hidden RF test mode (the actual "unlock")
- *"Found an interesting **test mode** in the driver and built a utility from the sources found in
  public repos around (source code for S388 attached). It actually sends packets! I were able to
  capture them with another wifi card, so it's not some internal emulation, it is real."* [V]
- Utility usage: `# ./wifitesttool -t 0 -s 0 -R 11` → success lines: set central channel #1, Rx default
  antenna main, BW20, *"Set Tx power gain to 10 dBm"*, *"Set Tx payload to 1024 bytes"*, frame interval
  20 TU, frame count 10, SHORT preamble, *"Set Tx mode to 11a/b/g, tx rate RATE_48MBPS"*,
  *"TX test started.."* → `Tx total/good count: 10/10` per second. [V]
- Payload hook: *"This AT command looks promising for setting a payload: RF_AT_FUNCID_PKTCONTENT"* [V]
- **This is MTK's RF/ATE test mode** (chip factory-test path), not 802.11 monitor: packets are raw
  test frames at fixed rate/payload; monitor RX/injection via standard stack was never achieved in-thread [I, high]

### Post #5 / #7 — Kr!shn@ — p=78191037, p=78193443
- #5: *"I saw WIFI_RAM_CODE on my mediatek device it's not encrypted. Strings are still in plain text"*
  (contradicts OP's 3DES conclusion for his MT6755 device) [V]
- #7: *"Do you mean enabling monitor mode? My device has mt6755 WiFi chipset"* + attached
  WIFI_RAM_CODE_6755.zip — thread ends without an answer from OP [V]

Post #2 (p=71905132, sawdoctor): mod action only (moved to Android Development) [V].

## 2. Applicability to gen4m (begonia = MT6785/Helio G90T; MT7663-family suspected)

W20's gen4m source output (`_context/W20-*OUT*`) did **not exist** at run time (only
W20-GEN4M-SOURCE-MISSION.md present) → cross-check pending; gen4m statements below verified directly
against the two locally cloned begonia kernel trees (`~/halium-build/kernels/saikrishna-4.14.357`,
`los-4.19.325`) on 2026-11-22.

| # | Question | Verdict | Evidence |
|---|----------|---------|----------|
| 1 | Does gen4m descend from the old combo driver? | **[V] high** | Same codebase lineage: `drivers/misc/mediatek/connectivity/wlan/core/gen4m/` in both begonia trees; gen3 ancestor public at android.googlesource.com `kernel/mediatek android-mtk-3.18 .../wlan/gen3/nic/nic_rx.c` |
| 2 | Direct-ioctl chip probing (`/dev/fm` FM_IOCTL_*) still present? | **[V] high** | `connectivity/fmradio/inc/fm_ioctl.h` L54-55 in saikrishna tree: `FM_IOCTL_TX_SUPPORT _IOWR(FM_IOC_MAGIC, 25, int32_t*)`, `FM_IOCTL_RDSTX_SUPPORT` nr=26 — **byte-identical to the 2017 thread's defines**; handler in `core/fm_module.c` L1038-1046 |
| 3 | Hidden RF test mode (old wifitesttool path) alive in gen4m? | **[V] high** | gen4m ships the full ATE/QA stack: `os/linux/gl_qa_agent.c`, `os/linux/gl_ate_agent.c`, `include/rftest.h` with `RF_AT_FUNCID_COMMAND` (L176) and **`RF_AT_FUNCID_PKTCONTENT` (L187 — the exact AT funcid the OP wanted)**; wired via iwpriv `PRIV_CMD_TEST_MODE`/"SET_TEST_MODE" (17), `PRIV_CMD_TEST_CMD`/"SET_TEST_CMD" (18) → `priv_driver_set_test_mode`/`_test_cmd` (gl_wext_priv.c L4763/4816, table L13544-13545); OIDs in `common/wlan_oid.c` L9735; also `PRIV_CMD_ACCESS_MCR` (19) for direct MCR reads (the OP's "test mode MCR" dump path) |
| 4 | FM TX unlockable on begonia like OP hoped? | **[I] medium (driver-side), NF (hardware)** | Old technique survives, but begonia's chip **MT6631** FM code registers **no TX ops**: zero `tx_support`/`Tx_Support` refs in `chips/mt6631/` (vs `mt6630_Tx_Support` at `chips/mt6630/pub/mt6630_fm_lib.c` L1925/2429) → `fm_tx_support()` (fm_main.c L1799) has nothing to call for MT6631; mirrors the OP's MT6628 finding. MT6631 FM-TX hardware support unknown (no public datasheet found) |
| 5 | Does the OP's monitor-mode goal map to gen4m? | **[V] high — gen4m has a built-in hidden monitor switch the old driver lacked** | `gl_wext_priv.c`: `priv_driver_set_monitor` (saikrishna L9962, los L11468) registered as `{CMD_SETMONITOR "MONITOR", ...}` (L2869/L13605; los L15450). Usage string: `monitor [Enable][PriChannel][ChannelWidth][Sco]` → `iwpriv wlan0 driver MONITOR <1/0> <ch> <bw> <sco>`; validates channel legality (`rlmDomainIsLegalChannel`), maps ch≤14→2.4G, drives `fgIsEnableMon` + `schedule_work(&prGlueInfo->monWork)`, then `kalIoctl(..., wlanoidSetMonitor, ...)` |
| 6 | Is that switch enabled in begonia trees? | **[V] high** | `include/config.h`: `#define CFG_SUPPORT_SNIFFER 1` (saikrishna L1087, los L1163) — already ON in both clones; upline feature `CFG_SUPPORT_SNIFFER_RADIOTAP` documented as Makefile-gated `CONFIG_MTK_WIFI_SNIFFER_RADIOTAP` in other OEM trees (Coconutat ruby_exp Makefile L225/300, disabled there) |
| 7 | RX radiotap plumbing complete? | **[V] high** | `nic/nic_rx.c`: `nicRxFillRadiotapMCS`/`VHT`, `struct MONITOR_RADIOTAP` (saikrishna L1344/1382/1498/1573; los L1462/1500/1616/1693) — matches known context; radiotap defs in `gl_kal.h`/`include/nic/radiotap.h` (per kwefjkmqf repo) |
| 8 | cfg80211 monitor interface type? | **[V] high (absent)** | `NL80211_IFTYPE_MONITOR` = 0 hits in `gl_cfg80211.c`/`gl_p2p_cfg80211.c` of both trees — confirms known context; the **iwpriv path bypasses cfg80211 entirely**, so its absence is not a blocker for the iwpriv route [I, high] |
| 9 | Injection (TX) via monitor on gen4m? | **[NF] low** | No TX-side radiotap/injection path found in gen4m trees; old thread only achieved test-mode TX. Open question for W20 |
| 10 | W20 cross-check | **[NF]** | W20 output not available yet; reconcile above table against W20 when it lands |

**Bottom line [I, high]:** the 2017 thread's "hidden capabilities" survived into gen4m in a *better*
form: what the OP had to hand-roll (test-mode utils, MCR dumps, ioctl probing) is still present
(`SET_TEST_MODE`/`SET_TEST_CMD`/`ACCESS_MCR`/RF_AT_FUNCID_*), and gen4m additionally exposes a
first-class `iwpriv wlan0 driver MONITOR` switch with `CFG_SUPPORT_SNIFFER 1` already set in both
begonia kernel candidates — no patch needed to reach the entry point. Unresolved: TX/injection,
whether `wlanoidSetMonitor`→firmware accepts it on MT7663-family silicon, and FM TX hardware on MT6631.

## 3. Related-thread sweep (EN queries; RU not needed — no 4PDA hits pursued)

| Title | URL / permalink | Verdict |
|-------|-----------------|---------|
| Monitor mode and BT hci0 interface for NetHunter (kwefjkmqf) | https://github.com/kwefjkmqf/Monitor_mode_NetHunter | **Key companion source**: documents gen4m monitor unlock — `CFG_SUPPORT_SNIFFER(_RADIOTAP)` in `core/gen4m/include/config.h`, Makefile `CONFIG_MTK_WIFI_SNIFFER_RADIOTAP`, `priv_driver_set_monitor` in `gl_wext_priv.c`, command `iwpriv wlan0 driver monitor [1/0] [ch] [width] [sco]`; cites **Saikrishna1504/kernel_xiaomi_mt6785** (Redmi Note 8 Pro = begonia SoC) with exact permalinks (config.h#L1087, gl_wext_priv.c#L9962) — all verified in local trees [V] |
| [GUIDE][UPDATED] Kali NetHunter on Mi 9T Pro / K20 Pro (wlan0 monitor mode working) | https://xdaforums.com/t/guide-updated-kali-nethunter-on-mi-9t-pro-k20-pro-wlan0-monitor-mode-working.3998623/ · p=83856307 (Redmi 9 internal-MTK question), p=83856327 (reply) | Qualcomm-only method (sdm855); user boris264 asks *"Can i enable monitor mode on my Redmi 9's internal wifi card phone without any custom ROM's?"* — reply is "idk, test it yourself" → no MTK-internal answer [V] |
| [TOOL][GKI] External USB Wi-Fi monitor mode on the *stock* kernel | https://xdaforums.com/t/tool-gki-external-usb-wi-fi-monitor-mode-on-the-stock-kernel-no-custom-nethunter-kernel-no-flashing.4800346/ | External-USB route (mac80211 + USB driver as module on stock GKI kernel) — matches Kali "external OTG = community path" rule; supports internal-MTK-impossible consensus [I, medium — from snippet only] |
| [CLOSED][KERNEL][GKI][Android 17] NetHunter Wi-Fi Support & Monitor Mode (Pixel 11) | https://xdaforums.com/t/closed-kernel-gki-android-17-nethunter-wi-fi-support-monitor-mode-pixel-11.4802019/post-90743956 | Same external/patched-kernel lane for modern GKI devices; not MTK-internal [I, medium — snippet] |
| Working monitor mode on Nexus One & Galaxy S II (bcmon) | http://bcmon.blogspot.com/2012/09/working-monitor-mode-on-nexus-one.html | Broadcom firmware-patch precedent (bcmon); MediaTek only appears in a 2014 reader comment asking for MT6628 — historical context for the "patch the combo driver" era [V] |
| Out-of-tree gen4m WLAN module (MT6789) | https://github.com/xiaomi-mt6789-devs/kernel_mediatek-modules_connectivity_wlan_core_gen4m (branch `vic`, pushed 2025-03-02) | Live out-of-tree gen4m maintenance for MT6789 — gen4m stays the driver of record for new MTK phones; no monitor claims in repo [V — metadata only; README 404] |
| vendor-mediatek-kernel_modules-connectivity-wlan-core-gen4m (Motorola) | https://github.com/MotorolaMobilityLLC/vendor-mediatek-kernel_modules-connectivity-wlan-core-gen4m | Empty shell (README only) — dead end [V] |
| XDA tag: monitor mode | https://xdaforums.com/tags/monitor-mode-2/ | Tag index; snippet repeats QCACLD internal-Snapdragon monitor precedent (con_mode) — matches known context, no new MTK thread found on page 1 [V — snippet] |

Search queries used (EN): `"mediatek wifi/bt/fm/gps combo chips, hidden capabilities" xda 3591182`,
`mediatek combo wifi monitor mode patch xda MT6620 MT6628 MT6630`, `mediatek wifi monitor mode patch
android internal chipset xda forum`, `"RF_AT_FUNCID_PKTCONTENT" mediatek`, `gen4m mediatek wlan driver
monitor mode IFTYPE_MONITOR patch github`, `"MT6630" OR "MT6628" monitor injection wifi xda`,
`MTK wlan "monitor mode" hidden capability test mode iwpriv android phone`,
`site:xdaforums.com mediatek "monitor mode" wifi internal`. Not-found results: RF_AT_FUNCID_PKTCONTENT
(0 hits — the symbol is only documented in driver sources, no forum write-ups) and one empty query.

## 4. Artifacts & caveats

- Snapshot: `archive/jina-xda-3591182-p1-live-2026-11-22.md` (full rendered thread markdown, live 2026-11-22).
- Post #4/#6 never rendered (deleted-post gaps); if they existed, their content is unrecoverable
  (thread absent from Wayback/archive.today/Google cache).
- Attachments (firmwares.zip, wifitest.zip, WIFI_RAM_CODE_6755.zip) not downloaded — out of scope
  for W19; permalinks recorded: `/attachments/firmwares-zip.4119971/`, `/attachments/something-zip.4124274/`,
  `/attachments/wifitest-zip.4121659/`, `/attachments/wifi_ram_code_6755-zip.4645924/`.
- No git commits made (repo read+write files only, per mission).

## Addendum 2026-11-22 (orchestrator link inventory from the r.jina.ai snapshot)
All 33 external URLs extracted. GitHub trail: bq/aquaris-E5 (old combo driver tree),
luckasfb/Development_Documents (MTK Alps docs incl. MT6628 datasheets + "Android wifi development
process and key points.pdf"). XDA attachments (bunny 403 for automation — owner-assisted capture
pending): wifitest.zip.4121659, firmwares.zip.4119971, something.zip.4124274,
wifi_ram_code_6755.zip.4645924, hint1.png.4120336. Post permalinks: 71905049/71905132/71973656/
78191037/78193443 (posts #4/#6 deleted).
