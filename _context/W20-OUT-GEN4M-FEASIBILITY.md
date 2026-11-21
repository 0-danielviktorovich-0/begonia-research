# W20 OUT — gen4m monitor-mode feasibility from source (2026-11-22)

Mission: W20-GEN4M-SOURCE-MISSION.md. Source-only analysis, no runtime testing.
Marks: **[V]** verified by reading code · **[I]** inferred from code, not provable from source alone · **[NF]** not found.

All paths relative to the clone root `drivers/misc/mediatek/connectivity/wlan/core/gen4m/` unless prefixed.
Primary target: `~/halium-build/kernels/saikrishna-4.14.357` (unified-kernel Track A, 4.14.357).
Cross-checked on `~/halium-build/kernels/los-4.19.325` (identical architecture, line numbers cited where they differ).
`~/halium-build/kernels/halium-ref-4.14.141/.../gen4m` — **[NF] directory absent**, not analyzed.

Chip build facts for begonia (MT6785/CONSYS_6785):
- `arch/arm64/configs/begonia_user_defconfig:1604` `CONFIG_MTK_COMBO_CHIP_CONSYS_6785=y`, `:1610` `CONFIG_MTK_COMBO_CHIP="CONSYS_6785"`, `:1616` `CONFIG_MTK_COMBO_WIFI=y` **[V]**
- `../../../../connectivity/Makefile:50-51` exports `MTK_COMBO_CHIP=CONNAC`, `WLAN_CHIP_ID=6785`; `:63` `obj-y += wlan/core/gen4m/` → begonia compiles **CONNAC** (chips/connac/connac.c, `#ifdef CONNAC` at connac.c:60). los-4.19 Makefile:58-59 identical. **[V]**

---

## Q1 — Radiotap path: who calls it, under which flag

**Master build flag: `CFG_SUPPORT_SNIFFER`, already =1 (compile-on) in both shipped trees.**
- `include/config.h:1087` `#define CFG_SUPPORT_SNIFFER 1` (saikrishna); `los .../include/config.h:1163` same. **[V]**
- Gating is a static config.h define, **not** a Kconfig option — no `SNIFFER` reference in any Makefile/Kconfig of the tree (no override path). **[V]**

Fill functions and their only caller:
- `nic/nic_rx.c:1344` `nicRxFillRadiotapMCS()`, `:1382` `nicRxFillRadiotapVHT()` — called **only** from `nicRxProcessMonitorPacket()` at `nic_rx.c:1646` and `:1657`. **[V]**
- `nicRxProcessMonitorPacket()` (`nic_rx.c:1490`) builds a full radiotap-2 header (`struct MONITOR_RADIOTAP`, `os/linux/include/gl_kal.h:348`; field bits `gl_kal.h:149-201`) from RXV Group 2/3 (TSFT, flags, rate, channel, RSSI/NF, antenna, MCS 19, AMPDU 20, VHT 21, MTK vendor NS bit 30, OUI `VENDOR_OUI_MTK`), prepends it to the skb and queues it for OS indication. Requires `ucGroupVLD` bits RX_GROUP_VLD_2|3 else silently drops (`nic_rx.c:1530-1534`). **[V]**
- Entire function is inside `#if CFG_SUPPORT_SNIFFER` (`nic_rx.c:1343` … `#else` empty stub at `:1715-1721`). **[V]**

