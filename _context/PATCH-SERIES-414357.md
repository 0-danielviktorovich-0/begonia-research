# Unified kernel 4.14.357 (begonia) — patch series + build-problem log

## Контекст
Первая сборка unified-ядра (clang 18.1.3, нативный arm64-контейнер Ubuntu 24.04).

## P-DTB (финал: P3 активен) — почему не собирался DTB
**Симптом 1**: `rosetta error: failed to open elf at /lib64/ld-linux-x86-64.so.2` на шаге DTC.
**Диагноз [V]**: MTK-дерево несёт прекомпилированный x86_64-бинарь `scripts/dtc/dtc_overlay`
(SHA256 ada1d813…; RE-вердикт через Ghidra/REA: штатный dtc-форк с overlay-поддержкой, gold-линковка,
посторонних строк/поведения нет), и правило `scripts/Makefile.lib:318` вызывает именно его.

**Симптом 2** (после P1): `xiaomi-mt6785-common.dtsi:20.1-17 syntax error` на `/dts-v1/; /plugin/;`.
**Диагноз**: dtsi-файлы MTK написаны в android-overlay-стиле (директивы внутри include-цепочки);
mainline dtc 1.4.x (исходники в самом дереве 4.14) такую грамматику режет, а **прекомпил MTK собран из
более нового dtc поколения 1.5+/AOSP external/dtc**, где android-overlay-грамматика есть. То есть код
MTK «не плохой и не грязный» — они не стали апгрейдить in-tree dtc, а приколотили свежий бинарь
(происхождение: AOSP external/dtc — гугловский форк dtc с ufdt/overlay; подтверждено живым логом
android.googlesource.com/platform/external/dtc). Прекомпил непереносим между архитектурами хоста.

**Пробованные варианты:**
- P1 `$(objtree)/scripts/dtc/dtc` (нативная сборка из исходников дерева) — FAIL: старая грамматика 1.4.x [V]
- P2 `dtc_overlay_aarch64` из Anonym3310/AkameKernel-begonia Q-OSS-SLMK (собственное решение владельца
  времён телефонных сборок; aarch64-бинарь, RE-проверен) — WORKS, но прекомпил остаётся прекомплом
- **P3 (АКТИВЕН): `dtc` из PATH** — Ubuntu 24.04 device-tree-compiler = **dtc 1.7.0**, нативный arm64,
  пакетный, современная грамматика. Проверено [V]: begonia.dtb собирается, exit=0, 88 492 B,
  108 варнингов (reg_format в MTK-фрагментах — косметика, трекается в логе сборки, не фатально).

## P-KVM: union-фрагмент дополнен (владелец)
CONFIG_VIRTUALIZATION/KVM/KVM_ARM_HOST/ARM64_VHE — задел под будущие движки Windows-on-phone
(Box64/Wine, FEX/Hangover, Winlator) и crossvm.

## Логи сборки
build-logs/ (в контейнере /halium-build/build-logs/) — полный stdout каждого билда + счётчик варнингов.
