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

The byte-identical original root and English/Russian navigation READMEs are preserved in [`legacy/`](legacy/) for change auditing. These are historical snapshots; **links inside them target the old paths** and may no longer resolve. Use the current [`README.md`](../README.md) and language indexes for live navigation.
