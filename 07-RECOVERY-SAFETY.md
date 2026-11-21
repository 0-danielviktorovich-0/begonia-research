# 07 — Recovery & Safety: bootloader unlock, unbricking, backups (Redmi Note 8 Pro / `begonia`, MT6785)

> **RESEARCH-ONLY DOCUMENT.** Everything below is *documentation of publicly available procedures*, compiled 2026-11-21. Nothing here was executed, and none of it should be run against real hardware without independent verification. Unlocking the bootloader wipes userdata, may trip anti-rollback, and can hard-brick the device. "User-hostile" operations (flashing, erasing partitions, exploit payloads) are described for research purposes only.
>
> Citation contract: URL + title/author + date + verified/inferred + confidence (high/medium/low). Verbatim quotes preserved in `>` blocks.

---

## 1. Official unlock path (Mi Unlock / Windows)

**Two variants of the device exist and the official path applies to both.** From the XDA megathread (Agent_fabulous, 2020-02-24, verified via Wayback snapshot 2026-04-15): *"There are 2 variants of the Redmi Note 8 Pro. 'begonia' is the global variant whereas 'begoniain' is the Indian variant. The only difference between the 2 is NFC… The TWRP and ROM builds target both, so you do not have to worry about a thing."* (high; verified-direct)

**Pinned XDA guide** — "[GUIDE][BEGONIA]Unlock Bootloader, Flash TWRP and Root[PROPER]", pritish1998, 2019-11-02 (last edited 2021-02-02), 16 pages. Live XDA is bot-blocked; verified via Wayback snapshot `http://web.archive.org/web/20230316035523/https://forum.xda-developers.com/t/guide-begonia-unlock-bootloader-flash-twrp-and-root-proper.3995919/` (high; verified-direct). Its steps, condensed verbatim:

1. *"Download the Mi Unlock app to PC, and sign in with your Mi Account"* (Windows-only tool)
2. Enable Developer Options (tap Build Number ×7); enable **USB Debugging** and **OEM Unlocking**; *"Also add account in Mi Unlock Status (Can be found in Developer Options"*
3. Install drivers: ADB, MediaTek VCOM, MTK USB drivers
4. Power off, hold **Volume Down + Power** → fastboot; connect; click *"Unlock"* in Mi Unlock Tool
5. *"You will be given a specific time (168 hours mostly)"* — i.e. **7-day wait**; *"Wait until that and redo Unlock process"*

The megathread independently confirms the wait: *"You need to unlock your device using the Unlock Tool that Xiaomi provides and wait for almost a week (168 hours) to gain unlock permissions. There's no way to get around this."* (high; verified-direct)

**Practical Windows setup notes** (from the Nura/pmOS wiki maintainer note, oldid=109575, verified-direct, high): wiki author used Windows 10 in virt-manager with (1) **USB2 ports, not USB3**, (2) Windows booted with signing disabled, (3) Xiaomi/MTK USB drivers installed manually via Device Manager, (4) *"make sure to use the QR code in the upper left on the starting screen, the other method login failed to send an SMS in my case."*

**XiaoMiToolV2** (francescotescari): closed-source Java jar (xiaomitool.com/V2; wiki: *"Be careful, it's a closed source jar!"* — it did work on Fedora Linux for the wiki author). **PR #98 verified via GitHub API** (verified-direct, high): title *"[UNLOCK IS DEAD] 2023-02-28 Xiaomi servers deny unlock request, but flash tool still works"*, opened 2023-02-28 by `nazarewk`, state **open, not merged**. Body: *"~looks like the tool can be declared officially dead~ … Xiaomi Server denied the request to unlock device. UPDATE: it is still very useful for flashing and recovering dead devices."* → **Current status (2026): XiaoMiToolV2 cannot perform the official unlock; it remains usable for flashing/recovery.** The official-tool lockout is why the community moved to the exploit path.

---

## 2. Exploit unlock path (mtkclient, BROM)

**mtkclient** — https://github.com/bkerler/mtkclient (bkerler). README + README-USAGE read from raw.githubusercontent.com `main` branch (verified-direct, high).

