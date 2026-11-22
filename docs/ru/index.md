# Каталог исследований — русский язык

**[Русский](index.md) · [English](../en/index.md)** · [Главная по-русски](overview.md) · [Главная международная](../../README.md)

Здесь можно **искать по-русски**, даже если исходный технический отчёт был написан на английском. В каждой строке ниже есть русскоязычное название и объяснение назначения, а ссылка ведёт к полному материалу. Точные идентификаторы аппаратных компонентов, исходников, Git-веток и ошибки намеренно остаются без перевода.

**Важно:** русские названия и аннотации пока не равны полному переводу всех английских глав 00–18. Главы 19–22 изначально написаны по-русски и доступны полностью. Статус каждого перевода — [i18n/catalog.json](../../i18n/catalog.json).

## Android и прошивки

| Глава | Что можно найти | Документ |
|---|---|---|
| **00** | Общая картина: аппаратная платформа, главные результаты исследования, риски и задачи | [Общий отчёт — оригинал EN](../en/research/00-README.md) |
| **01** | Откуда взяты сведения: ссылки на форумы, GitHub, даты, достоверность | [Источники — EN](../en/research/01-SOURCES.md) |
| **02** | MIUI по регионам, CFW и Non-CFW, GSI, Android 9–16, каталог кастомных систем | [История прошивок — EN](../en/android/02-FIRMWARE-HISTORY.md) |
| **10** | Инструкции из 4PDA и XDA, архивные копии, восстановление, работа с recovery | [Указатель инструкций — EN](../en/android/10-GUIDE-INDEX.md) |
| **11** | Происхождение драйверов, закрытых HAL и firmware, vendor blobs, сборочные инструменты | [Драйверы и исходники — EN](../en/kernels/11-BLOBS-FIRMWARE-SOURCES.md) |
| **19** | **Полный словарь CFW, Non-CFW, GSI, Android/Halium, vendor, preloader** | **[19 — полный русский текст](android/19-ROM-TERMS-GLOSSARY-RU.md)** · [English](../en/android/19-rom-terminology.md) |

## Ядра Linux и аппаратная поддержка

| Глава | Что можно найти | Документ |
|---|---|---|
| **03** | Линейки ядер 4.14/4.19, MiCode, LineageOS MT6785, связанные форки, Linux 6.x/7.x | [История ядер — EN](../en/kernels/03-KERNEL-HISTORY.md) |
| **04** | Экраны Tianma/CSOT, тач, GPU, Wi-Fi, камеры, микрофон, датчики, зарядка и их поддержка | [Матрица оборудования — EN](../en/kernels/04-HARDWARE-DRIVERS.md) |
| **05** | Ubuntu Touch 24.04, Halium 10, ошибки, сборка, микрофон и OTA | [Ubuntu Touch — EN](../en/linux/05-UBUNTU-TOUCH.md) |
| **06** | Droidian, postmarketOS, mainline-based ядра и что уже работает на реальном телефоне | [Сравнение Linux-портов — EN](../en/linux/06-DROIDIAN-POSTMARKETOS.md) |
| **08** | Приоритеты разработки Ubuntu Touch, экспериментального 4.19 и современного Linux | [Дорожная карта — EN](../en/linux/08-DEVELOPMENT-ROADMAP.md) |
| **14** | Какие драйверы отсутствуют в mainline, DTS, Wi-Fi, Audio и возможные пути исправления | [Переход к mainline — EN](../en/kernels/14-MAINLINE-UPGRADE-PATH.md) |
| **20** | **Исходники KernelSU, Non-KSU, KSU-Next, SukiSU, APatch, точные ветки 4.19** | **[20 — полный русский текст](kernels/20-KERNEL-419-ROOT-ECOSYSTEM-RU.md)** · [English summary](../en/kernels/20-kernel-root-ecosystem.md) |
| **23** | **Разработчик @Saikrishna1504, работающий Linux 4.19, источники, дата и запрос на патчи** | **[23 — двуязычное исследование и сообщение для автора](../en/research/23-419-TELEGRAM-OUTREACH.md)** |
| **24** | **Дерево устройства begonia, патчи Linux 4.19, аудио, IMS/VoWiFi, камера и firmware от Saikrishna1504** | **[Русский подробный конспект](research/24-saikrishna-source-audit.md)** · [английский полный отчёт](../en/research/24-SAIKRISHNA1504-DEVICE-STACK-AUDIT.md) |
| **22** | **Как перенести 4.14 → 4.19 → 6.x с ИИ, Ghidra и REA; Google Play Integrity** | **[22 — полный русский текст](kernels/22-KERNEL-FORWARD-PORT-AI-INTEGRITY-RU.md)** · [English summary](../en/kernels/22-kernel-forward-port.md) |

