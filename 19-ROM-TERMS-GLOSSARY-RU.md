# 19 — Словарь прошивок и архитектуры Redmi Note 8 Pro (begonia)

> Простое объяснение терминов из 4PDA/XDA и технических отчётов проекта. Аудит источников: 2026-11-21. Это справочник, **не инструкция по прошивке**. Все примеры относятся к Xiaomi Redmi Note 8 Pro (MT6785, `begonia`/`begoniain`), если не указано иное.

## 0. Главное за 30 секунд

**Не существует одной линейки «CFW → Non-CFW → GSI → Linux», где каждый следующий тип новее и лучше.** Эти названия описывают *разные свойства* системы:

| Вопрос | Варианты | Смысл |
|---|---|---|
| Кто и на какой базе собрал Android? | Xiaomi MIUI (stock), native AOSP/Lineage/crDroid, OEM port, GSI | Происхождение системного образа и степень адаптации |
| Какая низкоуровневая схема нужна? | Ранняя begonia CFW или Non-CFW/штатная совместимая база | Историческая схема загрузчиков, vendor и совместимости |
| Что в нижних слоях? | Android kernel+HAL, Halium+libhybris, native/mainline Linux | Ядро и способ доступа к аппаратуре |
| Какая версия *чего*? | Android 16, MIUI 12.5/Android 11 vendor, Linux 4.14 или 6.16, Ubuntu Touch 24.04 | Четыре **независимых номера**; не переносить их друг на друга |

**Типичная ошибка:** «ROM на Android 16 — значит ядро Linux 6.x и драйверы 2026 года». Нет: Android userspace, vendor blobs и версия ядра могут быть из принципиально разных поколений. [02 §1.3 и §4](02-FIRMWARE-HISTORY.md), [03](03-KERNEL-HISTORY.md), [11](11-BLOBS-FIRMWARE-SOURCES.md).

## 1. Историческая классификация 4PDA (begonia-specific)

### CFW (Custom Firmware, в сообществе begonia)

**Простыми словами:** старый технический способ адаптации кастомных ROM к Redmi Note 8 Pro, когда сочетали низкоуровневые компоненты разных поколений Android/MIUI и использовали **factory / engineering preloader + LK**. Целью было дать возможность загрузить кастомную систему и облегчить восстановление аппарата в условиях ограничений тех лет.

Это **не** синоним любого кастомного Android, не просто root/Magisk, не особый пользовательский интерфейс и не открытый код всего устройства.

