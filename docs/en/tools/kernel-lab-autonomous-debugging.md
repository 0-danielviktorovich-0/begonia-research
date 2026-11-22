# Autonomous Kernel Lab for begonia (Linux 4.14 / experimental 4.19)

**Status:** architecture proposal / unimplemented and untested on owner hardware. **Observed:** 2026-11-23. **Device:** Xiaomi Redmi Note 8 Pro (begonia, MT6785). **Host target:** macOS. **Scope:** research-only repository; device-flashing implementation belongs in a separately reviewed, opted-in development project. [Russian digest](../../../docs/ru/tools/kernel-lab-autonomous-debugging.md).

## Executive design

Create a crash-resilient, **host-supervised**, bounded development/test loop: build -> save symbols and known-good image -> deploy *only through an explicit hardware-test gate* -> detect boot phase -> collect evidence -> recover -> classify -> propose patch -> rerun tests. Autonomous does **not** mean unbounded: partition writes, BootROM exploitation, anti-rollback changes and calibration data access are not default capabilities.

**Hard limit:** software running inside a broken kernel cannot be relied on once it has stopped executing. ADB commands require a live adbd transport; fastboot commands require a functioning fastboot endpoint. Power-button or volume-button electrical control requires a separate, independently powered controller or a verified device-specific low-level interface. No method is guaranteed to revive every brick.

## 1. Control-plane / evidence-plane separation

- **macOS supervisor:** normal and recovery ADB, fastboot, USB topology, state machine, persistent host journal, retry budgets, optional USB hub power controller, offline crash analysis.
- **Kernel instrumentation:** validated reserved-memory pstore/ramoops, MTK AEE/MRDUMP audit, tracepoints/ftrace, dynamic debug; KGDB/KDB only after a supported serial transport is confirmed.
- **Recovery first-stage evidence collector:** copy original pstore data before any cleanup/rotation; test with a disposable canary, not a destructive panic on the daily driver.
- **Storage:** host archive is the source of truth; removable microSD and internal persistent storage are additional replicas, not guaranteed to be reachable during panic.
- **Independent hardware (optional):** tested, electrically isolated control of reset/physical buttons and USB data/power. Use only when software states cannot progress.

## 2. Preserve the *first* failure

Linux 4.14 ramoops stores panic/oops chunks in persistent RAM, but its record counter resets after reboot; later crashes can overwrite earlier ones. Console and persistent ftrace buffers can also wrap. Merely changing from Android's kernel to recovery's kernel does **not** make these buffers immune to overwriting.

**Crash Vault contract:**

1. Pre-allocate pstore/ramoops memory after verifying the exact MT6785 memory map, reserved-memory Device Tree nodes, secure/TEE/modem reservations and vendor AEE allocations. Never invent an address.
2. Audit BOTH Android and recovery kernel/DTB configurations for the same region, offsets and layouts. Minimize recovery-side persistent console/ftrace writing where practicable; early recovery printk may still have already overwritten a ring.
3. At earliest possible recovery init stage, read the untouched pstore files **before** any collector, log-rotation or erase action. Stage an immutable copy in RAM; then save to verified writable microSD and/or host. If no media is mounted, wait for the host while avoiding further writes to the source.
4. Record a unique attempt ID, boot generation, build Git SHA, full build manifest, kernel config/dtb hashes, wall-clock and monotonic timestamps where available, reason classification, SHA-256 and source filename, plus a copy of the raw bytes. Do not assume device time is valid early in boot.
5. Crash archives are append-only under `crashes/<attempt-id>/`; repeated boot attempts must not mutate an earlier entry. Deduplicate content by digest, not only by name. Preserve unknown formats in addition to decoded text.
6. Add an explicit `evidence_captured=true` gate. Do not automatically flash another experimental image until critical evidence has been collected, or a bounded timeout with an explicit loss-of-evidence classification has been recorded.
7. Include tests for pstore console overwrite, multiple consecutive panics, battery-off/cold boot, mismatched recovery DTB, failed SD mount, full SD, locked/encrypted userdata, and USB unplug/re-enumeration.

