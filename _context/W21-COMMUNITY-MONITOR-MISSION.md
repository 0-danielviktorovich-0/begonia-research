# W21 — Community attempts: internal-WiFi monitor on MTK Helio devices + NF-ledger re-check (2026-11-22)

Mission owner: Светозар. Repo: /Users/danielviktorovich/begonia-research (READ+WRITE files only; NO git commits).

## Goal
Sweep the community (ENGLISH-first web_search, GitHub, XDA public pages, Kali/NetHunter resources;
RU only for 4PDA) for ANY working internal-WiFi monitor mode on MTK Helio-generation devices
(G90T/MT6785 family and close siblings: MT6768/MT6785/Helio G80/G85/G90/G95 devices — Redmi Note 8 Pro,
Note 9, Note 10 variants, Realme/Oppo MTK models). Also re-check the not-found ledger items below.

## Specific asks
1. Any GitHub patch/repo enabling monitor (NL80211_IFTYPE_MONITOR or packet-capture netdev) in
   MTK **gen4m/wlan_drv_gen4m**-based Android kernels. Search terms (rotate, several passes):
   "gen4m monitor", "wlan_drv_gen4m monitor", "MTK wlan packet capture android", "cfg80211 monitor
   mediatek android patch", "netHunter internal wifi mediatek", site:github.com variants.
2. Kali NetHunter device-kernels index + forums: any MTK device with INTERNAL card monitor? (Kali
   docs claim unsupported generally — find exceptions, with permalinks.)
3. **NF-ledger re-checks** from docs/en/android/13-NETHUNTER-WIFI-EXTRAS.md §4 (read it first):
   - HYDRA kernel (viperkernels.com/devices/begonia, XDA t=4523225) — features list (site was JS-only).
   - "mt7663 pca monitor" exact-query retry.
   - Anything new on MT7663S/mt76 SDIO on Android 4.14/4.19 trees (not mainline).
4. Identify begonia's EXACT WiFi chip variant if any source pins it (SDIO ID, firmware file name,
   dts node in cloned kernels at ~/halium-build/kernels/*/arch/arm64/boot/dts/ or vendor dtsi —
   local grep allowed: search "wlan" / "7663" / "connac" in dts + gen4m config headers).

## Output contract
- File: _context/W21-OUT-COMMUNITY-SWEEP.md — findings table (source, permalink, device/chip, verdict
  [V/I/NF], 1-line summary), a section per numbered ask, and an updated "what to search next" list.
- Sources: append to /Users/danielviktorovich/AI-OS/.hermes/cache/scratch/begonia-recon/sources.jsonl
  (url, title, type, observed_at=2026-11-22, source_last_change_observed, used_for, notes).
- Every claim: permalink. Every not-found: the exact queries tried.

## Context
- The 13-file (docs/en/android/13-NETHUNTER-WIFI-EXTRAS.md) holds the prior verdicts — read §1 and §4
  FIRST so you don't repeat already-done searches; your job is NEW queries and ledger re-checks.
- English-first discipline (owner rule): RU only for 4PDA-specific content.
