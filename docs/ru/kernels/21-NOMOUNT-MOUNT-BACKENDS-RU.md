# 21 — NoMount, Metamodules, Magic Mount и OverlayFS: сравнительный аудит Android root-экосистемы

**Redmi Note 8 Pro (begonia, MT6785) / применимо и к другим Android-устройствам.**  
Дата проверки: **2026-11-21**. **Исходники проверены**, но **NoMount и другие root-модули на телефоне владельца не запускались**. Этот материал — дополнение к [16-ROOT-METHODS.md](../../en/android/16-ROOT-METHODS.md), [20-KERNEL-419-ROOT-ECOSYSTEM-RU.md](20-KERNEL-419-ROOT-ECOSYSTEM-RU.md) и [03-KERNEL-HISTORY.md](../../en/kernels/03-KERNEL-HISTORY.md), не замена исходным источникам. В этой документации «поддерживает» означает заявление upstream, **не успешный тест на begonia**.

## 1. Сначала разделяем три независимых слоя

```text
А. Кто выдаёт root и управляет разрешениями?
  Magisk / KernelSU / KernelSU-Next / SukiSU Nova / APatch
                         |
Б. Как «systemless» модули подменяют файлы?
  Magic Mount (bind/tmpfs) / OverlayFS / Mountify /
  NoMount (VFS redirection) / Hybrid Mount / Meta OverlayFS
                         |
В. Какие дополнительные функции подключены к ядру?
  SUSFS / NoMount kernel engine / KernelPatch KPM / NoMount LKM /
  NoMount-compatible VFS provider / Zygisk userspace
```

**NoMount не root-движок. SUSFS тоже не root-движок.** Можно запустить KernelSU без NoMount, либо KernelSU + NoMount; наличие `CONFIG_NOMOUNT=y` не означает `CONFIG_KSU=y`. `KSU` или `Non-KSU` в названии ZIP обычно означает вариант *с* или *без* встроенного KernelSU. Если `CONFIG_KSU` отключён, NoMount сам по себе root не предоставит. [Nova-Kernels `begonia_user_ksu_defconfig`](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785/blob/main/arch/arm64/configs/begonia_user_ksu_defconfig) и [обычный defconfig](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785/blob/main/arch/arm64/configs/begonia_user_defconfig) это наглядно показывают. [V]

## 2. NoMount — именно тот submodule из Nova-Kernels

