# Recovery для Redmi Note 8 Pro (begonia): проекты, исходники и актуальность

**Проверено 22 ноября 2026 года.** Это **русский конспект**, а не пословный перевод [полного англоязычного технического исследования](../../en/recovery/recovery-projects-begonia-2026.md). Есть [машинная таблица сравнения](../../../data/matrices/recovery-matrix.csv). Телефон не прошивался, работоспособность образов на конкретном экземпляре не проверялась.

## 1. Что действительно доступно

| Решение | Поддержка begonia | Доказательство |
|---|---|---|
| **TWRP (официальный)** | Устройство указано как `Current`, сопровождающий `theimpulson`, но **последний официальный образ — 3.7.0_9-0 от 06.10.2022** | [Страница](https://twrp.me/xiaomi/xiaomiredminote8pro.html) · [Сборки](https://eu.dl.twrp.me/begonia/) · [Исходники](https://github.com/TeamWin/android_device_redmi_begonia) |
| **TWRP — неофициальные** | Есть отдельные деревья под Android 12.1 и Unified TWRP для новых прошивок; наличие дерева ≠ наличие свежей проверенной сборки | [begonia-recovery](https://github.com/begonia-recovery/twrp_device_xiaomi_begonia) · [Neebe3289](https://github.com/Neebe3289/android_device_xiaomi_begonia) · [WuXing90 на 4PDA](https://4pda.to/forum/index.php?showtopic=974421&view=findpost&p=144354114) |
| **PitchBlack / PBRP** | Есть [официальная карточка](https://pitchblackrecovery.com/begonia/), сопровождающий Flamefusion; дата последнего официального образа не подтверждена | [Основное дерево PBRP](https://github.com/PitchBlackRecoveryProject/android_device_redmi_begonia-pbrp) · [альтернативное дерево](https://github.com/PitchBlackRecoveryDevices/android_device_redmi_begonia-pbrp) |
| **PBRP 4.0 от krispgece — неофициальный** | Образ от **11.10.2026**; автор заявляет поддержку своих **static + dynamic** сборок Infinity-X | [Образ и SHA-256](https://sourceforge.net/projects/infinity-x-begonia/files/begonia/recovery/) · [журнал изменений](https://github.com/krispgece/infinity_ota/blob/16/changelog/begonia.md) · [обсуждение XDA](https://xdaforums.com/t/4804111/) |
| **OrangeFox (официальный)** | **Поддержка прекращена для begonia**. Последний указанный релиз R11.0_0 Beta от 26.07.2020, **только для CFW** | [Официальная страница](https://orangefox.download/device/5eef879f5a65e7146387c434) |
| **OrangeFox — неофициальный** | Были исторические сборки и зеркала; без проверенного автора, исходников и совместимости не следует считать их безопасными | [Документация](https://wiki.orangefox.tech/) · [правила сборки](https://wiki.orangefox.tech/dev/building) |
| **Begonia Recovery Project (BRP), LR.Team** | Исторические форки / оформленные версии TWRP; **не доказано, что продолжают поддерживаться** | [Исследование безопасности](../../en/recovery/07-RECOVERY-SAFETY.md) |
| **SkyHawk/SHRP, RedWolf** | Для данного устройства **проверенных образов не найдено**; Redmi Note 8/8T — это другой код `ginkgo` | [Официальный канал SHRP](https://t.me/s/shrp_official) |
| **PixelExperience/Lineage Recovery** | Специфичны для ROM, подтверждён лишь исторический образ PixelExperience; не следует приписывать современную официальную поддержку LineageOS | [PixelExperience begonia](https://get.pixelexperience.org/begonia) |
| **UBports unified recovery** | Отдельная система восстановления и OTA для **Ubuntu Touch**, используемая Halium-10-портом begonia | [UBports документация](https://docs.ubports.com/en/latest/porting/finalize/UBports_recovery.html) · [исходники recovery](https://github.com/ubports/halium_bootable_recovery) · [исходники Begonia](https://gitlab.com/ubports/porting/community-ports/android10/xiaomi-redmi-note-8-pro/xiaomi-begonia) |
| **Заводской MIUI recovery** | Для штатного восстановления, соответствующего региональной версии прошивки; не универсален для кастомных ROM | [История firmware и MIUI](../../en/android/02-FIRMWARE-HISTORY.md) |

## 2. Почему нельзя выбрать просто «самый новый recovery»

У `begonia` важны **CFW / Non-CFW**, версия Android/vendor/ядра, **статическая либо динамическая** схема разделов, точный размер `recovery`/другого целевого раздела, **AVB**, шифрование `/data` (FDE/FBE), совместимость ZIP, ADB sideload, fastbootd и механизм OTA. TWRP отдельно предупреждает об опасности hard brick и поломке расшифровки данных при обновлении firmware.

Показательный случай: разработчик Infinity-X сообщает, что его **PBRP 4.0** подходит и для *собственных* static-, и для dynamic-сборок, но некоторые static PBRP 4.1 не могут установить его dynamic-сборку. **Это не универсальное доказательство превосходства одной версии.** Самообразный файл `.img` с правильным названием также не доказывает безопасность.

**Официальный OrangeFox для begonia больше не поддерживается**, несмотря на продолжающуюся разработку OrangeFox для других устройств. По [предупреждению разработчиков](https://wiki.orangefox.tech/warning-impersonators) нельзя считать стороннее зеркало официальным.

## 3. Приоритет для Linux и Ubuntu Touch

Наша цель — не только устанавливать Android ROM, но и обслуживать **Ubuntu Touch 24.04**, Droidian и postmarketOS. У UBports есть **собственный unified recovery** с обновлением через `system-image-upgrader`, файлами `recovery.fstab`, ramdisk overlay и механизмом LVM-миграции. Поэтому TWRP/PBRP/OrangeFox — полезные инструменты и источники кода, но **они не заменяют автоматически recovery UBports**. См. [исследование Ubuntu Touch](../../en/linux/05-UBUNTU-TOUCH.md) и [инструкции UBports](https://docs.ubports.com/en/latest/porting/finalize/UBports_recovery.html).

Для Droidian могут потребоваться zip-прошивка и `adb sideload` через подходящий Android recovery; для postmarketOS возможны другие методы. Выбирать конкретную последовательность следует по документации **конкретного релиза**.

## 4. Что проверять прежде чем прошивать

1. Точный код устройства, регион, исходный MIUI/vendor и тип разделов; обязательно учитывать `begoniain` отдельно, а не полагаться на сходство названий.
2. Проверенный оригинальный сайт/разработчик, исходники с Git SHA, дата выпуска **именно образа**, контрольная сумма SHA-256 и назначение образа.
3. Совместимость с `recovery`, `boot`, `dtbo`, `vbmeta`, `super`, шифрованием, конкретным ROM и его обновлениями. **Безопасно измерить размер разделов до записи**.
4. Рабочий путь аварийного восстановления и резервные копии уникальных `NVRAM/NVDATA/NVCFG/persist` **вне Git**, в зашифрованном хранилище; см. [диагностику без записи](../../en/recovery/18-DEVICE-PREFLIGHT-READONLY.md).
5. Отдельные тесты загрузки, сенсора, USB/ADB sideload, microSD/OTG, расшифровки данных, backup/restore, dynamic partitions, OTA и отката; каждый результат — `PASS`, `FAIL`, `UNKNOWN`.

**Итог:** для установки/сопровождения Ubuntu Touch прежде всего изучать **UBports unified recovery**. Для работы с современными Android ROM изучать **соответствующую ROM сборку recovery** и PBRP 4.0 от krispgece, не делая вывода, что неофициальный образ универсален. Официальные TWRP/PBRP удобны как первоисточники, но требуются даты и тесты именно для устройства.

*Состояние исследования — 22.11.2026. Пользовательское устройство не тестировалось; полный список источников и гипотез — в английском отчёте.*
