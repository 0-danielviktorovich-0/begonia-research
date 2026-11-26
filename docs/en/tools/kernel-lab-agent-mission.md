# Agent mission: Kernel Lab — feasibility first, no flashing

**Date:** 2026-11-23. **Hardware:** Redmi Note 8 Pro / begonia / MT6785. **Host:** owner's Mac. **Kernel:** downstream 4.14 (investigate 4.19 independently). **Status:** task specification, NOT completed execution.

## Read first

1. [Canonical Kernel Lab architecture](kernel-lab-autonomous-debugging.md).
2. [Read-only device preflight](../recovery/18-DEVICE-PREFLIGHT-READONLY.md).
3. [Recovery and unbrick safety](../recovery/07-RECOVERY-SAFETY.md).
4. [Kernel evidence and provenance](../research/begonia-kernel-and-rom-evidence-2026-11.md).
5. [Project evidence contract](../../../_context/CONTEXT.md), [requirements](../../../_context/REQUIREMENTS.md), [tools policy](../../../tools/README.md).
6. [Linux upstream AI coding assistants requirements](https://github.com/torvalds/linux/blob/master/Documentation/process/coding-assistants.rst). Do not invent Signed-off-by; a human signs DCO.

## Mission

Research and design a reproducible Mac-operated, safe, autonomous development loop that (a) distinguishes device/recovery/bootloader/USB failure states; (b) captures and protects the *first* crash across reboots; (c) resolves kernel Kconfig requests against actual dependencies; (d) documents verified, narrowly-scoped recovery mechanisms; (e) can later provide tools to external AI agents via a machine-readable interface.

**Constraint:** this knowledge-base repo is research-only. Do **NOT** flash, erase, unlock, run BROM exploit payloads, reconfigure the physical device, edit recovery/boot partitions or install host packages without explicit owner's new approval and a separate operational gate. No unreviewed scripts from the Internet. Work in an isolated git branch / PR.

## Deliverables (write files, not just chat)

- `data/matrices/kernel-lab-capability-matrix.csv`: `capability,layer,implementation,minimum_state,needs_hardware,macos_support,begonia_evidence,status,source_url,confidence`. Make each claim traceable, use VERIFIED / INFERRED / UNKNOWN.
- `docs/en/tools/kernel-lab-macos-device-inventory-RESULTS.md`: output of *approved read-only* checks including OS version, adb/fastboot versions, USB topology and device presence; redact serial numbers, device IDs that could identify owner, full file paths and secrets.
- `docs/en/tools/kernel-lab-kconfig-audit-RESULTS.md`: exact source tree/ref, available `scripts/config` and `scripts/kconfig/merge_config.sh`, candidate pstore/AEE/ftrace/lockdep/watchdog/KGDB Kconfig symbols, where they are defined, dependencies, actual base defconfig, and an effective-value verification proposal.
- `docs/en/tools/kernel-lab-recovery-audit-RESULTS.md`: known recovery boot/kernel/DTB config, pstore region parity, init action order, ADB gadget init path, recovery-persist capability, SD filesystem support, and known-good boot recovery procedure. Unknowns stay unknown.
- `docs/en/tools/kernel-lab-uart-audit-RESULTS.md`: credible board/net/pin mapping for MT6785 UART0, actual begonia board test pads if verifiable, electrical levels, console settings and whether accessible without opening. Do NOT present schematic chip signals as exposed pads.
- `docs/en/tools/kernel-lab-test-plan.md`: simulation/mocked USB state tests, first-failure preservation, bounded retries, known-good image checks, canary/cold-boot testing, end-to-end gates.
- Optional: a read-only host inventory script with no installation/writes and tests for it. Do not create or run a flashing agent.

## Work plan (independently verifiable checkpoints)

### Phase A — research-only mapping

- Record repository HEAD and exact kernel branch/tree SHAs; distinguish vendor 4.14, known bootable 4.19, public sources and speculation.
- Inventory existing device-tree `reserved-memory`, MTK AEE/MRDUMP and ramoops symbols; no blind DT memory offset.
- Identify recovery image kernel/DTB provenance, and whether it shares/destroys ramoops.
- Review root path implications of debugfs, permissive adb, arbitrary GDB/KGDB, and crash logs containing personal data.
- Build state model: android-adb, recovery-adb, fastboot bootloader, fastbootd (if tested), preloader/BROM, enumerated-without-adb, USB absent, unknown.
- Examine macOS USB hub support (including `uhubctl` per-port power and libusb version), read-only topology and device enumeration.
- Analyze Kconfig dependencies with the correct Kconfig environment and native Kbuild result; record any tool incompatibility.

### Phase B — safe implementation prototypes

- Mocked state-machine monitor: consume example `adb devices`, `fastboot devices` and macOS USB tree outputs; output correct state, reason, next safe action and attempt budget. No real device write.
- Pure offline crash archive tool: copy sample files; unique build/attempt ID; append-only directories; SHA-256; read-back verification; manifest; collision/error handling; no auto-delete.
- Pure offline Kconfig validation tool: compare requested symbolic fragment against effective `.config`; fail on missing/unset/mismatched symbols; output structured explanation. Consider Kconfiglib for dependency explanation.
- Agent tool API design with fixed methods and precise safety levels: `inventory`, `collect_logs`, `classify_state`, `verify_config`, `symbolize_crash`, `propose_fix` and separately gated `restore_known_good`. No arbitrary shell write command.

### Phase C — future owner-gated real testing (NOT part of this mission)

- Mac USB bridge: read-only observations first, supervised restart host ADB, then explicit approval for an allowlisted port cycle on a confirmed dedicated hub.
- A matching recovery kernel configuration and early pstore capture prototype; verify with non-destructive canary before deliberately injecting panics.
- Only after evidence capture and rollback are demonstrated: controlled boot-image deployment, single-writer lock, max reboot count, emergency stop and success criteria.
- No claim of unattended brick recovery until it is shown for precisely enumerated failure cases.

## Red-line rules

- No repartitioning, formatting, AVB/anti-rollback change, preloader/bootloader/NVRAM/NVDATA/persist/IMEI/RPMB/calibration writes.
- No automatic bootloader unlock, SLA/DAA workaround or exploit use.
- Do not equate powered hub port switching to switching off a battery-backed phone.
- Do not equate `adb devices` absence with device absence.
- Never replace or clear original pstore before immutable capture.
- Never enable production debug interfaces without an opt-in test profile.
- Never claim a kernel boots merely because it compiles, Kconfig resolves or Android version advances.
- A failed command must be surfaced as failed, with literal stderr; bounded retries, never infinite loops.
- Human must be able to override and stop the controller; files remain private until release audit.

## Reporting format

Report first: verified successes, blocked/unknown facts, high-severity safety risks, exact files changed, source URLs and SHA/branch references. Then implement safe mocks in isolated commits. Record commands executed and their outputs, not just the AI's conclusions. Distinguish PLANNED from IMPLEMENTED, DEVICE-TESTED from HOST-TESTED.

**Done condition for this mission:** a thoroughly verified design, capability matrix and safe prototype tests have been committed to a reviewable PR. No autonomous flashing or unbrick behavior may be presented as implemented.