- **What `mtk da seccfg unlock` does**: rewrites the `seccfg` partition flags (bootloader state) via the Download Agent after a BROM/DA exploit, then erases userdata/metadata. From README-USAGE, exact lines (verified-direct):
  > `python mtk.py e metadata,userdata,md_udc` → `python mtk.py da seccfg unlock` → `python mtk.py reset`
  (relock: `python mtk.py da seccfg lock`).
- **BROM mode entry**: README: *"boot into brom mode by powering off device, press and hold either vol up + power or vol down + power and connect the phone. Once detected by the tool, release the buttons."* pmOS wiki instruction for begonia specifically: *"Power off the phone and turn it on while holding Volume Up"*, then *"Backup preloader and run `mtk da seccfg unlock`"* (wiki, oldid=109575, high).
- **SLA / DAA / SBC for the MT6785 generation**: the megathread (verified-direct) explains them for begonia: *"Boot ROM implements security measures against attacks, which includes flashing improper or malicious firmwares. This is 'SLA' and 'DAA', that is 'Serial Link Authentication' or 'Download Agent Authentication'. This happens server side and requires the Mi Authorized Account, that only service ce[nters have]"*. mtkclient README-USAGE has a dedicated section: *"Bypass SLA, DAA and SBC (using generic_patcher_payload)"* → `python mtk.py payload`, with the note *"If you want to use SP Flash tool afterwards, make sure you select 'UART' in the settings, not 'USB'."* bypass_utility README states the same goal: *"Small utility to disable bootrom protection(sla and daa)"* (verified-direct). So on begonia the SLA/DAA wall is **bypassable locally by exploit — no authorized account needed** (medium-high: mtkclient ships an MT6785 payload and the community path works per pmOS wiki + 4PDA usage).
- **MT6785 support is explicit** in `mtkclient/config/brom_config.py` (verified-direct): hwcode `0x813: Chipconfig(... dacode=0x6785, name="MT6785", description="Helio G90", loader="mt6785_payload.bin", uart=0x11002000, brom_payload_addr=0x100A00, da_payload_addr=0x201000 ...)`. **Does every begonia unit expose BROM without auth?** mtkclient's MT6785 entry has a dedicated exploit payload (no `--loader` V6-style preloader requirement documented for MT6785 — the V6/new-protocol chips listed in README are MT6781/6789/6855/6886/6895/6983/8985, *not* MT6785), and the megathread says BROM entry needs no disassembly (below). Confidence **medium-high** that all begonia units (all shipped variants, MIUI 11/12 stock) reach BROM with the vol-up hold; no source documents an auth-locked MT6785 BROM, but per-unit efuse/SBC variation is not formally ruled out by any source I could read.
- **Backup commands from README-USAGE (exact, verified-direct)**: full flash `python mtk.py rf flash.bin`; all partitions `python mtk.py rl out`; single partition `python mtk.py r boot boot.bin`; preloader via BROM `python mtk.py r preloader preloader.bin --parttype=boot1` or `python mtk.py dumppreloader`; partition table `python mtk.py printgpt`; RPMB read `python mtk.py da rpmb r`. GUI dump: `python mtk_gui.py`.
- **Prerequisites**: Linux: python3 + `pip install pyusb pyserial json5`; README: *"For linux, a patched kernel is only needed when using old kamakiri (see Setup folder) (except for read/write flash)"* — i.e. **modern mtkclient on MT6785 does NOT need a kernel patch** for the da seccfg/rf/rl flow (medium-high). Windows: README-WINDOWS: Python ≥3.9, WinFsp, `pip3 install -r requirements.txt`, **UsbDk 64-bit** + normal MTK serial-port driver; test with *"UsbDkController -n … device with 0x0E8D 0x0003"* (verified-direct). AUR package `mtkclient-git` mentioned by pmOS wiki. mtkclient.com is even packaged in the Nura repos (wiki note).
- **Post-unlock AVB step** (README-USAGE): `python mtk.py da vbmeta 3` = disable verity + verification flags in vbmeta; and *"If you are getting a dm-verity error on Android 11, just press the power button, then the device should boot and show a yellow warning about unlocked bootloader and then the device should boot within 5 seconds."* (verified-direct, high).

