# begonia-research — shared context pack (2026-11-21, JST)

Research-only task. DO NOT flash anything, do not run untrusted scripts, do not download ROM images.
Deliverable: files in `/Users/danielviktorovich/begonia-research/` (UTF-8 Markdown/CSV/JSON, English).
Every subagent writes ONLY its assigned files, plus appends source records to the shared sources log.

## Device (verified facts)
Xiaomi Redmi Note 8 Pro, codename `begonia` (xiaomi-begonia), released Sept 24, 2019.
SoC MediaTek Helio G90T (MT6785), octa 2x Cortex-A76 + 6x A55, GPU Mali-G76 MC4, 6.53" 1080x2340 IPS,
4500 mAh, 64MP rear (GW1) + 20MP front, 4/6/8 GB RAM, 64/128/256 GB UFS 2.1.
Shipped Android 9 (MIUI 11 per pmOS/Nura wiki); last official Android 11 (MIUI 12.5).
Stock kernel 4.14.141 (per devices.ubuntu-touch.io). aarch64.

## Canonical sources (already fetched, full text on disk)
- Nura/pmOS wiki device page (Nura wiki is a pmOS-wiki continuation; wiki.postmarketos.org redirects there; oldid=109575):
  `/Users/danielviktorovich/AI-OS/.hermes/cache/web/wiki.nura.eco-6e9668ea25.md`
  Key: pmOS port status table (kernel 6.16.4, mainline=yes; screen/touch/GPU/NFC/sensors work; audio/camera/wifi/bt/gps/modem broken),
  unlock via mtkclient `mtk da seccfg unlock`, unbricking via BROM exploit + SP Flash Tool, partition map, boot chain BROM→PL→LK→Linux.
