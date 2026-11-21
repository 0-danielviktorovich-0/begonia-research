# W19 — MTK combo hidden capabilities: read XDA t=3591182 fully + related threads (2026-11-22)

Mission owner: Светозар (orchestrator). Repo: /Users/danielviktorovich/begonia-research (READ+WRITE files only; NO git commits).

## Goal
1. **Read XDA thread t=3591182 FULLY** ("Mediatek Wifi/BT/FM/GPS combo chips, hidden capabilities [MT6620/MT6628/MT6630]", https://xdaforums.com/t/mediatek-wifi-bt-fm-gps-combo-chips-hidden-capabilities-mt6620-mt6628-mt6630.3591182/):
   XDA blocks extractors (bunny.net) — use the isolated browser session `w19-xda` (Brave lane; the
   owner's profile already passes). Capture: the OP technique for unlocking monitor mode + FM TX on
   old MTK combo chips, which driver files/OIDs/debug commands are patched, links to any patches,
   post permalinks for every claim (`showtopic=3591182&view=findpost&p=<pid>`). Save page(s) to
   /Users/danielviktorovich/begonia-research/archive/ (offline snapshots) and summarize findings into
   /Users/danielviktorovich/begonia-research/_context/W19-OUT-XDA-CAPABILITIES.md.
2. **Assess applicability to gen4m** (the MT6785-era driver, descendants of those old combo drivers):
   does the unlock technique (debug FS, private OID/ioctl, test mode) appear in modern gen4m?
   Cross-check with W20's source findings (file below) if its output exists yet; otherwise note the
   question and answer from your own web findings.
3. **Related threads**: any other XDA/Kali/NetHunter threads about MTK internal-WiFi monitor
   (queries in ENGLISH first: "mediatek combo monitor mode patch", "MTK wlan monitor hidden",
   "gen4m monitor", "MT6630 monitor injection"; multi-language OK, RU only for 4PDA). Record each
   with permalink + 1-line verdict.

## Output contract
- File: _context/W19-OUT-XDA-CAPABILITIES.md — sections: OP technique (verbatim key quotes),
  applicability to gen4m (V/I/NF verdicts), related-thread table (title, URL, permalink, verdict).
- Sources: append to /Users/danielviktorovich/AI-OS/.hermes/cache/scratch/begonia-recon/sources.jsonl
  (fields: url, title, type, observed_at=2026-11-22, source_last_change_observed, used_for, notes).
- Every fact: [V] verified from source / [I] inferred / [NF] not found. Confidence: high/medium/low.
- Snapshots into archive/ with capture date; manifest line in archive/README.md if you add files.

## Known context (do not re-derive)
- gen4m has RX radiotap plumbing (nic_rx.c MONITOR_RADIOTAP) but gl_cfg80211.c lacks IFTYPE_MONITOR
  (verified in cloned trees ~/halium-build/kernels/saikrishna-4.14.357 and los-4.19.325).
- QCACLD precedent: monitor via sysfs con_mode=4, no patch (kimocoder/qualcomm_android_monitor_mode).
- Kali docs rule: internal Android WiFi monitor generally unsupported; external OTG cards = community path.
- begonia WiFi chip: MT7663-family suspected (not pinned); AkameKernel (owner's old kernel) ships
  external-adapter driver packs (rtl8188eus/fu, ath9k_htc).
