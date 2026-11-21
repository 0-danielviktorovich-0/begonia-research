# S1 MISSION — editor-in-chief pass (begonia-research, 2026-11-21)

Repo: /Users/danielviktorovich/begonia-research (private GitHub hub, autosynced every 15 min — you do NOT run git).
You are the editor-in-chief: apply the queued corrections, then write the three synthesis files.
≤24 tool calls. English deliverables. Evidence contract: titled hyperlinks everywhere (no bare URLs),
URL + date + verified/inferred + confidence on important claims, historical vs current status separated.

## READ FIRST (in this order)
1. /Users/danielviktorovich/begonia-research/_context/REQUIREMENTS.md (all 26 rows)
2. /Users/danielviktorovich/begonia-research/_context/CORRECTIONS.md (C1-C6 queue — yours to apply)
3. /Users/danielviktorovich/begonia-research/_context/CONTEXT.md (device facts, evidence contract)
4. /Users/danielviktorovich/begonia-research/02-07 (core deliverables), 10-GUIDE-INDEX.md (skim), _context/SOURCE-CENSUS.md

## TASK 1 — apply corrections (edit files in place, preserve all other content + citations)
- C1 → 07-RECOVERY-SAFETY.md: official TWRP EXISTS (twrp.me/xiaomi/xiaomiredminote8pro.html, page 2026-11-20,
  Status: Current, maintainer theimpulson, dl.twrp.me/begonia + eu.dl.twrp.me/begonia; verbatim warnings:
  "This device hard bricks really easily for unknown reasons. Restoring device without spending real money is
  impossible as of now." and "Updates break data decryption support in this device's TWRP."). Keep the
  historical "unofficial only (2020-2021)" as HISTORY, add current status + warnings. Note tension with
  pmOS-wiki "easy to unbrick" (eras/assumptions differ: paid authorized-account service vs mtkclient).
- C2 → 02-FIRMWARE-HISTORY.md: add Bliss OS 16.9 row (Bliss-v16.9-begonia-UNOFFICIAL-vanilla-2023080{8,9}.zip,
  AndroidFileHost flid=339073, community mirror, hash-unverified, 2023-08-08/09).
- C3 → 04 + 07: reference the begonia schematic artifact (AndroidFileHost fid=8889791610682869402, by TUSER HP,
  schematic.rar) as untrusted-mirror evidence of available board documentation (do not download).
- C4 → 03: add toolchain evidence note: Telegram channel begoniaupdateindonesia shows kernel builds using
  "Ubuntu Pure Linux Clang 14.0.1" (HYDRA PLUS kernel) — community signal, medium confidence.
- C5: SKIP — verified NOT needed (03 correctly attributes lineage-* branches to LineageOS/android_kernel_xiaomi_mt6785;
  orchestrator re-verified via ls-remote: 7 lineage branches there, 0 in AgentFabulous/begonia).
- C6 → 07: add "Recovery landscape" subsection: official TWRP (see C1) + OFFICIAL OrangeFox device page EXISTS
  (https://orangefox.download/device/begonia — HTTP 200 on 2026-11-21, title "Xiaomi Redmi Note 8 Pro (begonia) -
  OrangeFox Recovery"; archive: have orchestrator snapshot if missing) + historical UNOFFICIAL unified OrangeFox
  R11.1 for begonia/begoniain (XDA thread by Duchan_xda) + updates via Telegram t.me/s/Redminote8proupdates
  (#OrangeFox posts, MIUI 11 / Android 10 base builds). Mark official-listing verified, build freshness unverified.
- After applying: edit CORRECTIONS.md — mark each item "APPLIED <date>" (keep the history).

## TASK 2 — write 00-README.md (executive summary, ≤ ~250 lines)
- What this DB is (dual scope per REQUIREMENTS 24; north star = modern Ubuntu Touch), research date 2026-11-21.
- Major findings: 10-15 highest-confidence results across all files (official MIUI ended 2022-09-16 EEA;
  MiCode kernel drops 4.14.94/141/186; newest A16 ROMs still on 4.19.325 kernel; no mt6785 DTS in Linus master;
  pmOS 6.16.4 works screen/GPU/sensors but audio/camera/wifi/bt/modem broken — mainline driver gaps; UT 24.04
  active Halium-10 port; live Droidian port (begonia-linux, nightly 2026-11-15); unlock = Mi Unlock (168h,
  Windows) OR mtkclient BROM instant (MT6785 hwcode 0x813); official TWRP + OrangeFox pages exist as of 2026-11;
  Mu-Silicium = UEFI firmware project (Windows experiment), not a Linux ROM).
- Limitations & research-method notes (XDA/Anubis walls → Wayback/API/extractor; GitHub API rate limits;
  spoiler-block losses on 4PDA; per-build trees unpublished).
- How to use this DB (start at INDEX.md once it exists; per-rom sources in 02 §7; matrices; archive).
- File map table with links (00-10 + CSVs + sources.json + _context/* + archive).

## TASK 3 — write 08-DEVELOPMENT-ROADMAP.md
- P0 Ubuntu Touch modernization path (from 05: Halium-11 feasibility given AgentFabulous android-11.0 tree;
  known gaps mic/RTC/VoLTE/GPS/autobrightness; reuse candidates from Droidian (audio/mic working claim) and pmOS).
- P1 Mainline leverage: pmOS kernel 6.16.4-r0, Dinolek mt6785-mainline 6.16/7.1, kalpakprod 7.3.4 (2026-11-15!);
  what it would take to run UT-style userland on a mainline kernel (telephony/audio gaps documented in 06).
- P2 Android-side: LOS 24.0 base (kernel 4.19.325) as the freshest native base; kernel choices (Suzaku V2 claims,
  Nova 4.14.356); vendor baseline MIUI 12.5 (per 02).
- AI-assisted development architecture (original task §6): recommended toolchain per task (mtkclient scripting,
  pmbootstrap, halium build containers, adb/fastboot loops, UART if ever needed), test/verification workflow,
  and the reproducible R&D repo layout (this repo IS the template: _context + _cache + archive + matrices + indexes).
- Host matrix summary table (macOS native mtkclient/adb/UBports-Installer; Linux VM/docker for pmbootstrap/Halium/SPFT)
  sourced from 07's new sections.
- Device-repair outlook (REQUIREMENTS 25): battery model unknown — mark as open research (do not guess),
  point to 07 backup/safety practices; note owner's phone idles with battery drain; replacement-cost sources TBD.

## TASK 4 — write 09-OPEN-QUESTIONS.md
- Unresolved contradictions (from all files + indexer): hardbrick-era claims vs mtkclient era; TWRP build choice
  (unified 3.7.1 vs base-specific); ARB-absent claim (mi-faq.ru only, low); vbmeta patched-image vs
  --disable-verification; mic UT-broken vs Droidian-works (same Halium vendor, different stacks); accel BMI120
  works on pmOS despite missing driver in 6.16.4 config; charger MT6360 vs SMB1351 duty split; shipped MIUI
  10-vs-11 at launch; regional last-build mismatches (Global/RU/CN).
- Not-found ledger (per-ROM trees absent, Xiaomi device tree never published, UART pinout unknown, LK verified-
  partitions unknown, Suzaku base version unknown, battery model unknown).
- Pending human-browser checks: point to _context/HUMAN-ASSISTS.md (7 rows).
- Explicitly: what a continuation agent should do first (ranked 5 items).

## RULES
- Do NOT touch: 01-SOURCES.md, INDEX.md, index.json, archive/index.html, firmware/kernel/hardware CSVs
  (the assembler agent owns them next). Do not run git. Do not create files beyond 00/08/09.
- When done, your final message (≤300 words): corrections applied (one line each), files written,
  top-5 findings you'd headline, anything you could not verify.