**kamakiri (amonet-kamakiri/kamakiri)** — the older BROM exploit family by xyzz/chaosmaster. `kernel.patch` (verified-direct, fetched): patches Linux `drivers/usb/core/devio.c`, forcing `ret = 0` after each `check_ctrlrecip(...)` call (USBDEVFS control-submit, CLAIMINTERFACE, etc.) so unprivileged userspace can send arbitrary USB control transfers to the BROM — required to run kamakiri/bypass_utility against the phone from Linux. bypass_utility README: *"To use kamakiri you need FireISO or this patch for your kernel. Prebuilt kernels for various distros are available"*(github.com/amonet-kamakiri/prebuilt-kernels). On Windows no kernel patch is needed (UsbDk instead). kamakiri repo README 404s; the patch is the documented artifact.

**MTK-bypass/bypass_utility** (verified-direct): standalone *"disable bootrom protection(sla and daa)"* tool feeding **SP Flash Tool**: run `python main.py`, connect powered-off phone **holding Volume+**, wait for *"Protection disabled"*, *"After that, without disconnecting phone, run SP Flash Tool"* (Linux: SP Flash in **UART Connection mode**). Payloads from MTK-bypass/exploits_collection. This is the exact flow the pmOS wiki unbricking recipe references.

---

## 3. Recovery & flashing tools

**TWRP status**: **No official TWRP.** Verified: `https://twrp.me/xiaomi/` fetched 2026-11-21 contains **zero** matches for "begonia" (grep of saved HTML) (verified-direct, high). Unofficial TWRP exists, all via XDA/Telegram (live XDA blocked; snippet-level, medium):
- `[RECOVERY][begonia][UNOFFICIAL] TWRP …` — xdaforums.com/t/3972573 (early 3.x, later closed per android.stackexchange.com/questions/237521).
- `[RECOVERY][CFW][3.3.1-0][begonia] Unofficial TWRP recovery for begonia(in) [05/06]` — xdaforums.com/t/4002397, 2019-11-13.
- `[RECOVERY][UNOFFICIAL] Begonia Recovery Project Themed TWRP 3.5.0 V2 UNIFIED [begonia/begoniain]` — xdaforums.com/t/4242717.
- Telegram `t.me/s/Redminote8proupdates`: *"TWRP Recovery v3.5.1_10 | Unified | UNOFFICIAL. Updated: 18/03/'21"* — latest version date I could verify (medium).

The XDA guide's original recommendation was **LR.Team TWRP** (a Chinese third-party build, linked from post #1, 2019), with the author himself noting *"Wait for a proper TWRP"*; early TWRP could not even make backups (*"can't make the folder, key unavailable"*, post #6, 2019-11-04). For pmOS/UBports the wiki instead uses the stock recovery path: `pmbootstrap install --android-recovery-zip` → `adb push pmos-xiaomi-begonia.zip /sdcard` → flash zip in recovery (wiki, verified-direct).

**pmOS flashing via fastboot** (wiki, verified-direct): `pmbootstrap flasher flash_rootfs` + `flash_kernel` + `fastboot reboot`; **bootloop fix**: *"run `pmbootstrap flasher flash_vbmeta` (partition name 'vbmeta') and then flash_kernel"* — the documented vbmeta reflash for AVB-triggered bootloops (high).

**SP Flash Tool unbricking flow (Nura/pmOS wiki, verbatim, oldid=109575, verified-direct, high)** — Requirements (GNU/Linux): kernel patched with amonet-kamakiri/kamakiri `kernel.patch`; Python3 `pyusb pyserial json5`; **SP Flash Tool (tested with version 5.2208)**; MTK-bypass/bypass_utility; *"Known working partitions (from backup or Android ROM)"*; **MT6785 scatter file by michaelskyf**: https://gist.github.com/michaelskyf/eff1894ec531e659f2a2ec393ba61697. Steps (verbatim):
> 1. Run the exploit
> 2. Connect the device via USB and hold Volume Up (+)
> 3. When "Protection disabled" message appears, open SP Flash Tool
> 4. Select partition images that you want to write and click Download (for info/steps: youtube.com/watch?v=wm0UFvjSvVg)
> 5. After green checkmark image appears, restart your phone

