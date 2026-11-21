# W17 MISSION — 16-ROOT-METHODS.md (root-methods registry for begonia)

Deliverable: `16-ROOT-METHODS.md` in the repo root. Research-only: no flashing, no executing
untrusted scripts. Budget: ≤ 30 tool calls. Sources file: append to
`~/AI-OS/.hermes/cache/scratch/begonia-recon/sources.jsonl` (JSONL, fields:
url/title/type/author/observed_at=2026-11-21T+timeZ/source_last_change_observed/null/used_for).
Conventions: observation stamps ISO 8601 UTC; every claim = titled markdown link;
[V] verified / [I] inferred / [NF] not found (with the search list); confidence high/medium/low;
never invent versions, dates, or URLs. Do NOT edit other research files. No git.

## Scope (owner's request, 2026-11-21)
Collect ALL root methods that exist for begonia (Xiaomi Redmi Note 8 Pro, MTK MT6785, Android
9→17 era ROMs), with what each needs, current status/freshness, and risk notes:
1. **Magisk** — boot.img patch path (patch boot in TWRP / Magisk app; extract boot.img from the
   fastboot package; vbmeta disabling -- AVB; A/B notes if any). Latest Magisk release + version
   used by begonia guides.
2. **KernelSU / KernelSU-Next (+ SUSFS)** — kernel-integrated: which begonia kernels ship it
   (AkameKernel, Suzaku V2 claims KernelSU 35053 + SUS-FS 2.2.0 per 03-KERNEL-HISTORY §2.3,
   cvnertnc/Begonia-Kernel-Builder (archived 2026-09-16) as fork-and-run template,
   Nova-Kernels kernel_xiaomi_mt6785). LKM/KPMonkey generic-install variants if documented for MTK.
3. **APatch** and **SukiSU** — availability for begonia/MT6785 (4PDA threads t=1082492 / t=1108076
   are the RU hubs; check the begonia CFW шапка t=974421 for device-specific builds).
4. **Patched/custom kernels with root built in** — the 4PDA kernel list (шапка of t=974421):
   Coconut, PoWeR, UnicornHorn, QuantumKiller/Neutrino, Suzaku — note which are "root included"
   vs root-via-Magisk-anyway.
5. **Direct/exploit methods** — mtkclient-based (bootloader unlock first: `mtk da seccfg unlock`),
   any old MTK exploits if still relevant (mtk-su by ...? state its status for MT6785 honestly —
   likely N/A; do not invent). Magisk-Delta/other forks only if real links found.

## Sources to mine (priority order)
- 4PDA: CFW шапка t=974421 (kernel/root sections), Magisk t=774072, KernelSU t=1067995,
  APatch t=1082492, SukiSU t=1108076, unlock thread 965629 (spoilered posts are human-assisted —
  skip if guest-hidden, note it in HUMAN-ASSISTS terms already used).
- XDA begonia Megathread 4056527 (root section) + the unlock guide 3995919.
- Official docs: topjohnwu/Magisk releases page, KernelSU-Next docs (github rifsxd/KernelSU-Next),
  APatch (bmax121/APatch), SukiSU (SukiSU-Ultra repo), ksu docs on SUSFS.
- Telegram: find the Redmi Note 8 Pro updates channel(s) the owner remembers ("что-то апдейт/
  обновления Redmi Note 8 Pro") — search site:t.me redmi note 8 pro, tgstat/telemetr mirrors,
  the CFW шапка (4PDA threads often link their TG). Record t.me links + what they publish +
  last-visible-post date; do NOT join anything.
- Existing repo files: 03-KERNEL-HISTORY.md (§2.3 kernel zips), 10-GUIDE-INDEX.md (§2 root),
  07-RECOVERY-SAFETY.md (unlock) — cross-reference, do not duplicate; link instead.

## File structure
1. Matrix table: method | what it patches | needs (unlock? TWRP? custom kernel?) | works on which
   ROM bases (A9→A17) | status/freshness (observation-stamped) | risks | sources.
2. Per-method subsections with concrete steps as documented by sources (verbatim quotes for the
   critical warnings; begonia-specific caveats e.g. AVB2.0 Close warning from the unlock guide).
3. Telegram channels subsection (what exists, what it publishes, links, freshness).
4. Open questions + not-found ledger (searched: ...).
5. Update `README.md` file-list row (add 16-ROOT-METHODS.md line, ISO stamp) — allowed; nothing else.

## Definition of done
- File exists, all links titled, no bare URLs, JSONL lines valid JSON, honest [NF] markers,
  `bash tools/audit_bare_urls.py` passes for the new file (run it).
