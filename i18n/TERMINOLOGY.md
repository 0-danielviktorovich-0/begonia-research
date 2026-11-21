# Controlled technical terminology — English ↔ Русский

**Status:** reviewed seed glossary for i18n/l10n, 2026-11-21. [English index](../docs/en/index.md) · [Русский указатель](../docs/ru/index.md).

Use the **preferred** Russian expression in continuous prose; preserve **English alias, command spelling and original identifiers** at first mention and whenever users are likely to search for them. In commands and file paths never translate the original spelling. This is a controlled term list, not a claim about device compatibility.

| English term / searchable alias | Русский рекомендуемый эквивалент | Правило употребления |
|---|---|---|
| internationalization (i18n) | интернационализация (i18n) | Подготовка проекта к нескольким языкам; не путать с n8n |
| localization (l10n) | локализация (l10n) | Перевод + адаптация терминов, поиска и навигации |
| translation | перевод | Полный перевод отличается от аннотации/краткого обзора |
| source of truth | первоисточник / основной источник фактов | Различать авторский источник и подтверждение независимым тестом |
| kernel | ядро Linux | Версия Android ≠ версия ядра |
| kernel source tree | дерево исходного кода ядра | При первом употреблении добавить «kernel tree» |
| kernel configuration / defconfig | конфигурация ядра / defconfig | Имена CONFIG_* и имена файлов оставлять в оригинале |
| kernel fork | форк ядра | Fork ≠ автоматическая поддержка устройства |
| backport | обратный перенос патча / бэкпорт | Перенос исправления из нового ПО в старую ветку |
| forward-port | перенос на более новую версию | Не называть простым обновлением номера |
| mainline Linux | основная ветка ядра Linux (mainline) | Mainline-based fork ≠ включено upstream |
| upstream | исходный вышестоящий проект / upstream | Не путать с unofficial/community ROM |
| downstream vendor kernel | модифицированное ядро производителя / vendor kernel | Сохранять термины downstream/vendor |
| device tree (DTS/DTB) | дерево устройств / аппаратное описание платы | DTS исходник; DTB бинарник; DTBO overlay |
| driver | драйвер | Различать драйвер ядра и HAL-библиотеку |
| vendor blob | закрытый компонент производителя / vendor blob | Не обязательно полностью закрыт; проверять лицензию |
| firmware | микропрограмма / firmware | Слово многозначно: отдельный компонент или комплект разделов |
| firmware package | набор низкоуровневых микропрограмм / firmware package | Не путать с системным ROM |
| ROM / stock ROM / custom ROM | прошивка / заводская / кастомная прошивка | Оставлять ROM для поиска и совместимости с форумами |
| CFW (begonia) | CFW, историческая кастомная firmware-база begonia | Это специальная схема загрузчиков, НЕ любой кастомный ROM |
| Non-CFW | Non-CFW, обычная совместимая загрузочная база | Не означает отсутствие firmware |
| GSI | универсальный системный образ Android (GSI) | Generic System Image, НЕ GKI |
| GKI | универсальный образ ядра Android (GKI) | Generic Kernel Image, НЕ GSI |
| OEM port | порт оболочки/прошивки производителя | Перенос с другого аппарата |
| bootloader | загрузчик | BROM, preloader и LK — разные этапы цепочки |
| BROM / BootROM | встроенное ПЗУ начальной загрузки / BootROM | Не переводить BROM в командах |
| preloader | ранний загрузчик (preloader) | Чувствительный раздел, ошибочная запись может привести к кирпичу |
| recovery | среда восстановления (recovery) | TWRP/OrangeFox; не синоним полного заводского ROM |
| fastboot | Fastboot | Протокол, а не конкретная ОС |
| device unbrick / hard-brick | восстановление «кирпича» / полный отказ загрузки | Не обещать гарантии восстановления |
| A/B slots | слоты A/B | Наличие зависит от модели/разметки, не от версии Android |
| dynamic partitions | динамические разделы | Тип разметки, не синоним Non-CFW |
| HAL (Hardware Abstraction Layer) | уровень абстракции оборудования (HAL) | Различать Android HAL и Linux kernel driver |
| Halium | Halium | Техническое имя собственное, оставить оригинал |
| libhybris | libhybris | Не переводить |
| userspace | пользовательское пространство / userspace | Android 16 UI может работать с ядром 4.x |
| Root / su | права суперпользователя (root) | Root ≠ разблокированный загрузчик |
| KernelSU / KSU | KernelSU / KSU | Проект и семейство методов root, не переводить |
| Non-KSU | ядро без встроенного KernelSU (Non-KSU) | Не гарантирует отсутствие другого root |
| Magisk | Magisk | Название проекта |
| APatch / KernelPatch | APatch / KernelPatch | Root-патч ядра, точные названия |
| NoMount | NoMount | VFS-механизм подмены файлов, НЕ самостоятельный root |
| SUSFS | SUSFS | Дополнительные патчи файловой подсистемы, НЕ самостоятельный root |
| Magic Mount | Magic Mount | Mount backend, не менеджер root |
| Mountify / Hybrid Mount | Mountify / Hybrid Mount | Отдельные backend/metamodule проекты |
| OverlayFS | OverlayFS | Стандартная технология Linux, не переводить в коде |
| metamodule | метамодуль (metamodule) | Слой монтирования системных модулей |
| systemless modification | модификация без изменения исходных системных разделов | Не равно «невидимо» |
| Play Integrity | Google Play Integrity | Серверная/аппаратная аттестация, не простая проверка наличия su |
| vendor security patch | обновление безопасности компонентов производителя | Не считать равным обновлению Android UI |
| observed / verified / reported / inferred | наблюдено / проверено / заявлено автором / выведено | Не смешивать [V], [D], [I], [U] |
| rollback baseline | проверенная исходная сборка для отката | Указать точный SKU, SHA и необходимые разделы |
| source blob SHA | Git Blob SHA исходного файла | Не путать с SHA коммита; используется для обнаружения устаревшего перевода |

## Examples of incorrect translations to avoid

- **Non-CFW = «без прошивки»** — incorrect. Use «без старой CFW-схемы».
- **Mainline-based = «официально поддерживается Linux»** — incorrect. Use «форк на основе mainline; патчи могут не быть в upstream».
- **KernelSU = «магиск внутри ядра»** — misleading. Different architecture and upstream.
- **NoMount = «root без следов»** — unsupported. NoMount is file-redirection infrastructure; root detection and attestation are separate.
- **Firmware = always «вся операционная система»** — incorrect: firmware often refers to modem, DSP, wireless, touch and boot chain components.
- **Working on rosemary = working on begonia** — unsupported: board-level hardware differs despite MT6785-family overlap.

## Translator review checklist

Check **every number, filename, date, Git SHA, source URL, table entry and confidence label** in both language versions. Preserve direct links to originals. Prefer a clear explanatory sentence over a literal Russian or English calque.

For additions propose an English term, preferred Russian equivalent, aliases, forbidden ambiguous alternatives and a source. Do not translate corporate/project trademarks, config keys or code.