Wiki footnote: SP Flash *"did not work for me. You can also use https://mtkclient.com/ … It even has a GUI (python mtk_gui.py)"* — mtkclient is a full SP Flash alternative on this device. **Contradiction note:** bypass_utility README says SP Flash in *UART* mode on Linux; the wiki flow and YouTube guide don't specify — treat UART-mode as the bypass_utility-author recommendation.

---

## 4. Test points & UART

**Test points: not needed, and no documented test-point photo set found.** Megathread (verified-direct, high): *"The phone will enter BootROM if you hold the keys at the correct time. You do not need to take the phone apart to short any pins. Just login and bind to your special account, hit 'Download' in SP Flash and hold the keys for 5-15 seconds with the device plugged in."* — i.e. **BROM entry = hold Vol-Up while plugging USB**; disassembly is unnecessary on MT6785 (the SLA/DAA wall, not hardware access, was the obstacle). Web search for begonia test-point teardown documentation returned only low-quality social/video results (e.g. a YouTube short "REDMI NOTE 8 PRO EDL OR TEST POINT AND FLASHING POINT" — content unverified) and an unrelated Redmi Note 8 (ginkgo, Snapdragon) test-point video. **Verdict: only video/photo-grade evidence exists for physical test points on begonia; no authoritative written test-point doc was found in accessible sources** (medium → mark unknown).

**UART: unknown / undocumented in accessible sources.** Search for "begonia uart" / mt6785 UART pads found nothing device-specific. Indirect evidence only: mtkclient `brom_config.py` sets BROM/PL debug `uart=0x11002000` for hwcode 0x813 (MT6785), and the pmOS wiki's `/proc/iomem` dump shows kernel serial devices `serial@11002000` and `serial@11003000` (AP UART0/1). No source documents where these pads are on the begonia PCB or a working UART-console pinout. **Mark unknown** (pending human-browser/4PDA search if needed).

**Flash-mode entry keys** (pmOS wiki, verified-direct, high): Recovery = *"Hold Volume Up and Power while connecting the device to a computer"*; Fastboot = *"Hold Volume Down and Power"*; from fastboot, `fastboot oem poweroff` shuts down. Megathread adds: on *factory* bootloader (pre-MIUI, CFW-era) *"Power + Vol Up … loads a menu"* with mode selection — obsolete on MIUI builds.

---

## 5. Backup strategies (do BEFORE unlock/flash — research-only)

1. **Full flash + per-partition dump via mtkclient from BROM** (README-USAGE, verified-direct, high): `mtk r preloader preloader.bin --parttype boot1` (preloader), `mtk rl out` (all partitions), `mtk rf flash.bin` (entire UFS), `mtk printgpt` (GPT). pmOS wiki makes preloader backup step 1 of unlocking (*"Backup preloader and run `mtk da seccfg unlock`"*).
2. **Why preloader matters most** (megathread, verified-direct, high): *"Assuming you have the factory preloader installed — Load SP Flash tool … Connect device and don't hold any keys … It should start flashing right away without any authorization prompt!"* — with a stock preloader, unbricking happens through **preloader mode with no auth**; *"If you don't have factory preloader, you will have to flash via BootROM"* which (pre-mtkclient) meant a Mi Authorized Account. The wiki's equivalent exploit flow replaces the account with bypass_utility/kamakiri.
3. **NVRAM/NVDATA/persist** (IMEI/radio/sensor calibration): partitions `nvram` (67.1MB), `nvdata` (67.1MB), `nvcfg` (33.6MB), `persist` (73.9MB), plus `protect1/2`, `proinfo`, `seccfg`, `otp`, `sec1` — all present in the GPT below; dump them individually with `mtk r <name> <file>` before any write. No source documents begonia-specific IMEI-restore procedure; **mark unknown**.
4. **Full-restore ROM**: real, currently-documented sources for begonia fastboot images (third-party mirrors of official Xiaomi bigota packages — the official en.miui.com downloader is defunct; bigota direct URLs exist behind these pages):
   - xmfirmwareupdater.com/miui/begonia/ — table incl. **V12.5.15.0.RGGEUXM EEA fastboot 2022-08-26 (last stable)**, CN V12.5.6.0.RGGCNXM 2022-06-02, ID V12.5.6.0.RGGIDXM, RU V12.5.3.0.RGGRUXM, Global V12.5.1.0.RGGMIXM 2021-06-29 (snippet-level, medium).
   - xiaomirom.com/en/rom/redmi-note-8-pro-begonia-global-fastboot-recovery-rom/ — fastboot history V10.4.2.0.PGGMIXM (A9) → V12.5.1.0.RGGMIXM (A11) (snippet, medium).
   - mifirm.net/model/begonia.ttt (fastboot tgz + MiFlash usage).
   - Region check before flashing: `fastboot getvar product` → begonia / begoniain / begonia_ru / _id / _in / _cn / _eea (XDA t/3993359, kujangsbj, 2019-10-29, snippet, medium).
   MiFlash via fastboot only works while fastboot is alive; dead devices need the SP Flash/mtkclient paths of §3.
