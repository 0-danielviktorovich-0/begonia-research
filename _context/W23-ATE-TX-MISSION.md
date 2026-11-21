# W23 — ATE test-mode TX: map the captured 2017 toolchain onto begonia's gen4m (2026-11-22)

Mission owner: Светозар. Repo: /Users/danielviktorovich/begonia-research (READ+WRITE files only; NO git commits).

## Goal
Design the internal-TX-injection experiment for begonia's gen4m via the ATE/RF-test path: map the
captured 2017 MTK ATE toolchain (archive/xda-3591182/extracted/wifitest/) onto the driver code in the
local clones, and produce an implementable experiment plan (userspace + kernel touchpoints).

## Inputs (read first)
- _context/W22-OUT-INJECTION-PATCHES.md — Task 3: internal TX NF after 22 rotations; TX-chain map
  gl_init.c:1518 → gl_kal.c:2134 → wlan_lib.c:3951 → nic_tx.c:1126/1512 (TXD v2); FW-acceptance = blocker.
- _context/W19-OUT-XDA-CAPABILITIES.md — ATE stack alive in gen4m: gl_qa_agent.c, gl_ate_agent.c,
  rftest.h (RF_AT_FUNCID_PKTCONTENT L187), iwpriv SET_TEST_MODE/SET_TEST_CMD/ACCESS_MCR handlers
  (gl_wext_priv.c:4763/4816).
- archive/xda-3591182/extracted/wifitest/ — the 2017 toolchain: libwifitest.c (WIFI_TEST_set wrapper),
  libwifitest.h (command set), main.c (CLI), wifi_hw_test_tool, nvram/, testmode1.pcap (author's capture).
- Local clones: ~/halium-build/kernels/{saikrishna-4.14.357,los-4.19.325}/.../wlan/core/gen4m/
  (+ ../common/rftest* if present — find it).

## Questions (answer with file:line evidence)
1. Command coverage: which RF_AT_FUNCID_* of the 2017 libwifitest exist verbatim in begonia's gen4m
   rftest.h? Specifically the TX-capable ones (RATE, TX_COUNT, PKTCONTENT, TX_LENG, POWER, BANDWIDTH,
   continuous TX start/stop). Build a table: 2017 funcid → begonia status (present/renamed/gone).
2. Transport: HOW does userspace reach the ATE engine in gen4m — iwpriv SET_TEST_CMD framing
   (which OID / private command / /proc path), and does the 2017 libwifitest ioctl structure match
   begonia's (struct names/sizes in the clones)?
3. TX path when ATE is armed: trace nic_tx/ate_engine flow — does ATE TX bypass the normal BSS queue
   (i.e., can it emit arbitrary 802.11 frames with custom payload via RF_AT_FUNCID_PKTCONTENT), and what
   limits exist (rate/channel locked, length caps, encryption bypass)?
4. Firmware: which FW command/ATE opcode carries PKTCONTENT TX (search fw includes: ate/qa cmd IDs,
   e.g. 0x30-0x3F range), and what evidence exists that CONNAC FW honors it (any gen4m-era QA docs,
   `ate_test` references, QA tool repos for MT6785/6631).
5. Experiment plan: concrete steps to TRY ATE-TX injection on the device (root shell commands via
   iwpriv /proc/wlan/driver, expected observability: external sniffer sees our frames), risks
   (radio state lockup, regulatory, nvram dependency — the nvram/ dir in the 2017 pack), and a
   decision gate: when ATE-TX is a dead end vs when to write the monx-style TX LKM instead.
6. Cross-check W22's estimate: does the ATE path reduce the 600–1200 LOC kernel estimate (i.e., can
   injection ship with ZERO kernel changes, userspace-only via existing ATE interface)?

## Output contract
- File: _context/W23-OUT-ATE-TX-MAP.md — per-question sections, file:line evidence, [V]/[I]/[NF],
  final "experiment plan" + "kernel-LOC delta" sections.
- Sources: append to /Users/danielviktorovich/AI-OS/.hermes/cache/scratch/begonia-recon/sources.jsonl
  (observed_at=2026-11-22) for any web references.
- English-first if you search the web; the primary work is LOCAL source analysis.
