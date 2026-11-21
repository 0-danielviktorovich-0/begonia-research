# W20 — gen4m source dive: monitor-mode feasibility in the driver we ship (2026-11-22)

Mission owner: Светозар. Repo: /Users/danielviktorovich/begonia-research (READ+WRITE files only; NO git commits).

## Goal
Determine, from SOURCE CODE ONLY (no speculation), what it takes to add NL80211 monitor mode to the
MTK gen4m WiFi driver as shipped for begonia, and whether hidden capture paths already exist.

## Sources (local clones, read freely)
- ~/halium-build/kernels/saikrishna-4.14.357/drivers/misc/mediatek/connectivity/wlan/core/gen4m/
- ~/halium-build/kernels/los-4.19.325/drivers/misc/mediatek/connectivity/wlan/core/gen4m/
- (reference, older lineage) ~/halium-build/kernels/halium-ref-4.14.141/ same path if present.
- Upstream comparison if needed: github search for other gen4m forks (e.g. openwrt MT7981 gen4m-adjacent
  trees, mt76 references). English queries only.

## Specific questions (answer each with file:line evidence)
1. **Radiotap path**: nic_rx.c has nicRxFillRadiotapMCS/VHT + MONITOR_RADIOTAP structs — who calls
   them, under which build flag / feature switch (grep the whole gen4m dir; check Kconfig/Makefile
   feature flags like CFG_SUPPORT_* that gate monitor/packet-capture).
2. **Hidden capture modes**: any "packet capture"/"p2p dev monitor"/debug netdev/OID paths
   (grep: capMode, PKT_CAP, mon, debugfs, proc entries) — list every entry point with file:line.
3. **cfg80211 gap**: os/linux/gl_cfg80211.c change_if_type covers STATION/ADHOC/AP — what would
   IFTYPE_MONITOR registration require (which ops, which internal BSS-info role enum exists — grep
   BSS_ROLE / NETWORK_TYPE / AIS / P2P role enums for a monitor-ish role).
4. **Firmware**: does the gen4m driver download per-mode firmware (FW files in
   firmware/ or wlan/ dirs)? Is there a separate "capture/monitor" firmware or ram code path?
5. **Verdict**: a scoped implementation sketch (files to touch, est. complexity small/medium/large,
   risks: firmware dependence, regulatory) for the unified kernel (4.14.357 first).

## Output contract
- File: _context/W20-OUT-GEN4M-FEASIBILITY.md — per-question sections with file:line evidence
  (paths relative to the clone), final "implementation sketch" section, explicit [V]/[I]/[NF] marks.
- No sources.jsonl needed unless you consult web pages (then append as usual, observed_at=2026-11-22).

## Context
- Purpose: owner wants internal-WiFi monitor mode on begonia (NetHunter/security work) without
  external dongles; Kali docs say generally unsupported, but gen4m's radiotap code suggests dormant
  capability. QCACLD precedent: monitor enabled via sysfs con_mode=4 with no patch.
- The unified kernel plan: _context/HALIUM-UT-BUILD-PLAN.md (Track list), skill unified-kernel-build.
