# begonia-research

Research knowledge base for **Xiaomi Redmi Note 8 Pro (`begonia`)** — firmware, kernels, hardware drivers,
Ubuntu Touch, Droidian, postmarketOS, bootloader/recovery — prepared as the foundation for AI-assisted
Linux porting work (Ubuntu Touch first, then modern Halium and mainline).

**Status: research in progress (started 2026-11-21).** Files `00–09` and the matrices are being written
by parallel research agents; this README is a placeholder until `00-README.md` (executive summary) lands.

## Repository layout

- `00-README.md` … `09-OPEN-QUESTIONS.md` — the research deliverables (Markdown, UTF-8)
- `firmware-matrix.csv`, `kernel-matrix.csv`, `hardware-support-matrix.csv` — structured matrices
- `sources.json` — aggregated source index (access status, dates, credibility)
- `_context/CONTEXT.md` — the shared context pack: verified device facts, canonical source list,
  evidence contract, tool-access verdicts. **Every collaborating agent must read this first.**
- `_cache/` — full-text snapshots of the primary sources as fetched on 2026-11-21 (4PDA threads,
  pmOS/Nura wiki, UBports device page)
- `begonia-research.zip` — final packaged deliverable (added at the end of the run)

## Collaboration rules (for ChatGPT and any other agent)

1. Read `_context/CONTEXT.md` before writing anything. It defines the evidence contract:
   every important claim carries exact URL, title/author, date, forum permalink where applicable,
   repo branch/commit where applicable, verified-vs-inferred flag, and a confidence level
   (high / medium / low). No invented versions, URLs, or compatibility claims.
2. This is a **research-only** repo: no device flashing, no execution of untrusted scripts.
3. When editing deliverables, keep the existing citation style and separate *historical* claims
   from *current status*. Record inaccessible sources explicitly instead of substituting snippets.
4. Live xdaforums.com is bot-blocked for automated tools (bunny.net); use the Wayback snapshots
   listed in `_context/CONTEXT.md`, or flag the fact as "pending human-browser check".

## Primary sources (see `_context/CONTEXT.md` for the full annotated list)

- 4PDA: Redmi Note 8 Pro — unofficial firmware thread (t=974421) and MIUI thread (t=965629)
- XDA: Redmi Note 8 Pro megathread CFW (4056527, via Wayback)
- UBports: devices.ubuntu-touch.io/device/begonia + GitLab port repos
- pmOS/Nura wiki: Xiaomi Redmi Note 8 Pro (xiaomi-begonia) — kernel 6.16.4 mainline port
- GitHub: AgentFabulous/begonia (kernel), Dinolek/mt6785-mainline; GitLab: nura/pmaports
