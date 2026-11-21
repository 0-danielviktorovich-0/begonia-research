# 22 — Forward-port Linux 4.14→4.19→6.x using AI; payment integrity (English digest)

**[English directory](README.md) · [Полный оригинал на русском](../../22-KERNEL-FORWARD-PORT-AI-INTEGRITY-RU.md)**

> **DIGEST ONLY — not a complete translation.** Source [Russian report 22](../../22-KERNEL-FORWARD-PORT-AI-INTEGRITY-RU.md), Git Blob 5bb882d1a43d89799f2ba5a0d0b4f0c6ea63245c, observed and reconciled with the 2026-11-21 Telegram date correction. Kernel functionality on the owner's device has not been independently tested. For all evidence, limitations and examples read the full Russian original.

## What changed between kernel generations

The original Redmi Note 8 Pro uses Xiaomi/vendor Linux 4.14.x. Later custom 4.14 stable/backport releases do **not** become Linux 4.19 by changing their version number. A **forward-port** involves choosing a viable Linux 4.19 base for the SoC family and migrating board-specific DTS, panel/touch, clocks, regulators, battery/charging, USB, audio, Wi-Fi, vendor drivers, build config and Android vendor/ABI integration.

[LineageOS/android_kernel_xiaomi_mt6785](https://github.com/LineageOS/android_kernel_xiaomi_mt6785) and [xiaomi-mt6785-dev/android_kernel_xiaomi_mt6785](https://github.com/xiaomi-mt6785-dev/android_kernel_xiaomi_mt6785) both expose Linux **4.19.325**, but the directly checked board DTS and defconfig identify **rosemary**. That is not proof of a deployable begonia image. See [the developer's 4.19 announcement and source request](../../23-419-TELEGRAM-OUTREACH.md): the author reports a working begonia prototype and invites testers, but a reproducible patchset is still needed.

For **mainline-based** work, [Dinolek/mt6785-mainline](https://github.com/Dinolek/mt6785-mainline) and [kalpakprod/mt6785-linux](https://github.com/kalpakprod/mt6785-linux) carry modern Linux forks, not necessarily upstreamed MT6785 support in the Linux kernel. Upstream kernel-version numbers are insufficient without the actual SoC/board drivers.

## AI/reverse-engineering workflow

AI agents and tools such as Ghidra, Coccinelle, static analyzers and Reverse Engineer Anything can accelerate API migrations, device-tree comparisons, driver archaeology, compile error triage, symbol and HAL investigation, patch documentation, regression tests and log correlation.

They **cannot prove** electrical pinouts, power sequencing, modem security requirements, camera ISP calibration or sleep stability without hardware evidence. Every patch should have traceable source commit, compiled output, board revision, logs, hardware tests and rollback strategy.

## Experimental Wi-Fi result

The maintainer of [criollojoel10/begonia-pmos-tianma](https://github.com/criollojoel10/begonia-pmos-tianma) reports **working Wi-Fi on a physical begonia with Linux 6.16.4 on 2026-09-27**, using a ported MediaTek vendor wireless stack (wlan_gen4m and WMT). This is independent of whether native upstream mt76 SDIO support is fully integrated on this board; it is **an author-reported result**, not an independent reproduction.

## Root methods and payments

Google [Play Integrity verdicts](https://developer.android.com/google/play/integrity/verdicts) distinguish BASIC, DEVICE and STRONG signals. [Google Wallet Help](https://support.google.com/wallet/answer/12200245) warns that root, custom ROM and unlocked bootloader may prevent tap-to-pay. Magisk, KernelSU/KernelSU-Next, SukiSU, APatch, SUSFS and NoMount have different local modification footprints; **none guarantees passing device/hardware attestation or bank-specific checks**.

For payment reliability, stock certified firmware without root and with a correctly locked bootloader is generally safer than experimenting with kernel/root hooks. **Never relock a modified or cross-region ROM merely to satisfy a check**, due to bricking risk.

## Concrete project workstreams

1. **Ubuntu Touch / Halium 10:** reliable daily-driver path, fix audio, power and OTA.
2. **Android/Halium Linux 4.19:** first obtain the actual begonia forward-port sources, defconfig and logs; do not copy a rosemary boot image.
3. **postmarketOS Linux 6.x/7.x:** build on documented MT6785 DTS/driver work, validate wireless/charging/audio and upstream patches step by step.
4. Keep root and mount-bypass experiments as a **separate Android laboratory task**, not a requirement for mobile Linux.

The [full Russian report](../../22-KERNEL-FORWARD-PORT-AI-INTEGRITY-RU.md) includes detailed test requirements and the payment comparison table.
