# 21 — NoMount, OverlayFS and systemless modification backends (English digest)

**[English directory](../index.md) · [Полный оригинал на русском](../../ru/kernels/21-NOMOUNT-MOUNT-BACKENDS-RU.md)**

> **DIGEST ONLY, NOT A COMPLETE TRANSLATION.** Source: [Russian technical report](../../ru/kernels/21-NOMOUNT-MOUNT-BACKENDS-RU.md), Git Blob 9da4ba4a9861959952f765c75417235328ca5c1d, observed 2026-11-21. All runtime behavior is upstream-reported; no test was carried out on the owner's Redmi Note 8 Pro.

## Three independent layers

1. **Root provider:** Magisk, KernelSU/KernelSU-Next, SukiSU Nova or APatch decides how superuser privileges are granted.
2. **Systemless mount/file-injection backend:** Magic Mount, OverlayFS, Mountify, NoMount or Hybrid Mount determines how module-supplied files appear in Android's directories.
3. **Kernel add-on:** SUSFS, NoMount's VFS engine or KernelPatch extensions modify kernel behavior. They are not interchangeable with the root manager.

NoMount is **not** a root manager. SUSFS is also **not** a root manager. Enabling NoMount does not itself grant root.

## How NoMount works

The primary repository is [maxsteeel/nomount](https://github.com/maxsteeel/nomount). It intercepts path resolution and directory enumeration inside the Virtual File System. In place of a conventional bind or overlay mount, it redirects file operations to replacement content in memory and can synthesize directory entries, whiteouts and opaque directories. Per-UID rules can control which processes see which virtual files.

The [Nova-Kernels MT6785 source](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785) includes NoMount as a Git submodule. Its KSU variant has CONFIG_NOMOUNT=y along with KernelSU-Next and SUSFS. The project is on **Linux 4.14.356**, not an upstream 4.19 or GKI kernel.

**Legacy compatibility:** for Linux 4.14/4.19, upstream instructs developers to integrate NoMount into kernel sources or build an exact compatible LKM. Precompiled generic GKI modules (typically Linux 5.10+) are not drop-in replacements.

The latest release observed in the original audit was [NoMount v2.3.1, 2026-11-19](https://github.com/maxsteeel/nomount/releases/tag/v2.3.1) with driver protocol v23. The author's performance claims do not constitute begonia benchmark results.

## Comparison

| Backend | Main strength | Limitations |
|---|---|---|
| Magic Mount / bind mounts | Familiar kernel semantics, broad existing module ecosystem | Observable mount entries and mounting overhead |
| OverlayFS | Standard Linux layering with lower/upper/work directories | Requires filesystem/xattr, suitable CONFIG_OVERLAY_FS and compatible SELinux/mount setup |
| [Mountify](https://github.com/backslashxx/mountify) | Combines module overlays, tmpfs and ext4-sparse modes | Still real mounts, explicit CONFIG_OVERLAY_FS and other kernel prerequisites |
| [NoMount](https://github.com/maxsteeel/nomount) | File redirection without traditional mounts; selective UID view | Deep VFS hook complexity and potential kernel panics, legacy integration effort |
| [Hybrid Mount](https://github.com/Hybrid-Mount/meta-hybrid_mount) | Per-module or per-path choice of Overlay/Magic/VFS | More configuration, VFS provider/ABI requirements and conflict potential |
| [SUSFS](https://gitlab.com/simonpunk/susfs4ksu) | Adds visibility/mount-metadata controls to compatible kernel root stacks | Not a replacement for root or every file-injection backend |

**NoMount/SUSFS do not guarantee root invisibility**, passing Play Integrity or support in banking/payment applications. File-system traces are only one set of observable signals, and vendor/AVB/hardware-attestation signals are separate.

## Recommendations for this hardware project

For Android kernel experiments, maintain a reproducible **Non-KSU control build**, compare KSU in isolation, then add SUSFS or NoMount one at a time. Record exact submodule and kernel SHAs, boot logs, performance and systemless module behavior. For Ubuntu Touch and postmarketOS, Android root/NoMount is not a requirement for the Linux port; upstreamable kernel drivers, DTS and stable hardware initialization are the real priority.

Read the [full Russian report](../../ru/kernels/21-NOMOUNT-MOUNT-BACKENDS-RU.md) for code-level details, the per-feature tests and risks. See [terminology](../../../i18n/TERMINOLOGY.md) for EN↔RU search aliases.
