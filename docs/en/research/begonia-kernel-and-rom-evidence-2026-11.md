# Begonia kernel/ROM source verification — November 2026

**Device:** Xiaomi Redmi Note 8 Pro, `begonia` (MediaTek MT6785/Helio G90T). **Checked:** 2026-11-21.  
**Scope:** distinguish genuine device-specific 4.14 sources, 4.19 *build references*, and Android ROM release versions. Research only — not a flashing recommendation.

## Findings from pinned upstream revisions

| Project | Pinned revision / inspected file | Evidence | Interpretation |
|---|---|---|---|
| [WuXing90/begonia_kernel_dev](https://github.com/WuXing90/begonia_kernel_dev) | [Suzaku-bka at `0d2ec0ae973ec500b559e282fcafb544d295ba5d`](https://github.com/WuXing90/begonia_kernel_dev/tree/0d2ec0ae973ec500b559e282fcafb544d295ba5d); [Makefile](https://github.com/WuXing90/begonia_kernel_dev/blob/0d2ec0ae973ec500b559e282fcafb544d295ba5d/Makefile) | `VERSION=4; PATCHLEVEL=14; SUBLEVEL=356; EXTRAVERSION=-openela-rc1` | **Linux 4.14.356**, not a 4.19 kernel. |
| [Saikrishna1504/kernel_xiaomi_mt6785](https://github.com/Saikrishna1504/kernel_xiaomi_mt6785) | [main at `a63454e153cd57f410c7f6f8565f05b943198be1`](https://github.com/Saikrishna1504/kernel_xiaomi_mt6785/blob/a63454e153cd57f410c7f6f8565f05b943198be1/Makefile) | `VERSION=4; PATCHLEVEL=14; SUBLEVEL=357; EXTRAVERSION=-openela` | **Linux 4.14.357** source. |
| [Saikrishna1504/device_redmi_begonia](https://github.com/Saikrishna1504/device_redmi_begonia) | [axion `0ce116f1e5cffd58953fc37c24fb600b6e003272`, BoardConfig.mk](https://github.com/Saikrishna1504/device_redmi_begonia/blob/0ce116f1e5cffd58953fc37c24fb600b6e003272/BoardConfig.mk) | `TARGET_KERNEL_CONFIG := k85v1_64_k419_defconfig vendor/begonia.config` | **4.19-targeting config reference**, *not proof of an available buildable 4.19 kernel tree*. |
| [Saikrishna1504/local_manifests](https://github.com/Saikrishna1504/local_manifests) | [udc `079a599d2208192a3457f6cc2a2e490e2716da42`, mt6785.xml](https://github.com/Saikrishna1504/local_manifests/blob/079a599d2208192a3457f6cc2a2e490e2716da42/mt6785.xml) | `kernel/xiaomi/mt6785` → `kernel_xiaomi_mt6785`, revision `main` | Publicly referenced kernel source still targets **4.14**. Check any private/local override before claiming 4.19. |
| [AxionAOSP-devices/android_device_redmi_begonia](https://github.com/AxionAOSP-devices/android_device_redmi_begonia) | [axion `334810a4315a0fca3b250eebec0f5c69ff0ddab9`, BoardConfig.mk](https://github.com/AxionAOSP-devices/android_device_redmi_begonia/blob/334810a4315a0fca3b250eebec0f5c69ff0ddab9/BoardConfig.mk) | `TARGET_KERNEL_CONFIG := begonia_user_defconfig`; LLVM flags | A **different published device configuration**. Do not assume equivalence to Saikrishna's k419 config. |
| [AxionAOSP/official_devices](https://github.com/AxionAOSP/official_devices) | [Wiki/begonia.md at `aa130566749d970c5537a7f4d3e3310d06403d4e`](https://github.com/AxionAOSP/official_devices/blob/aa130566749d970c5537a7f4d3e3310d06403d4e/Wiki/begonia.md) | Installation/recovery/dirty-flash procedure | Confirms an official Axion device installation guide, **does not identify its Linux kernel version**. Do not transplant its destructive wipe instructions to other ROMs. |

## LineageOS 23.2: Android version is not Linux kernel version

- [Saalim Quadri's LineageOS 23.2 begonia release notes](https://squadri.me/devices/begonia-lineageos/) (posted 2026-03-28) explicitly list **Android 16.2 + Linux kernel 4.14**, with links to a [specific XDA release thread](https://xdaforums.com/t/rom-unofficial-lineageos-23-2-redmi-note-8-pro-begonia.4783655/) and the WuXing90 kernel source.
- The XDA page could not be fetched directly in this research session (HTTP 502). Its content, subsequent posts, and change logs are **not independently validated** here.
- Other community reports mention experimentation with a begonia Linux 4.19 port. Such a claim should remain **unverified as a usable port** until an accessible exact commit, 4.19 Makefile, begonia DTS/defconfig, build configuration, boot logs, and tested functionality matrix are available.

## Review checklist for a candidate 4.19 port

1. Pin an actual upstream commit SHA, not just a branch or an Android release name.
2. Inspect `Makefile` (`VERSION`, `PATCHLEVEL`, `SUBLEVEL`) and `arch/arm64/configs` for *begonia*-specific config fragments.
3. Verify DT/DTS matches MT6785 **begonia**, not merely another MT6785 product such as *rosemary*.
4. Inspect recent commits and patches around display, touch, GPU, Wi-Fi, modem, cameras, clocks, regulators, power management, and boot chain.
5. Require reproducible build steps, non-destructive test and serial/ramoops/earlycon logs before claiming a functional phone kernel.

**Platform scope:** Apple Silicon, iOS 18, and generic unrelated SoC examples cannot serve as evidence for *begonia*. Device-specific source links, build logs, and verified commit IDs take priority.

Related: [kernel history](../kernels/03-KERNEL-HISTORY.md), [hardware/driver map](../kernels/04-HARDWARE-DRIVERS.md), [kernel forward-port notes](../kernels/14-MAINLINE-UPGRADE-PATH.md), [Saikrishna device-stack audit](24-SAIKRISHNA1504-DEVICE-STACK-AUDIT.md).