## Автономная разработка и отладка ядра (исследовательский проект)

| Тема | Документация |
|---|---|
| Kernel Lab: сохранение первого сбоя, recovery, SD-карта, USB без перевтыкания, Kconfig, UART | **[Подробный русский конспект](tools/kernel-lab-autonomous-debugging.md)** · [Полная архитектура EN](../en/tools/kernel-lab-autonomous-debugging.md) — **пока проект, а не испытанная система** |
| Инвентаризация ADB/Fastboot и USB на Mac | [Пошаговая инструкция EN](../en/tools/kernel-lab-macos-inventory.md) |
| Готовое безопасное задание для агента | [Agent Mission EN](../en/tools/kernel-lab-agent-mission.md) |

## Root, безопасность и инструменты разработки

| Глава | Что можно найти | Документ |
|---|---|---|
| **07** | Разблокировка, BROM/mtkclient, TWRP и OrangeFox, безопасные резервные копии | [Восстановление и безопасность — EN](../en/recovery/07-RECOVERY-SAFETY.md) |
| **26** | **Каталог TWRP, PBRP, OrangeFox, UBports Recovery: официальные и неофициальные сборки** | **[Русский конспект](recovery/recovery-projects-begonia-2026.md)** · [полный английский отчёт](../en/recovery/recovery-projects-begonia-2026.md) · [CSV](../../data/matrices/recovery-matrix.csv) |
| **09** | Неизвестные компоненты, конфликты сведений, что нужно перепроверить | [Открытые вопросы — EN](../en/research/09-OPEN-QUESTIONS.md) |
| **12** | Используемые инструменты, AI-агенты, автоматизация исследования | [Инструменты и навыки — EN](../en/tools/12-SKILLS-AND-REUSE.md) |
| **13** | NetHunter, режим мониторинга Wi-Fi, USB Gadget и функциональность ядер | [Сетевые эксперименты — EN](../en/android/13-NETHUNTER-WIFI-EXTRAS.md) |
| **15** | План обратной разработки, анализ бинарных прошивок, сравнение HAL и драйверов | [План reverse engineering — EN](../en/linux/15-RE-IMPROVEMENT-PLAN.md) |
| **16** | Magisk, KernelSU, APatch, способы получения root и риски | [Способы root — EN](../en/android/16-ROOT-METHODS.md) |
| **17** | Проверка достоверности информации о прошивках и recovery | [Независимый аудит — EN](../en/research/17-INDEPENDENT-AUDIT.md) |
| **18** | Команды ADB/Fastboot только для чтения, инвентаризация неизвестной прошивки | [Безопасная диагностика — EN](../en/recovery/18-DEVICE-PREFLIGHT-READONLY.md) |
| **21** | **NoMount, OverlayFS, Magic Mount, Mountify, SUSFS, Hybrid Mount** | **[21 — полный русский текст](kernels/21-NOMOUNT-MOUNT-BACKENDS-RU.md)** · [English summary](../en/kernels/21-nomount-and-mount-backends.md) |

## Удобный поиск для людей и ИИ

Ищите одновременно по русскому и английскому эквиваленту. Например: **«загрузчик / bootloader / preloader»**, **«ядро / kernel / Linux 4.19»**, **«микрофон / microphone / audio routing»**, **«подмена файлов / systemless / NoMount»**.

Для поиска по индексам используйте [двуязычный машинный указатель](../../i18n/topics.json). Таблицы с исходниками: [прошивки](../../data/matrices/firmware-matrix.csv), [ядра](../../data/matrices/kernel-matrix.csv), [аппаратная поддержка](../../data/matrices/hardware-support-matrix.csv). Для каждого найденного факта проверяйте первоисточник в [sources.json](../../data/catalog/sources.json) и его дату.

[Требования к профессиональному переводу](../../i18n/README.md) · [Технический глоссарий EN↔RU](../../i18n/TERMINOLOGY.md). Нельзя автоматически объявлять текст «полностью переведённым», если часть разделов, таблиц, ссылок или оговорок отсутствует.

## Сверка исходников ядер и прошивок (2026)

[Проверенные Git-коммиты и версии Linux 4.14/4.19 — английский исследовательский оригинал](../en/research/begonia-kernel-and-rom-evidence-2026-11.md). Русский тематический маршрут пока ведёт к англоязычной статье; полный перевод не заявлен.
