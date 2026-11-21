# begonia-research — shared context pack (2026-11-21, JST)

> **New source-stack audit (2026-11-21):** [Saikrishna1504 begonia public GitHub ecosystem](../24-SAIKRISHNA1504-DEVICE-STACK-AUDIT.md) and [21-entry source inventory](../saikrishna-source-inventory.csv) cover working Android device tree, vendor blobs, low-level firmware, MediaTek AIDL HAL, 10 IMS and 4 camera patches, audio policies and six **Nov 13–15** 4.19 migration commits. Crucial caveat: device/axion expects `k85v1_64_k419_defconfig vendor/begonia.config`, while published [local manifest](https://github.com/Saikrishna1504/local_manifests/blob/udc/mt6785.xml) still selects Linux **4.14** source `kernel_xiaomi_mt6785@main`; the missing 4.19 source/fragment requires developer confirmation. Do not flash unverified firmware/preloader/TEE or copy proprietary binary payloads.

> **Language contract (2026-11-21):** English is the international/default metadata language; Russian is first-class for navigation, search and professionally reviewed translation. Start at [EN](../docs/en/README.md) / [RU](../docs/ru/README.md); obey [i18n policy](../i18n/README.md), [terminology](../i18n/TERMINOLOGY.md), [catalog](../i18n/catalog.json), [topic labels](../i18n/topics.json) and [translation checks](../tools/check_i18n.py). Reports 19–22 were originally authored in Russian; the English 19 translation is a full draft, 20–22 are digests, never claim full translated coverage. New technical terminology may not change immutable IDs, SHAs or code paths.

> **4.19 provenance correction:** [@Saikrishna1504](https://t.me/saikrishna1504) reports a working begonia Linux 4.19 forward-port; a third-party channel index dates the public post **likely 2026-11-17**, not September. Exact post ID/media and source/patchset remain unverified; [evidence and unsent DM](../23-419-TELEGRAM-OUTREACH.md). Do not confuse with 2026-09-27 Linux 6.16.4 Wi-Fi experimental result.

> **Post-wave access update (2026-11-21):** The early XDA/Anubis “blocked” notes below describe the worker's first fetch attempts, **not the final access status**. Hermes later captured the live XDA megathread first page (40 posts), XDA unlock/DT/MTK threads and Nura pages via Brave, plus selected 4PDA spoiler texts via the authenticated owner's browser. See [_context/HUMAN-ASSISTS.md](HUMAN-ASSISTS.md) and files in `_cache/` / `archive/`. **Coverage remains selective**; captures are not all pages or attachments. Try a real browser on bot walls before declaring inaccessible.

Research-only task. DO NOT flash anything, do not run untrusted scripts, do not download ROM images.
Deliverable: files in `/Users/danielviktorovich/begonia-research/` (UTF-8 Markdown/CSV/JSON; English main metadata with Russian first-class navigation and explicitly tracked translation coverage).
Every subagent writes ONLY its assigned files, plus appends source records to the shared sources log.

SCOPE (user 2026-11-21): dual-purpose DB — Linux ports (north star: modern Ubuntu Touch) AND the full Android custom ecosystem (ROMs/kernels/recoveries incl. TWRP & OrangeFox/firmware). Telegram sources: t.me/s/<channel> previews, no subscription. Every artifact gets source/open-code links; agents attempt discovery themselves.
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

Timestamps: all 'last updated'/'applied at' stamps use ISO 8601 UTC (YYYY-MM-DDTHH:MM:SSZ); JST optional in parentheses.

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

## Bot-block escalation policy (user, 2026-11-21 — MANDATORY)
On any bot-wall: 1) real browser first (isolated session via browser_exec session=...), 2) safe alternates
(Wayback snapshot, official API endpoints, server-side extractor), 3) skill-based safe workarounds
(reverse-engineering of the check is allowed ONLY passively: understand it, do not attack third-party infra).
If still blocked after ~2 distinct approaches, STOP and log the URL into _context/HUMAN-ASSISTS.md —
the human will pass the check in his own browser and drop the file into archive/human/.
Auth-walled downloads: never register forum accounts; cite URL + log to HUMAN-ASSISTS.md for the human.
Always hunt for sources beyond the obvious four (GitHub/4PDA/XDA/GitLab): SourceForge, kernel.org,
lore.kernel.org, Xiaomi official mirrors, TWRP mirrors, public Telegram channels.

## Format doctrine (user, 2026-11-21 — TOP PRIORITY)
Optimize FIRST for AI agents, SECOND for humans: stable file/section naming, fixed table columns, CSV/JSON
for structured data, explicit IDs and permalinks, no prose-only mush; human-readable INDEX/README ride on top.
## Hyperlink & public-readiness rules (user, 2026-11-21 — MANDATORY)
1. No bare plain-text URLs in deliverables: every source mention is a markdown link `[title](URL)`;
   forum facts link to the post permalink; repo facts link to the exact branch/commit/file.
2. The repo may go PUBLIC: format for an outside developer/agent — self-explaining navigation
   (README, REQUIREMENTS.md, archive/index.html), privacy-clean content, explicit Limitations,
   and a LICENSE decision before publishing.

## Offline archive requirement (user/ChatGPT, 2026-11-21 — MANDATORY)
Every important source page cited in the research gets an offline snapshot in /Users/danielviktorovich/begonia-research/archive/
(full HTML, openable locally in a browser, links clickable) + a row in archive/index.html pairing
original URL <-> offline copy <-> snapshot date. Raw markdown twins live in _cache/. Binary firmware/kernel
images are NOT committed (repo weight); small text artifacts (scatter files, defconfigs, APKBUILDs) are OK.
Orchestrator owns archive/index.html — subagents only fetch snapshots into archive/ with clear slugs and
mention them in their sources.jsonl records.

## Per-ROM source inventory requirement (user, 2026-11-21 — MANDATORY)
For EVERY ROM/firmware listed in the research, do not stop at ready-made build links: find and attach ALL
underlying sources so the entry is reusable for development — kernel source repo+branch, device tree,
vendor tree/blobs source, manifest (local_manifests), build instructions, recovery/installer assets.
Sources may live on official Xiaomi channels (MiCode/Xiaomi_Kernel_OpenSource), vendor mirrors, forums
(4PDA/XDA posts with permalinks), GitHub/GitLab — anywhere; hunt them down and cite them.
Firmware entries: extend 02-FIRMWARE-HISTORY.md with a "Per-ROM source inventory" section and add
kernel_source_url,device_tree_source_url,vendor_source_url,manifest_url columns to firmware-matrix.csv.
Custom kernels: catalog every quality custom kernel ever built for begonia (dev, repo, base version,
Android compatibility, status, what made it good) — this belongs in 03-KERNEL-HISTORY.md.
Anything unfindable gets an explicit "not found (searched: <where>)" marker — never a guess.

## Tool budget
≤ 20 tool calls each. Prefer web_search + web_extract + terminal curl (GitHub/GitLab APIs).
GitHub API: https://api.github.com/repos/OWNER/REPO/... (unauthenticated ok, ~60 req/h).
GitLab API: https://gitlab.com/api/v4/projects/<url-encoded-path>/... (unauthenticated ok).
gitlab.nura.eco needs `curl -sk` (self-signed cert). Use Wayback for XDA. No browser needed unless stuck.

## Finish protocol
When done: write your assigned file(s) into /Users/danielviktorovich/begonia-research/, append sources,
and return a summary (≤ 300 words): files written, 3-8 key findings with confidence, contradictions found,
inaccessible sources. Your final message is the ONLY thing the orchestrator reads — make it dense.
