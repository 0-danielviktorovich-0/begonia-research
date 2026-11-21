# 24 — GitHub @Saikrishna1504: исходники begonia, перенос Linux 4.19 и патчи компонентов

**Русский язык:** [Эта страница](24-saikrishna-source-audit.md) · [Полный английский отчёт](../../24-SAIKRISHNA1504-DEVICE-STACK-AUDIT.md) · [Русский каталог](README.md).

> **Статус перевода: подробный технический конспект (DIGEST), НЕ полный перевод.** Исходный английский документ содержит полную таблицу, даты, ссылки, пояснения и ограничения. Проверка по GitHub выполнена 21 ноября 2026 года; на физическом телефоне никакие тесты не проводились.

## 1. Главная находка — настоящее продвижение к Linux 4.19

В профиле [Saikrishna1504](https://github.com/Saikrishna1504) найдено 103 публичных репозитория; часть посвящена другим устройствам. В актуальной ветке [device_redmi_begonia@axion](https://github.com/Saikrishna1504/device_redmi_begonia/tree/axion) уже опубликована настройка сборки ядра **4.19**:

- **TARGET_KERNEL_CONFIG:** k85v1_64_k419_defconfig и vendor/begonia.config.
- **TARGET_KERNEL_SOURCE:** kernel/xiaomi/mt6785.
- **Формат загрузочного образа:** Image.gz-dtb, header version 2.
- **Компилятор:** Clang r416183b.
- **Уровень обновлений безопасности vendor:** 2022-04-01 — современный Android-интерфейс не делает старые vendor-компоненты новыми.

Таким образом, существует не только сообщение автора о работающем ядре, но и **реальная серия изменений для begonia**.

## 2. Шесть коммитов переноса 4.19, которые нужно изучать

| Дата UTC | GitHub-коммит | Технический смысл |
|---|---|---|
| 13.11.2026 | [d78e16d11686](https://github.com/Saikrishna1504/device_redmi_begonia/commit/d78e16d11686806b1f0b24c6b3c149255a950ac0) | Переход на конфигурацию Linux 4.19 и новый DTBO |
| 13.11.2026 | [46c71c286a14](https://github.com/Saikrishna1504/device_redmi_begonia/commit/46c71c286a14d0be1fd262e9ebe17749258c200e) | SELinux: разрешения для GPU, питания, sysfs и аппаратных служб |
| 13.11.2026 | [1f27a5cc808d](https://github.com/Saikrishna1504/device_redmi_begonia/commit/1f27a5cc808d3eb13dc0b093a85c33fc50498165) | init.mt6785.rc: новые настройки schedutil, UClamp и управления частотами |
| 13.11.2026 | [f0255137e02a](https://github.com/Saikrishna1504/device_redmi_begonia/commit/f0255137e02ab26039392f795c72a03a97fb2287) | powerhint.json: более 300 изменённых строк регулирования производительности |
| 14.11.2026 | [dd3c64579236](https://github.com/Saikrishna1504/device_redmi_begonia/commit/dd3c6457923662570d4b83212112cd55c74d8a41) | Исправления путей USB OTG и SD-карты для 4.19 |
| 15.11.2026 | [38c6dfbba60f](https://github.com/Saikrishna1504/device_redmi_begonia/commit/38c6dfbba60f008be7f07ff8fb77614bd45c46a1) | Сборка Clang r416183b, NO_GCC, Image.gz-dtb |

В описаниях автор прямо указывает **rosemary** как источник части изменений SELinux, init и powerhint. Это особенно ценный инженерный след для сравнения двух деревьев и самостоятельного дальнейшего переноса на более новые версии Linux.

### Проблема воспроизводимости

В [манифесте MT6785](https://github.com/Saikrishna1504/local_manifests/blob/udc/mt6785.xml) устройство выбирается из ветки **axion**, рассчитанной на 4.19, а исходники ядра — из [kernel_xiaomi_mt6785@main](https://github.com/Saikrishna1504/kernel_xiaomi_mt6785), где Makefile по-прежнему показывает **Linux 4.14.357-openela**. В проверенном LineageOS MT6785 4.19 есть основной k419_defconfig, но **vendor/begonia.config не обнаружен**. Следовательно, нужен точный URL нового kernel tree, SHA и недостающий фрагмент. Это не опровержение работы автора — только факт неполноты доступной нам цепочки сборки.

## 3. Ценные группы GitHub-репозиториев

| Область | Репозитории | Зачем нам |
|---|---|---|
| **Дерево телефона** | [device_redmi_begonia](https://github.com/Saikrishna1504/device_redmi_begonia) | Настройки панели, аппаратных HAL, аудио, питания, безопасности и сборки |
| **Proprietary vendor** | [vendor_redmi_begonia](https://github.com/Saikrishna1504/vendor_redmi_begonia) | Библиотеки MTK Audio, Camera, IMS, Video Codec2, GNSS и модема |
| **Низкоуровневые firmware** | [vendor_redmi_begonia-firmware](https://github.com/Saikrishna1504/vendor_redmi_begonia-firmware) | audio_dsp, camera VPU, модем, SCP/SSPM, LK, preloader и TEE. **Не прошивать без проверки** |
| **Ядро Power 4.14** | [kernel_xiaomi_mt6785](https://github.com/Saikrishna1504/kernel_xiaomi_mt6785) | Сравнение старых драйверов/патчей с новой 4.19-веткой |
| **MediaTek HAL** | [hardware_mediatek](https://github.com/Saikrishna1504/hardware_mediatek) и [hardware_xiaomi](https://github.com/Saikrishna1504/hardware_xiaomi) | Современные Android AIDL интерфейсы Bluetooth, USB, Thermal, Health |
| **Связь, IMS и VoWiFi** | [Imsservice](https://github.com/Saikrishna1504/Imsservice), [архив IMS](https://github.com/Saikrishna1504/vendor_redmi_begonia-ims) | Обратная разработка MediaTek IMS, адаптация старых API |
| **Камера** | [MiuiCamera_smali](https://github.com/Saikrishna1504/MiuiCamera_smali), [архив MiuiCameraLeica](https://github.com/Saikrishna1504/vendor_MiuiCameraLeica) | Работа закрытого camera userspace, протоколы и ошибки совместимости |
| **Recovery** | [device_xiaomi_begonia-pbrp](https://github.com/Saikrishna1504/device_xiaomi_begonia-pbrp) | Исторический PBRP с prebuilt kernel/DTB/DTBO |
| **Манифесты и OTA** | [local_manifests](https://github.com/Saikrishna1504/local_manifests), [OTA](https://github.com/Saikrishna1504/OTA) | Сборка компонентов и архив старых релизов |

В машинном [реестре из 21 репозитория](../../saikrishna-source-inventory.csv) дополнительно указаны ветки, даты обновлений, назначение и степень подтверждения.

Не следует путать: репозиторий автора [android_kernel_device_modules_6.1](https://github.com/Saikrishna1504/android_kernel_device_modules_6.1) относится к **другому MediaTek MT6897** и не доказывает наличие Linux 6.1 на begonia; [flashing_guide](https://github.com/Saikrishna1504/flashing_guide) пока описывает только **duchamp**; а [Begonia_OSS](https://github.com/Saikrishna1504/Begonia_OSS) содержит лишь небольшой набор Dolby EQ-настроек, не полное ядро.

## 4. Почему для нашего Ubuntu Touch особенно ценны аудио и IMS

В дереве устройства есть [audio_policy_configuration.xml](https://github.com/Saikrishna1504/device_redmi_begonia/blob/axion/configs/audio/audio_policy_configuration.xml) с маршрутами **Built-In Mic, Built-In Back Mic, Voice Call In, Echo Ref In**. Имеются десятки файлов AudioParam (усиление, запись, Speech/VoIP, шумоподавление DMNR, эхоподавление, конфигурация NXP-усилителя), а также [libshim_audio.cpp](https://github.com/Saikrishna1504/device_redmi_begonia/blob/axion/libshims/audio/libshim_audio.cpp).

Это нужно сравнить с аудиомаршрутизацией **Ubuntu Touch Halium 10** и **Droidian**, где автор порта сообщает о работающем микрофоне. Замена vendor на новую версию без анализа интерфейсов может всё сломать.

Отдельный набор из **10 патчей IMS** включает:
- [0010](https://github.com/Saikrishna1504/device_redmi_begonia/blob/axion/blob-patches/ImsService/0010-ImsService-WfcHandler-Fix-fatal-crash.patch): исправление ClassCastException в VoWiFi WfcHandler.
- [0006](https://github.com/Saikrishna1504/device_redmi_begonia/blob/axion/blob-patches/ImsService/0006-ImsService-Fix-NPE-on-ImsCallSessionProxy.patch): защита от NullPointerException.
- [0008](https://github.com/Saikrishna1504/device_redmi_begonia/blob/axion/blob-patches/ImsService/0008-ImsService-Switch-to-shared-libs-to-mtk-frameworks.patch): новые зависимости MediaTek framework.

Также обнаружены **4 патча MIUI Camera**, включая [изменение вызовов CaptureResult от 15.10.2026](https://github.com/Saikrishna1504/device_redmi_begonia/blob/axion/blob-patches/MiuiCamera/0001-ICustomCaptureResult-Fix-CaptureResultExtras-and-Tot.patch). [extract-files.py](https://github.com/Saikrishna1504/device_redmi_begonia/blob/axion/extract-files.py) показывает конкретные исправления ELF/Codec2/Audio/Camera dependencies. Это полезно для поиска ошибок ABI при использовании Android 11 vendor с более новыми системами.

**Ограничение:** Android APK/smali-патчи не становятся автоматически нативными Linux-драйверами. Реальное VoWiFi зависит от модема, оператора и HAL, а камера — от ISP и закрытого стека. Чужие бинарные файлы не следует дублировать в базе без проверки прав.

## 5. Что делать дальше

1. Написать [@Saikrishna1504](https://t.me/saikrishna1504), сообщив, что мы изучили его [коммиты 4.19 от 13–15 ноября](https://github.com/Saikrishna1504/device_redmi_begonia/commit/d78e16d11686806b1f0b24c6b3c149255a950ac0), и запросить **точное дерево ядра, SHA, vendor/begonia.config, DTS/DTBO и работающие аппаратные компоненты**.
2. Сопоставить device axion, vendor bka, firmware bka и **реальное ядро 4.19**, не используя старый несогласованный манифест как готовую сборку.
3. Выполнить побайтовое/структурное сравнение аудиоконфигураций, ELF-зависимостей и логов между Android, Ubuntu Touch и Droidian.
4. Исследовать переносимые идеи в SELinux, init и powerhint, но не переносить эти Android-настройки как есть в чистый mainline Linux.
5. Низкоуровневые файлы preloader, LK, md1img, TEE не записывать без подтверждённой региональной совместимости и резервной копии уникальных разделов.

**Источники и пределы проверки:** полные ссылки, полный список 21 проекта, timestamps и приоритеты находятся в [английском оригинале](../../24-SAIKRISHNA1504-DEVICE-STACK-AUDIT.md). Никаких сборок или тестов на устройстве не проводилось.
