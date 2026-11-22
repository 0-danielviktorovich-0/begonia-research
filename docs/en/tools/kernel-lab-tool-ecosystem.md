# Reuse existing professional tooling before building a custom Kernel Lab

**Observed:** 2026-11-23. **Device:** begonia / MT6785 / downstream Linux 4.14, separately experimental 4.19. **Status:** tool-capability research, *not installed/tested on owner Mac*. This is a companion to the [canonical architecture](kernel-lab-autonomous-debugging.md) and [bounded agent mission](kernel-lab-agent-mission.md).

## A. Board orchestration: primary reuse candidates

| Tool | Existing capability | begonia / macOS fit | Decision |
| --- | --- | --- | --- |
| [labgrid](https://github.com/labgrid-project/labgrid) | Resources/drivers for Android USB fastboot, serial consoles, managed power/reset and pytest integration | Very good architecture/API pattern; verify whether full feature set runs natively on macOS; Linux host/VM may be easier | **First investigate; do not rewrite its state-machine abstractions** |
| [Linaro LAVA](https://lava.readthedocs.io/en/latest/introduction/concepts.html) | Automated hardware CI, deploy/boot/test, recovery and device health checks | Designed around reliable independent reset, serial console and working bootloader; likely overkill for one phone | **Reference for robust lab design**, consider Linux host for scale |
| [uhubctl](https://github.com/mvp/uhubctl) | Per-port USB hub power control on supported models; macOS support | Immediate candidate for recovery gadget not re-enumerating after reboot | **Prioritize compatible hub validation** |
| [Android platform-tools](https://developer.android.com/tools/releases/platform-tools) | ADB, fastboot, standard reboot and shell paths | Native Mac installation; already user's primary interface | **Core transport**, does not rescue absent endpoints |
| [mtkclient](https://github.com/bkerler/mtkclient) | MTK BROM/DA transport and device recovery research | macOS installation documented; exact device firmware/security path unverified | **Separate emergency playbook only** |

**Important insight from LAVA:** automated recovery requires an externally controllable reset path, a reliable bootloader and visibility into boot failure. LAVA's own docs explicitly discuss battery/USB power leakage and states that automation may fail to recover. Therefore do not promise 100% autonomous unbrick simply by installing it.

## B. Crash preservation, tracing and root cause

| Tool | Role | Notes for Linux 4.14 |
| --- | --- | --- |
| `pstore / ramoops` | Persistent crash records and optional persistent tracing | Upstream v4.14 functionality; potential overwrite across boots; validate memory map and recovery parity |
| MTK AEE / MRDUMP | MediaTek exception and dump handling | Branch-specific: inspect actual Kconfig, drivers, bootloader/DRAM requirements |
| `ftrace` / `trace-cmd` / `kernelshark` | Function/event tracing and visualization | Usually possible; verify exact 4.14 kernel trace facilities and host userspace tool versions |
| `dynamic_debug` / `kprobes` | Scoped logging/instrumentation | Depends on enabled options, probe sites and vendor fork |
| `KGDB` / `KDB` with GDB | Stop/inspect kernel registers and call stacks | KGDB needs validated communications transport (serial debug is not automatic via ADB) |
| `vmlinux` + `addr2line` / `faddr2line` | Offline crash symbolization | Archive **exact** unstripped image and build identity; account for KASLR/relocation |
| `kdump` + `crash` | Analyze large kernel core images | Depends on crash-kernel/reserved-memory feasibility; generally higher complexity on phones |
| `LKDTM` | Intentional fault injection for tests | Dangerous: only isolated disposable controlled tests; requires explicit opt-in |
| [AOSP recovery-persist](https://android.googlesource.com/platform/bootable/recovery/+/refs/heads/main/recovery-persist.cpp) | Moves recovery pstore messages to persisted storage | Design reference; custom recovery may omit it |

## C. Kconfig and build correctness

| Tool | Role |
| --- | --- |
| `make menuconfig` | Interactive ncurses editor, useful for human exploration |
| `scripts/config` | CLI toggles, **does not automatically enable dependencies** |
| `scripts/kconfig/merge_config.sh` | Apply fragments and verify effective values |
| `make olddefconfig` | Normalize config with actual Kbuild rules |
| [Kconfiglib](https://github.com/ulfalizer/Kconfiglib) | Programmatic symbol/dependency/choice/visibility graph; build own resolver and structured error reports |
| `scripts/diffconfig` / `make savedefconfig` | Review minimal effective changes if present in the exact tree |
| `make W=1`, `scripts/checkpatch.pl`, Sparse, Smatch, Clang static analyzer | Compile-time, lint and static-analysis quality gates; set up with branch-compatible toolchains |

A valid Kconfig result **does not** prove a working DTB, boot image, drivers or hardware. Keep known-good baseline, exact commits, build symbols and reproducible toolchains for every experiment.

## D. Automated testing and kernel fuzzing

| Tool | Use | Caveat |
| --- | --- | --- |
| [syzkaller](https://github.com/google/syzkaller) | Unsupervised coverage-guided kernel fuzzing, including documentation for Android ARM physical devices | `KCOV`, debug-capable builds, compatible host and reliable external recovery needed; high-risk on a daily phone |
| [KUnit](https://docs.kernel.org/dev-tools/kunit/index.html) | In-kernel unit tests | Not assumed available in vendor Linux 4.14; audit/backport separately and avoid introducing compatibility issues |
| [kselftest](https://docs.kernel.org/dev-tools/kselftest.html) | Kernel subsystem tests via userspace | Availability/test prerequisites vary; do not run destructive tests on owner device |
| [TuxRun](https://tuxrun.org/) | Curated Linux testing on virtual or supported targets | Useful for generic ARM64 kernel testing; not a faithful MT6785 smartphone emulator |
| [QEMU](https://www.qemu.org/) / [Renode](https://renode.io/) | Emulator/prototype of portable or isolated components | Does not emulate proprietary MT6785 boot chain, GPU, modem or board without major development |

Use mocked inputs for USB state machine and crash archive on Mac first; then Linux VM/emulator for portable code; only then hardware-in-the-loop on a disposable/test device.

## E. Selection guidance

**Small one-phone lab:** start with platform-tools + native macOS USB inventory + uhubctl + a minimal restricted state machine. Adapt labgrid ideas if native support proves awkward. Persist crash evidence before any additional flash attempts.

**Multi-device lab:** migrate command execution to a pinned Linux host, evaluate labgrid and LAVA with serial and power-control resources.

**Deep kernel engineering:** use exact-build ftrace/AEE/ramoops, symbolization, Kconfiglib and upstream tools before developing proprietary instrumentation.

**Privacy/security:** raw kernel dumps may contain personal data; store them privately, never put them in an ordinary research source ledger or publicly accessible repository.

## Sources (checked 2026-11-23)

- [labgrid overview](https://labgrid.readthedocs.io/en/latest/) and [resource/driver architecture](https://github.com/labgrid-project/labgrid/blob/master/doc/overview.rst): verified published project features; exact macOS fit unknown.
- [LAVA: device integration](https://lava.automotivelinux.org/static/docs/v2/device-integration.html) and [CI power/recovery](https://lava.automotivelinux.org/static/docs/v2/lava_ci.html): verified external-reset and rescue limitations.
- [uhubctl](https://github.com/mvp/uhubctl): verified macOS and per-port-hub capability, actual hub untested.
- [syzkaller Android ARM kernel device setup](https://github.com/google/syzkaller/blob/master/docs/linux/setup_linux-host_android-device_arm-kernel.md): verified upstream workflow, not validated for MT6785.
- [Linux 4.14 ramoops](https://kernel.org/doc/html/v4.14/admin-guide/ramoops.html): directly applicable Linux version feature, device wiring unverified.
- [Kconfiglib](https://github.com/ulfalizer/Kconfiglib): verified programmatic Kconfig engine, device-specific dependencies to audit.

**Scope boundary:** this document inventories professional tool reuse; it does not demonstrate that these utilities have been installed, that the phone's UART is accessible, or that recovery from arbitrary bricked states is possible.