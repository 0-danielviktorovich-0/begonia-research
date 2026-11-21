# W23 OUT — ATE test-mode TX: 2017 toolchain → begonia gen4m map + injection experiment plan (2026-11-22)

Mission: `W23-ATE-TX-MISSION.md`. Owner: Светозар. Marks: **[V]** verified (read file/byte-compare) · **[I]** inferred, not provable from source alone · **[NF]** not found.
Inputs: W22-OUT Task 3 (internal TX NF, FW-acceptance blocker) · W19-OUT (ATE stack alive [V]) · `archive/xda-3591182/extracted/` (wifitest toolchain + testmode1.pcap) · local clones saikrishna-4.14.357 / los-4.19.325.

**Bottom line:** the 2017 ATE toolchain maps onto begonia's gen4m almost byte-for-byte — same ioctls (+8/+9/+11), same OID numbers, same magic key 2011, same funcid enum (PKTCONTENT=12 verbatim), same ATE/QA agents compiled in. ATE TX is reachable **from a root shell with zero kernel changes**. The only unresolved question is FW-side: whether CONNAC FW honors *arbitrary* packet content (funcid 12 / 101/103) — a 30-minute on-device test with an external sniffer decides between "injection ships userspace-only (0 LOC)" and "W22's 600–1200 LOC TX LKM stands".

---

## Q1 — Command coverage: 2017 `ENUM_RF_AT_FUNCID_T` vs begonia `include/rftest.h` **[V]**

2017 header: `wifitest/libwifitest/libwifitest.h:167-233`. Begonia: `core/gen4m/include/rftest.h:174-352` (saikrishna; los identical at same lines). Enum positions/values are **verbatim identical** for 0–46 and 64–75.

| 2017 funcid (val) | begonia rftest.h | status |
|---|---|---|
| VERSION (0)…TX_PWR_MODE (31) | L175-206, same values | **present verbatim** |
| **PKTCONTENT (12)** | **L187**, value 12 | **present verbatim** (W19:187 confirmed) |
| TXED_COUNT (32)…RX_RSSI (46) | L209-223, same values | **present verbatim** |
| — | FW_INFO(47), DRV_INFO(48), PWR_DETECTOR(49), WBRSSI_IBSSI(50) L224-227 | begonia-only additions |
| SET_RX_DEF_ANT (63) | absent | **gone** (2017-only) |
| SET_DPD_RESULT (64)…WRITE_EFUSE (67) | L230-233 | present verbatim |
| SET_MAC_DST_ADDRESS (68) / SET_MAC_SRC_ADDRESS (69) | **SET_MAC_ADDRESS (68)** L234 + **SET_TA (69)** L235 | **renamed/merged** (DA↔68, TA↔69; chunk-half flag BIT(18)) |
| SET_RXOK_MATCH_RULE (70) | SET_RX_MATCH_RULE (70) L236 | renamed |
| SET_CHANNEL_BANDWIDTH (71)/SET_DATA_BANDWIDTH (72)/SET_PRI_SETTING (73)/SET_TX_ENCODE_MODE (74)/SET_J_MODE_SETTING (75) | SET_CBW/SET_DBW/SET_PRIMARY_CH/SET_ENCODE_MODE/SET_J_MODE (71-75) L239-243 | renamed, same values |
| — | ICAP 80-85; QA-tool 90-134 (`#if CFG_SUPPORT_QA_TOOL`, config.h:233=1): **SET_MAC_HEADER(101), SET_SEQ_CTRL(102), SET_PAYLOAD(103)** L274-276, SET_DBDC_BAND_IDX(104), SET_TX_PATH(113), SET_NSS(114), SET_ANTMASK(115), MPS 128-134 | begonia-only |
| — | SET_ANT_SWP (153) L349 (`CFG_SUPPORT_ANT_SWAP=1`, config.h:261) | begonia-only |

Commands enum: 2017 STOPTEST(0)/STARTTX(1)/STARTRX(2)/RESET(3)/OUTPUT_POWER(4)…CW(10) = begonia L355-376 verbatim, + ICAP(11)…RDD_OFF(16).
**TX-capable set (RATE 3, PKTLEN 6, PKTCNT 7, PKTINTERVAL 8, POWER 2, CHNL_FREQ 18, BANDWIDTH 15, ACKPOLICY 11, SET_MAC_ADDRESS 68, SET_TA 69, SET_CBW/DBW 71/72, COMMAND STARTTX/STOPTEST, + 101/102/103): all present.** TX limits in the same header: `RF_AT_PARAM_TX_80211HDR_BYTE_MAX=32`, `RF_AT_PARAM_TX_80211PAYLOAD_BYTE_MAX=2048` (→ 2080 B total, L107-113); `TX_PKTCNT_UNLIMITED=0` (L117); interval default 50 µs (L120); `RF_AT_ACK_POLICY_NOACK=1` (L391).

