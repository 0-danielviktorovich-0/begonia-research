# macOS runbook: read-only ADB / fastboot / USB-state inventory

**As of 2026-11-23. Status:** proposed runbook, NOT executed on owner's Mac or begonia device. Use alongside the [Kernel Lab architecture](kernel-lab-autonomous-debugging.md) and [agent mission](kernel-lab-agent-mission.md).

## Safety classification

**Read-only on Mac / device:** inspect tool versions, list USB devices, list ADB/fastboot endpoints, read boot reason, list pstore, capture crash evidence. **Host service state only:** restart ADB server. **Changes physical USB state:** uhubctl cycle — permitted only after hub/port validation, separate opt-in. **Phone reboot:** adb reboot / fastboot reboot — mode-changing, require approval and clear verified state. **Firmware write:** out of scope.

## 1. Host baseline (non-destructive)

```sh
sw_vers
uname -m
command -v adb || true
command -v fastboot || true
command -v uhubctl || true
command -v python3 || true
adb version 2>&1 || true
fastboot --version 2>&1 || true
system_profiler SPUSBDataType
ioreg -p IOUSB -l -w 0
```

Outputs can contain serial numbers and private paths; redact before committing. `fastboot --version` may differ by tool release. Never declare a tool installed until verified by local output.

Recommended installation **only after owner permission**: `brew install android-platform-tools libusb uhubctl`. On macOS 26+, the uhubctl project documents libusb >= 1.0.30. Confirm actual versions, hub compatibility and whether the hub truly cuts VBUS vs only data.

## 2. Determine available protocol

```sh
adb devices -l
fastboot devices -l
ioreg -p IOUSB -l -w 0
```

- ADB `device`: Android or recovery adbd available; use `adb shell getprop ro.bootmode` and `getprop sys.boot_completed` to distinguish stage, not only transport.
- ADB `unauthorized` or `offline`: address adb authentication/startup; not proof of bootloop.
- Fastboot listed: query read-only `fastboot getvar product` and `fastboot getvar is-userspace` where supported; record errors rather than assuming support.
- USB enumerated with no ADB/fastboot: capture exact VID/PID/interface class and identify known MediaTek preloader/bootrom states vs custom recovery USB gadget.
- Nothing enumerated: separate USB cable, hub, host and device faults; a dark screen is not proof of a dead boot chain.

Read-only Android commands after confirmation of shell access:

```sh
adb shell uname -a
adb shell getprop ro.boot.bootreason
adb shell getprop ro.bootmode
adb shell getprop sys.boot_completed
adb shell ls -l /sys/fs/pstore
adb shell cat /proc/cmdline
```

`/sys/fs/pstore` may be missing, unreadable or already rotated. Android permission and SELinux apply. Do not run a reboot merely to confirm pstore until archive design is validated.

## 3. Stale ADB versus missing USB re-enumeration

When recovery seems to appear only after the owner re-plugs cable:

1. Collect output of `adb devices -l`, `fastboot devices -l` and Mac USB tree **before physical replug**.
2. Re-run the same inventory **after replug**. Diff VID/PID, address, interfaces and mode. This identifies whether root cause is adb-server, gadget initialization or host USB enumeration.
3. If Mac shows USB gadget but ADB client is stale, test host-only `adb kill-server; adb start-server; adb devices -l`. If adbd is alive but one ADB transport is `offline`, consider `adb reconnect offline` based on the installed platform-tools release.
4. If Mac does not detect gadget, ADB reset cannot repair it. Diagnose recovery init, USB configfs/legacy Android gadget and UDC binding in the recovery kernel, and optionally use tested `uhubctl` physical port cycle.
5. Never ascribe a fix without repeated A/B trials on the same recovery build and the same cable/port topology.

**Passive USB recheck** and **restart ADB server** are different from a USB port power toggle. `libusb_reset_device()` is not a guaranteed unplug emulation on macOS; in particular, historical macOS reset shortcomings are documented in libusb issue #455.

## 4. uhubctl: fixed-port example (NOT an invitation to run now)

First identify the dedicated port and verify no unrelated device shares power switching:

```sh
sudo uhubctl
```

Then, only when approved, replace placeholders using actual output:

```sh
sudo uhubctl -l <hub-location> -p <port-number> -a cycle
```

Do not run the placeholders literally. Allowlist the hub path, port, maximum retries and minimum time between cycles in a separate host controller. Record before/after USB topology. If the hub does not genuinely power-switch that port, choose a validated model or focus on recovery gadget fixes instead.

## 5. Controlled mode transitions (approval required)

When ADB responds and an explicit boot-mode transition is authorized:

```sh
adb reboot recovery
# Or, in a separate test:
adb reboot bootloader
```

When genuine bootloader fastboot responds, check model and command support; `fastboot reboot` normally returns to the default system boot path. `fastboot reboot recovery` is **not** a universally supported command; fastbootd is a different mode and may not exist on this device.

If the kernel panics before adbd runs, the Mac cannot send an adb command into that crashed kernel. Options are a tested watchdog/panic recovery strategy, bootloader-controlled boot paths, a suitable always-available USB mode or independent hardware button/reset control.

## 6. Diagnostic-first recovery strategy

Recovery should export ADB reliably, but pstore capture must **not depend on ADB being up**: run a minimal early local collector that saves raw logs to safe staging before recovery's own logging wraps persistent memory. ADB becomes a way to transfer an already sealed evidence bundle.

On an initialized recovery, pull **copy-only** evidence to Mac; exact paths and permissions require inspection:

```sh
adb shell ls -la /sys/fs/pstore
# Example: available file name must be discovered first.
adb pull /sys/fs/pstore/console-ramoops-0 ./console-ramoops-0
```

The collector should attach boot/build metadata and compute SHA-256 on host. Avoid deleting files in `/sys/fs/pstore` after extraction until its persistence and read-back behavior is tested.

## 7. Read-only compatibility inventory for MediaTek

When Mac USB tree enumerates MTK Preloader or BootROM, record hardware VID/PID, firmware/SoC evidence and tool compatibility. [mtkclient](https://github.com/bkerler/mtkclient) provides macOS installation docs but not universal MT6785 rescue; authenticated loader and hardware entry methods may be required. No generic unlock, bypass, erasing or partition write belongs in the routine recovery loop.

## 8. Success matrix

| Experiment | Evidence of success | Failure to record |
| --- | --- | --- |
| Normal Android -> recovery | Recovery detected with USB topology and ADB; pstore retained | stale adbd, missing interface, wrong VID/PID |
| Recovery -> Android | System boots and health checks pass | reboot loop, missing boot reason |
| ADB server restart | Reconnect without cable movement | no USB endpoint / server still stale |
| Dedicated USB hub cycle | Recovery re-enumerates without manual cable pull | hub unsupported / unrelated devices drop |
| Crash Vault canary | Immutable, hash-verified first crash bundle survives second boot | console wrapped / missing record / SD mount failure |
| Fastboot classification | Correct device-specific fastboot state, no write | fastbootd confusion / incorrect device |
| Kconfig normalization | Requested effective symbols match | dependencies unmet / silently disabled |

## Sources

- [Android ADB official guide](https://developer.android.com/tools/adb)
- [Android platform-tools release notes](https://developer.android.com/tools/releases/platform-tools)
- [uhubctl upstream project and macOS install guidance](https://github.com/mvp/uhubctl)
- [libusb macOS reset issue #455](https://github.com/libusb/libusb/issues/455)
- [Android fastbootd architecture](https://source.android.com/docs/core/architecture/bootloader/fastbootd)

Sources inspected 2026-11-23. Device behavior has **not** been independently tested as part of this document.