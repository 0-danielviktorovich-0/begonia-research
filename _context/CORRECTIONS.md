# Corrections queue — apply to deliverables after augmentation agents finish (2026-11-21)

Own-file edits are deferred while augmentation agents hold the files (W9 edits 07; W8 edits 02).
Apply each correction at the synthesis pass, then delete the row.

## C1 — 07-RECOVERY-SAFETY.md : official TWRP exists (was: none)
- Was written: "No official TWRP: twrp.me/xiaomi has zero begonia matches (grep-verified); unofficial builds only (LR.Team; TWRP 3.5.1_10 Unified 2021-03-18)".
- New verified fact: twrp.me/xiaomi/xiaomiredminote8pro.html — "TWRP for Xiaomi Redmi note 8 Pro", page updated 2026-11-20, Status: **Current**, Maintainer: **theimpulson**, downloads dl.twrp.me/begonia / eu.dl.twrp.me/begonia, "Device Tree / files" + XDA support thread linked. Offline: archive/twrp-begonia-page.html, archive/twrp-begonia-dl.html.
- Resolution: the historical claim (2020-2021 era: unofficial only) stays as history; the CURRENT status is official TWRP support (page fresh as of 2026-11-20). Likely page update post-dates the Wayback/megathread evidence W6 used.
- Add verbatim warnings to 07: "This device hard bricks really easily for unknown reasons. Restoring device without spending real money is impossible as of now." / "Updates break data decryption support in this device's TWRP." — and note the tension with the pmOS-wiki "easy to unbrick via BROM exploit" (different eras/assumptions: paid authorized-account service vs mtkclient; keep both, dated).
- Sources: this census (SOURCE-CENSUS.md) + archived page. Confidence: high (fetched 2026-11-21).

## C2 — 02-FIRMWARE-HISTORY.md : Bliss OS 16.9 missing
- AndroidFileHost hosts Bliss-v16.9-begonia-UNOFFICIAL-vanilla-20230808.zip (+20230809) — a 2023 Android-13-era unofficial ROM absent from the ROM catalog. Add one row (class: community mirror, hash-unverified; source: androidfilehost.com/?a=show&w=files&flid=339073).

## C3 — 04/07 : device schematic artifact
- AndroidFileHost hosts "Xiaomi Redmi Note 8 Pro (begonia) Schematic.rar" by TUSER HP (fid=8889791610682869402) — schematic boardview-class artifact; reference it in 04 (hardware) and 07 (test points/UART) as untrusted-mirror evidence of available documentation (do not download per research-only policy).

## C4 — kernel notes (from census)
- t.me/begoniaupdateindonesia posts show kernel builds using "Ubuntu Pure Linux Clang 14.0.1" (HYDRA PLUS kernel) — toolchain evidence for 03's toolchain section (community signal, medium).
- Erfan treble GSIs used vendor image "begonia-user 10/QP1A.190711.020/20.5.14" (2.66 GiB) — historical GSI vendorbase data point for 02 (medium).