5. **RPMB/keys**: `mtk da rpmb r`, `mtk da generatekeys` exist in README-USAGE (verified-direct) — research note, not a routine backup.

### Partition map (begonia, 64 GB unit, GPT; from pmOS wiki `parted` dump, oldid=109575, verified-direct, high)

Storage: SAMSUNG KM2H7001CM-B518 UFS, 4096B sectors. Key partitions (number:name:size):
recovery(67.1MB), misc(4MB), **para**(524kB), expdb(21MB), frp(8.4MB), **vbmeta**(8.4MB), nvcfg(33.6MB), **nvdata**(67.1MB), metadata(33.6MB), **persist**(73.9MB), **protect1/2**(8.4MB each), **seccfg**(8.4MB), otp(50.3MB), sec1(2MB), **proinfo**(3.1MB), efuse(524kB), **nvram**(67.1MB), md1img(157MB), boot_para(27MB), spmfw, audio_dsp, scp1/2, sspm_1/2, cam_vpu1-3, gz1/2, **lk**(2MB), **lk2**(2MB), **boot**(67.1MB), logo(67.1MB), **dtbo**(33.6MB), **tee1**(5.2MB), **tee2**(9.9MB), vendor(1.6GB ext2), system(3.8GB ext4), cache(453MB), gsort, oem_misc1, exaid(134MB), cust(872MB), userdata(56.1GB), flashinfo. *(Full start/end offsets in wiki cache lines 307-366; `preloader` itself is not a GPT entry — it lives in boot0/boot1 regions, read via `--parttype boot1`.)*

### Boot chain (pmOS wiki, verified-direct, high)

> 1. **BROM**: boots when power is applied; initializes flash storage, starts preloader. 2. **PL (preloader)**: initializes USB/GPIO/timers; *"If Volume Up is held, PL will hand control back to BROM"* (download mode). 3. **LK (Little Kernel)**: displays logo and *"verifies some partitions (TODO: which partitions?). If it fails to verify partition, it won't continue."* 4. Linux.

