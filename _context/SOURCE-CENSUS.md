# Source census — source classes beyond GitHub / 4PDA / XDA (2026-11-21)

Probed with live searches; every class lists evidence actually seen (not assumed). Confidence in brackets.
Purpose: standing source classes for this and future researches (see REQUIREMENTS.md row 21).

## Verified classes

- **Xiaomi official mirrors** [high] — full last-official set cross-confirmed: xiaomirom.com/en/download/redmi-note-8-pro-begonia-stable-V12.5.15.0.RGGEUXM (fastboot 4.4 GB, 2022-08-26); xmfirmwareupdater.com/miui/begonia/stable/V12.5.15.0.RGGEUXM (package miui_BEGONIAEEAGlobal_V12.5.15.0.RGGEUXM_cd5652a4c4_11.0.zip); xiaomifirmware.com/firmware/begonia (recovery 2.4 GB 2022-09-16, fastboot 2022-08-26, region-suffix table); mifirm.net/downloadzip/11792. Matches 02's "official MIUI ended 2022" finding from an independent class of sources.
- **TWRP official** [high] — **twrp.me/xiaomi/xiaomiredminote8pro.html EXISTS, page dated 2026-11-20, Status: Current, maintainer `theimpulson`**, downloads at dl.twrp.me/begonia + eu.dl.twrp.me/begonia. Two warnings verbatim: "This device hard bricks really easily for unknown reasons. Restoring device without spending real money is impossible as of now."; "Updates break data decryption support in this device's TWRP." → contradicts 07's "no official TWRP" (see CORRECTIONS.md). Offline copy: archive/twrp-begonia-page.html + archive/twrp-begonia-dl.html.
- **SourceForge** [high] — community mirror ecosystem is alive: sourceforge.net/projects/miui-greeshan-repack/files/MIUI/Xiaomi-Redmi-Note-8-Pro-begonia/ (regional MIUI repacks incl. MIUI-12.5-Stable-ID); projects/begoniadump (partition dumps); projects/begonia-projects ("Projects [Redmi Note 8 Pro]"); TWRP-DYNAMIC-ORANGE-RECOVERY-BEGONIA. Class: community mirrors — verify each file before use.
- **AndroidFileHost** [medium-high] — device folders with old+new artifacts: twrp-3.3.1-0-begonia_UNOFFICIAL.img (2019-11-13), Bliss-v16.9-begonia-UNOFFICIAL-vanilla-20230808.zip (Bliss OS 16.9 — a 2023 ROM not yet in 02), and notably **Xiaomi Redmi Note 8 Pro (begonia) Schematic.rar by TUSER HP** — hardware schematic, valuable for test-points/RE (04/07). Class: forum mirror — untrusted until hash-checked.
- **Public Telegram (t.me/s/ web previews)** [high] — t.me/s/begoniaupdateindonesia (device channel; kernel posts: "Used Ubuntu Pure Linux Clang 14.0.1 in HYDRA PLUS" — kernel-dev channel evidence); t.me/s/ProjectTreble_Updates (Erfan GSIs; begonia vendor image 2.66 GiB, fingerprint begonia:10/QP1A.190711.020/20.5.14). Class: community channel logs — citable as community signal, not as primary docs.
- **GSMarena** [high] — gsmarena.com/xiaomi_redmi_note_8_pro-9812.php (specs/review/compare; "first smartphone with a 64 MP camera" news context). Class: spec reference.
- **Repair-shop ecosystem** [low-medium, untrusted] — romdevelopers.com downloads tagged "begonia NvRam"/"begonia Dump" (2.61 GB dumps, WhatsApp contact = paid-service pattern); forum.gsmhosting.com/vbb/f296/xiaomi-redmi-note-8-pro-begonia-flashing-success-2937215 (SP Flash Tool flow logs). Class: useful for what files exist (NVRAM/dump availability) but NOT citable for procedures.

## Dead ends / weak negatives

- **lore.kernel.org for MT6785**: site-scoped search returns nothing; kernel W2 already found no mt6785 DTS in Linus master via two independent probes → mainlining happens in forks (Dinolek/kalpakprod), not via ML patches yet. [medium-high negative]
- **gitlab.postmarketos.org search**: no direct hits for begonia/mt6785 beyond the mt6785-mainline/linux repo already cited in 06 (APKBUILD source=). [medium]

## Recommended standing crawls (for future researches)

1. Xiaomi mirror cluster (xiaomirom/xiaomifirmware/xmfirmwareupdater/mifirm) — canonical ROM/fastboot history.
2. twrp.me device pages — official recovery status + maintainer + device-specific warnings.
3. SourceForge project search on codename — repacks/dumps/recoveries.
4. AndroidFileHost codename folders — legacy artifacts incl. schematics.
5. t.me/s/ previews of codename channels — current community pulse (kernels, ROM announcements).
6. GSMarena — hardware/spec cross-check.
7. (keep) GitHub + GitLab APIs, 4PDA via extractor, XDA via Wayback, nura/pmaports via API.
