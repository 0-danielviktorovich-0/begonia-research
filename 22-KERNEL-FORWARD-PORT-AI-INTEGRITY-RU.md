# 22 — От Linux 4.14 к 4.19, далее к 6.x/7.x: инженерный план и пределы AI-портирования; Android root vs платежи

**Дата независимой проверки:** 2026-11-21. Устройство: Xiaomi Redmi Note 8 Pro (begonia, MT6785). **Это исследование исходников и документации, а не проверка на телефоне пользователя**. Ссылки на связанные отчёты: [03-KERNEL-HISTORY.md](03-KERNEL-HISTORY.md), [14-MAINLINE-UPGRADE-PATH.md](14-MAINLINE-UPGRADE-PATH.md), [20-KERNEL-419-ROOT-ECOSYSTEM-RU.md](20-KERNEL-419-ROOT-ECOSYSTEM-RU.md), [21-NOMOUNT-MOUNT-BACKENDS-RU.md](21-NOMOUNT-MOUNT-BACKENDS-RU.md).

## 1. Linux 4.14 → 4.19: что означает перенос на деле

**Нельзя получить функциональный 4.19, изменив цифры `VERSION`, `PATCHLEVEL`, `SUBLEVEL` в Makefile.** В MT6785 существовали разные кодовые базы, собранные под разные Android-устройства. Практически важны три **разных** операции:

1. **Stable backport внутри 4.14:** Xiaomi выпустила несколько snapshot-веток 4.14.x для begonia, затем сообщество поднимало stable sublevel и переносило выборочные bugfix/security patches. Ядро *остаётся* 4.14 с vendor ABI.
2. **Межветочный vendor forward-port (4.14→4.19):** взять MediaTek/Android **4.19**-базу, в которой уже реализован похожий MT6785/Helio G95, адаптировать begonia board-DTS, дисплей, сенсоры, зарядку, audio codec, radio/camera interfaces, конфигурации и toolchain; переносить недостающие патчи по одному, согласовывая Linux API. Источники MT6785/rosemary полезны **как эталон, но не готовая загрузочная сборка begonia**.
3. **Mainline-based forward-port (6.x/7.x):** перенести/переписать SoC/board support на современном Linux — clock controller, pinctrl, PMIC, DRM, USB, UFS, Wi-Fi, audio, camera, modem. Нужна совместимая Linux userspace-сторона; Android proprietary HAL автоматически не совместим с современным mainline. Для долговременного результата предпочтительны upstream style/DTS bindings и минимальные out-of-tree patches.

### Подтверждённые исходники для первых двух пунктов