(Medium-article cross-ref: medium.com/swlh/modding-the-redmi-note-8-pro-an-adventure-e473e84d4d14. LK's exact verified-partition list remains undocumented — wiki TODO.)

---

## 6. Brick risks & unbricking

**What bricks begonia** (megathread, verified-direct, high): *"doing things like: Tripping AVB / Flashing an incompatible boot and dtbo / Flashing a weird boot image / ??? will result in a brick. You won't have fastboot, you won't have anything in such cases. Only Boot ROM download mode"*. pmOS wiki names the classic case: *"If something went terribly wrong (e.g. boot.img doesn't contain valid DTB), your device will hard-brick. Fortunately it's easy to unbrick the device."* The 2019 XDA thread shows early victims (post #10, snarl, 2019-11-17: *"Bricked my China Rom Phone… Should I REM out the antirollback check lines in flash_all.bat?"* — anti-rollback in MIUI flash scripts was a live risk; cross-region China↔Global flashing caused bootloops, posts #8/#9).

**Unbricking — two documented regimes:**
1. **Stock-preloader regime (megathread, pre-mtkclient era, high)**: with factory preloader intact, SP Flash + any ROM flashes via preloader mode **without auth** (§5.2). *"Before we go any further, know that there is no way for you to unbrick a phone that's already bricked and is running the MIUI preloader. (Visit a Service Center in such a case)"* — from 2020, when BROM flashing required a **Mi Authorized Account** (service-center-only, server-side SLA/DAA). Megathread explicitly warns against paid online "unbrick services" (*"highly overpriced… could result in you getting scammed, or have your data stolen"*), and asks anyone with an authorized account to help the community.
2. **Exploit regime (2021+, mtkclient/bypass_utility — pmOS wiki path, high)**: BROM is reachable on key-press (no test point), SLA/DAA are bypassed locally by payload (§2), so a full hard-brick is recoverable at home: exploit → SP Flash 5.2208 (or mtkclient itself) → write known-good `preloader/lk/lk2/boot/...` from backup or ROM → reboot. Megathread's equivalent SP Flash-only recipe for the bricked-with-logo case: load Android 9 firmware, **uncheck preloader, lk and lk2**, connect, Download.
3. **Bootloop (soft-brick)**: reflash **vbmeta** (`pmbootstrap flasher flash_vbmeta`, wiki; `mtk da vbmeta 3`, mtkclient) + kernel/boot; dm-verity yellow-state on A11 recovers with a power-key press (mtkclient README-USAGE).
4. **Brick prevention (historical)**: leaked factory firmware *"had a lot of security checks disabled, and compiled in engineering mode"* (discovered by @Xakep1993); megathread's CFW-era prevention was to run factory preloader/LK, *"does not work with the MIUI 11 Android 10 China build"* (verified-direct, historical).

---

## 7. Hardware revisions

- **begonia (global) vs begoniain (India)**: only difference is **NFC hardware absent on begoniain** (*"it's not as if it's disabled, the hardware is just not present"*, megathread, verified-direct, high). All custom software/TWRP is unified across both.
- **Region SKUs** via `fastboot getvar product`: begonia (CN/Global), begonia_ru, _id, _in, _eea (XDA t/3993359, snippet, medium).
- **Storage/RAM variants** (4/6/8 GB RAM; 64/128/256 GB UFS 2.1): no source documents differing partition layouts; the only GPT dump available is a 64 GB Samsung unit (wiki). **No PCB revisions / hw-rev variants documented anywhere accessible** (unknown).
- China-variant users reported TWRP backup-encryption failures on Chinese ROM (XDA posts #5/#6, 2019) — ROM-side, not hardware revision.

## 8. Limitations

- **Live XDA inaccessibility**: xdaforums.com blocked for our tools (bunny.net challenge; per context pack, tested 3×). All XDA evidence here came from the two Wayback snapshots (unlock guide 2023-03-16, megathread 2026-04-15) or search snippets; TWRP thread bodies (t/3972573, t/4002397, t/4242717) were **not** read in full — version/author details beyond titles and the Telegram 3.5.1_10 (2021-03-18) row are **pending human-browser check**.
- **web.archive.org is inconsistently reachable from this environment** (web_extract refused the wayback URL as "private/internal network"; curl succeeded). Depth of Wayback coverage of XDA thread pages beyond OP is unverified.
- **Test-point documentation**: only video/photo-grade hits (YouTube shorts); no authoritative written test-point map found → **unknown**.
- **UART**: no begonia-specific UART pinout source found → **unknown** (only SoC-level BROM UART base 0x11002000 from mtkclient config).
- **LK verified-partition list**: pmOS wiki itself marks it TODO — unknown.
- **PR #98 comment thread** (post-2023 developments in XiaoMiToolV2) not enumerated; only the PR body verified.
- Fastboot-ROM mirrors (xmfirmwareupdater/xiaomirom/mifirm) are third-party re-hosts; no bigota URL was verified byte-for-byte. Do not flash unverified images (research-only).
- 4PDA threads' unbrick pages were not re-mined for this dimension beyond the context pack (page 1 + last page caches on disk contain no test-point/UART specifics I could locate via search of the cached files).