**Первичный upstream:** [maxsteeel/nomount](https://github.com/maxsteeel/nomount), [README](https://github.com/maxsteeel/nomount/blob/master/README.md), [инструкция для ядра](https://github.com/maxsteeel/nomount/blob/master/kernel/README.md), [Releases](https://github.com/maxsteeel/nomount/releases). [V 2026-11-21]

**На дату проверки последний опубликованный релиз — `v2.3.1` от 2026-11-19.** Официальный changelog утверждает ускорение перечисления модулей (до 100 раз в одном тестовом сценарии; **не универсальный бенчмарк для begonia**), перенос обработки whiteouts/opaque/.replace в нативный бинарник. Протокол драйвера остаётся **v23**, с релизом v2.3.0 совместим по протоколу; разработчик всё равно рекомендует обновлять kernel и metamodule совместно. [V, GitHub Releases API, `v2.3.1`]

### Принцип

- **VFS path redirection:** при обращении к исходному пути ядро возвращает содержимое из другого файла; без реального `mount` поверх `/system` или `/vendor`.
- Поддерживает **файлы и каталоги**, подстановку новых файлов в `readdir`, **whiteouts** (виртуальное удаление), **opaque directories** (скрыть старое содержимое каталога), перенаправление с ограничением по **UID**.
- Работает в RAM и не должен добавлять bind/overlay mount-строки в `/proc/mounts` для своих подмен; **не означает полной недетектируемости**: другие следы, свойства устройства/bootloader, SELinux, несовпадающие API, поведение `stat`/`mmap` или ошибки модуля способны выдавать модификацию.
- Имеет пользовательскую **metamodule** и **kernel subsystem**. WebUI и CLI управляют правилами; правила, введённые вручную через CLI, очищаются при reboot, если их заново не восстанавливает metamodule.

### Где он в NoVA

[`.gitmodules`](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785/blob/main/.gitmodules):
```ini
[submodule "KernelSU"]
    path = KernelSU
    url = https://github.com/KernelSU-Next/KernelSU-Next
    branch = legacy
[submodule "NoMount"]
    path = NoMount
    url = https://github.com/maxsteeel/nomount
```

В [`begonia_user_ksu_defconfig`](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785/blob/main/arch/arm64/configs/begonia_user_ksu_defconfig) присутствуют `CONFIG_KSU=y`, `CONFIG_KSU_MANUAL_HOOK=y`, `CONFIG_KSU_SUSFS=y` **и `CONFIG_NOMOUNT=y`**. В обычном [`begonia_user_defconfig`](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785/blob/main/arch/arm64/configs/begonia_user_defconfig) — `# CONFIG_KSU is not set`. Сборочный скрипт [`nova-build.sh`](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785/blob/main/nova-build.sh) имеет `--build`, `--build-ksu`, `--build-all`. [V; факт конфигурации != доказанный boot]

### Ограничения по ядрам

| Среда | Требование разработчика NoMount |
|---|---|
| Типичный **GKI 5.10+** | Готовые LKM из ZIP для **точно совместимой** ветки/ABI; kernel rebuild не всегда нужен, но не гарантировано на любом GKI |
| **Legacy 4.14 / 4.19**, как у begonia | **Встроить код в kernel source (`CONFIG_NOMOUNT=y`) или собрать собственный LKM для этого ядра**; готовые GKI-модули не подходят |
| Строго ограниченное ядро | Возможно потребуется built-in; нельзя рассчитывать на загрузку `.ko` |

**Риски:** ранние VFS-хуки работают в чувствительной части ядра; ошибка указателя, refcount, inode lifecycle, recursion или `mmap` может привести к зависанию/перезагрузке. Файловые и SELinux-контексты, семантика каталогов, конфликты правил и несовместимый userspace могут сломать приложения. Преимущество «меньше mount-следов» покупается **большим вмешательством в VFS**. Влияние на батарею/CPU/скорость запусков на begonia **не измерено**.

**Не использовать `curl ... | bash` из README на основной машине или ядре без чтения скрипта/фиксации коммита.** Для воспроизводимости закреплять SHA submodules и сравнивать diff.

## 3. Сравнение ROOT-движков: плюсы, минусы, для кого

| Подход | Плюсы | Минусы/риски | Для begonia (legacy 4.14/4.19) |
|---|---|---|---|
| **Magisk** ([topjohnwu](https://github.com/topjohnwu/Magisk), [install docs](https://topjohnwu.github.io/Magisk/install.html)) | Распространённый, зрелый, без обязательной компиляции ядра; Zygisk, большой выбор модулей; легко адаптировать к конкретному stock `boot.img` | Ramdisk/boot changes, может ломаться при смене firmware/OTA; интеграция init и mount видна по косвенным признакам; модули и root повышают attack surface | **Первый кандидат для обычного root**, но только с boot image ТОЧНО текущей ROM и проверенным rollback. Нет гарантии на любой кастомной прошивке |
| **Original KernelSU** ([tiann/KernelSU](https://github.com/tiann/KernelSU), [FAQ](https://kernelsu.org/guide/faq.html)) | Root в ядре, точная выдача прав по приложениям/UID, отдельный kernel manager; metamodule-архитектура, без обязательного Magisk init hook | Для штатного современного upstream основная поддержка **GKI 5.10+**; старые non-GKI — архивные инструкции; kernel+manager связаны версиями | Требуется **кастомная/legacy интеграция**. Не рекомендовать просто последнюю GKI-сборку |
| **KernelSU-Next** ([upstream](https://github.com/KernelSU-Next/KernelSU-Next)) | Развивает KSU, есть legacy/non-GKI ответвления, совместим с отдельными metamodule/SUSFS интеграциями; подтверждён NoVA | Больше upstream-форков, ABI и версий; требуется сборка ядра и тест, возможны конфликты hooks | **Хороший вариант для исследовательского 4.14/4.19 ядра**, если root действительно нужен |
| **SukiSU Nova** ([upstream](https://github.com/SukiSU-Nova/SukiSU-Nova), [integration](https://sukisu.org/guide/how-to-integrate)) | Альтернативный KSU-fork, дополнительные функции KPM/менеджера; legacy manual integration заявлена | Новые fork-specific функции/зависимости; меньше гарантий прямой совместимости с чужим KSU/SUSFS stack; ещё один слой поддержки | Только **отдельной экспериментальной веткой** после проверки в точном kernel source; не смешивать наугад |
| **APatch / KernelPatch** ([bmax121/APatch](https://github.com/bmax121/APatch), [docs](https://apatch.dev/what-is-apatch.html)) | Root через patch kernel image, не обязательно пересобирать исходники полного kernel tree; поддержка APM/KPM; привлекателен когда исходники неполны | Патч boot/kallsyms должен соответствовать конкретному ядру; риск boot failure, поддержку ABI, модулей и версии проверять отдельно | **Потенциально применим**, подтверждённой готовой безопасной инструкции для конкретного begonia нет |
| **Non-KSU kernel** | Меньше kernel-root hooks, можно использовать без root или с отдельным Magisk, проще сравнивать boot/питание без лишних патчей | Нет встроенного KSU; не гарантирует целостность ROM, если отдельно установлены иные root-инструменты | **Лучше как контрольная базовая сборка при отладке драйверов/USB/питания** |

`GKI` = Generic Kernel Image и не тождественен `GSI` = Generic System Image. Для старых vendor-деревьев `kprobe`, `CONFIG_KSU_MANUAL_HOOK`, `CONFIG_KALLSYMS` и `CONFIG_MODULES` могут влиять на возможность интеграции. Наличие root-ядра не обновляет Linux ABI, DTB или Wi-Fi драйвер.

## 4. Сравнение методов «systemless» подмены файлов

| Backend / инструмент | Плюсы | Минусы/условия | Основа |
|---|---|---|---|
| **Magic Mount / bind mounts** | Понятная семантика Linux VFS, исторически широко совместим с Magisk-модулями; не требует отдельных VFS-патчей | Множество mount-записей/пространств имён, накладные расходы на сложных наборах модулей, mount-метаданные наблюдаемы; не равен полноценной невидимости | [Magisk](https://github.com/topjohnwu/Magisk), [KernelSU differences](https://kernelsu.org/guide/difference-with-magisk.html) |
| **Meta OverlayFS** | Использует встроенный Linux OverlayFS; прозрачный upper/lower/workdir, один механизм для многих файлов; хорошо подходит для набора systemless-файлов | Требует `CONFIG_OVERLAY_FS` и подходящих файловых систем/xattr/SELinux, оверлей создаёт реальные mount-объекты; конфликты файлов и слои | [KernelSU meta-overlayfs](https://github.com/KernelSU-Modules-Repo/meta-overlayfs); README прямо называет его *reference implementation*, а не гарантированным оптимальным вариантом |
| **Mountify** | KernelSU metamodule, также заявлена работа с APatch/Magisk; объединяет подмены через OverlayFS, есть WebUI, tmpfs и ext4-sparse режимы | `CONFIG_OVERLAY_FS=y`; желательно `CONFIG_TMPFS_XATTR=y`; всё ещё реальные mounts и обнаруживаемые следы; ext4 sparse и некоторые файловые системы/whiteouts могут конфликтовать; модуль поддерживается на страх пользователя | [backslashxx/mountify](https://github.com/backslashxx/mountify), README [V] |
| **NoMount** | Не создаёт традиционных mounts; виртуальная подмена в памяти, выборочная видимость по UID, whiteout/opaque, горячие изменения правил | Нужны VFS kernel hooks/LKM, сложная отладка/ABI, возможны несовместимости с приложениями и `mmap`, критические kernel crashes; поведение на 4.14/4.19 begonia **не проверено** | [maxsteeel/nomount](https://github.com/maxsteeel/nomount), README и `kernel/README.md` [V] |
| **Hybrid Mount** | Переключение `overlay`/`magic`/`vfs` по модулю и пути, fallback, разные требования приложений можно разделять | Большая сложность конфигурации; VFS provider/API version must match, Kernel/SELinux/ABI, конфликт paths/whiteouts; автор предупреждает о запрете совместного внедрения конфликтующих VFS engines | [Hybrid-Mount/meta-hybrid_mount](https://github.com/Hybrid-Mount/meta-hybrid_mount) [V] |
| **«Без module mount»** | Нет лишних mount/redirect hooks; базовое ядро проще и безопаснее для диагностики | Не работают модули, требующие файловой подмены; обычные root-команды/daemon/service могут при этом работать | [KernelSU metamodule docs](https://kernelsu.org/guide/metamodule.html) |

**Примечание об обнаружении root:** отсутствие новых записей `/proc/mounts` не делает bootloader/AVB/root незаметными, не гарантирует прохождение Play Integrity и не означает, что банковское приложение будет работать. Детекторы могут анализировать множество сигналов, и система может быть нестабильной. Рассматривать эти инструменты как инженерную инфраструктуру, а не обещание «обхода всего».

### SUSFS и NoMount не одно и то же

[SUSFS](https://gitlab.com/simonpunk/susfs4ksu) добавляет в ядро механизмы управления видимостью путей/монтирований/метаданных для KernelSU-подобной экосистемы. **NoMount непосредственно реализует подмену файлов без mounts**, то есть это *механизм инъекции*, а не лишь сокрытия уже имеющихся mounts. Их можно встретить вместе в NoVA, но сочетание двух патчей VFS увеличивает площадь возможных конфликтов. Не считать, что «больше скрывающих патчей = лучше». Сверять `fs/`, hook points, `CONFIG_*`, shared locks, submodule SHA.

### Что такое metamodule

В современных [KernelSU docs](https://kernelsu.org/guide/metamodule.html) metamodule выбирает **способ монтирования/включения модулей** в системе. Это надстройка для module ecosystem, а не ядровой `su` сама по себе. Можно использовать обычный модуль и metabackend в одной системе; обычно не стоит запускать **несколько конкурирующих mount-metаmodules** одновременно, если это прямо не поддержано проектом.

### Другие одноимённые проекты

[NoMount-Suite](https://github.com/Bouteillepleine/NoMount-Suite) описывается как переписанный/другой проект на основе Prism VFS. **Не смешивать** его releases/patches и `maxsteeel/nomount` только по совпадению названия. Аналогично «ZeroMount», «Hybrid Mount», «Mountify» — отдельные авторы/ветки/ABI; нужно проверить источник конкретного модуля.

## 5. Что выбрать именно для нашего проекта

**Пользовательский Android:**
- Без необходимости root: **Non-KSU**, минимально модифицированное ядро.
- Нужен обычный root для тестов приложений: **Magisk** на собственном точном boot.img + проверки SELinux/OTA/дата-шифрования.
- Создаём своё экспериментальное 4.14/4.19 ядро: **KernelSU-Next legacy** + manager, отдельная `Non-KSU` контрольная сборка; NoMount/SUSFS включать **отдельными вариантами**, а не всё сразу.
- Нужна файловая подмена и простая отладка: сначала обычный mount backend, затем сравнительный NoMount на выделенной тестовой ветке; **влияние на производительность/маскировку/совместимость измерять**, не предполагать.

**Ubuntu Touch / Droidian:** Android Magisk/KernelSU/NoMount не являются необходимыми для работы Linux; для исправления микрофона, Wi-Fi, питания важнее сравнение kernel driver, HAL, audio policy, DT и сервисов. NoMount может быть использован как **Android-side эксперимент**, но не заменяет нормального Halium overlay/системную конфигурацию.

**postmarketOS mainline:** системный Linux предоставляет модель root/sudo сам; Android `KSU`, Magisk и NoMount не являются зависимостями. Для Linux-порта приоритет драйверы, regulator/pinctrl/DTS, power-management, RF и firmware.

### Практическая матрица проверки (когда устройство будет готово)

| Измерение | A — Non-KSU | B — KernelSU-Next | C — KSU + SUSFS | D — KSU + NoMount |
|---|---|---|---|---|
| `uname -r`, boot image SHA | записать | записать | записать | записать |
| Версия KernelSU/manager/SUSFS/NoMount | n/a | записать | записать | записать |
| Boot, recovery, encryption, SELinux | проверить | проверить | проверить | проверить |
| Systemless module install + remove | baseline | проверить | проверить | проверить |
| Sleep/standby, battery drain, CPU | baseline | сравнить | сравнить | сравнить |
| File reads, `stat`, mmap, whiteout, readdir | baseline | проверить | проверить | проверить |
| Crash/dmesg/pstore и rollback | baseline | проверить | проверить | проверить |

Вносить **только одну переменную за эксперимент** и не менять вместе поколение 4.14→4.19, vendor, bootloader и root stack. Перед любыми тестами — [18-DEVICE-PREFLIGHT-READONLY.md](../../en/recovery/18-DEVICE-PREFLIGHT-READONLY.md) и резервные копии уникальных разделов.

## 6. Проверенные первоисточники и степень уверенности

1. [maxsteeel/nomount README](https://github.com/maxsteeel/nomount/blob/master/README.md), [kernel/README](https://github.com/maxsteeel/nomount/blob/master/kernel/README.md), [latest release v2.3.1](https://github.com/maxsteeel/nomount/releases/tag/v2.3.1) [V 2026-11-21; дата/тег GitHub Releases API].
2. [Nova-Kernels .gitmodules](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785/blob/main/.gitmodules), [NoVA KSU defconfig](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785/blob/main/arch/arm64/configs/begonia_user_ksu_defconfig), [build script](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785/blob/main/nova-build.sh) [V].
3. [KernelSU module](https://kernelsu.org/guide/module.html), [metamodule](https://kernelsu.org/guide/metamodule.html), [Magisk comparison](https://kernelsu.org/guide/difference-with-magisk.html), [KernelSU-Next](https://github.com/KernelSU-Next/KernelSU-Next) [V official docs].
4. [backslashxx/mountify README](https://github.com/backslashxx/mountify), [meta-overlayfs README](https://github.com/KernelSU-Modules-Repo/meta-overlayfs), [Hybrid Mount README](https://github.com/Hybrid-Mount/meta-hybrid_mount), [NoMount Suite README](https://github.com/Bouteillepleine/NoMount-Suite) [V].
5. [Magisk official](https://topjohnwu.github.io/Magisk/install.html), [APatch official FAQ](https://apatch.dev/faq.html), [SukiSU Nova official](https://github.com/SukiSU-Nova/SukiSU-Nova) [V].

**Ограничения:** исследование READ-ONLY исходников; не проводились измерения latency/battery/antidetection, не доказана совместимость `NoMount v2.3.1` с фактическим KSU submodule SHA выбранной NoVA сборки, не проверено содержимое собранного ZIP и Android-устройства владельца. Некоторые `master`/`main` ссылки могут измениться; для воспроизводимых билдов закрепить SHA и hashes. **Никаких готовых flash-пакетов не рекомендовано.**
