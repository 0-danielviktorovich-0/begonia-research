# HALIUM → UT → pmOS build plan (begonia, owner-approved route, 2026-11-22)

Owner's stated sequence: Halium base for Ubuntu Touch first, then other Linuxes, then postmarketOS;
RE of drivers/firmware/blobs runs through all phases. Axion 2.9 (A16) is the reflash-return path —
the zip is on the host (`AI-OS/.hermes/cache/scratch/begonia-flash/`, SHA256 2aa00f3a…c861) — full
TWRP backup explicitly skipped by owner.

## Ground truth found (2026-11-22, verified live)

| Asset | State | Source |
|---|---|---|
| UT official community port | exists, **Halium 10.0**, kernel 4.14.141, "under heavy development"; GitLab device+kernel sources; **microphone broken** ([device page](https://devices.ubuntu-touch.io/device/begonia/)) | [device source](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia), [kernel](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/kernel-xiaomi-mt6785) (branches halium-10.0, halium-10.0-cfw, lineage-17.1) |
| **Droidian adaptation (begonia-linux org)** | Halium-10 + Debian; release 2024-09-15 (3 adaptation .debs); hardware matrix from porter README: **microphone ✔, camera ✔, calls/data/SMS/dual-SIM/MMS ✔, fingerprint ✔, rotation ✔, BT ✔, NFC ✔, GPS partial, hotspot ✗, encryption ✗** | [adaptation repo (droidian branch)](https://github.com/begonia-linux/adaptation-xiaomi-begonia/tree/droidian), kernel: [begonia-linux/linux-android-begonia](https://github.com/begonia-linux/linux-android-begonia); porters Halhadus (main), rifux; support t.me/begonia_linux |
| Halium-10 Android base | A10-era vendor required (MIUI 12.0.x A10 or LOS 17.1 — kernel repo carries a lineage-17.1 branch) | porter practice + repo branches [V] |
| rubencarneiro halium-11 branch (cited in [15](../docs/en/linux/15-RE-IMPROVEMENT-PLAN.md)) | **NOT FOUND** (git ls-remote empty) — correct 15 when reworked | [V-absence 2026-11-22] |
| Host build env | Docker 29.9.3 on the Mac — halium-boot/kernel builds runnable in containers (aarch64 target on arm64 host) | [V-host] |

## Route (decision: Droidian-first)

1. **Phase 1 — Droidian baseline** (fastest working-Linux win; mic works):
   a. Obtain MIUI 12.0.x A10 fastboot package for begonia (recipe: [15](../docs/en/linux/15-RE-IMPROVEMENT-PLAN.md)
      unpacking; MD5-verified via XM Firmware Updater index) → flash stock system+vendor (A10 base).
   b. Flash halium-boot (begonia-linux/linux-android-begonia build) to boot.
   c. Flash Droidian rootfs (bullseye arm64 from droidian.org) to data; install the 3 adaptation .debs
      (release "latest" 2024-09-15).
   d. Walk the hardware matrix on-device; record deltas vs the porter table (this is our baseline doc).
2. **Phase 2 — build our own halium-boot** (docker): kernel from begonia-linux/linux-android-begonia,
   Halium-10 config fragment + initrd; learn the config/blob plumbing (this is where RE starts:
   mixer_paths, audio_policy, fw files from the A10 vendor).
3. **Phase 3 — UT rootfs on the same halium-boot**: reuse Phase-2 boot + A10 vendor; UT device tree from
   the GitLab community port as reference; fix the UT microphone using the Droidian audio diff
   ([05 §](../docs/en/linux/05-UBUNTU-TOUCH.md) mic row) — this was the 15-plan's first milestone anyway.
4. **Phase 4 — pmOS mainline** ([15-RE](../docs/en/linux/15-RE-IMPROVEMENT-PLAN.md) staging: Wi-Fi/BT mainline spike → audio driver).
5. **RE thread throughout**: A10 vendor unpack (simg2img + debugfs; never execute ELBs), Ghidra 12.1.4 +
   Craft Anything ready on the host; blobs ledger → [11-BLOBS-FIRMWARE-SOURCES.md](../docs/en/kernels/11-BLOBS-FIRMWARE-SOURCES.md).

## Return-to-Android path (kept intentionally cheap)

Axion zip re-flash from TWRP (package carries FW+TWRP; [07 §N.2](../docs/en/recovery/07-RECOVERY-SAFETY.md)) — ~10 min.
Safety images already on host: nvram/nvdata/nvcfg/persist/boot (A14-era, taken 2026-11-22 pre-flash).

## Open items

- Exact MIUI 12.0.x A10 fastboot package version for begonia (Global vs EEA — [17 A06](../docs/en/research/17-INDEPENDENT-AUDIT.md):
  regional discipline) — pick after checking the adaptation README's install section + t.me/begonia_linux.
- Droidian rootfs edition (bullseye vs trixie-era) matching the 2024-09 adaptation debs.
- Whether halium-boot builds exist as CI artifacts (avoid local build for Phase 1; build only in Phase 2).


## Update 2026-11-22 (owner decision: 4.14 now, 4.19 when ready; halium version question answered)

- **Owner's halium-version question** ("why old halium when new exists"): the adaptation layer is the
  bottleneck, not the halium number. Halium-14 expects an **A14 vendor** + generic-system-style setup;
  begonia has **no halium-14 adaptation** — porters spent years building the halium-10 one (Droidian:
  working mic/camera). The Axion **A16 vendor** would need a halium-16-era hybris — no ecosystem.
  Staged answer: halium-10 now (adaptation exists) → halium-14 research as Phase C (we own the RE).
- **Kernel-config jackpot**: the running Axion 4.19.325 kernel exposes `/proc/config.gz` — captured on
  device (`begonia-flash/logs-axion/axion-4.19.325-config.txt`, 5500 lines): **CONFIG_ASHMEM=y,
  BINDER_IPC/BINDERFS=y with "binder,hwbinder,vndbinder", OVERLAY_FS=y** already set — the future 4.19
  halium kernel is config-wise 90% ready. Public 4.19 trees: LOS-24.0 (4.19.325), mtkpapa/Sakurajima07
  (4.19.324); the exact `st20-PoWeR+` build source is not identified yet (registered).
- **Host build workspace ready**: `~/halium-build/kernels/` — `saikrishna-4.14.357` (1.4G, Phase B
  target), `halium-ref-4.14.141` (1.2G, droidian reference halium patches), `los-4.19.325` (1.5G,
  future 4.19). Next: docker build container + halium.fragment drafting against the reference tree.
- Skill created: **halium-kernel-patching** (ladder A/B/C, config checklist, docker build, fastboot-boot
  iteration loop).
