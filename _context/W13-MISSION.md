# W13 MISSION — NetHunter, Wi-Fi monitor mode & useful hacks/portables (begonia, 2026-11-21)

Repo: /Users/danielviktorovich/begonia-research (orchestrator runs git — you do NOT).
Read FIRST: _context/REQUIREMENTS.md (rows 31, 32), _context/CONTEXT.md (evidence contract, bot-block policy).
Helpful background already in repo: 04-HARDWARE-DRIVERS.md (Wi-Fi chip unknown so far — part of your job to pin it),
06 (pmOS mainline kernel 6.16.4, config gaps), 10-GUIDE-INDEX.md, _context/SOURCE-CENSUS.md.
Tool budget ≤20 calls. English. Titled hyperlinks; verified/inferred + confidence on claims;
explicit "not found (searched: …)" markers; no flashing, no running untrusted scripts.

## DELIVERABLE: /Users/danielviktorovich/begonia-research/13-NETHUNTER-WIFI-EXTRAS.md

### Section 1 — Wi-Fi chip & monitor mode
- Pin the actual Wi-Fi/BT chip for begonia (suspected MT7663 family — verify via kernel trees in
  kernel-matrix.csv / vendor trees / 4PDA; cite exactly what you saw; if unresolvable, say so).
- Research monitor-mode support: mainline `mt76` driver (does it cover the chip? which kernel version?
  firmware file name), vendor-driver patches (search: "MT7663 monitor mode patch", "begonia monitor mode",
  "mt7663 pca monitor", "MediaTek wifi monitor mode github"), Kali/NetHunter kernel patches for MTK devices.
- pmOS angle: pmOS 6.16 currently ships no MTK WLAN driver (04 §finding) — could enabling `mt76` in the
  defconfig give Wi-Fi AND monitor mode? Mark as analysis vs verified.
- Owner note: he once received such patches privately (source lost) — rediscover publicly; if nothing
  public exists, state that explicitly.

### Section 2 — Kali NetHunter on begonia
- Is there official/community NetHunter support for begonia or MT6785 devices? (kali.org/nethunter devices
  list, NetHunter gitlab, XDA/4PDA threads.) What install paths would apply (TWRP zip, rootless, custom kernel
  requirements)? Cite sources; mark unverified gaps.

### Section 3 — Useful hacks & portables (REQUIREMENTS 32) — BREADTH WARNING
NetHunter is only ONE class. This section is the general developer toolbox for begonia: everything the
community normally applies to make a device better — unlocks of hidden functionality, optimizations
(thermal/battery/sched/perf profiles), harnesses (KernelSU-Next/SUSFS, Magisk module ecosystem), vendor
tweaks, debloat lists, props/overlays, audio-vc mods, charging mods, camera workarounds, anything portable
from sibling devices or GSIs. Search broadly: what do begonia/MT6785/MIUI-MTK developers actually use?
- Kernel patches/harnesses: KernelSU-Next + SUSFS (cvnertnc builder archived — 03), Suzaku V2 claims (03),
  Nova-Kernels (03) — what's reusable TODAY.
- Sibling MT6785/MT6785T devices (rosemary, merlin, galahad?): known patches/fixes worth porting (search
  "rosemary kernel patch", "mt6785 optimization", thermal/battery/sched tweaks; cite what you actually find).
- USB-Ethernet gadget configs (pmOS wiki user note: "you can enable kernel configs to use USB Ethernet") —
  where that config lives (pmOS kernel package), how to enable.
- Magisk modules / misc device hacks from 4PDA/XDA guides (10-GUIDE-INDEX has the index — reuse it, don't redo).
- Anything else portable: phh GSI tweaks, overlays, vendor tweaks (02 GSI section).

### Section 4 — What to search next / not found
- Ranked list of leads you could not verify (with the exact queries that failed).

## OUTPUT
Write the file, append consulted sources to /Users/danielviktorovich/AI-OS/.hermes/cache/scratch/begonia-recon/sources.jsonl,
and return ≤250 words: Wi-Fi chip verdict + monitor-mode verdict, NetHunter verdict, top-5 portable finds,
not-found list. Do NOT touch any other research file. Do not run git.
