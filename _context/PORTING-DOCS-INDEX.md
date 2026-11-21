# PORTING-DOCS-INDEX — official porting & kernel-development documentation (W16, 2026-11-21)

Scope: the OFFICIAL development/porting documentation one must read — and usually ACTIVATE (defconfigs,
DTB wiring, package formats, boot-image formats) — when porting a device (begonia = Redmi Note 8 Pro,
MT6785/Helio G90T). Companion to `10-GUIDE-INDEX.md`, which covers FORUM guides only.

Method: research-only session, 2026-11-21 (JST). Every URL below was fetched this session unless its
access field says otherwise. Citation style: URL + what it covers + why it matters for begonia/MT6785 +
access status + confidence (high/medium/low). Consulted sources appended to
`AI-OS/.hermes/cache/scratch/begonia-recon/sources.jsonl` (lines 192–216).

Access legend: **verified-direct** = page fetched and read this session · **linked-verified** = URL
confirmed by navigation from a fetched page, page body not read · **404** = fetched, dead · **blocked** =
fetch refused by the tool's network filter · **not verified** = existence not checked this session.

---

## 1. Kali NetHunter official (kali.org/docs/nethunter, gitlab.com/kalilinux/nethunter)

**1.1 [Kali NetHunter — documentation hub](https://www.kali.org/docs/nethunter/)** — covers: the three
editions (Rootless / Lite / full NetHunter) and what each requires; "a custom kernel can extend that
functionality by adding additional network and USB gadget drivers as well as Wi-Fi injection support for
selected Wi-Fi chips"; install flow (unlock → stock AOSP or LineageOS → Magisk → flash zip); §8
"Porting NetHunter to New Devices"; CI-generated kernel/device lists at nethunter.kali.org
(`kernels.html`, `device-kernels.html`, `images.html`). | why: defines exactly what a begonia kernel must
gain for full NetHunter (USB-gadget + Wi-Fi-injection pieces); begonia is not among the ~110 published
devices, so a port starts from the porting chapters below. | access: verified-direct. | confidence: high.

**1.2 [Porting NetHunter to New Devices with kernel builder](https://www.kali.org/docs/nethunter/porting-nethunter-kernel-builder/)** —
covers: the official porting loop — kernel builder (`kali-nethunter-kernel-builder`), `local.config`,
"Configure & compile kernel from scratch", NetHunter patches, AnyKernel zip, "Edit Anykernel config";
hard prerequisites "device with an unlocked bootloader … must be able to get root"; "it's all about the
kernel". Notably its "Finding Kernel Sources" list (Google/LG/Samsung/HTC/OnePlus/Motorola/Sony) **omits
MediaTek entirely** — relevant to §6. | why: this is the procedure a begonia NetHunter kernel port would
follow; kernel source for begonia comes from the Xiaomi drop / community forks, not an MTK portal. |
access: verified-direct. | confidence: high.

**1.3 [Porting NetHunter to New Devices (manual)](https://www.kali.org/docs/nethunter/porting-nethunter/)** —
covers: the non-builder, step-by-step kernel porting path (referenced from hub §8 and from 1.2 as the
fallback when builds fail). | why: the manual route is the one you'd hit on an MTK 4.14 tree where the
builder's example configs don't match. | access: linked-verified. | confidence: high (existence).

**1.4 [Configuring the Kernel — General](https://www.kali.org/docs/nethunter/nethunter-kernel-2-config-1/)** —
covers: the first official config pass: clear local version, hostname "kali", `CONFIG_SYSVIPC=y`,
`CONFIG_MODULES=y`, `CONFIG_MODULE_UNLOAD=y`, `CONFIG_MODULE_FORCE_UNLOAD=y`, `CONFIG_MODVERSIONS=y`,
and `CONFIG_BUILD_ARM64_APPENDED_DTB_IMAGE=y` + `IMG_GZ_DTB=y` (appended `Image.gz-dtb`). Part of a
series: [Patching a Kernel](https://www.kali.org/docs/nethunter/nethunter-kernel-1-patching/) → this page
→ [Configuring the Kernel — Network](https://www.kali.org/docs/nethunter/nethunter-kernel-3-config-2/)
(series existence linked-verified from the fetched page). | why: the appended-DTB packaging is the
classic MTK/Android-4.x convention; begonia instead passes `mediatek/mt6785.dtb` via mkbootimg `dtb`
(AOSP header-v2 style, repo-verified) — a real packaging decision to make. | access: verified-direct. |
confidence: high.

**1.5 [Building NetHunter](https://www.kali.org/docs/nethunter/building-nethunter/)** — covers: building
NetHunter images from the GitLab repo with the Python build scripts; installer-builder and
add-your-own-device instructions live in the
[nethunter-installer README](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-installer/-/blob/main/README.md).
| why: after the kernel builds, an AnyKernel/installer zip is how it reaches begonia. | access:
linked-verified. | confidence: high (existence).

**1.6 [Installing NetHunter on top of Android](https://www.kali.org/docs/nethunter/installing-nethunter/)** —
covers: device prep (unlock, stock AOSP or LineageOS, Magisk root) then flash the NetHunter zip in
Magisk; SHA256 verification of the zip first. | why: begonia end-state (unlocked + Magisk) that the
kernel port must land into. | access: linked-verified. | confidence: high (existence).

**1.7 [NetHunter GitLab group](https://gitlab.com/kalilinux/nethunter)** — covers: the official repos —
subgroups `build-scripts` (11 projects, incl. [kali-nethunter-kernels](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-kernels),
the official "Adding Your Device" repo linked from hub §8, and the kernel builder), `apps`, `store`,
`nh-resources`, `nh-scripts`. The hub states 250+ kernels for 110+ devices are maintained here. | why:
this is where a working begonia kernel + device entry would be submitted for official releases. |
access: verified-direct (group page; subgroup pages via navigation). | confidence: high.

**1.8 [Wireless Cards (Known Working Hardware)](https://www.kali.org/docs/nethunter/wireless-cards/)** —
covers: officially verified injection-capable wireless hardware (mostly external USB adapters); in-kernel
injection remains chip-dependent per the hub. | why: begonia's built-in Wi-Fi (MT7663 family suspected,
per repo 04/13) is not on any official NetHunter injection list — monitor-mode status for it is tracked
in repo `13-NETHUNTER-WIFI-EXTRAS.md`. | access: linked-verified. | confidence: high (existence).

## 2. LineageOS official (wiki.lineageos.org, github.com/LineageOS)

**2.1 [Devices — LineageOS Wiki catalog](https://wiki.lineageos.org/devices/)** — covers: the complete
official device catalog (644 devices shown) with per-device build guides (`/devices/<codename>/build`),
plus the warning "Devices not listed are **not supported**" and the vendor/SoC filters (MediaTek is a
listed SoC-vendor filter). | why: **begonia is absent from the catalog** (case-insensitive grep of the
fetched page: no "begonia", no "mt6785"/"g90t") — so no official "Build for begonia" page exists, and an
official LineageOS port would mean adding device tree + kernel repos under the LineageOS org's rules.
Community LOS trees exist (e.g. AgentFabulous/begonia, repo 02/03) but are unofficial. | access:
verified-direct. | confidence: high.

**2.2 [LineageOS Wiki device page for begonia](https://wiki.lineageos.org/devices/begonia/)** — covers:
nothing — **HTTP 404**. | why: confirms 2.1; the mission's conditional "if the device page exists"
resolves to: it does not. | access: 404 (dead link). | confidence: high.

**2.3 [LineageOS repo manifest (android)](https://github.com/LineageOS/android)** — covers: the official
`repo` manifest that per-device build guides clone; per-device manifests/branches select LOS version and
kernel. | why: an unofficial begonia LOS port would be expressed as a manifest + device/kernel repos
against this. | access: **not verified** this session — raw `README.md` returned 404 on `HEAD` and
`lineage-22.2`, and `github.com` is blocked to the fetcher; the repo's existence is nonetheless
referenced from NetHunter's kernel-builder page ([org repo list](https://github.com/orgs/LineageOS/repositories)).
| confidence: low-medium.

## 3. AOSP official (source.android.com, android.googlesource.com)

**3.1 [Kernel overview](https://source.android.com/docs/core/architecture/kernel)** — covers: official
kernel taxonomy — LTS → Android Common Kernels (ACK, from
[kernel/common](https://android.googlesource.com/kernel/common)), GKI/KMI from 5.10, branch types,
certified boot image, DLKM/vendor modules; "What's next" routing to ACK pages and GKI development. |
why: begonia's 4.14 kernel is a pre-GKI ACK-lineage vendor tree (repo 03) — everything below the GKI
boundary (config, DTB, headers) is the porter's responsibility. | access: verified-direct. |
confidence: high.

**3.2 [Device tree overlays (DTB/DTBO)](https://source.android.com/docs/core/architecture/dto)** — covers:
the official DTB/DTBO contract — compile DTS→DTB with `dtc`, flash locations (appended to boot.img vs
dedicated dtb/dtbo partitions), Android 9 rule that the bootloader must not modify DTO properties, and
the subpages [implement](https://source.android.com/docs/core/architecture/dto/implement),
[compile](https://source.android.com/docs/core/architecture/dto/compile),
[multiple](https://source.android.com/docs/core/architecture/dto/multiple),
[syntax](https://source.android.com/docs/core/architecture/dto/syntax),
[partitions](https://source.android.com/docs/core/architecture/dto/partitions). | why: begonia/MT6785
DTB wiring (`mediatek/mt6785.dtb`) must slot into one of these official patterns; pmOS/Halium/NetHunter
each choose differently. | access: verified-direct. | confidence: high.

**3.3 [Android Verified Boot (AVB)](https://source.android.com/docs/security/features/verifiedboot/avb)** —
covers: Verified Boot 2.0 reference implementation — dm-verity metadata generation, libavb in the
bootloader, common footer format, rollback protection; build-system integration in
`platform/external/avb/README.md`. | why: begonia runs unlocked (orange state), but any custom boot
chain must still satisfy/circumvent AVB consistently with vbmeta handling — the official reference for
what is being signed and verified. | access: verified-direct. | confidence: high.

**3.4 [Boot image header](https://source.android.com/docs/core/architecture/bootloader/boot-image-header)** —
covers: header versioning per Android release ("Android 10 must use boot header version 2"; v3/v4 for
11+; legacy v0), `mkbootimg` arguments `header_version`, `dtb`, `dtb_offset`, `recovery_dtbo`, and
`BOARD_MKBOOTIMG_ARGS` wiring; canonical struct in
[mkbootimg/bootimg.h](https://android.googlesource.com/platform/system/tools/mkbootimg/+/refs/heads/android17-release/include/bootimg/bootimg.h).
| why: begonia builds use **header v2** (repo 05 deviceinfo) — this page is the normative format
reference behind that choice, and the reason v3's removed fields (second stage, recovery DTBO) matter if
headers are bumped. | access: verified-direct. | confidence: high.

**3.5 [Android Common Kernel repo (kernel/common)](https://android.googlesource.com/kernel/common)** —
covers: the official ACK source the docs above describe; per-version `android-4.14`-era branches hold
the `android-base`/`android-recommended` config fragments (sibling repo `kernel/configs`). | why: the
upstream baseline begonia's 4.14 vendor tree diverges from; the config fragments are the official
"minimum config for Android" reference when pruning `begonia_user_defconfig`. | access: linked-verified
(linked from 3.1); `kernel/configs` fragment location: not verified this session. | confidence:
high (link) / medium (configs detail).

## 4. postmarketOS official (wiki.postmarketos.org → wiki.nura.eco, docs.postmarketos.org → docs.nura.eco)

**4.1 [Porting to a new device](https://wiki.postmarketos.org/wiki/Porting_to_a_new_device)** — covers:
the complete official porting guide — the package triad `device-vendor-codename` (with `deviceinfo` and
feature configs: udev rules, ALSA UCM), `linux-vendor-codename` (kernel package + patches; shared
`linux-postmarketos-*` packages for close-to-mainline), `firmware-vendor-codename` ("often needed to get
e.g. WiFi and Bluetooth working"); pmbootstrap chroot workflow; pmaports `device/{main,community,testing,downstream}`
categories; the downstream-vs-(close-to)-mainline decision and the
[Mainlining#Supported SoCs](https://wiki.nura.eco/wiki/Mainlining) check; ends in "Submit the
device-specific packages to pmaports". | why: begonia's actual pmOS port follows this template exactly —
`device/testing/` device package + `linux-postmarketos-mediatek-mt6785` (mainline 6.16.4, repo 06).
Note: wiki.postmarketos.org now redirects to the rebranded **Nura** wiki (fetched as
[wiki.nura.eco, oldid=109210](https://wiki.nura.eco/wiki/Porting_to_a_new_device)); repo 06 already
recorded this redirect. | access: verified-direct (via redirect). | confidence: high.

**4.2 [(Close to) Mainline](https://wiki.nura.eco/wiki/(Close_to)_Mainline)** — covers: official
terminology — "close to mainline" = kernel.org tree + "a few patches" that are feasible to upstream, vs
downstream/vendor kernels (ACK forks with MTK drivers that assume Android HALs). | why: the mt6785
mainline fork is precisely a close-to-mainline kernel; the page defines the upgrade path in repo
`14-MAINLINE-UPGRADE-PATH.md`. | access: verified-direct. | confidence: high.

**4.3 [Documentation index (docs.postmarketos.org)](https://docs.postmarketos.org/)** — covers: the
official docs portal (redirects to docs.nura.eco) — [pmbootstrap manual](https://docs.nura.eco/pmbootstrap/main/index.html)
(building images, installing, package building), [pmaports docs](https://docs.nura.eco/pmaports/main/index.html),
plus hardware-ci and BPO build-queue docs. | why: pmbootstrap is the tool that ACTIVATES a port locally
(`pmbootstrap init` → device list comes from the device package). | access: verified-direct. |
confidence: high.

**4.4 [pmaports repository](https://gitlab.postmarketos.org/postmarketOS/pmaports)** — covers: the
official package repo where device/kernel/firmware packages live and where a port is upstreamed
(APKBUILD format; category rules per 4.1). | why: begonia packages already live here under
`device/testing/` (repo 06) — the contribution target for any new MTK6785 package work. | access:
linked-verified (linked from 4.1); CONTRIBUTING.md not opened. | confidence: high (existence).

## 5. Halium official (docs.halium.org, halium.org)

**5.1 [Halium porting guide](https://docs.halium.org/en/latest/)** — covers: the official Halium porting
manual — [First steps](https://docs.halium.org/en/latest/porting/first-steps.html), Get Halium source,
[Build Halium](https://docs.halium.org/en/latest/porting/build-sources.html),
[Install Halium](https://docs.halium.org/en/latest/porting/install-build/index.html),
[Debug Halium](https://docs.halium.org/en/latest/porting/debug-build/index.html), plus supplementary
[Device Overview](https://docs.halium.org/en/latest/supplementary/devices/index.html) and
[Hardware and kernel enablement](https://docs.halium.org/en/latest/supplementary/hardware-enablement.html)
(linked-verified). | why: begonia's Ubuntu Touch and Droidian ports are Halium-10 adaptations
(kernel-xiaomi-mt6785 `halium-10.0`, repo 05/06) — this is the spec those kernel patches implement
(binder, defconfig enablement, halium-boot initramfs). | access: verified-direct. | confidence: high.

**5.2 [halium.org/build/portal](https://halium.org/build/portal)** — covers: nothing — **GitHub Pages
404** ("The site configured at this address does not contain the requested file"). | why: the mission
asked to flag this; the live documentation is at docs.halium.org (5.1), not on halium.org. | access: 404
(dead link). | confidence: high.

**5.3 [Halium hardware and kernel enablement](https://docs.halium.org/en/latest/supplementary/hardware-enablement.html)** —
covers: the official checklist of kernel-side work for GNU/Linux userspace on an Android kernel. | why:
the general reference behind the begonia-specific enablement commits already catalogued in repo 05
(AppArmor, SquashFS, binder, RFKill, cgroups). | access: linked-verified. | confidence: high (existence).

## 6. MediaTek-specific official sources

**6.1 [developer.mediatek.com](https://developer.mediatek.com/)** — MediaTek's developer portal. |
access: **blocked** — the fetcher refused the URL ("private or internal network address"); status not
verified this session. | confidence: low (existence well-known, contents unchecked).

**6.2 [opensource.mediatek.com](https://opensource.mediatek.com/)** — MediaTek's open-source portal. |
access: **blocked** (same filter). | confidence: low.

**6.3 Official public MT6785 phone kernel sources / docs** — **none found on official channels this
session.** Verified-direct evidence: Kali's official "Finding Kernel Sources" list (1.2) names no
MediaTek portal at all. The de-facto official channel for begonia kernel source is Xiaomi's GPL drop
(MiCode/opensourcing via Xiaomi), and the working trees in this repo (UBports-hosted
`kernel-xiaomi-mt6785`, AgentFabulous/begonia, Dinolek `mt6785-mainline`) are community-maintained
derivatives. | confidence: medium-high (inference from verified absence + repo 03/05/06).

**6.4 gen4m / MTK WLAN build documentation** — no official public gen4m (MTK Android kernel branch
naming) or MTK WLAN driver build docs were located this session; nothing to link. | confidence: low
(absence claim, not proof of nonexistence).

**6.5 [Linux and the Devicetree (kernel.org)](https://docs.kernel.org/devicetree/usage-model.html)** —
covers: the SoC-agnostic official kernel documentation baseline — DT as platform identification /
runtime config / device population, `compatible` conventions, bindings, overlays; sibling docs under
[devicetree index](https://docs.kernel.org/devicetree/index.html). | why: for close-to-mainline MT6785
work (new DTS/bindings in the 6.16 fork) this is the official rulebook MTK bindings must follow. |
access: verified-direct. | confidence: high.

## 7. "What is usually activated when porting" — checklist distilled from the above

Each item linked to the official document that mandates or defines it:

1. **Bootloader unlock + root as prerequisite** — [NetHunter kernel-builder porting page](https://www.kali.org/docs/nethunter/porting-nethunter-kernel-builder/)
   ("device must be unlockable/rootable"); [pmOS porting guide](https://wiki.nura.eco/wiki/Porting_to_a_new_device)
   step 1 ([Unlocking Bootloaders](https://wiki.nura.eco/wiki/Unlocking_Bootloaders)); [NetHunter install](https://www.kali.org/docs/nethunter/installing-nethunter/)
   (unlock → Magisk). begonia: Xiaomi unlock (repo 05/07).
2. **Boot image header version** — [AOSP boot image header](https://source.android.com/docs/core/architecture/bootloader/boot-image-header):
   Android 10 ⇒ header v2 (begonia's case, repo 05); mkbootimg `header_version`/`dtb`/`dtb_offset` args.
3. **DTB/DTBO packaging decision** — three official modes: appended `Image.gz-dtb`
   ([NetHunter config page](https://www.kali.org/docs/nethunter/nethunter-kernel-2-config-1/),
   `CONFIG_BUILD_ARM64_APPENDED_DTB_IMAGE`), `dtb`+`dtb_offset` in boot.img ([AOSP boot image header](https://source.android.com/docs/core/architecture/bootloader/boot-image-header)),
   or dedicated dtb/dtbo partitions ([AOSP DTB/DTBO page](https://source.android.com/docs/core/architecture/dto)).
   begonia: `mediatek/mt6785.dtb` via deviceinfo/mkbootimg.
4. **Kernel config baseline** — [NetHunter Configuring the Kernel](https://www.kali.org/docs/nethunter/nethunter-kernel-2-config-1/):
   `CONFIG_SYSVIPC`, `CONFIG_MODULES`, `MODULE_UNLOAD`, `FORCE_UNLOAD`, `MODVERSIONS`; AOSP-side minimums
   via the ACK config fragments ([kernel/common](https://android.googlesource.com/kernel/common), 3.5).
5. **USB gadget/configfs + HID (NetHunter functionality)** — [NetHunter hub](https://www.kali.org/docs/nethunter/)
   (custom kernel adds "USB gadget drivers"; HID/BadUSB attacks are full-edition features);
   [USB Arsenal](https://www.kali.org/docs/nethunter/nethunter-usbarsenal/) and
   [HID attacks](https://www.kali.org/docs/nethunter/nethunter-hid-attacks/) app pages (linked-verified).
   begonia: W13-ADDENDUM-USB-HID context in `_context/`.
6. **Wi-Fi injection / monitor mode** — [NetHunter hub](https://www.kali.org/docs/nethunter/)
   (injection "for selected Wi-Fi chips") + [wireless cards list](https://www.kali.org/docs/nethunter/wireless-cards/).
   begonia: MT7663 not on any official list — tracked in repo 13.
7. **Firmware packages** — [pmOS porting guide](https://wiki.nura.eco/wiki/Porting_to_a_new_device):
   `firmware-vendor-codename` "often needed to get e.g. WiFi and Bluetooth working". begonia analog:
   `firmware-xiaomi-begonia-*` packages (repo 06).
8. **Kernel enablement for Linux userspace** — [Halium hardware/kernel enablement](https://docs.halium.org/en/latest/supplementary/hardware-enablement.html)
   (binder, security modules, cgroups) + [pmOS (Close to) Mainline](https://wiki.nura.eco/wiki/(Close_to)_Mainline)
   for the mainline-kernel track. begonia: halium-10.0 patch set (repo 05) and mt6785-mainline (repo 06/14).
9. **sepolicy / vendor overlay + system pairing** — [Halium Build/Install chapters](https://docs.halium.org/en/latest/porting/build-sources.html)
   (halium-boot + GSI pairing; begonia overlay specifics already in repo 05).
10. **Verified boot state / AVB** — [AOSP AVB](https://source.android.com/docs/security/features/verifiedboot/avb):
    what the unlocked boot chain skips and what must still be consistent (vbmeta, dm-verity).
11. **Upstreaming the result** — [pmOS porting guide](https://wiki.nura.eco/wiki/Porting_to_a_new_device)
    final step → [pmaports](https://gitlab.postmarketos.org/postmarketOS/pmaports); NetHunter →
    [kali-nethunter-kernels](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-kernels)
    ("Adding Your Device") / [kernel-builder](https://www.kali.org/docs/nethunter/porting-nethunter-kernel-builder/)
    workflow.

## Gap vs this repo

Citation census (regex count over root-level `00-*.md`…`14-*.md`, `*.csv`, `sources.json`, 2026-11-21):

- **Already cited in the repo's research files:** `kali.org` (01-SOURCES ×4, 13-NETHUNTER-WIFI-EXTRAS ×13),
  `wiki.lineageos.org` (02 ×2, firmware-matrix.csv ×2), `wiki.postmarketos.org` (06) / `wiki.nura.eco`
  (00, 02, 04, 07, 10, 13, hardware csv) / `docs.postmarketos.org|docs.nura.eco` (01, 07) /
  `gitlab.postmarketos.org` (03, 04, 06, 14, kernel csv), `halium.org|docs.halium.org` (01, 14),
  `docs.kernel.org|kernel.org` (00, 03, 08, 09, 13, 14), `developer.android.com` (10-GUIDE-INDEX),
  MediaTek mentions (everywhere, but as vendor names — no official MTK portal URL cited anywhere).
- **New this session (domains never cited in 00-15):** `source.android.com` — 4 entries (3.1–3.4,
  kernel/DTO/AVB/boot-header); `gitlab.com/kalilinux` — 2 entries (1.7 + build-scripts repos). → **6 of
  28 entries sit on previously-uncited domains; 22 of 28 extend domains already cited** (but several are
  first-time *pages*: pmOS porting-guide main page, LineageOS devices catalog, kernel.org DT usage model).
- **New findings of the negative kind:** no official LineageOS begonia page (404, §2.2);
  `halium.org/build/portal` dead (404, §5.2); no official public MT6785 phone kernel docs (§6.3–6.4);
  NetHunter's official kernel-source list omits MediaTek (§1.2).
- **Unverified/blocked, kept out of the entry counts' "verified" claims:** `github.com/LineageOS/android`
  (raw README 404 on two branches + github.com fetch-blocked, §2.3), `developer.mediatek.com` and
  `opensource.mediatek.com` (fetch-blocked, §6.1–6.2).

---
*Researched 2026-11-21 (JST), W16. Research-only: nothing flashed, cloned or downloaded. 28 indexed
entries + 11 checklist items; every entry's URL status reflects this session's fetches.*