- История от разработчика Kshitij Gupta: [“Modding the Redmi Note 8 Pro — An Adventure”](https://medium.com/swlh/modding-the-redmi-note-8-pro-an-adventure-e473e84d4d14) — смешивание Android 9/10 firmware и использование factory preloader/LK для исторического CFW-проекта.
- Объяснение куратора темы TTTT555 (10.02.2021, посты около #7212–7214): [4PDA, страница с объяснением CFW/Non-CFW/GSI](https://4pda.to/forum/index.php?showtopic=974421&st=7200). Смысл: CFW — сочетание старых и новых драйверов, адаптированное под утёкший сервисный preloader. [V-search: поисковая индексация видит сообщение; прямое открытие страницы в среде ревьюера даёт HTTP 403; R: Hermes сохранил снапшоты форума].
- [XDA CFW Megathread](https://xdaforums.com/t/guide-info-psa-redmi-note-8-pro-megathread-cfw.4056527/), в репозитории есть архивные и Brave-копии (см. `archive/` и `_cache/`).

**Статус:** историческая/устаревшая линия; в шапке 4PDA ныне отнесена к устаревшим прошивкам. **Риск:** неподходящие LK/preloader/boot/dtbo/vbmeta могут полностью заблокировать загрузку; возвращение со старого CFW требует индивидуально проверенного пути. «CFW» не означает «гарантированно безопасно».

### Non-CFW

**Простыми словами:** современные для сообщества begonia кастомные Android ROM, адаптированные к обычной заводской загрузочной базе (без требований старого CFW-набора engineering preloader/LK). Это **не** означает, что в системе «нет firmware».

- Куратор TTTT555 назвал Non-CFW потомками CFW, приспособленными к более поздним штатным загрузчикам, с унификацией recovery и более удобной установкой: [4PDA](https://4pda.to/forum/index.php?showtopic=974421&st=7200).
- Современная [шапка 4PDA 974421](https://4pda.to/forum/index.php?showtopic=974421) прямо помечает Non-CFW как стандартные кастомные прошивки и выделяет их как актуальную категорию.
- Внимание: Non-CFW **не гарантирует** совместимости с любым vendor, recovery или ядром. Шапка отдельно разделяет MIUI 11/12 Android 10 vendor-base и MIUI 12.5 Android 11 vendor-base. См. [02 §1.3](02-FIRMWARE-HISTORY.md), [10 §2](10-GUIDE-INDEX.md).

### GSI (Generic System Image)

**Простыми словами:** универсальный системный Android-образ на основе [Project Treble](https://source.android.com/docs/core/architecture/treble), а не сборка, обязательно специфичная для begonia.

- При типичной установке GSI меняют системный слой, а существующие vendor и ядро остаются; иногда нужны отдельные vendor-патчи, vbmeta-настройки и другие изменения. Это не гарантия «меняется только system» для каждого стороннего ZIP.
- GSI **не противоположность** Non-CFW: один термин про универсальность `system`, другой — про историческую низкоуровневую базу begonia.
- [Официальное определение Google](https://developer.android.com/topic/generic-system-image) и [02 §2](02-FIRMWARE-HISTORY.md): ранние GSI для begonia сталкивались с проблемами звука, связи и анимаций.
- Не путать **Android GSI** с **Halium GSI** в документации UBports: это разные образы/окружения, хотя оба используют идею универсального системного слоя.

### «Другое» на 4PDA

Это **категория каталога форумной темы**, а не независимый формат firmware. В шапке собраны GSI и родственные варианты, Linux/UEFI и необычные сборки по отдельным рубрикам. Название раздела само по себе ничего не говорит о совместимости со штатным preloader.

## 2. Виды Android-систем: независимая ось классификации

| Термин | Суть | Пример/оговорка |
|---|---|---|
| **Stock / MIUI / factory ROM** | Система и фирменные образы Xiaomi для конкретного региона/варианта | Заводская база для отката; последние линии begonia — MIUI 12.5 / Android 11 [02 §1](02-FIRMWARE-HISTORY.md) |
| **Custom ROM** | Любая сторонняя модифицированная Android-система; широкое слово | Может быть CFW, Non-CFW, device-specific или GSI-derived |
| **Native ROM / device-specific build** | Android собран с адаптациями именно для `begonia`: device tree, vendor configuration, kernel | Например, [crDroid для begonia](https://crdroid.net/begonia) (конкретные ветки и доступность — [02 §7.4](02-FIRMWARE-HISTORY.md)) |
| **AOSP** | Android Open Source Project, исходная открытая платформа Android | Не равен «все драйверы открыты» |
| **LineageOS-based / crDroid / Evolution X** | Различные проекты пользовательской системы на Android; имя проекта не определяет vendor/kernel поколения | Важен **конкретный build** и его manifest/device/kernel/vendor refs |
| **OEM port** | Перенесённая с другого производителя/устройства фирменная Android-оболочка | Например, OriginOS, ColorOS, EMUI, ROGUI; больше закрытых компонентов и совместимость не гарантирована — [02 §3.7](02-FIRMWARE-HISTORY.md) |
| **GSI-based adaptation** | GSI, дополненная устройственно-специфическими патчами | Может быть визуально похожа на native ROM, но сборочная архитектура другая |

**OFFICIAL/UNOFFICIAL** в названии конкретной ROM означает признание **её собственного проекта**, а не Xiaomi, Android или LineageOS. «Official AxionOS» и «official crDroid» — разные статусы разных команд. `OFFICIAL` в 4PDA-посте перепроверять по сайту самой ROM.

**Vanilla / GApps:** сборка без предустановленных сервисов Google / с ними. **OSS:** open-source components или тег ветки исходников (например `Q-OSS`/`R-OSS`); **не** свидетельство полностью открытых драйверов. **Root, Magisk, KernelSU, APatch:** способы изменить привилегии/ядро, не самостоятельный тип ROM.

## 3. Четыре слоя устройства: самая важная модель для porting

```text
[ПРИЛОЖЕНИЯ И UI]
Android 16 / MIUI / crDroid
или Ubuntu Touch 24.04 / Droidian / postmarketOS
          ↓
[СИСТЕМНЫЕ СЛУЖБЫ И HARDWARE API]
Android HAL и vendor blobs; через Halium/libhybris — в Linux-портах
или нативные Linux-драйверы и userspace
          ↓
[ЯДРО + DEVICE TREE / DTBO]
Например, Linux 4.14.x (Android vendor/Halium)
или порт Linux 6.16.x/новее на MT6785
          ↓
[BOOT CHAIN + НИЗКОУРОВНЕВАЯ FIRMWARE]
BROM → preloader → LK → kernel; vbmeta/AVB, модем, PMIC,
контроллер экрана/тача и прочие бинарные прошивки
```

### `firmware` — перегруженное слово

1. **«Прошивка телефона»** в разговоре: весь ROM/системное окружение.
2. **Firmware bundle / firmware package** на Xiaomi: набор низкоуровневых образов модема, загрузчиков, DSP, доверенного окружения и т.п., иногда предлагаемый отдельно от полной MIUI.
3. **Peripheral firmware**: микрокод Wi-Fi, BT, тачскрина, DSP и т.п., который загружается при запуске устройства/драйвера.
4. **Vendor blobs / vendor.img**: закрытые HAL-библиотеки, параметры, иногда прошивки периферии; это **не** весь firmware-пакет и не всё ядро.
5. **Kernel source / kernel image**: код и собранное ядро Linux. Условные `Q-OSS` и `R-OSS` связаны с поколениями исходников Xiaomi Android 10/11 (сопоставление в [03 §1](03-KERNEL-HISTORY.md)), но OSS-тег **не** гарантирует отсутствие закрытых модулей или совместимость с любой Android 16 ROM.

**Следствие:** «поставить последние драйверы» нельзя одной операцией. Нужно установить, какой компонент живёт в каком разделе, кому принадлежит его интерфейс и совместимы ли ядро, HAL, DTB/DTBO, прошивки модема и пользовательская система.

## 4. Linux-порты не обязаны иметь Android userspace

| Порт | ОС пользователя | Как работает железо | Плюсы / текущие ограничения |
|---|---|---|---|
| [Ubuntu Touch begonia](https://devices.ubuntu-touch.io/device/begonia/) | Ubuntu Touch 24.04 | **Halium 10** и Android-vendor ядро (4.14.141) + proprietary HAL | Очень многое работает; официальный статус говорит, что микрофон записи не работает; VoLTE экспериментален |
| [Droidian begonia](https://github.com/begonia-linux/adaptation-xiaomi-begonia) | Linux / Droidian | Android-derived kernel + libhybris / vendor | В README портера микрофон работает, полезно как эталон для UT; не независимая аппаратная проверка |
| [postmarketOS begonia](https://wiki.postmarketos.org/wiki/Xiaomi_Redmi_Note_8_Pro_(xiaomi-begonia)) | Alpine-based mobile Linux | Mainline-**based fork** для MT6785 + открытые драйверы | Больше свободы, но по [06](06-DROIDIAN-POSTMARKETOS.md) всё ещё отсутствует целый ряд функций (связь, камера, аудио и пр.) |

**Halium 10 ≠ Ubuntu Touch 10 ≠ Android 10 в интерфейсе пользователя.** Halium 10 обозначает поколение аппаратной совместимости (Android 10 vendor interface); запущенная система при этом может быть Ubuntu Touch 24.04.

**Mainline-based fork ≠ upstream Linux support.** Ядро из ветки Dinolek/MT6785 может быть основано на новой Linux-версии и содержать устройство-specific изменения, ещё не включённые в официальное дерево Linux. См. [03 §4](03-KERNEL-HISTORY.md), [14](14-MAINLINE-UPGRADE-PATH.md).

## 5. Загрузчики и специальные разделы — кратко

| Термин | Назначение |
|---|---|
| **BROM / BootROM** | Встроенный загрузочный код MediaTek SoC; один из путей аварийного восстановления при поддерживаемой конфигурации |
| **Preloader** | Ранняя инициализация платформы/памяти/USB; чрезвычайно чувствителен к несовместимой замене |
| **LK / Little Kernel** | Следующий этап загрузки; может выполнять проверку и выбор режима |
| **Fastboot** | Протокол связи с загрузчиком для чтения сведений и записи разделов, **не** сам ROM |
| **Recovery (TWRP/OrangeFox/PBRP)** | Отдельная среда обслуживания/установки; **важна совместимость конкретной версии** с текущим ROM/vendor/encryption/layout |
| **boot.img** | Обычно ядро + загрузочные данные/ramdisk (состав зависит от поколения Android) |
| **dtb / dtbo** | Device Tree — аппаратное описание платы/панели/питания и его overlays |
| **vbmeta / AVB** | Метаданные Android Verified Boot; неверная конфигурация может сорвать загрузку |
| **NVRAM / NVDATA / persist** | Уникальные калибровки и настройки конкретного устройства; хранить только приватно |
| **OTA** | Обновление системы поверх сети; не гарантирует обновление низкоуровневых драйверов/boot chain |
| **Treble / VNDK** | Разделение Android system и vendor с определёнными интерфейсами совместимости |

Дополнительно: **A-only / A/B** — схема слотов обновления, **dynamic partitions / super** — способ разметки логических системных разделов; ни одна из этих характеристик автоматически не следует из номера Android. Фактическую структуру begonia проверять на устройстве, а не переносить инструкцию от другого телефона.

## 6. Частые опасные заблуждения

1. **«Android 16 = драйверы Android 16»** — неверно. ROM может использовать MIUI 12.5/Android 11-era vendor и старую ветку Linux.
2. **«Non-CFW = без firmware»** — неверно. Non-CFW означает отсутствие требований **старой CFW-схемы**.
3. **«GSI — более новая Non-CFW»** — неверно; GSI описывает универсальность system, а Non-CFW — платформенную совместимость begonia.
4. **«Версия ОС = версия Linux-ядра»** — неверно: Ubuntu Touch 24.04 работает на Linux 4.14, если порт построен на Halium 10.
5. **«Есть официальная страница recovery, значит бинарник новый и подходит к Android 16»** — неверно. См. [17-INDEPENDENT-AUDIT.md](17-INDEPENDENT-AUDIT.md), отдельную ветку [PR #1](https://github.com/0-danielviktorovich-0/begonia-research/pull/1): сайт TWRP обновлён в 2026, а официальный последний образ датируется 2022; OrangeFox begonia официально не поддерживается, последний перечисленный beta рассчитан на CFW.
6. **«mtkclient всегда гарантирует unbrick»** — неверно: зависит от конкретного аппаратного/программного состояния и сохранённых заводских данных.
7. **«Достаточно включить CONFIG_… в ядре»** — неверно: для реального драйвера также нужны DT nodes/pinctrl/regulators, firmware, совместимый интерфейс и userspace. Подробно в [14 §0](14-MAINLINE-UPGRADE-PATH.md).
8. **«OSS = все драйверы открыты»** — неверно: vendor blobs могут остаться проприетарными.
9. **«Mainline fork = полностью upstream ядро»** — неверно; проверить, какие MT6785-патчи реально попали в kernel.org.

## 7. Как разбирать одну конкретную прошивку из каталога

**Вместо одной надписи “Non-CFW Android 16” заполнять:**

```yaml
name: "пример, не реальный проверенный билд"
kind: "native device-specific / GSI / OEM-port / Linux-port"
cfw_era_compat: "CFW / Non-CFW / n-a / unknown"
android_userspace: "unknown"
halium_generation: "n-a or version"
vendor_base: "MIUI branch + fingerprint/hash or unknown"
firmware_bundle: "build + region + hashes or unknown"
kernel: "version + tree + exact commit or unknown"
boot_chain_requisites: "documented only / unknown"
recovery_compat: "exact image + source + tested or unknown"
panel_revision: "Tianma / CSOT / unknown"
source_url: "link to original build post"
source_code: "kernel/device/vendor/manifest, missing explicitly"
tested_device: "begonia/begoniain; hardware revision"
verified_on_device: false
```

For a true image, never fill unknowns by copying data from a nearby ROM name or a newer OS release date.

### Что выбрать для нашего проекта

- **Первая практическая линия:** проверенная Ubuntu Touch 24.04/ Halium 10; фиксы звука, микрофона, RTC, сна и стабильности.
- **Референс драйверов:** Droidian и соответствующие Android device/vendor/kernel trees; сравнение работающего микрофона.
- **Отдельная экспериментальная линия:** postmarketOS с MT6785 mainline-based fork, сначала питание, Wi-Fi, audio, затем модем/камера.
- **Сервисная линия:** ровно один идентифицированный штатный комплект Xiaomi для конкретной региональной модели, резервные копии NVRAM/NVDATA и проверенный recovery path. Никаких случайных «обновлений на последний vendor» без ABI-анализа.

## Основания и пределы проверки

- [Пост TTTT555 на 4PDA (индексируемая страница, 2021)](https://4pda.to/forum/index.php?showtopic=974421&st=7200); прямое открытие в этой среде — 403, использована индексация поисковика; Hermes ранее сохранил выборочные страницы и посты.
- [Страница прошивок 4PDA (актуальная шапка)](https://4pda.to/forum/index.php?showtopic=974421); кеш и поисковые выдержки.
- [XDA Megathread](https://xdaforums.com/t/guide-info-psa-redmi-note-8-pro-megathread-cfw.4056527/), архивные копии в `archive/` и `_cache/`.
- [Kshitij Gupta, historical CFW engineering article](https://medium.com/swlh/modding-the-redmi-note-8-pro-an-adventure-e473e84d4d14).
- [Android Developers: GSI](https://developer.android.com/topic/generic-system-image), [UBports: Introduction to porting](https://docs.ubports.com/en/latest/porting/introduction/Intro.html), [UBports begonia feature matrix](https://devices.ubuntu-touch.io/device/begonia/).
- Развернутые аппаратные и version-specific сведения лежат в [02](02-FIRMWARE-HISTORY.md), [03](03-KERNEL-HISTORY.md), [05](05-UBUNTU-TOUCH.md), [06](06-DROIDIAN-POSTMARKETOS.md), [07](07-RECOVERY-SAFETY.md) и [11](11-BLOBS-FIRMWARE-SOURCES.md).

**Достоверность:** высокая для общих определений и первичных руководств Google/UBports; высокая для того, как в 2021 году куратор сообщества определял CFW/Non-CFW, но прямой доступ к его сообщению в этой среде ограничен 403; рабочая пригодность конкретных ROM/recovery **не проверялась на устройстве**. Сведения привязаны к опубликованным источникам, не служат гарантией успешной прошивки.