Runtime switch and RX routing:
- `include/nic/hal.h:114-118`: `HAL_MON_EN(prAdapter)` = `prGlueInfo->fgIsEnableMon` when SNIFFER, else `FALSE`. **[V]**
- Caller: `nicRxProcessPacketType()` `nic/nic_rx.c:3572`. For `RX_PKT_TYPE_RX_DATA` (`:3582-3600`) and for offloaded `RX_PKT_TYPE_SW_DEFINED` frames (`:3636-3660`), **every** frame is diverted to `nicRxProcessMonitorPacket()` when `HAL_MON_EN` — i.e. monitor capture is BSS-agnostic and global (data, mgmt via RX_DATA type, offloaded EAPOL/ARP/TDLS). USB HIF path wired too: `os/linux/hif/usb/hal_api.c:842-846` (not used on begonia SDIO/CONSYS). **[V]**
- Delivery: `os/linux/gl_kal.c:1159-1160` selects `prGlueInfo->prMonDevHandler` as rx netdev; `:1221-1227` sets raw `PACKET_OTHERHOST`/`ETH_P_802_2` (no eth_type_trans) — proper raw 802.11 delivery. **[V]**
- The monitor netdev itself: `os/linux/gl_init.c:156` `NIC_MONITOR_INF_NAME "radiotap%d"`; `:1841-1844` `wlan_mon_netdev_ops` (ndo_open/ndo_stop only — **no ndo_start_xmit ⇒ RX capture only, no injection**); `:1846-1899` `wlanMonWorkHandler()` allocates `ether_setup` netdev, forces `->type = ARPHRD_IEEE80211_RADIOTAP` (`:1875-1876`), `register_netdev`; `INIT_WORK` at `:2856`; teardown `:2235-2240`. All inside `#if CFG_SUPPORT_SNIFFER` (`:1822`). **[V]**

## Q2 — Hidden capture paths (entry points)

1. **Full hidden monitor via private driver command `"MONITOR"`** — the big one:
   - `os/linux/gl_wext_priv.c:2869` `#define CMD_SETMONITOR "MONITOR"`; table entry `:13605` `{CMD_SETMONITOR, priv_driver_set_monitor}` inside `#if CFG_SUPPORT_SNIFFER`. **[V]**
   - `priv_driver_set_monitor()` `gl_wext_priv.c:9962`: syntax `MONITOR <enable> <pri_channel> <channelWidth> <ext/sco>` (argc≥5, `:9993`; usage string `:10117`); validates legal channel via `rlmDomainIsLegalChannel()` `:10023-10027`; then `:10092-10094` sets `fgIsEnableMon` + `schedule_work(&prGlueInfo->monWork)` (creates/destroys `radiotap0`), and `:10106` `kalIoctl(wlanoidSetMonitor, …)` with `PARAM_CUSTOM_MONITOR_SET_STRUCT`. los: `:3818`, `:11468`, `:11598-11612`, table `:15450`. **[V]**
   - OID → firmware: `common/wlan_oid.c:13138` `wlanoidSetMonitor()` sends **FW command `CMD_ID_SET_MONITOR = 0xFC`** (`include/wsys_cmd_handler_fw.h:358`) with `struct CMD_MONITOR_SET_INFO {enable, band, pri_channel, sco, width, S1, S2}` (`include/nic_cmd_event.h:2640-2650`). los oid `:13686`. **[V]**
   - Same commands reachable **without iwpriv** via procfs: `os/linux/gl_proc.c:97` `#define PROC_DRIVER_CMD "driver"`, `:1442` `proc_create(PROC_DRIVER_CMD, 0664, gprProcRoot, &drivercmd_ops)` → `/proc/wlan/driver` accepts the priv-cmd strings. **[V]**
2. **Promiscuous RX-filter path** (separate, FW filter only): `include/wlan_oid.h:121` `PARAM_PACKET_FILTER_PROMISCUOUS 0x20`; netdev `IFF_PROMISC` → `os/linux/gl_init.c:1376-1377`, `gl_p2p.c:1890-1892`; `common/wlan_oid.c:8019-8025` (packet-filter OID); helper `common/wlan_lib.c:3103` `wlanSetPromiscuousMode()`. Captures only per-current-channel RX filter, no radiotap. **[V]**
3. **RF-test ICAP (engineer-mode IQ capture)**: `common/wlan_oid.c:9461` `wlanoidRftestSetTestIcapMode`, wired into hook table `os/linux/gl_hook_api.c:165` and `:4568`. Test/ATE domain. **[V]**
4. **ATE engine promiscuous RX**: `wlan_service/service/test_engine.c:2173, 2329` (`rx_filter.bPromiscuous`). **[V]**
5. Debug surfaces (not capture): procfs `mcr` (register peek/poke) `gl_proc.c:1398`, `pkt_delay_dbg` `:1405`, `set_cam` `:1417`, `country` `:1433`, `efusedump` `:1455`, `dbglevel` `:1294`; sysfs attrs macaddr/pm/wifiver/softap/memdump `os/linux/gl_sys.c:264,288,360,455,481`. **[V]**
6. debugfs entries: **[NF]** (procfs+sysfs only). "p2p dev monitor" iftype: **[NF]** — `p2pSetMode` (`gl_p2p_init.c:185`) is P2P-GO/AP mode only; no monitor role in P2P.

