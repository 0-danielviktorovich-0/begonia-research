# Offline archive

Pairing of original sources ↔ offline copies so every important context in this research is
readable locally (open any `.html` in a browser; links point back to the network originals).

- **Extracted copies** (`*-extracted.html`): clean full text produced by our fetcher from the live page
  (survives anti-bot walls that block plain curl), converted to standalone HTML with pandoc. This is the
  canonical citation layer — the research files quote from this content.
- **Raw snapshots** (`.html` without suffix): verbatim server HTML for pages that serve it to plain HTTP
  clients (UBports, Wayback/XDA, GitHub). May look unstyled offline (external CSS) but content is complete.
- **`files/`**: small text artifacts worth keeping verbatim (mtkclient usage docs, MT6785 scatter file,
  pmaports deviceinfo, GitLab API JSONs).
- **Not archived on purpose**: ROM/kernel binary images, vendor dumps (multi-GB) — see the research files
  for canonical URLs to fetch them on demand.

Snapshot date: 2026-11-21. Regenerate index: final packaging pass.

## Pre-refactor navigation snapshots

The byte-identical original root and English/Russian navigation READMEs, plus the three pre-refactor documents superseded by concurrent-main reconciliation (kernel history, root methods, topic map), are preserved in [`legacy/`](legacy/) for change auditing. These are historical snapshots; **links inside them target the old paths** and may no longer resolve. Use the current [`README.md`](../README.md) and language indexes for live navigation.

## W19 XDA thread snapshot (2026-11-22)

- [`jina-xda-3591182-p1-live-2026-11-22.md`](jina-xda-3591182-p1-live-2026-11-22.md) — XDA t=3591182 "Mediatek Wifi/BT/FM/GPS combo chips, hidden capabilities" (ogurets, 2017), full rendered thread via r.jina.ai live fetch. Direct XDA blocked (bunny.net) and the thread has no Wayback/archive.today captures; captured 2026-11-22 for W19-MONITOR-XDA-MISSION (summary in `_context/W19-OUT-XDA-CAPABILITIES.md`).

| archive/kali-nethunter-docs-index-2026-11-22.md | https://www.kali.org/docs/nethunter/ | 2026-11-22 | owner-supplied; NetHunter index: editions, porting/patching guides, known hardware |