- UBports device page (full): `/Users/danielviktorovich/AI-OS/.hermes/cache/web/devices.ubuntu-touch.io-ec972a5657.md`
  Key: Halium 10.0, noble 24.04 stable 24.04-1.4 (2026-07-13), rc 24.04-1.5 RC 5 (2026-10-09), daily 2026-10-14,
  last device-repo commit 2026-10-10; maintainer TheKit, dev Rúben Carneiro; feature matrix (mic broken, RTC broken,
  VoLTE/GPS global issues, auto-brightness not working → repowerd#11); repos:
  https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia (id 23878040, master, last 2026-10-19)
  https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/kernel-xiaomi-mt6785 (id 23877901, halium-10.0, last 2026-07-08)
- 4PDA custom-ROM thread (GSI era → native ROMs), 1234 pages, first post by Xakep1993 2019-12-01 (p=91427572):
  page 1 full text: `/Users/danielviktorovich/AI-OS/.hermes/cache/web/4pda.to-f04dcfb8af.md`
  last page (1234, activity 2026-11-20, mentions mainline "Mu-Silicium" ROM + screenshots): `/Users/danielviktorovich/AI-OS/.hermes/cache/web/4pda.to-ef64985ef0.md`
- 4PDA MIUI thread, 1110 pages, first post by SPIRITic 2019-09-12 (p=88821588):
  page 1: `/Users/danielviktorovich/AI-OS/.hermes/cache/web/4pda.to-2d5e44a9d3.md`
  last page: `/Users/danielviktorovich/AI-OS/.hermes/cache/web/4pda.to-1564c662ad.md`
- XDA megathread https://xdaforums.com/t/guide-info-psa-redmi-note-8-pro-megathread-cfw.4056527/ is BLOCKED by bunny.net bot
  challenge for our tools (web_extract and headless browser both fail). Use Wayback snapshots
  (https://web.archive.org/web/2024/<url>) or record the limitation. Do not spend more than 2 tool calls trying to bypass.

## Verified repo facts (via GitHub/GitLab API, 2026-11-21)
- github.com/AgentFabulous/begonia — "Linux kernel source tree for the Redmi Note 8 Pro (xiaomi-mt6785)",
  default branch android-11.0, last push 2022-06-23; branches: a10-rebase, android-9.0, android-10.0-orig,
  android-10.0-staging, android-10.0, android-11.0-cfw, android-11.0-old, android-11.0-staging, android-11.0,
  android-12.0, mali-merge, staging.
- github.com/Dinolek — includes `mt6785-mainline` (last push 2026-06-17) and `highway_net`; Dinolek is the Nura/pmOS
  begonia maintainer. Note: Dinolek's GitHub only shows some repos (private forks not visible).
- gitlab.nura.eco/nura/pmaports — id 226, branch main, last activity 2026-11-21 (active today);
  device/testing/device-xiaomi-begonia and device/testing/linux-postmarketos-mediatek-mt6785 packages.
- pmOS wiki MR: https://gitlab.nura.eco/nura/pmaports/-/merge_requests/1909 (initial begonia MR).

## Output contract (per research task spec)
For every important technical claim include: exact URL; source title/author when available; publication/update date;
forum post number or permalink when applicable; exact repo branch/commit/release/file path when relevant;
whether verified directly or inferred; confidence: high/medium/low. Preserve short verbatim quotes for key claims.
Historical claims must be separated from current status. NEVER invent versions, URLs, dates, or compatibility.
If a page is inaccessible, state that explicitly in your file under a "Limitations" heading.

## Shared sources log (append 1 JSON object per line; fields: id,url,title,author,date,access,credibility,used_for)
`/Users/danielviktorovich/AI-OS/.hermes/cache/scratch/begonia-recon/sources.jsonl`
Append with python (open(...,'a')) or printf single-line. id = short unique slug like `4pda-cfw-thread`.
Do NOT rewrite the file; append only. Do not add records for the already-listed canonical sources above
(EXCEPT if you fetched them fresh yourself — then mark access:"verified-direct").

## CSV headers (write exactly these columns, UTF-8, comma-separated, quote fields containing commas)
- firmware-matrix.csv: category,name,version,android_base,region_variant,maintainer,release_or_latest_date,status,notes,source_url,confidence
  (category: official-miui | custom-rom | gsi | kernel-rom-bundle)
- kernel-matrix.csv: kernel_name,repo_url,linux_base,android_base,branch_or_ref,maintainer,last_commit_date,status,used_by,notes,source_url,confidence
- hardware-support-matrix.csv: component,ut_2404_status,droidian_status,pmos_6_16_status,android_custom_status,driver_or_hal,known_issues,source_url,confidence
  (status values: works | partial | broken | unknown; cite the feature table row you got it from)

## Pinned/index posts (user emphasis: study them!)
Both 4PDA threads have the "шапка" (pinned first posts) with guide indexes; XDA megathread post #1 is the
guide/PSA index. ALWAYS read those first (cache files above contain page 1 = posts #1-#20; use search_files on the
cache .md files to locate specific ROM guides/links inside, e.g. pattern "Lineage|crDroid|Evolution|Mu-Silicium").
When you cite a forum fact, give the post permalink (4pda.to/forum/index.php?showtopic=<id>&view=findpost&p=<pid>).

## XDA access verdict (2026-11-21, tested 3x)
Live xdaforums.com is blocked for BOTH web_extract and the headless browser (bunny.net "Hold tight" challenge
never resolves). Do NOT burn tool calls on live XDA: use these verified Wayback snapshots —
megathread: http://web.archive.org/web/20260415164458/https://xdaforums.com/t/guide-info-psa-redmi-note-8-pro-megathread-cfw.4056527/
unlock guide: http://web.archive.org/web/20230316035523/https://forum.xda-developers.com/t/guide-begonia-unlock-bootloader-flash-twrp-and-root-proper.3995919/
Other XDA URLs: resolve a snapshot via https://archive.org/wayback/available?url=<url> (1 call), or record a limitation.
User's own desktop browser may still open live XDA — if a fact can ONLY come from live XDA, put it in your file's
Limitations as "pending human-browser check" instead of guessing.

## Tool budget
≤ 20 tool calls each. Prefer web_search + web_extract + terminal curl (GitHub/GitLab APIs).
GitHub API: https://api.github.com/repos/OWNER/REPO/... (unauthenticated ok, ~60 req/h).
GitLab API: https://gitlab.com/api/v4/projects/<url-encoded-path>/... (unauthenticated ok).
gitlab.nura.eco needs `curl -sk` (self-signed cert). Use Wayback for XDA. No browser needed unless stuck.

## Finish protocol
When done: write your assigned file(s) into /Users/danielviktorovich/begonia-research/, append sources,
and return a summary (≤ 300 words): files written, 3-8 key findings with confidence, contradictions found,
inaccessible sources. Your final message is the ONLY thing the orchestrator reads — make it dense.