Second full enum copy (incl. 101-166, HE-TB 158-167) exists in the **uncompiled** test engine `wlan_service/glue/hal/gen4m/operation_gen4m.c:61-248` — built only when the external build sets `MTK_WLAN_SERVICE_PATH` (Makefile:696-720 saikrishna / :884-908 los; not set in normal builds → `CONFIG_WLAN_SERVICE=0`) **[V]**.

## Q2 — Transport: how userspace reaches the ATE engine **[V]**

**2017 framing** (`libwifitest.c`): `WIFI_TEST_set(u4FuncIndex,u4FuncData)` L584-635 packs `PARAM_MTK_WIFI_TEST_STRUC_T{u4FuncIndex,u4FuncData}` (8 B, L170-173) into `NDIS_TRANSPORT_STRUCT{ndisOidCmd=0xFFA0C911 (OID_CUSTOM_MTK_WIFI_TEST_), inLen=8, outLen=8, content[16]}` (L163-168, L606-608), `wrq.u.data.flags=15 (PRIV_CMD_OID)`, `ioctl(SIOCIWFIRSTPRIV+8)` (L124-126, L611-615). Arm = OID_CUSTOM_TEST_MODE 0xFFA0C901; abort = 0xFFA0C906; MCR = 0xFFA0C801 (L131-134). Sub-field addressing: funcid bits 16-31 = byte offset, `TEST_SET_CMD_OFFSET=16` (L137-139) — 2017 MAC writes use `funcid | (4<<16)` (L1031, L2069).

**Begonia side — byte-identical numerics** (`os/linux/include/gl_wext_priv.h` saikrishna / los):
- `IOCTL_SET_STRUCT=SIOCIWFIRSTPRIV+8`, `GET_STRUCT=+9`, `SET_STRUCT_FOR_EM=+11` (h:92-94; los h: same) = 2017 L124-126 exactly.
- OIDs: `0xFFA0C801 / 0xFFA0C901 / 0xFFA0C906 / 0xFFA0C911` (h:218/224/227/228) = 2017 values exactly; + ICAP 0xFFA0C913 (h:229).
- `PRIV_CMD_OID=15` (h:132) = 2017 flags; **`PRIV_CMD_TEST_MAGIC_KEY=2011`** (h:272, "Don't change it for future compatibility"), ICAP 2013 (h:273).
- Handler table `rIwPrivHandler[]` (gl_wext.c:240-264): `[+8]=priv_set_struct`, `[+18-0]…`; named args (gl_wext.c:114-238): **`set_test_mode`** (PRIV_CMD_TEST_MODE=17, 1 int, L176-177), **`set_test_cmd`** (PRIV_CMD_TEST_CMD=18, 2 ints, L178-179), `get_test_result`, `set_mcr/get_mcr` (19), `set_oid/get_oid` (PRIV_CMD_OID=15, 256 B, L215-217), `set` (PRIV_QACMD_SET=29, 2000-char, L194 → ATE/QA agent), `driver` (L137, the priv_driver string table).
- Integer path body: `__priv_set_int` (gl_wext_priv.c:932-997): `PRIV_CMD_TEST_MODE` + magic 2011 → OID_CUSTOM_TEST_MODE; 0 → ABORT; `PRIV_CMD_TEST_CMD` copies `pu4IntBuf[1..2]` (8 B) → `OID_CUSTOM_MTK_WIFI_TEST` in/out=8 (L959-966); query path L1245-1273 returns funcdata in `prIwReqData->mode`.
- String path: `iwpriv wlan0 driver SET_TEST_MODE <magic>` / `SET_TEST_CMD <idx> <data>` (CMD defines gl_wext_priv.c:2940-2941; table L13544-13545; los :3888-3889/:15378-15379) → `priv_driver_set_test_mode` (4763-4814; los 5634) → `kalIoctl(wlanoidRftestSetTestMode/AbortTestMode)`; `priv_driver_set_test_cmd` (4816-4866; los 5687) → `struct PARAM_MTK_WIFI_TEST_STRUCT` → `kalIoctl(wlanoidRftestSetAutoTest, 8 B)`.

