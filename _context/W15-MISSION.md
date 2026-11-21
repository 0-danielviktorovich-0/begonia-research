# W15 MISSION — RE-driven improvement plan for begonia (2026-11-21)

Repo: /Users/danielviktorovich/begonia-research (orchestrator runs git — you do NOT).
Read FIRST: _context/REQUIREMENTS.md (rows 33, 37), _context/CONTEXT.md, 00-README.md (major findings),
04 (component IDs + gaps), 06 (why Halium works), 07 (host matrix: mtkclient native on macOS), 08 (P0/P1/P2 roadmap),
13 (extras: F_HID=y, ath9k_htc monitor recipe, AkameKernel), 14 (mainline gaps per tree).
Owner facts you MUST honor: Ghidra 12.1.4 + Craft Anything installed on his Mac (verified 2026-11-21);
AkameKernel = a TRUSTED FIRST-PARTY kernel asset with private maintainer access (identity withheld from public docs); original MIUI 12.5 fastboot ROM
= ground truth where everything works. ≤22 tool calls. English; titled links; verified/inferred + confidence;
research-only: no flashing, no executing untrusted binaries; artifacts >50MB stay OUT of the repo.

## DELIVERABLE: /Users/danielviktorovich/begonia-research/15-RE-IMPROVEMENT-PLAN.md

### Section 1 — Ground truth & unpacking recipe
- The one firmware to grab as reference: last MIUI 12.5 EEA fastboot ROM (V12.5.15.0.RGGEUXM, 2022-08-26,
  4.4GB tgz — link from 02/census; also recovery 2.4GB zip alternative). Exact download recipe, expected
  structure (images: vendor.img.ext4/win, system, odm?, nvram/nvdata images, preloader, lk, tee, cam/vpu firmware),
  unpack tools per artifact (simg2img for sparse, payload-dumper-go for OTA payload.bin, 7z/mount for ext4,
  strings/ghidra for ELF blobs), where extraction results live (scratch, NOT repo), disk/time estimates.
- Which partitions/what inside them matter for WHICH subsystem (map: audio params + libaudio → 04 audio gap;
  wifi gen4m blobs+cfg → 13/14 WiFi gap; camera libs/sensors → 04; modem NVRAM → 07 backups; touch firmware
  already handled by pmOS pkg; GPU kbase/blobs → panfrost alternatives).

### Section 2 — Per-subsystem improvement matrix (difficulty-rated)
For each broken/limited subsystem (from 04/06/14): what the stock firmware has (ground truth), what mainline/
Halium lacks, the concrete RE or kernel-work path, difficulty (easy/medium/hard/extreme + why), and whether
an AI agent can drive it with the owner only running tests. Cover at least: audio (AFE/machine driver via
mt6797 template + mt6359 — cite 14), WiFi (mt76 vs gen4m RE — chip ID first per 14), camera (seninf/camsv
per kalpakprod + heavy userspace), sensors glue, battery/charging (MT6360), touch (solved — pmOS pkg), HID/USB
(already F_HID=y — polish recipes per 13), monitor-mode (internal no-patch; external dongle recipe per 13).

### Section 3 — Sequencing recommendation (user's question)
Structured answer: fix UT on Halium-10 first → Halium-11 (AgentFabulous android-11.0 base) → mainline (pmOS
path) with RE filling gaps — OR jump straight to newer stacks? Give a reasoned recommendation with effort
estimates per stage, the 'Mali driver precedent' (panfrost pushed via RE + upstreaming) as the model for
'reverse-engineer what does not work', and what AkameKernel's resurrection adds (first-party kernel: refresh
toolchain, KSU-Next/SUSFS, monitor-mode patches from 13 — a first-party testbed for kernel experiments).

### Section 4 — Test-resource checklist
Concrete list the owner/agents need for the test phase: downloads (links+sizes), host tools (mtkclient,
adb/fastboot, payload-dumper-go, simg2img, 7z, Ghidra/Craft Anything), device-side state (unlocked BL, TWRP/
OrangeFox, current ROM), safety rails (07 backups), and the exact 'agent proposes → owner runs' loop design.

## OUTPUT
Write the file; append sources to /Users/danielviktorovich/AI-OS/.hermes/cache/scratch/begonia-recon/sources.jsonl;
return ≤250 words: unpacking recipe verdict, top-3 highest-ROI RE targets with difficulty, sequencing
recommendation one-liner, Akame resurrection verdict. Do NOT touch other research files. No git.
