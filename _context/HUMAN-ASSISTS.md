# HUMAN-ASSISTS — pages only a human browser can open (2026-11-21)

Agents could not access these (bot-walls survived browser + alternates). Даниил offered to pass checks
manually. **How to help:** open the URL in your normal browser, wait out the challenge, then
`Ctrl+S / Cmd+S` → "Web page, complete" into `archive/human/<same-slug>.html` inside the repo
(autosync will push it). One sitting covers all rows.

| # | URL | Wall | Why it matters | Suggested filename |
|---|-----|------|----------------|--------------------|
| 1 | https://gitlab.nura.eco/nura/pmaports/-/merge_requests/1909 | Anubis ("Making sure you're not a bot"; even headless browser gets "🐴 О нет!") | The initial postmarketOS begonia port MR — authorship/dates visible only on the rendered page | `human-nura-pmaports-mr1909.html` |
| 2 | https://gitlab.nura.eco/nura/pmaports/-/tree/main/device/testing/device-xiaomi-begonia | Anubis | Rendered package file listing (we hold API JSON, page adds descriptions) | `human-nura-pmaports-device-dir.html` |
| 3 | https://xdaforums.com/t/guide-info-psa-redmi-note-8-pro-megathread-cfw.4056527/ | bunny.net challenge | LIVE megathread (newer than the 2026-04-15 Wayback snapshot; recent posts hold 2026 ROM/kernel links) | `human-xda-megathread-live.html` |
| 4 | https://forum.xda-developers.com/t/guide-begonia-unlock-bootloader-flash-twrp-and-root-proper.3995919/ | bunny.net | Unlock/TWRP/root guide — verify the Wayback copy is not missing later edits | `human-xda-unlock-guide-live.html` |
| 5 | (optional) any begonia TWRP thread from megathread index | bunny.net | Unofficial TWRP builds (LR.Team 3.5.1_10) — download page often links devhost files | `human-xda-twrp-<slug>.html` |

## Already-covered by machines (no human needed)

- 4PDA threads — our server-side extractor passes (snapshots in `archive/`).
- GitLab API data (tree/MR/deviceinfo JSON) — captured in `archive/files/`.
- kernel.org / GitHub / raw.githubusercontent — open.

> Note: files dropped into `archive/human/` get indexed into `archive/index.html` at the final pass.