**Struct match:** `struct PARAM_MTK_WIFI_TEST_STRUCT{u4FuncIndex;u4FuncData}` (wlan_oid.h:1739-1742) — identical layout to 2017's `PARAM_MTK_WIFI_TEST_STRUC_T`. **The 2017 libwifitest ioctl structure matches begonia as-is** [V]; its binary would run if rebuilt without the libnvram dependency (Android.mk links `libnvram`, only used to *query* 5G-band support — libwifitest.c:56/1417, not for TX).

**Third transport (richer):** `IOCTL_IWPRIV_ATE=+17` → `priv_ate_set` (gl_wext_priv.c:2342/2395) → `AteCmdSetHandle` (gl_ate_agent.c:2645) over `rAtePrivCmdTable` (L94-183): `ATE=ATESTART|ATESTOP|TXFRAME|TXSTOP|RXFRAME|RXSTOP` (SetATE L227-265 → gl_hook_api.c MT_ATEStart L115 / MT_ATEStartTX L330 = funcid 1/1 …), **`ATEDA`/`ATESA`** (custom DA/SA, L279/322), `ATECHANNEL/ATETXPOW0/ATETXGI/ATETXBW/ATETXLEN/ATETXCNT/ATETXMCS/ATETXMODE/ATEIPG/ATEVHTNSS/ATETXANT/ATERXANT`, `WriteEfuse`, `TxPower`, RDD/ByPassCac. `CFG_SUPPORT_QA_TOOL=1` (config.h:233) and `gl_ate_agent.o`/`gl_qa_agent.o` are in the build list (Makefile:487-488, 495-496; los 610-611/618-619) **[V]**. QA daemon path `IOCTL_QA_TOOL_DAEMON=+16` → `priv_qa_agent` (HQA binary protocol, gl_qa_agent.c, ~110 commands; e.g. `hqa_set_txcontent_ext` L8632-8708 takes payload *rule*+len+1 byte → `MT_ATESetTxPayLoad`).

## Q3 — TX flow when ATE is armed **[V for driver, I for FW]**

Arm: `wlanoidRftestSetTestMode` (wlan_oid.c:9401-9439) → FW `CMD_ID_TEST_CTRL` `{ucAction=0, u4OpMode=1}`; completion `nicCmdEventEnterRfTest` (nic_cmd_event.c:1050-1152): `fgTestMode=TRUE`, indicate MEDIA_DISCONNECT on all AIS vifs, `nicTxRelease(TRUE)`, clear security/mgmt frames, flush glue TX packets, re-init MGMT FSMs, 500 ms wait, then NVRAM manufacture-data reload (`CFG_SUPPORT_NVRAM=1` config.h:816/867 → `wlanLoadManufactureData`, L1142-1150).

Every funcid set: `wlanoidRftestSetAutoTest` (wlan_oid.c:9649-9687; los 10155) → **`rftestSetATInfo` (wlan_oid.c:9690-9752; los 10196) — a pure FW passthrough**: builds `struct CMD_TEST_CTRL` (nic_cmd_event.h:813-821: `ucAction=1` + union{PARAM_MTK_WIFI_TEST_STRUCT}) and sends `ucCID=CMD_ID_TEST_CTRL`. **Zero driver-side funcid dispatch, zero size negotiation; the funcid interpreter lives in firmware.** Set-buffer length check is `#if 0`'d (L9663-9672). Query mirror `rftestQueryATInfo` (L9978; los …) same passthrough (query ACTION=2).

