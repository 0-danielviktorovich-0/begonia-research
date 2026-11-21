# 20 — MT6785 kernel provenance and root frameworks (English digest)

**[English directory](../index.md) · [Полный оригинал на русском](../../ru/kernels/20-KERNEL-419-ROOT-ECOSYSTEM-RU.md) · [Русский каталог](../../ru/index.md)**

> **DIGEST ONLY — not a complete translation.** For full source-by-source evidence, forks, exact build settings, citations and limitations, consult the [authoritative Russian report](../../ru/kernels/20-KERNEL-419-ROOT-ECOSYSTEM-RU.md). Based on source Git Blob e21b0654cb71a9d69ac04bfc820f23a9c6e9033c observed 2026-11-21. Not tested on a physical begonia.

## Main distinctions

KSU and Non-KSU are **kernel build variants**, not Android ROM formats. A Non-KSU build does not provide KernelSU automatically, but might be rooted separately with Magisk or APatch. KSU variants integrate an eligible KernelSU-family implementation and require matching manager, hooks, kernel ABI and modules. SUSFS is an optional kernel filesystem extension; it is **not a root method by itself**.

In [Nova-Kernels/kernel_xiaomi_mt6785](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785), the two defconfigs and nova-build.sh distinguish ordinary and KernelSU builds. The KSU config includes CONFIG_KSU=y, CONFIG_KSU_MANUAL_HOOK=y, CONFIG_KSU_SUSFS=y and CONFIG_NOMOUNT=y. KernelSU-Next is sourced as a legacy Git submodule. The checked kernel Makefile reports **Linux 4.14.356**, not 4.19.

## Identifying the actual Linux 4.19 source

| Tree and branch | Checked version | What remains to prove |
|---|---|---|
| [LineageOS MT6785 lineage-24.0](https://github.com/LineageOS/android_kernel_xiaomi_mt6785) | Linux 4.19.325 | The identified DTS/defconfig concern **rosemary**; not a verified begonia flash |
| [xiaomi-mt6785-dev lineage-24.0](https://github.com/xiaomi-mt6785-dev/android_kernel_xiaomi_mt6785) | Linux 4.19.325 | Same observed HEAD as LineageOS (30485853fa89); not independent evidence of begonia functionality |
| [Saikrishna1504 main](https://github.com/Saikrishna1504/kernel_xiaomi_mt6785) | Linux 4.14.357-openela | An active Power-kernel source, **not** a checked 4.19 tree |
| [Nova-Kernels main](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785) | Linux 4.14.356 | Separate KSU and Non-KSU build pipeline |

A developer's later public Telegram message about a working begonia 4.19 port is recorded in the [dedicated outreach and evidence note](../research/23-419-TELEGRAM-OUTREACH.md). That claim requires a reproducible kernel revision, device tree, exact vendor base, boot logs and real hardware tests. **Do not substitute rosemary boot images on begonia.**

## Root projects and roles

| Project | Layer | Primary benefit | Main limitation |
|---|---|---|---|
| [Magisk](https://github.com/topjohnwu/Magisk) | Android boot/init | Widely used without rebuilding a kernel tree | Exact boot-image and OTA compatibility |
| [KernelSU-Next](https://github.com/KernelSU-Next/KernelSU-Next) | Kernel root | Legacy/non-GKI integration and app policy | Matching hooks, manager and kernel build |
| [SukiSU Nova](https://github.com/SukiSU-Nova/SukiSU-Nova) | Fork of KernelSU family | Alternative features and patch ecosystem | Fork-specific compatibility |
| [APatch](https://github.com/bmax121/APatch) | Patching boot kernel image | Sometimes usable without rebuilding the tree | Kernel symbols/ABI/boot image matching |
| [SUSFS](https://gitlab.com/simonpunk/susfs4ksu) | Kernel filesystem extension | Selective filesystem/mount visibility features | Requires matching patches; not independent root |
| [NoMount](https://github.com/maxsteeel/nomount) | VFS file-injection backend | File replacement without traditional mounts | Legacy kernels need integrated hooks or custom LKM |

For the complete source and reproducibility checklist (Makefile versions, branch names, SHAs, defconfigs and module upstreams), read the [Russian original](../../ru/kernels/20-KERNEL-419-ROOT-ECOSYSTEM-RU.md) and the structured [provenance CSV](../../../data/matrices/kernel-root-provenance.csv). For mount-provider trade-offs use [21 — English digest](21-nomount-and-mount-backends.md).

**Scope:** no binaries tested or flashed, no claim of guaranteed successful root or banking app compatibility.