**Media hierarchy:** pstore RAM (volatile across some resets) -> first-stage recovery staging -> microSD and permitted internal location -> Mac immutable archive. SD is **not** a panic-time filesystem write target. Test file system support and filesystem consistency; avoid writing to userdata before unlock/decryption; avoid calibration/protected partitions. Android's `recovery-persist` is an upstream design reference, not proof that a custom recovery ships it.

Potential advanced option: a *prevalidated* block-backed persistent crash journal or reserved dedicated partition, but **NOT** a blind backport of modern `pstore/blk` into 4.14. The space, wear, panic-time I/O safety and loader interactions need separate review.

## 3. Device state machine (host-owned)

| State | Grounded observation | Supported transition / next action |
| --- | --- | --- |
| `ANDROID_ADB` | `adb devices -l` shows device; boot completion separately verified | Save logs, `adb reboot recovery` or `adb reboot bootloader` after gate |
| `RECOVERY_ADB` | Recovery adbd responds | Freeze/copy pstore first; then read-only inventory; optional approved restore |
| `FASTBOOT_BOOTLOADER` | `fastboot devices -l` and command support checked | Query variables; *approved* known-good boot restore; reboot |
| `FASTBOOTD` | Userspace fastboot endpoint verified | Treat separately from bootloader fastboot; support is device/ROM dependent |
| `USB_ENUMERATED_NO_ADB` | Mac USB tree sees device, but no adbd/fastboot transport | Classify VID/PID/interface; restart host ADB; **never** assume a USB USB-reset will boot a stalled kernel |
| `USB_DISAPPEARED` | No matching device in host topology | Retry bounded observation; approved port cycle on verified port; reclassify |
| `MTK_PRELOADER_OR_BROM` | Confirmed MTK enumeration, not just a dead screen | Read-only research/inventory by expert; **no default exploit or partition write** |
| `UNRESPONSIVE` | No usable software transport | Escalate to separately validated hardware controller or human; stop attempts at limit |
| `UNKNOWN` | Conflicting observations | Do not flash; preserve logs and seek more evidence |

Critical: boot stage and USB state are **independent**. Absence from `adb devices` does not mean no USB device or a bricked phone. `fastboot reboot recovery` and `adb reboot fastboot` have platform-specific meaning; do not assume all modes exist on begonia.

## 4. macOS USB re-enumeration without cable pulling

Use this **escalation ladder**, with logs and strict max attempts:

1. Record `adb devices -l`, `fastboot devices -l`, `ioreg -p IOUSB -l -w 0` and `system_profiler SPUSBDataType`. Determine whether macOS sees the phone, its VID/PID, and its physical hub location.
2. If only ADB is stale, use `adb kill-server && adb start-server && adb devices -l`; optionally `adb reconnect` if an ADB transport exists. Restarting adb does **not** force a missing device to enumerate.
3. When Android/recovery shell remains accessible, inspect USB gadget setup, adbd init and USB function, and test a device-side USB-gadget rebind **only on a controlled build**. Existing permission/SELinux/init restrictions apply.
4. Evaluate `uhubctl` and its real per-port power switching on macOS. On macOS 26+ verify libusb >= 1.0.30. Read-only discovery: `sudo uhubctl`. If a hub and exact port are known and support is tested, use `sudo uhubctl -l <hub> -p <port> -a cycle` after a gate. Some hubs disconnect data but not VBUS; USB power cycling may not turn off a battery-backed phone.
5. If only native macOS libusb is available, device reset may not reliably re-enumerate; do not promise a generic software equivalent of physically unplugging a cable. Use a supported hub or a Linux companion host for stronger USB control when needed.

Never apply `uhubctl -a cycle` to all ports or unverified topology; this can disconnect unrelated equipment and the host's storage/network. Do not grant the AI unrestricted root access; expose an allowlisted fixed-port command wrapper.

## 5. Kconfig automation, no terminal UI required

The white terminal UI is `make menuconfig`. For agents use the Kconfig model and deterministic checks:

