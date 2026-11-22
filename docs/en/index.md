# Knowledge base — English topic directory

**[English](index.md) · [Русский](../ru/index.md)** · [Project README](../../README.md) · [Source index](research/master-topic-index.md)

This is the primary international entry point for the Redmi Note 8 Pro (begonia, MT6785) research database. Every report remains accessible even when a verified full translation has not yet been completed.

**Translation status:** original English reports are complete source documents; chapters 19–22 were originally authored in Russian. Their English pages are explicitly labelled as **full translation** or **English digest**. A digest is a searchable introduction, **not a substitute for the complete original**. The machine catalog at [i18n/catalog.json](../../i18n/catalog.json) records these distinctions.

## Firmware and Android

| ID | Subject | Source or English page |
|---|---|---|
| 00 | Project summary and high-confidence findings | [Executive summary](research/00-README.md) |
| 01 | Primary source register, provenance and freshness | [Sources](research/01-SOURCES.md) |
| 02 | Stock MIUI history, CFW/Non-CFW, GSI and custom ROM catalog | [Firmware history](android/02-FIRMWARE-HISTORY.md) |
| 10 | Curated 4PDA/XDA guide and forum-post index | [Guide index](android/10-GUIDE-INDEX.md) |
| 11 | Vendor blobs, firmware, kernel/device trees and build recipes | [Artifact provenance](kernels/11-BLOBS-FIRMWARE-SOURCES.md) |
| 19 | **CFW, Non-CFW, GSI and Android/Linux terminology** | **[Full English translation](android/19-rom-terminology.md)** · [Russian original](../ru/android/19-ROM-TERMS-GLOSSARY-RU.md) |

## Kernels, driver support and Linux distributions

| ID | Subject | Source or English page |
|---|---|---|
| 03 | MT6785 Linux 4.14 and 4.19, upstream and vendor branches | [Kernel history](kernels/03-KERNEL-HISTORY.md) |
| 04 | Panels, touch, Mali GPU, modem, Wi-Fi, cameras, sensors | [Hardware and driver inventory](kernels/04-HARDWARE-DRIVERS.md) |
| 05 | Ubuntu Touch 24.04 on Halium 10 and its known issues | [Ubuntu Touch](linux/05-UBUNTU-TOUCH.md) |
| 06 | Droidian and postmarketOS port comparison | [Linux ports](linux/06-DROIDIAN-POSTMARKETOS.md) |
| 08 | Prioritized engineering roadmap | [Development roadmap](linux/08-DEVELOPMENT-ROADMAP.md) |
| 14 | Mainline Linux 6.x/7.x approach, missing drivers and DT work | [Mainline upgrade path](kernels/14-MAINLINE-UPGRADE-PATH.md) |
| 20 | KSU/Non-KSU, Linux 4.19 upstreams and patch provenance | [English digest](kernels/20-kernel-root-ecosystem.md) · [Full Russian original](../ru/kernels/20-KERNEL-419-ROOT-ECOSYSTEM-RU.md) |
| 23 | **Linux 4.19 begonia developer announcement, contact and source-request draft** | [Developer outreach and evidence](research/23-419-TELEGRAM-OUTREACH.md) · [@Saikrishna1504](https://t.me/saikrishna1504) |
| 24 | **Saikrishna1504: begonia source-stack and 4.19 migration commits** | **[Full English audit](research/24-SAIKRISHNA1504-DEVICE-STACK-AUDIT.md)** · [21-repo CSV](../../data/matrices/saikrishna-source-inventory.csv) · [Russian digest](../ru/research/24-saikrishna-source-audit.md) |
| 22 | Kernel forward-port using AI/REA, payment integrity | [English digest](kernels/22-kernel-forward-port.md) · [Full Russian original](../ru/kernels/22-KERNEL-FORWARD-PORT-AI-INTEGRITY-RU.md) |

## Root, recovery, safety and reverse engineering

| ID | Subject | Source or English page |
|---|---|---|
| 07 | Bootloader, official recovery, BROM, backups and brick safety | [Recovery and safety](recovery/07-RECOVERY-SAFETY.md) |
| 26 | **Recovery project status, builds, sources, compatibility, Ubuntu Touch** | [Full audit](recovery/recovery-projects-begonia-2026.md) · [comparison CSV](../../data/matrices/recovery-matrix.csv) · [RU digest](../ru/recovery/recovery-projects-begonia-2026.md) |
| 09 | Open questions, contradictions and missing sources | [Open questions](research/09-OPEN-QUESTIONS.md) |
| 12 | Tool reuse, agent workflows and technical skills | [Tools and skills](tools/12-SKILLS-AND-REUSE.md) |
| 13 | NetHunter, Wi-Fi monitor mode and USB gadget support | [NetHunter extras](android/13-NETHUNTER-WIFI-EXTRAS.md) |
| 15 | Reverse-engineering priorities and subsystem investigation | [RE improvement plan](linux/15-RE-IMPROVEMENT-PLAN.md) |
| 16 | Magisk, KernelSU, APatch and root workflows | [Root methods](android/16-ROOT-METHODS.md) |
| 17 | Independent audit of claims, freshness and recovery risk | [Audit](research/17-INDEPENDENT-AUDIT.md) |
| 18 | Read-only phone inventory, prerequisites before flashing | [Device preflight](recovery/18-DEVICE-PREFLIGHT-READONLY.md) |
| 21 | NoMount, SUSFS, OverlayFS, Mountify, Hybrid Mount | [English digest](kernels/21-nomount-and-mount-backends.md) · [Full Russian original](../ru/kernels/21-NOMOUNT-MOUNT-BACKENDS-RU.md) |

## Autonomous kernel development lab (research proposal)

| Topic | Source / status |
|---|---|
| Kernel Lab: panic-proof crash archiving, recovery, MTK AEE, UART and agent-supervised test architecture | [Canonical English design](tools/kernel-lab-autonomous-debugging.md) · [Russian digest](../ru/tools/kernel-lab-autonomous-debugging.md) — **proposed, not device-tested** |
| macOS: ADB, fastboot, USB re-enumeration and uhubctl | [Read-only Mac runbook](tools/kernel-lab-macos-inventory.md) |
| AI agent onboarding and evidence-first tasks | [Bounded mission](tools/kernel-lab-agent-mission.md) · [AGENTS.md](../../AGENTS.md) |

## Find information without knowing its original language

Search by *concept* (e.g. bootloader, загрузчик, preloader), by *component* (e.g. MT6359, NT36672A, wlan_gen4m), or by *stable topic ID* in the bilingual [topic index](../../i18n/topics.json). The canonical technical identifiers and evidence links are not translated. Machine-readable source data: [sources.json](../../data/catalog/sources.json), [index.json](../../data/catalog/index.json), [firmware-matrix.csv](../../data/matrices/firmware-matrix.csv), [kernel-matrix.csv](../../data/matrices/kernel-matrix.csv).

For contributions and translation review follow the [localization rules](../../i18n/README.md), [controlled terminology](../../i18n/TERMINOLOGY.md) and [translation status catalog](../../i18n/catalog.json). Every translation must state its original source revision, review state and limitations.

## Upstream kernel verification (2026)

[Git-SHA-pinned begonia ROM and kernel source audit](research/begonia-kernel-and-rom-evidence-2026-11.md) — directly compares WuXing90, Saikrishna1504 and AxionAOSP. 
