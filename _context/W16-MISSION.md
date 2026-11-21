# W16 MISSION — official porting & kernel-development docs index (user demand, 2026-11-21: "обязательно")

Repo: /Users/danielviktorovich/begonia-research (orchestrator runs git — you do NOT).
Context: the guide index (10-GUIDE-INDEX.md) covers FORUM guides; the user demanded the OFFICIAL
development/porting documentation be indexed too — what one must read and usually ACTIVATE when porting
a device (kernels, DTB, defconfigs, peripherals). ≤14 tool calls. English; titled markdown links;
verified/inferred + confidence; no git; research-only.

## DELIVERABLE: /Users/danielviktorovich/begonia-research/_context/PORTING-DOCS-INDEX.md

Sections (each entry: official title as markdown link | what it covers | why it matters for begonia/MT6785 |
access status | confidence):
1. Kali NetHunter official: kali.org/docs/nethunter/* (kernel building, "NetHunter kernels" GitLab
   gitlab.com/kalilinux/nethunter, wireless/monitor-mode docs, installation docs) — cite the pages you open.
2. LineageOS official: wiki.lineageos.org device-build docs ("Build for begonia" if the device page exists,
   generic "Build Guides"), repo manifests.
3. AOSP official: source.android.com kernel docs (kernel config requirements per Android version, DTB/DTBO
   requirements, verified boot/AVB pages relevant to begonia).
4. postmarketOS official: wiki porting pages (Porting to a new device, Close to Mainline, pmbootstrap docs at
   docs.postmarketos.org), pmaports contribution guide.
5. Halium official: halium.org/build/portal docs (build + porting checklists; note 404s if hit).
6. MediaTek-specific: any official MTK developer portals/source releases relevant to MT6785; MTK android
   kernel config conventions; gen4m/wlan build docs if public.
7. "What is usually activated when porting" checklist distilled from the above: DTB/DTBO wiring, defconfig
   pieces (configfs/HID, USB gadgets, WLAN), firmware packages, sepolicy, boot image headers — each item
   linked to the official doc that mandates it.
Finish with a "Gap vs this repo" note: which of these docs are already cited in 00-15 and which are new.

## OUTPUT
Write the file; append consulted sources to
/Users/danielviktorovich/AI-OS/.hermes/cache/scratch/begonia-recon/sources.jsonl.
Final message ≤150 words: sections covered, entry count, dead links, new-vs-already-cited ratio.
Do NOT touch other research files. No git.
