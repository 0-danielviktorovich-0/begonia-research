# HUMAN-ASSISTS — pages only a human browser can open (2026-11-21)

Agents could not access these (bot-walls survived browser + alternates). The repo owner offered to pass checks manually
manually. **How to help:** open the URL in your normal browser, wait out the challenge, then
`Ctrl+S / Cmd+S` → "Web page, complete" into `archive/human/<same-slug>.html` inside the repo
(autosync will push it). One sitting covers all rows.

| # | URL | Wall | Why it matters | Suggested filename |
|---|-----|------|----------------|--------------------|
| 1 | https://gitlab.nura.eco/nura/pmaports/-/merge_requests/1909 | Anubis ("Making sure you're not a bot"; even headless browser gets "🐴 О нет!") | The initial postmarketOS begonia port MR — authorship/dates visible only on the rendered page | `human-nura-pmaports-mr1909.html` |  ✅ RESOLVED 2026-11-21 via Brave (playwright-brave) — captured: _cache/nura-mr1909-page-live-2026-11-21.md
| 2 | https://gitlab.nura.eco/nura/pmaports/-/tree/main/device/testing/device-xiaomi-begonia | Anubis | Rendered package file listing (we hold API JSON, page adds descriptions) | `human-nura-pmaports-device-dir.html` |  ✅ RESOLVED 2026-11-21 via Brave — captured: _cache/nura-device-dir-page-live-2026-11-21.md
| 3 | https://xdaforums.com/t/guide-info-psa-redmi-note-8-pro-megathread-cfw.4056527/ | bunny.net challenge | LIVE megathread (newer than the 2026-04-15 Wayback snapshot; recent posts hold 2026 ROM/kernel links) | `human-xda-megathread-live.html` |  ✅ RESOLVED 2026-11-21 via Brave — LIVE megathread captured: _cache/xda-megathread-live-2026-11-21.md (47KB, 40 posts of page 1)
| 4 | https://forum.xda-developers.com/t/guide-begonia-unlock-bootloader-flash-twrp-and-root-proper.3995919/ | bunny.net | Unlock/TWRP/root guide — verify the Wayback copy is not missing later edits | `human-xda-unlock-guide-live.html` |  ✅ RESOLVED 2026-11-21 via Brave — LIVE unlock guide captured (20KB, newer than the 2023 Wayback copy)
| 5 | (optional) any begonia TWRP thread from megathread index | bunny.net | Unofficial TWRP builds (LR.Team 3.5.1_10) — download page often links devhost files | `human-xda-twrp-<slug>.html` |

## Already-covered by machines (no human needed)

- 4PDA threads — our server-side extractor passes (snapshots in `archive/`).
- GitLab API data (tree/MR/deviceinfo JSON) — captured in `archive/files/`.
- kernel.org / GitHub / raw.githubusercontent — open.

> Note: files dropped into `archive/human/` get indexed into `archive/index.html` at the final pass.
| 6 | https://xdaforums.com/t/xiaomi-mt6785-begonia-device-tree-source-releases.3999013/ | bunny.net | Device-tree source releases thread — no Wayback snapshot found; matters for kernel/DT lineage | `human-xda-dt-sources.html` |  ✅ RESOLVED 2026-11-21 via Brave — captured: _cache/xda-3999013-dt-sources-live-2026-11-21.md
| 7 | https://xdaforums.com/t/unlock-mtk-bootloader.4428577/ | bunny.net | MTK unlock method thread (mtkclient era) — no snapshot; recovery/dev context | `human-xda-mtk-unlock.html` |  ✅ RESOLVED 2026-11-21 via Brave — captured: _cache/xda-4428577-mtk-unlock-live-2026-11-21.md
| 8 | https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=90018812 | guest view OK; spoiler contents hidden from our extractor | MIUI-thread pinned unlock+TWRP+root guide — full steps sit in spoiler blocks the extractor drops | `human-4pda-p90018812-spoilers.html` |
| 9 | https://4pda.to/forum/index.php?showtopic=965629&view=findpost&p=90501329 | guest view OK; spoiler contents hidden from our extractor | Unbrick walk-through (GLOBAL V10.4.5.0.PGGEUXM) — steps in spoilers; 07 has the entry, not the steps | `human-4pda-p90501329-spoilers.html` |

> Note on fidelity: our 4PDA snapshots match the guest-rendered page text; a logged-in browser shows the same
> posts plus images/attachments and expands spoilers. Live XDA may be NEWER than the Wayback snapshot we used.
