# W14 MISSION — mainline upgrade path & open-driver development for begonia (2026-11-21)

Repo: /Users/danielviktorovich/begonia-research (orchestrator runs git — you do NOT).
Read FIRST: _context/REQUIREMENTS.md (row 33 context + general contract), _context/CONTEXT.md,
03-KERNEL-HISTORY.md (kernel landscape: MiCode 4.14 drops; LOS 4.19.325; Dinolek/mt6785-mainline 6.16/7.1;
kalpakprod/mt6785-linux 7.3.4 created 2026-11-15), 04-HARDWARE-DRIVERS.md (driver gaps + component IDs),
06-DROIDIAN-POSTMARKETOS.md (pmOS 6.16.4: what works/broken and WHY - mainline driver gaps).
User goal (row 33/U: 'mainline variant research'): what exists in the world for moving begonia OFF 4.14 to a
modern mainline kernel and/or developing open drivers - with the MINIMUM goal 'get Ubuntu Touch running'
(also acceptable: pmOS-style mainline). ≤20 tool calls. English; titled links; verified/inferred+confidence;
honest not-found markers; research-only.

## DELIVERABLE: /Users/danielviktorovich/begonia-research/14-MAINLINE-UPGRADE-PATH.md

### Section 1 — State of the art (verified)
CAVEAT from the owner (first-hand, 2026-11-21): enabling a kernel config alone was NOT sufficient on this
device — something still did not work (details forgotten). Hunt what the missing piece typically is for such
cases on MTK: firmware files (e.g. mt7663 firmware for WiFi), DT nodes/pinctrl, userspace glue — check pmOS
wiki user notes (Halhadus USB-Ethernet comment) and bring-up threads for concrete examples. Reflect this in
every 'just enable X' claim below.

- What Dinolek/mt6785-mainline (6.16/7.1 branches, tags 6.16.3-r0/6.16.4-r0/7.1-r0) and kalpakprod/mt6785-linux
  (7.3.4) actually contain vs pmOS feature table: which subsystems are enabled (check their defconfigs via
  raw.githubusercontent: mt6785_defconfig or similar), which pmOS-broken items (audio ASoC/mt6359 machine driver,
  camera pipeline, WLAN mt76, modem, battery/charger) are present/missing in each tree. Cite Makefile/defconfig
  evidence (raw fetches).
- What Linus-master has for MT6785-family SoC today (03 found NO mt6785 dts in master — re-confirm and state
  which mediatek dts are closest, e.g. mt6785 vs mt6853/mt6789 generation support).

### Section 2 — The option tree (analysis, clearly marked)
- Option A: Ubuntu Touch stays Halium-based (4.14/4.19 Android kernel) — the pragmatic UT path. Check whether
  NEWER Halium releases exist and are reusable (halium-11, halium-12.x, halium-16? — verify what actually
  ships today: docs.ubports.com porting pages + halium org); Android-11 vendor + AgentFabulous android-11.0
  tree as the base; what that buys vs current Halium-10.
- Option B: UT on mainline kernel — state honestly: no telephony (modem unsupported in mainline), mic/audio
  would need a machine driver; who has ever run UT-style stacks on mainline MTK (search 'halium mainline mediatek',
  'ubuntu touch mainline kernel mediatek') - cite or mark nothing-found.
- Option C: pmOS-style mainline (best mainline story; gaps per 06) + what specifically to build: ranked driver
  worklist (WiFi mt76 enable, audio mt6359/mt6785 machine driver upstream refs - cite any existing mt6359
  codec driver in mainline; camera seninf/isp status for mt6785-family; charger/PMIC MT6360 support already
  mainline per 04).
- Option D: open-driver development plan: which components are realistic for community/owner RE work
  (touchscreen already shipped in pmOS as firmware pkg; battery/charger via MT6360; what needs Ghidra-class RE
  of vendor blobs - cross-ref 11 when it exists).

### Section 3 — What the world already has
- Other mainline-MTK handset efforts to learn from (mt6797/mt6785/mt6833 phones in postmarketOS; megapixels/
  camera stacks; any 'mainline android phone' projects) - 3-6 concrete links, cite what you saw.
- Upstream engagement points: linux-mediatek ML (lore.kernel.org/linux-mediatek), Mediatek maintainers for
  sound/soc (verify names from mainline MAINTAINERS via raw github), pmOS aports workflow for device bring-up.

### Section 4 — Recommended route for THIS owner
- Ranked recommendation (A now, C parallel, B long-term or never) with the concrete first 3 work items each,
  tied to files/sections in this repo. Explicit about effort levels and unknowns.

## OUTPUT
Write the file; append sources to /Users/danielviktorovich/AI-OS/.hermes/cache/scratch/begonia-recon/sources.jsonl;
return ≤250 words: per-tree driver verdicts, option-tree one-liner, top-3 first work items, not-found list.
Do NOT touch other research files. Do not run git.


## Owner clarification needed (do not block)
The owner mentioned possibly 'Linux Eduрота' (voice-input artifact, ambiguous) as a generic published
Linux option — list candidate interpretations (postmarketOS, generic mainline, EDK2/UEFI route) in your
final message so the orchestrator can confirm with the owner.