**Conclusion:** a complete, compile-enabled, firmware-backed monitor-mode stack already ships, armed by one private command. Kali's "unsupported" applies to the *missing NL80211 surface*, not the capability.

## Q3 — cfg80211 gap: what IFTYPE_MONITOR registration requires

- `os/linux/gl_cfg80211.c:131-187` `mtk_cfg80211_change_iface()`: handles `NL80211_IFTYPE_STATION`→`NET_TYPE_INFRA`, `NL80211_IFTYPE_ADHOC`→`NET_TYPE_IBSS` (`:152-156`), **`else return -EINVAL`** (`:156`). AP path delegates into it from `mtk_cfg_add_iface` at `:6533-6534`. Wired in `mtk_wlan_ops` `os/linux/gl_init.c:402-405`; second table `mtk_cfg_ops` `:458-461` (unified wiphy), p2p table `gl_p2p.c:132-136`. **[V]**
- Wiphy advertisement: `gl_init.c:2411-2412` `interface_modes = STATION|ADHOC`; `:2501-2505` adds AP/P2P_CLIENT/P2P_GO/STATION under `CFG_ENABLE_UNIFY_WIPHY`; p2p wiphy `gl_p2p.c:1442-1446`. **No `BIT(NL80211_IFTYPE_MONITOR)` anywhere** — `rg interface_modes` shows only these three sites. **[V]**
- Channel ops: **no `.set_monitor_channel`** in any cfg80211_ops table **[V]** — monitor channel today comes only from the priv-cmd args inside `CMD_MONITOR_SET_INFO`.
- Internal role enums: `include/nic/wlan_def.h:468-472` `NETWORK_TYPE_{AIS,P2P,BOW,MBSS}`; `include/mgmt/cnm.h:205-210` `ENUM_CNM_NETWORK_TYPE_T {OTHER,AIS,P2P_GC,P2P_GO}`; no BSS_ROLE/monitor-ish role exists **[V]** — but **none is needed**: monitor RX intercepts in `nicRxProcessPacketType` *before* any BSS processing and delivers to a separate netdev (`radiotap0`), and `wlanoidSetMonitor` is a direct FW command, not a BSS-mode OID **[I]**.
- Minimum NL80211 hookup: (a) advertise `BIT(NL80211_IFTYPE_MONITOR)` at `gl_init.c:2411` (+2501 block if unified wiphy desired); (b) add `NL80211_IFTYPE_MONITOR` branch in `mtk_cfg80211_change_iface` that reuses the `priv_driver_set_monitor` logic (set `fgIsEnableMon`, `schedule_work(monWork)`, `kalIoctl(wlanoidSetMonitor,…)`); (c) implement `.set_monitor_channel` mapping `cfg80211_chan_def` → band/pri/sco/width/S1/S2 (the exact fields `CMD_MONITOR_SET_INFO` already carries; width→CW_* mapping logic exists in `priv_driver_set_monitor` `:10044-10100` to copy).

## Q4 — Firmware: per-mode download, separate capture FW?

- FW is downloaded per chip from names built at runtime: `chips/connac/connac.c:152-203` builds 4 fallback name types per flavor/Eco version (`WIFI_RAM_CODE_soc1_0[_<flavor>]_<eco>[.bin]`), patch `mtsoc1_0_patch_e%x_hdr.bin` (`connac.c:210-223`); loaded via `kalRequestFirmware` (`os/linux/include/gl_kal.h:618`, `request_firmware_direct` `:908`); plus `wifi.cfg` config file `gl_init.c:3305`. Binaries are **not in the kernel tree** — they ship in the vendor firmware partition. **[V]**
- Naming varies only by chip/IP-set/flavor/Eco — **no per-mode (monitor/capture) firmware image or RAM-code path exists**: no `monitor`-named FW anywhere (`rg -i monitor chips/` → empty **[V]**), no alternate download branch keyed on `fgIsEnableMon`. Monitor mode is entered at runtime with FW command 0xFC on the same RAM code **[V for the driver side]**.
- Whether the *shipped CONNAC firmware binary* implements 0xFC and emits RXV group2/3 in that mode is not provable from driver source **[I]** — the driver's completeness (cmd struct, event plumbing, RXV parsers, vendor radiotap NS) strongly indicates it is exercised upstream (this is MediaTek's production sniffer path), but treat FW behavior as the one unknown to verify on device.