- [MiCode/Xiaomi_Kernel_OpenSource](https://github.com/MiCode/Xiaomi_Kernel_OpenSource) P/Q/R begonia 4.14.xx (значения и ветки в [03 §1](03-KERNEL-HISTORY.md)).
- [Saikrishna1504/kernel_xiaomi_mt6785](https://github.com/Saikrishna1504/kernel_xiaomi_mt6785) `main`: Makefile **4.14.357-openela**. Более высокий sublevel 4.14 **не** значит 4.19.
- [LineageOS/android_kernel_xiaomi_mt6785](https://github.com/LineageOS/android_kernel_xiaomi_mt6785) `lineage-24.0` и [xiaomi-mt6785-dev/android_kernel_xiaomi_mt6785](https://github.com/xiaomi-mt6785-dev/android_kernel_xiaomi_mt6785) `lineage-24.0`: Makefile **4.19.325**, один и тот же наблюдаемый Git HEAD **`30485853fa89`** на 2026-11-21.
- **Важная граница:** в этом 4.19 дереве найдены `arch/arm64/configs/rosemary_defconfig`, `arch/arm64/boot/dts/mediatek/rosemary.dts` и ссылки на `rosemary`; GitHub code search по этому дереву на слово `begonia` не дал совпадений. Следовательно, **оно не признано готовым begonia kernel**. [rosemary_defconfig](https://github.com/xiaomi-mt6785-dev/android_kernel_xiaomi_mt6785/blob/lineage-24.0/arch/arm64/configs/rosemary_defconfig), [rosemary.dts](https://github.com/xiaomi-mt6785-dev/android_kernel_xiaomi_mt6785/blob/lineage-24.0/arch/arm64/boot/dts/mediatek/rosemary.dts). Отрицательный результат поиска не исключает неиндексированные файлы; лучше подтвердить локальным полным git tree diff.
- Комьюнити автор сообщил в [публичном Redmi Note 8 Pro Updates Telegram](https://t.me/s/RedmiNote8ProUpdates) осенью 2026, что **портировал 4.19 и тестировал 1–2 недели**. **Это developer self-report [D], а не независимая валидация**: в найденном сообщении нет привязанного sha kernel tree + образа + полного списка hardware-test результатов; дата сообщения зависит от зеркала, ориентир сентябрь 2026.

### Как доказать, что «4.19 для begonia работает»

Необходима полная цепочка **исходный commit SHA → defconfig/DTS → vendor/firmware-base → boot.img/DTBO → проверенный результат на физическом begonia**. Минимальные отчёты: `uname -a`, лог kernel panic/dmesg, USB ADB, LCD panel (Tianma/CSOT), touch, зарядка, suspend/resume, audio/mic, телефонная связь, камера, GPS, Wi-Fi/BT, NFC, update/recovery. **Без этой цепочки исходник 4.19 для MT6785 может относиться преимущественно к rosemary.**

### Сборка портируемой ветки: технические шаги (без прошивки)

1. Зафиксировать исходный begonia 4.14 tree/commit, итоговый rosemary/MT6785 4.19 tree/commit, соответствующие Android vendor images, SOC revision, panel.
2. Сравнить `arch/arm64/boot/dts/mediatek`, drivers/misc/mediatek, input/touch, display DRM, clk, regulator, thermal, charger, Wi-Fi/BT, audio and camera sensor sources. Составить **матрицу эквивалентов driver + DTS nodes + firmware**. Не копировать целый каталог старого 4.14 поверх 4.19.
3. Для переноса идти по подсистемам: clocks + pinctrl + PMIC → UFS/USB/console → display/touch → suspend/charging → wireless → audio → camera/modem. Сначала компиляция и bootlogs, потом реальное тестирование.
4. Обновить Linux API (таймеры, DMA/IOMMU, regulator/clock, DRM/media API, VFS, cfg80211/BT и vendor Android binder) и адаптировать DTS/bindings. Не смешивать одновременное обновление ядра/Android vendor/baseband/root framework.
5. Для Android-совместимости проверить Android boot header, AVB/vbmeta, vendor modules/KMI, Binder, ashmem alternatives, SELinux, MediaTek HAL и init. Linux 4.19 не обещает работу с Halium10 просто по номеру ядра.
6. Для каждого патча записывать `source URL`, parent commit, patch, license/redistribution, compile outcome, hardware test outcome, rollback plan. Собрать две базовые конфигурации без root и с root, если Android root вообще нужен.

## 2. Переход на современный mainline-based Linux — уже есть задел

Исследование [14-MAINLINE-UPGRADE-PATH.md](14-MAINLINE-UPGRADE-PATH.md) фиксирует [Dinolek/mt6785-mainline](https://github.com/Dinolek/mt6785-mainline) с форками на 6.16/7.1 и [kalpakprod/mt6785-linux](https://github.com/kalpakprod/mt6785-linux) на Linux 7.3.4. «Основано на mainline» **не означает** включение изменений MT6785 в `torvalds/linux`: поддержка SoC в этих форках остаётся out-of-tree, как объяснено в [03 §4](03-KERNEL-HISTORY.md).

### Новое важное уточнение: Wi-Fi уже доказательно запущен в сторонней mainline-based сборке

[criollojoel10/begonia-pmos-tianma README](https://github.com/criollojoel10/begonia-pmos-tianma/blob/main/README.md) [V, читаемый source и авторский отчёт] **утверждает испытание на физическом begonia 27 сентября 2026 года** с **Linux 6.16.4**, MediaTek vendor wireless modules `mtk-vendor-btif` + `wmt_drv` + `wlan_gen4m`, и корректным комплектом `WMT_SOC.cfg`/firmware. По логам автора создаётся `wlan0`, обнаруживаются сети 2.4/5 GHz, получаются DHCP, DNS, ping, HTTPS; приложены boot/build traces и проектные конфигурации. Это **авторская проверка [D], не тестировалась независимым ревьюером на устройстве пользователя**, и **не является upstream поддержкой WLAN через чистый mt76**. Остальные mainline / чистые pmOS сборки могут иметь Wi-Fi broken.

**Вывод:** не повторять безоговорочно в [00](00-README.md)/[04](04-HARDWARE-DRIVERS.md)/[06](06-DROIDIAN-POSTMARKETOS.md) «никакая mainline begonia сборка не имеет Wi-Fi». Правильно: **базовая Dinolek/Nura-матрица сообщала об отсутствии Wi-Fi**, но сторонний пакет от criollojoel10 демонстрирует **частично/практически работоспособную vendor-driver-based WLAN интеграцию**. Для upstream mt76 путь отдельный, с определением фактического RF chip ID и SDIO/power sequencing. Vendor wireless stack также не равен полностью открытым драйверам.

Это прекрасный пример гибридной техники: **современное ядро + перенос устаревшего MTK-драйвера + firmware + systemd/scripts + реальные логи**. Он особенно полезен как образец работы для AI-агентов.

## 3. Как ускорить работу с AI и REA / RIA

Под REA здесь понимается **Reverse Engineer Anything** в доступных репозиториях (например, [axpie/reverse-engineer-anything](https://github.com/axpie/reverse-engineer-anything)). Названий и форков много; **источник установленного пользователем skill не подтверждён** — перед установкой проверить авторство, лицензии, подписи/хеши и реальные разрешения. AI+Ghidra/REA отлично помогает с **исследованием**, но без платных закрытых SDK нельзя гарантировать полнофункциональные modem/camera HAL.

**Что AI способен автоматизировать с высокой практической пользой:**

- Соотнесение старых и новых `struct`, driver callbacks, kernel exported symbols, header API, Kconfig и DTS/bindings; поиск соответствующих upstream backports/patches.
- Генерация маленьких компилируемых изменений (с traceable rationale + tests), анализ build errors, static analysis (`sparse`, `smatch`, `Coccinelle/spatch`, `clang-tidy` where applicable), `dtbs_check`, `dt_binding_check`, `checkpatch.pl`.
- Выявление двоичных интерфейсов vendor HAL: `readelf`, `objdump`, symbol/strings, Ghidra/REA; поиск Android audio routing/GNSS/camera tuning, где нет доступного исходного кода. Следить за лицензией, не публиковать закрытые blobs без прав.
- Сопоставление dmesg/pstore/tracepoints до/после, классификация kernel oops и минимизация патча, auto-bisect с возможностью **реально тестировать** проблемную сборку.
- Реестры `kernel source SHA + feature patch SHA + board + hardware tests` и генерация Markdown/CSV без вымышленных «работает».

**Чего AI не может «додумать» надёжно:** электрические напряжения и reset/power sequencing реальной платы, неизвестную инициализацию secure-world/TEE, калибровки радио, точную ISP/модемную конфигурацию или стабильность sleep/power на реальном устройстве. Нужны измерения, bootlogs, тестирование и иногда аппаратное отладочное оборудование. Угаданный регистр может привести к data corruption и hard-brick. Изменять сразу 4.14→6.x с обновлением vendor/root нецелесообразно.

### Рекомендуемая архитектура трех веток работы

1. **Stable UT/Halium10** — инженерные фиксы микрофона/питания/OTA, приоритет ежедневного использования.
2. **4.19 Android/Halium experiment** — **только когда найдены точные begonia-specific changes и подтверждены hardware tests**, сравнение 4.14↔4.19 на одной vendor базе.
3. **6.16/7.x mainline-based pmOS experiment** — за основу взять Dinolek + результаты criollojoel10 Wi-Fi, добавлять аудио/зарядку/камера; цель — Linux drivers и upstreamable changes. Смена Linux 7.x не означает улучшения, если теряются рабочие компоненты.

## 4. Root-обнаружение и платежи: что действительно важно

Разные проверки:
1. **Простое приложение** ищет `su`, менеджер, следы `zygisk`, изменённые `mountinfo`, неожиданные процессы/SELinux.
2. **Сложное приложение** проверяет приложения/хуки, окружение, kernel state и root-modification traces, даже если `su` не выдаётся.
3. **Google Play Integrity** выдаёт разные device labels: `MEETS_BASIC_INTEGRITY`, `MEETS_DEVICE_INTEGRITY`, `MEETS_STRONG_INTEGRITY`. На Android 13+ `STRONG` требует hardware-backed signals и достаточно свежих обновлений **OS и vendor**, а `DEVICE` может включать проверку certified manufacturer OS / locked bootloader. [Google official verdicts](https://developer.android.com/google/play/integrity/verdicts); [setup](https://developer.android.com/google/play/integrity/setup).
4. **Google Wallet** отдельно заявляет, что **root, custom ROM или unlocked bootloader могут лишать права на бесконтактные платежи**. [Official Google Wallet support](https://support.google.com/wallet/answer/12200245). Банк вправе применять дополнительные правила независимо от Google.

| Подход | Что в теории меньше выдаёт | Чего не устраняет | Что гарантировано? |
|---|---|---|---|
| **No root + штатный сертифицированный ROM + штатно закрытый bootloader** | Нет root manager, root-hooks, чужих mount-modules; соответствует исходной модели Android security | Возраст штатных обновлений, банк/регион/карта всё ещё важны | **Лучший шанс официальной совместимости, но не безусловная гарантия** |
| **Magisk** | Можно ограничивать права приложений и модификации userspace; удобно поддерживать | Boot/ramdisk/zygisk/mount footprint и bootloader/integrity сигнал | **Нет** |
| **KernelSU / KernelSU-Next** | Контроль доступа на уровне ядра, меньше обязательных init/userspace изменений; профили приложений | Patch самого ядра, root manager, mounts/modules, AVB/boot state | **Нет** |
| **KSU + SUSFS / NoMount / Mountify** | Может уменьшать **отдельные** user-visible mount/metadata fingerprints; конфигурация зависит от форка | Нельзя легально «переключить» аппаратную аттестацию изменённого boot chain настройкой VFS; root/SELinux/kernel/userspace по-прежнему могут быть обнаружены | **Нет** |
| **SukiSU Nova** | Варианты KSU functionality и дополнительных modules/hiding | Ещё больше fork-specific переменных и attack surface | **Нет** |
| **APatch** | Kernel image patch, без полной пересборки tree, меньше традиционных Magisk init следов при некоторых конфигурациях | Modified kernel, bootloader status, detection surface, image matching risk | **Нет** |

**Результат для Redmi Note 8 Pro:** назвать один root-метод, который достоверно **обеспечивает стабильные бесконтактные платежи и работу любого банка на кастомном ROM**, нельзя. Плагины, hiding modules, SUSFS и NoMount не заменяют **сертифицированную загрузку/аппаратную аттестацию**. На Android 13+ официальное `STRONG` и новая vendor security patch на телефоне 2019 года будут особенно сложными; прошивка Android 16 сама по себе **не обновляет firmware/vendor сертифицированным образом**.

**Практически надёжнее:** держать отдельное немодифицированное устройство для платежей или использовать штатную сертифицированную прошивку на полностью совместимом телефоне. Для begonia исследовательские ROM/UT/pmOS и бесконтактные платежи могут потребовать **разных устройств**. **Не релочить** bootloader на модифицированной/чужого региона прошивке ради попытки «пройти проверку» — риск brick.

### Тестировать по слоям, а не «не работает банк — установить 5 скрывающих модулей»

- Узнать Play Protect certification и конкретную ошибку Wallet/банковского приложения; оценивать отдельно app-local root check и server-side Play Integrity.
- Проверить, работает ли обычный NFC-чип/экран оплаты: NFC hardware works ≠ платежный кошелёк authorizes transaction.
- Если root не нужен, не устанавливать его: лучший контрольный тест для проекта — ROM без KSU/Magisk/APatch.
- Логи тестов обезличить; не публиковать банковские данные, токены или устройства с уникальными calibration partitions.

## 5. Проверенные пробелы

- Точное **исходное дерево и полный patchset** заявленного рабочего begonia 4.19 порта неизвестны; не приписывать его автоматически LineageOS rosemary tree.
- Нужны hardware-specific `panel` и питание/пробуждение тесты на разных ревизиях begonia.
- Wi-Fi bridge `wlan_gen4m` из criollojoel10 repo: verify module SHAs and license compliance before upstream/reuse.
- Полное Play Integrity/Wallet поведение на конкретных старых begonia ROM, текущем bootloader state и конкретных банковских приложениях **не тестировалось**.
- Эффективность REA/Ghidra/AI при переносе **конкретного** драйвера зависит от source/ABI/logs и не оценена измерениями.

**Research only; no software installed or executed on a physical phone.**
