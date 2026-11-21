# W22 — Injection patches: Anonym3310 originals + Kali NetHunter official patch sets + internal-TX search (2026-11-22)

Mission owner: Светозар. Repo: /Users/danielviktorovich/begonia-research (READ+WRITE files only; NO git commits).

## Owner's framing (do not lose)
1. Owner's old GitHub account **Anonym3310** contains a collection of patches (likely in
   AkameKernel-begonia or a patches dir). Find them and find their ORIGINALS (upstream patch sources).
2. Official Kali NetHunter docs/builds applied patches to enable injection — locate the official patch
   sets and what exactly they enable.
3. Goal: injection support for the unified kernel — external adapters FIRST (proven path), and check
   whether INTERNAL (gen4m) TX injection is feasible at all (RX-only is the current known state:
   radiotap0 netdev has no ndo_start_xmit [V, W20]).
4. **Do NOT treat AkameKernel configs as truth** — owner built it semi-amateurishly; it's a pointer to
   WHAT exists, every choice verified against MODERN guides (Kali docs, morrownr, aircrack-ng repos).

## Tasks
1. **Anonym3310 scan**: list all repos/branches of https://github.com/Anonym3310 (GitHub API is fine:
   api.github.com/users/Anonym3310/repos). Focus: AkameKernel-begonia (branches Q-OSS-SLMK etc.),
   any patches/ dirs, additional-drivers-pack, commit messages mentioning injection/monitor/rtl.
   Clone shallowly into /tmp if needed (terminal available). Extract: WHICH patches exist (file names,
   chipsets), WHERE their originals live (aircrack-ng/rtl8188eus, kelebek333/rtl8188fu,
   aircrack-ng/rtl8812au, Kali's nethunter kernel patches, ath9k_htc mainline). Note which patches are
   owner-modified vs verbatim upstream (diff if cheap).
2. **Kali NetHunter official patch sources**: find the official kernel patch sets NetHunter ships
   (gitlab.com/kalilinux/nethunter + nethunter.com kernel build docs + the NetHunter GitLab
   kernel-patches repo(s)). What patches does the official build apply for: rtl8188eus, rtl8188fu,
   rtl8812au/8821au, ath9k_htc, rtw88? Where do they live (exact repo paths), what do they change
   (monitor/injection flags)? Quote the Kali docs lines on external cards (kali.org/docs/nethunter/wireless-cards/).
3. **Internal gen4m TX injection search** (ENGLISH, 5+ rotated passes, don't quit early):
   "gen4m injection", "mediatek wifi injection android", "connac injection", "wlan_drv_gen4m tx inject",
   "MT6789 injection", "monx injection", "gen4m ndo_start_xmit monitor", site:github.com variants,
   XDA/GitHub/Kali forums. Verdict per pass; if a single artifact exists — full analysis like W21 did
   for RX. If truly nothing: state the engineering estimate of what internal TX would require
   (gen4m TX path: nicTxSendMessage/P_MBSS queues, radiotap TX netdev with a crafted TX hook)
   — file:line evidence from the clones (~/halium-build/kernels/saikrishna-4.14.357/...gen4m/).
4. **Modern-guide adapter list**: from kali.org/docs/nethunter/wireless-cards/ + morrownr + aircrack-ng,
   produce the CURRENT recommended external-adapter chipset list for NetHunter (monitor+injection) and
   which kernel options/driver sources each needs — this feeds the unified kernel's driver-pack decision
   (replacing AkameKernel-derived choices).

## Output contract
- File: _context/W22-OUT-INJECTION-PATCHES.md — sections per task, evidence with permalinks/file:line,
  [V]/[I]/[NF] marks, the modern adapter table, and a "unified kernel patch stack" proposal
  (which patches to apply in our build, with original sources).
- Sources: append to /Users/danielviktorovich/AI-OS/.hermes/cache/scratch/begonia-recon/sources.jsonl
  (url, title, type, observed_at=2026-11-22, source_last_change_observed, used_for, notes).
- Every not-found: exact queries tried (all rotations).

## Context
- W21 already swept RX-monitor (found mt6789-wifi-monitor, RX-only) — do NOT re-do RX; your scope is TX/injection.
- Prior knowledge: Kali docs "external cards necessary because Android devices do not support monitor
  mode" + chipset list (rtl8187/8192CU etc.); AkameKernel shipped rtl8188eus/rtl8188fu + ath9k_htc AR9271 support.
- English-first discipline; RU only for 4PDA. Multi-pass minimum: 5 rotations per subtopic before any [NF].