- Maintain a pinned, device-specific baseline defconfig from an **actually working boot**. Always keep its Git SHA and source revision.
- Generate fragments: `production.fragment`, `debug.fragment`, `deep-debug.fragment`, each scoped to the exact kernel tree and compiler.
- Apply via kernel `scripts/kconfig/merge_config.sh` or `scripts/config`; then run `make O=<output-dir> ARCH=arm64 olddefconfig` and compare requested vs effective config values.
- Use [Kconfiglib](https://github.com/ulfalizer/Kconfiglib) to inspect symbol prompts, expressions, dependencies, visibility and choices. It can help build an agent resolver, but it **cannot guarantee** valid device hardware behavior.
- Treat unmet dependencies, silent symbol changes, `select` risks, warnings and missing symbols as **hard failures** before any deployment.
- Archive `.config`, `savedefconfig` (when supported), fragment list, `scripts/diffconfig` report (if present), DTB/DTBO, linker map, `vmlinux` debug symbols, image SHA-256, Git commit and toolchain version.
- Differential test changes to Device Tree, init/boot image and kernel separately; a missing boot does not automatically implicate Kconfig.

Example **illustrative only** from a correctly prepared kernel source and out dir:

```sh
./scripts/config --file out/.config -e FTRACE -e FUNCTION_TRACER
make O="$PWD/out" ARCH=arm64 olddefconfig
grep -E '^CONFIG_(FTRACE|FUNCTION_TRACER)=' out/.config
```

The effective config must be reviewed; `scripts/config` edits text but does not recursively enable all dependencies. Host tools may run directly on macOS, but kernel/Android builds often require a pinned Linux environment/container/VM for reproducibility.

## 6. Research-first diagnostic profile

Audit supported Kconfig symbols, then evaluate `CONFIG_PSTORE`, `CONFIG_PSTORE_RAM`, `CONFIG_PSTORE_CONSOLE`, `CONFIG_PSTORE_FTRACE`, `CONFIG_PSTORE_PMSG`, `CONFIG_KALLSYMS`, `CONFIG_DEBUG_INFO`, `CONFIG_FRAME_POINTER`, `CONFIG_FTRACE`, `CONFIG_FUNCTION_TRACER`, `CONFIG_DYNAMIC_DEBUG`, `CONFIG_MAGIC_SYSRQ`, watchdog/lockup detector, MTK AEE/MRDUMP. `KGDB`/`KDB`, KASAN and Lockdep are OPTIONAL separate diagnostic profiles; memory, timing, security and ABI effects must be measured. No blanket enabling in production.

For precise symbolization maintain exact-build `vmlinux` and address normalization for relocation/KASLR. Collect panic backtraces, Android logcat, tombstones, boot reason, init logs and, when available, early serial output. A stack frame can indicate the symptom instead of the root cause; validate with controlled change isolation and `git bisect` when repeatable.

## 7. UART, BROM, button control

A purported begonia schematic names `UTXD0`/`URXD0` as application-processor UART signals, but **accessible board pads, signal voltage, connector route and boot-stage enablement are NOT verified**. Ordinary USB-C ADB is not a direct UART console. Before board work: seek service photos, test-point mapping and DT `stdout-path`, `console=`, `earlycon`, `ttyMT*` settings. If pads are confirmed, use measured correct-voltage USB–TTL serial with shared GND; never attach 5 V serial wiring or drive a signal before validation.

[mtkclient](https://github.com/bkerler/mtkclient) and MediaTek Preloader/BROM tools are relevant escalation research, but MT6785 security and firmware differences, loader authentication, timing and possible physical-key/test-point requirements mean these are **not** generic guaranteed rescue paths. Never erase RPMB, `seccfg`, calibration, `preloader`, `nvram`, `nvdata`, `persist`, or `protect*` without a distinct device-owner-led emergency procedure and backups.

If truly unattended physical-key control is needed, a small independent controller that electrically simulates a validated button press is preferable to a motorized finger, but requires electrical isolation, proper power design and board-level testing. It cannot fix damaged hardware.

## 8. Safety gates and trial sequence

**Read-only first:** current device inventory, cable/hub discovery, kernel source config scan, recovery init scan, recovery USB classification, pstore check, unbrick-tool capability matrix. No firmware/partition writes in this repository.

**Controlled non-destructive phase:** verify pstore read and host archive; test reboot Android -> recovery -> Android; detect Android and recovery USB topology; test `uhubctl` separately, only for a dedicated port with owner approval.

**Optional later flashing lab (different repo and explicit opt-in):** complete partition and backup manifest; golden recovery and boot image independently verified; compatible anti-rollback / AVB checked; known-good recovery path rehearsed; flash allowlist; evidence-captured gate; single writer lock; retry limit; emergency stop; signed audit log; dry-run implementation.

**Revert to production:** switch to lean production configuration, remove test-only adbd/root/gadget services and permissive security changes; disable excessive logging and debug sockets; keep a secure minimal crash capture policy if desired. Validate filesystem permissions and SELinux policies.

## 9. Acceptance criteria for future agents

- Inventory runs without rewriting the device and without requiring manual USB cable pulls.
- Supervisor correctly distinguishes host ADB failure, USB enumeration failure, kernel bootloop, recovery, fastboot, MTK enumeration and unknown.
- Once recovery ADB is available, original pstore is archived with content SHA and unique attempt ID **before** a second test is allowed.
- Repeated panics preserve prior host/SD copies; a failed SD mount cannot delete RAM evidence.
- Every Kconfig request is checked against the effective result before build.
- One known-good kernel/recovery combination is demonstrated manually and documented before any autonomous write-capable feature.
- No claim of UART, earlycon, fastbootd or arbitrary brick recovery unless observed on this exact device/build.
- All actions have bounded retries, user-readable logs, and a hard stop on unknown state.

## 10. Primary sources / provenance

All links below are **original references checked by search on 2026-11-23**; no device-specific test was performed by this document.

- [Linux v4.14 ramoops oops/panic logger](https://kernel.org/doc/html/v4.14/admin-guide/ramoops.html) — verified direct documentation: reboot counter / overwrite and reserved RAM requirements; **high**.
- [Android Open Source Project: recovery-persist.cpp](https://android.googlesource.com/platform/bootable/recovery/+/refs/heads/main/recovery-persist.cpp) — verified source design for transfer to persistent recovery logs; **high**.
- [uhubctl README and compatibility/FAQ](https://github.com/mvp/uhubctl) — verified upstream documentation for supported USB hubs/macOS and power-switch limitations; **high**.
- [Linux Kconfig merge_config.sh](https://github.com/torvalds/linux/blob/master/scripts/kconfig/merge_config.sh) — verified upstream implementation with effective-config validation, but master is not the exact vendor 4.14 branch; **high for generic functionality / device-specific version unverified**.
- [Kconfiglib](https://github.com/ulfalizer/Kconfiglib) — verified library API and functionality, compatibility with exact vendor fork untested; **medium**.
- [Google Android Debug Bridge guide](https://developer.android.com/tools/adb) — verified official ADB modes and troubleshooting; **high**.
- [Android fastbootd design](https://source.android.com/docs/core/architecture/bootloader/fastbootd) — generic reference; support on begonia unknown; **high generic / unverified device**.
- [MTKClient](https://github.com/bkerler/mtkclient) — open-source MTK transport and recovery research; no guaranteed support for current firmware; **medium for device-specific**.
- [Linux upstream AI coding assistant policy](https://github.com/torvalds/linux/blob/master/Documentation/process/coding-assistants.rst) — verified upstream guidance, applicable when submitting patches upstream; **high**.
- [Begonia hardware and recovery audit](../recovery/07-RECOVERY-SAFETY.md) — local historical research, test procedures still require verification.

**Next:** read the companion [agent mission](kernel-lab-agent-mission.md) and [macOS inventory](kernel-lab-macos-inventory.md). This is a feasibility plan, not a report that any autonomous recovery cycle already works.