## Q5 — Verdict + implementation sketch (saikrishna 4.14.357 first)

**Verdict: SMALL — glue work, not a driver feature build.** A firmware-backed, radiotap-producing monitor netdev (`radiotap0`) already exists behind `CFG_SUPPORT_SNIFFER=1`, reachable today via `iwpriv wlan0 driver "MONITOR 1 6 20 0"` / `/proc/wlan/driver` **[V]**. NL80211 standard-tools support needs ~3 small patches; injection is the only big-ticket absence.

### Sketch
1. `os/linux/gl_init.c` (2411, 2501): add `BIT(NL80211_IFTYPE_MONITOR)` to `interface_modes` on both wiphys. *Trivial.*
2. `os/linux/gl_cfg80211.c` (`mtk_cfg80211_change_iface`, ~131-187): accept `NL80211_IFTYPE_MONITOR`; factor the body of `priv_driver_set_monitor` (gl_wext_priv.c:9962-10120) into a shared helper (enable + default 20 MHz channel) and call it. *Small.*
3. `os/linux/gl_init.c` (`mtk_wlan_ops`/`mtk_cfg_ops`, :402/:458) + `gl_cfg80211.c`: implement `.set_monitor_channel` → translate `chandef` (freq→chan, width→CW_20/40/80/160, sco/S1/S2) reusing the width table in `priv_driver_set_monitor:10044-10100` → `wlanoidSetMonitor`. *Small-medium.*
4. (Optional, later) TX injection: add `ndo_start_xmit` to `wlan_mon_netdev_ops` (`gl_init.c:1841`), parse radiotap, push via mgmt/data TX path. *Medium-large; FW TX-monitor behavior unknown **[I]**.*
5. Userspace: `iw dev wlan0 set type monitor` then `ip link set radiotap0 up` (or keep priv cmd for NetHunter scripts); tcpdump on `radiotap0`.

### Files to touch
`os/linux/gl_init.c`, `os/linux/gl_cfg80211.c`, `os/linux/gl_wext_priv.c` (refactor only), optionally `include/nic/hal.h` untouched. Same diff applies to los-4.19.325 (offsets: change_iface same file, priv cmd `:11468`, ops `gl_init.c:2359+`).

### Risks
- **FW dependence**: 0xFC support + RXV group2/3 in monitor mode is firmware-side, unverifiable from source **[I]**; failure mode = silent empty captures (`nic_rx.c:1530` drop). Verify on device first via the existing priv command *before* writing any patch.
- **Regulatory**: priv path enforces `rlmDomainIsLegalChannel` (`gl_wext_priv.c:10023`); DFS channels and regdom-passive channels will be refused; country IE/prof overrides apply (`/proc/wlan/country`, `gl_proc.c:1433`).
- **One-radio hijack**: enabling monitor diverts *all* RX data/OFLD frames to `radiotap0` for the whole adapter (`nic_rx.c:3582-3660`) — wlan0 STA/AP effectively stops receiving normal traffic while armed; only one monitor netdev, no per-vif isolation.
- **Android userspace**: radiotap0 socket access needs NET_RAW/SELinux on the Android side; irrelevant on the Halium/Linux side (ANDROID_PARANOID_NETWORK already off per unified plan).
- **Quirk**: mon netdev is `ether_setup` + type override (`gl_init.c:1875-1876`); known MTK pattern, safe on 4.14/4.19.
- halium-ref-4.14.141 gen4m absent — could not confirm older lineage **[NF]**.