So "does ATE TX bypass the normal BSS queue?" — **moot by design**: TX is *firmware-generated* from the test template, not pushed through `nic_tx.c`/TXD v2 at all (W22's chain gl_init.c:1518→gl_kal.c:2134→wlan_lib.c:3951→nic_tx.c:1126 is not in this path; no `inject` concept needed). The FW emits: header per funcids 68/69 (DA/TA), 101 (FrameCtrl+Duration), 102 (SeqCtrl), payload per 12 (legacy PKTCONTENT) or 103 (`SET_PAYLOAD` = fill *rule*: `(rule<<16)|byte`, gl_hook_api.c:1141-1171), length per 6, rate per 3 (MCS via BIT(31)), power per 2, interval per 8, count per 7 (0=unlimited), BW per 71/72/73, ack policy per 11 (NOACK=1), started by 1/STARTTX, stopped by 1/STOPTEST — each a 4-byte value, multi-byte fields sent in chunks with selector bits in the funcindex (proven mechanism: `MT_ATESetMACAddress` sends addr bytes 0-3 then bytes 4-5 with `funcid|BIT(18)`, gl_hook_api.c:1474-1504).

**Arbitrary 802.11 frames via PKTCONTENT?** The driver forwards funcid 12 untouched, but **no in-tree caller ever drives multi-byte content through it** (only consumers: rftest.h enum + uncompiled operation_gen4m.c). Whether CONNAC FW still accepts offset-chunked PKTCONTENT writes is **FW-side, unverifiable from source [I]** — the primary experiment (E3 below) tests exactly this. Known limits from the header **[V]**: total ≤2080 B, header ≤32 B, rate/locked params are set-not-negotiated, frames carry no keying (protected flag 0 — see pcap), ack policy NOACK available. Additional quirks found: `MT_ATESetMacHeader` has a `||`-instead-of-`|` bug (gl_hook_api.c:2095 — FrameCtrl|Duration always collapses to 0/1), so FC control should be driven via raw funcid 101 calls, not that helper.

**On-air proof from the 2017 capture [V]:** `testmode1.pcap` (extracted/, 9 radiotap packets, linktype 127) — all frames **QoS-Data FC=0x0088, protected flag 0**, QoS-ctrl 0x0020 (**NoAck**), DA=00:80:12:13:14:15, SA=01:00:00:00:00:00, BSSID=ab:cd:00:00:00:00 (FW template placeholders), 1024 B frames of pseudo-random fill, seq incrementing 40→43, rate 0x60=48 Mbps (matches post #3 "RATE_48MBPS"), ch 2412, HW-appended FCS, received at −48 dBm. ATE TX is **real RF**, not emulation — but with FW-generated payload, i.e. the custom-content gap is the whole experiment.

## Q4 — Firmware command IDs + CONNAC evidence **[V for IDs, I for FW behavior]**

- Carrier: **`CMD_ID_TEST_CTRL = 0x01`** (wsys_cmd_handler_fw.h:175, "Define CMD ID from Host to firmware (v0.07)") — the mission's 0x30-0x3F hypothesis is **disproven**: that range is roaming/phy/NOA/UAPSD (L223-238). Actions: 0=switch mode (op 1=RF test, 2=ICAP), 1=Set ATInfo, 2=Query ATInfo.
- CONNAC extended space: **`CMD_ID_LAYER_0_EXT_MAGIC_NUM=0xED`** (wsys_cmd_handler_fw.h:341) + **`EXT_CMD_ID_RF_TEST=0x04`** (nic_cmd_event.h:284) — used by the modern engine (`wlanoidExtRfTestICapStart/Status`, wlan_oid.c:9794-9856) for ICAP/RDD; neighbors: EFUSE 0x01, RF_REG 0x02, RADIO_ON_OFF 0x05, OBTW 0x2F. There is **no separate ATE opcode in the 0x30-0x3F WSYS range [NF]**.
- FW honoring: driver-side code is production-complete for MT6631 (begonia, CONNAC 2.0) — ATE/QA agents + OIDs are built in, `nicCmdEventEnterRfTest` expects a FW completion event, and per-chip `chips/mt6631/` supplies `u2CmdTxHdrSize` etc. Direct public documentation of the FW funcid interpreter: **[NF]** (closed). Corroboration that MTK FW testmode semantics survive across CONNAC generations: openwrt **mt76** ships `mt76-test`, explicitly "similar to the ATE command set of the SDK driver" (`tools/README.md`), mapping `tx_count/tx_length/tx_rate_*/tx_power` to the same ATETX* parameter names, with `tx_frames` = "send packets with configurable rate/txpower" — again *generated* payloads, no arbitrary-content parameter in the ATE mapping. In-tree QA-era funcids beyond 2017 (101/102/103, 128-134) exist precisely because FW learned new content-control commands by MT6632-era — circumstantial evidence the set kept growing [I].

## Q5 — Concrete on-device experiment plan (root shell, zero kernel changes)

**Tooling:** any iwpriv (wireless-tools, static build fine) or a 30-line C ioctl caller; external monitor-capable card (ath9k_htc/rtl8812au) on another host running wireshark/tcpdump. No NVRAM work needed — `fgNvramAvailable` is satisfied by the phone's own calibrated data (gl_kal.c:5187-5193; set at driver init).

```sh
su
# --- E0: arm ATE (FW CMD_ID_TEST_CTRL opMode=1; wlan0 disconnects & queues flush)
iwpriv wlan0 set_test_mode 2011          # magic 2011 = RF test mode; dmesg | grep RFTEST
# --- E1: basic TX (channel 1, 48 Mbps, 1024 B, unlimited, NOACK)
iwpriv wlan0 set_test_cmd 18 2412000     # 18=CHNL_FREQ, data=freq kHz (gl_hook_api.c:522)
iwpriv wlan0 set_test_cmd 71 0           # 71=SET_CBW 20MHz; 72=SET_DBW; 73=SET_PRIMARY_CH
iwpriv wlan0 set_test_cmd 2 30           # 2=POWER (raw gain; START LOW)
iwpriv wlan0 set_test_cmd 3 10           # 3=RATE: RF_AT_PARAM_RATE 10 = 48M (MCS: 3|0x80000000)
iwpriv wlan0 set_test_cmd 6 1024         # 6=PKTLEN
iwpriv wlan0 set_test_cmd 7 0            # 7=PKTCNT, 0=unlimited
iwpriv wlan0 set_test_cmd 8 20000        # 8=PKTINTERVAL µs (default 50)
iwpriv wlan0 set_test_cmd 11 1           # 11=ACKPOLICY, 1=NOACK (rftest.h:391)
iwpriv wlan0 set_test_cmd 1 1            # 1=COMMAND, 1=STARTTX  → SNIFF NOW (2412)
iwpriv wlan0 set_test_cmd 1 0            # STOPTEST
iwpriv wlan0 get_test_result 32 0        # 32=TXED_COUNT; 33=TXOK_COUNT
iwpriv wlan0 set_test_mode 0             # abort test mode, restore normal driver
```
Pass E1 = sniffer sees the template stream (à la testmode1.pcap) and TXED_COUNT climbs → FW testmode + TX engine alive on MT6631.

```sh
# --- E2: header control (DA/TA/FC/seq) — still zero-LOC
iwpriv wlan0 set_test_cmd 69 0x11223344          # 69=SET_TA bytes0-3 (memcpy order, gl_hook_api.c:1476)
iwpriv wlan0 set_test_cmd $((69|0x40000)) 0xcafe # BIT(18) = bytes4-5 (gl_hook_api.c:1489)
iwpriv wlan0 set_test_cmd 68 0xdeadbeef          # 68=SET_MAC_ADDRESS (DA) bytes0-3; +BIT(18) for 4-5
iwpriv wlan0 set_test_cmd 101 0x0208             # 101=SET_MAC_HEADER low half: FrameCtrl=0x0208 (QoS data, but try 0x00c0/0x00a0 mgmt deauth/disassoc!)
iwpriv wlan0 set_test_cmd 102 $((40<<4))         # 102=SET_SEQ_CTRL
# STARTTX → sniffer: do OUR DA/SA/FC/seq appear?
```
Pass E2 = frames with our addresses (and FC type if 101 honored). Deauth/disassoc emission would already be operationally significant even without custom payload.

```sh
# --- E3: arbitrary payload — the decision gate (PKTCONTENT=12, 4 B/call, offset<<16)
for off in $(seq 0 4 1020); do iwpriv wlan0 set_test_cmd $((12 | (off<<16))) 0x41424344; done
# also try modern: 103=SET_PAYLOAD rule mode; then STARTTX
# sniffer diff: our 0x41 pattern in captured payloads?
```
- **E3 pass** → arbitrary data-frame injection, **userspace-only**, done.
- **E3 fail but E2 pass** → header-controlled template TX only (useful: custom MACs, fixed rate/power, deauth attempt via FC) — still 0 kernel LOC; full arbitrary content needs the W22 LKM.
- **E1 fail** (TXED=0 or no RF) → retry via the QA/ATE string path `iwpriv wlan0 set ATE=ATESTART` → `ATE=TXFRAME` (gl_ate_agent.c:94-183/227-265; PRIV_QACMD_SET=29, gl_wext.c:194); then dead-end → W22 LKM.

**Risks:** (1) Radio state lockup — arm/disarm reset FSMs (disconnect+flush, 500 ms blocking); recovery ladder: `set_test_mode 0` → `ATE=ATESTOP` → rmmod/insmod wlan_drv_gen4m → reboot. Factory-exercised path, but on a modified FW unknown. (2) Regulatory — NOACK TX at raw gain on any channel; bench only, low gain, shielded/attenuated. (3) nvram — arm-time `wlanLoadManufactureData`; missing manufacture data = WARN + possibly wrong TX power tables, not a blocker; the 2017 pack's nvram/ (mt6577 libnvram) is irrelevant to begonia [V]. (4) FW-acceptance — exactly W22's blocker; here tested in 30 min instead of 600-1200 LOC of kernel work. (5) funcid-12 semantics could differ on CONNAC (2017 capture proves emission, not custom content) — treat E3 as unknown-by-design.

**Decision gate vs monx-style TX LKM:** if E3 (or E3+E2 for data-only) passes → ship injection userspace-only; write the LKM only if arbitrary-content funcids are rejected AND header-only control is insufficient for the use case (e.g., need mgmt frames *with* body, beacon crafting, or E1/E2 both fail). The LKM spec (W22 §3.4, 600-1200 LOC, radiotap parser + TXD v2 path) remains the fallback unchanged.

## Q6 — Does ATE reduce W22's 600–1200 LOC kernel estimate? **[V/I]**

**Yes — for the ATE variant the kernel delta is ZERO LOC.** Every touchpoint exists and is compiled in: OIDs (wlan_oid.c:9401-10077), iwpriv transports (gl_wext_priv.c:932-997/4763-4866, gl_wext.c:240-264), ATE/QA agents (Makefile:487-496), FW carrier (CMD_ID_TEST_CTRL=0x01 + 0xED/0x04). The experiment needs only a userspace driver (shell loop or ~100-LOC C tool calling `PRIV_CMD_TEST_CMD` / `SIOCIWFIRSTPRIV+8` directly — no iwpriv binary required). The *uncompiled* `wlan_service/` engine (template-frame TX, operation_gen4m.c:1424-1480) could be enabled by build flag (`MTK_WLAN_SERVICE_PATH`) — still 0 code LOC, but build-config + untested glue; not needed for the shell path. Residual kernel work only materializes if the decision gate sends us to the LKM (then W22's estimate stands). W22 Task-3's FW-acceptance blocker is thereby converted from a build-first unknown into a cheap userspace-first measurement.

---

### Source map (primary, local)
- 2017: `archive/xda-3591182/extracted/wifitest/libwifitest/{libwifitest.h,libwifitest.c}`; `extracted/testmode1.pcap`; `wifitest/libwifitest/Android.mk` (libnvram link).
- saikrishna-4.14.357 `…/wlan/core/gen4m/`: `include/rftest.h` (174-352, 355-376); `include/wlan_oid.h:1739-1742/1915`; `include/nic_cmd_event.h:280-344, 813-821`; `include/wsys_cmd_handler_fw.h:173-175, 341`; `include/config.h:233/261/816/1087`; `common/wlan_oid.c:9401-9752, 9978+`; `nic/nic_cmd_event.c:1050-1152`; `os/linux/gl_wext_priv.c` (92-102→h, 272-273→h, 932-997, 2940-2941, 4763-4866, 13544-13545); `os/linux/gl_wext.c:114-238, 240-264, 448-458`; `os/linux/gl_ate_agent.c:88-183, 227-265, 2645+`; `os/linux/gl_hook_api.c:115-139, 330-358, 502-542, 1141-1171, 1459-1507, 2081-2125`; `os/linux/gl_qa_agent.c:400-700, 8632-8708`; `Makefile:428, 487-496, 694-720`; `os/linux/gl_kal.c:5187-5193`; `wlan_service/glue/hal/gen4m/operation_gen4m.c:61-248, 1424-1480`.
- los-4.19.325 cross-check: `rftest.h:187`; `gl_wext_priv.c:3888-3889, 5634-5737, 15378-15379`; `gl_wext_priv.h:292-293`; `gl_hook_api.c:330/1141/2081`; `wlan_oid.c:10155-10196`; `ioctls h:101-102` — all consistent [V].

### Web sources (also appended to sources.jsonl)
- openwrt/mt76 `tools/README.md` — mt76-test utility, "similar to the ATE command set of the SDK driver"; ATETX* parameter table; `tx_frames`/`rx_frames` states (fetched 2026-11-22).
- GitHub openwrt/mt76 (context7 mirror page) — mac80211-based driver family for MT76xx/CONNAC-era chips.
- XDA t=3591182 post #3 (via W19 snapshot) — 2017 on-device ATE TX evidence.
