# 20 — Происхождение ядер 4.14/4.19 и экосистема root: KernelSU, Non-KSU, Magisk, APatch, SUSFS

**Begonia / Redmi Note 8 Pro (MediaTek MT6785)**  
Дата проверки: **2026-11-21**. Независимое дополнение к [03-KERNEL-HISTORY.md](03-KERNEL-HISTORY.md), [16-ROOT-METHODS.md](16-ROOT-METHODS.md) и [19-ROM-TERMS-GLOSSARY-RU.md](19-ROM-TERMS-GLOSSARY-RU.md). Все проверки выполнены **без телефона**, по исходным файлам, веткам и документации. Исходные версии не скачивались и не запускались.

Статусы доказательств: **[V]** — непосредственно получен/прочитан файл или метаданные upstream 2026-11-21; **[D]** — утверждение разработчика/README/поста (не тестировалось на устройстве); **[I]** — логический вывод; **[U]** — не удалось проверить. **Важно:** подтверждённое наличие исходников / успешно компилируемый kernel ≠ подтверждённая стабильная работа с экраном, камерой, зарядкой и мобильной связью на конкретном begonia.

## 1. Что значит KSU и Non-KSU в названии ZIP

- **KSU** в релизе ядра обычно означает **KernelSU**, ядровую реализацию `su` и контроля root-разрешений. Для работы нужен **соответствующий KernelSU Manager**, совместимая версия KernelSU в *загруженном ядре*, иногда дополнительные userspace-компоненты/модули. Просто установить Manager на произвольный телефон **недостаточно**.
- **Non-KSU** — тот же проект ядра, собранный **без KernelSU**. Это **не запрет на root** и не гарантия отсутствия root: Magisk может быть установлен через ramdisk/boot; отдельный APatch — через собственную модификацию kernel image.
- **KSU + SUSFS** — KernelSU с патчами/модулем SUSFS. SUSFS не является самостоятельным root-решением, добавляет механизмы сокрытия/маскирования путей, mount metadata и других файловых наблюдений. Это **не гарантирует** прохождение Play Integrity, банковских проверок или «необнаружимость».
- **KSU-Next, SukiSU (Nova/Ultra), RKSU, rsuntk/legacy** — отдельные форки, релизы и реализации идеи KernelSU; **одинаковое слово “KSU” не означает совместимые версии менеджера, ABI и патчей**.
- **Root ≠ разблокированный bootloader ≠ ROM ≠ recovery**. Это четыре разные характеристики. Root повышает риски атаки на Android; для разработки Ubuntu Touch/нативного Linux Android-root-менеджеры **не обязательны**.

**Прямое доказательство двух вариантов для нашего устройства:** [Nova-Kernels/kernel_xiaomi_mt6785 `nova-build.sh`](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785/blob/main/nova-build.sh) [V] реализует `-b/--build` (обычный), `-k/--build-ksu` (KSU+SUSFS) и `-a/--build-all`; обычный [`begonia_user_defconfig`](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785/blob/main/arch/arm64/configs/begonia_user_defconfig) задаёт `# CONFIG_KSU is not set`, а [`begonia_user_ksu_defconfig`](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785/blob/main/arch/arm64/configs/begonia_user_ksu_defconfig) содержит `CONFIG_KSU=y`, `CONFIG_KSU_MANUAL_HOOK=y`, `CONFIG_KSU_SUSFS=y`, `CONFIG_NOMOUNT=y`. **В обеих конфигурациях `CONFIG_KPROBES` отключён**, используется ручной hook, а не kprobe. Версия ядра в [Makefile](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785/blob/main/Makefile): **4.14.356**. [`.gitmodules`](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785/blob/main/.gitmodules) указывает **`KernelSU-Next/KernelSU-Next` branch `legacy`** и `maxsteeel/nomount`; сборочный скрипт упаковывает результат посредством форка AnyKernel3.

**Последствие:** KSU/Non-KSU в этом проекте — реальная сборочная вариация, а не просто два названия одного архива. Нельзя без проверки переносить этот вывод на другой ZIP: иногда в названии “KSU” указывают root-метод с иными форками.

## 2. Где брать исходники ядер begonia — версии и доказательства

Новый реестр наблюдений: [kernel-root-provenance.csv](kernel-root-provenance.csv). См. также существующую [kernel-matrix.csv](kernel-matrix.csv) и [03](03-KERNEL-HISTORY.md) для исторических веток.

| Источник/ветка | На самом деле в Makefile (2026-11-21) | Роль / статус | Уверенность |
|---|---|---|---|
| [Xiaomi MiCode](https://github.com/MiCode/Xiaomi_Kernel_OpenSource) `begonia-p-oss`, `q-oss`, `r-oss` | 4.14.94 / 4.14.141 / 4.14.186 | Исторические исходники производителя для Android 9/10/11. Не новый Linux API и не полный vendor source | [V,R] high (история в [03 §1](03-KERNEL-HISTORY.md)) |
| [AgentFabulous/begonia](https://github.com/AgentFabulous/begonia) `android-11.0` | 4.14.253 | Ранний объединяющий community-форк для begonia, Android 11. Важен для изучения истории драйверов/bootloader | [V,R] high |
| [Saikrishna1504/kernel_xiaomi_mt6785](https://github.com/Saikrishna1504/kernel_xiaomi_mt6785) `main` и `kaeru` | **4.14.357-openela** | **Активная база Power**; HEAD `a63454e153cd`, авторская дата коммита 2026-10-31. Это **НЕ 4.19** | [V] high |
| [F640/kernel_xiaomi_mt6785_begonia_power_kernel](https://github.com/F640/kernel_xiaomi_mt6785_begonia_power_kernel) `bka`, `ksu`, `susfs` | `bka`: **4.14.356-openela-rc1**; `ksu`/`susfs`: **4.14.355-openela** | Множество экспериментальных веток: название `ksu` говорит о назначении, **реальную `CONFIG_KSU` всё равно проверять**. Не 4.19 по проверенным веткам | [V] high |
| [Nova-Kernels/kernel_xiaomi_mt6785](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785) `main` | **4.14.356** | Исходники и разделённая build pipeline Non-KSU/KSU+SUSFS. Последний наблюдаемый HEAD `a808b0f2de1d` от 2026-10-03; подробности выше | [V] high |
| [LineageOS/android_kernel_xiaomi_mt6785](https://github.com/LineageOS/android_kernel_xiaomi_mt6785) `lineage-23.2`, `lineage-24.0` | **4.19.325** (обе ветки) | Ключевая **реальная 4.19**-ветка для MT6785; HEAD `30485853fa89` 2026-10-31 на `lineage-24.0` | [V] high **только для дерева/версии**, не для установки на begonia |
| [xiaomi-mt6785-dev/android_kernel_xiaomi_mt6785](https://github.com/xiaomi-mt6785-dev/android_kernel_xiaomi_mt6785) `lineage-24.0` | **4.19.325** | Активное дерево MT6785; проверено **то же самое HEAD `30485853fa89`**, что у LineageOS на `lineage-24.0`. Нельзя считать отдельным независимым патчсетом по этому снимку | [V] high |
| [xiaomi-mt6785-dev/android_kernel_xiaomi_mt6785-4.19](https://github.com/xiaomi-mt6785-dev/android_kernel_xiaomi_mt6785-4.19) `lineage-22.2`, `power`, `lineage-23.1` | 4.19.324 / 4.19.325 / 4.19.325 | **Архивированное** дерево; GitHub org сообщает, что оно перенесено в новый репозиторий без суффикса `-4.19`. Не считать текущим upstream для новых работ | [V] high |
| [mtkpapa/mt6785_kernel_4.19](https://github.com/mtkpapa/mt6785_kernel_4.19) `t` | **4.19.324** | Ещё один найденный 4.19-форк; происхождение и tested-on-begonia неизвестны | [V] version; [U] tested |
| [Sakurajima07/android_kernel_xiaomi_mt6785-4.19](https://github.com/Sakurajima07/android_kernel_xiaomi_mt6785-4.19) `lineage-22.2` | **4.19.324** | Community fork; степень отличия от upstream ещё нужно сравнить через merge-base/diff | [V] version; [U] tests |
| [WuXing90/KernelSU_Action_begonia](https://github.com/WuXing90/KernelSU_Action_begonia) `begonia-13.0` | **не дерево ядра** | CI-шаблон для сборки сторонних 4.14/4.19 kernel trees с опцией KSU/without KSU; берёт source/branch/defconfig параметрами | [V] README |

**Критическое разграничение.** [Официальная LineageOS запись rosemary](https://github.com/LineageOS/lineage_wiki/blob/main/_data/devices/rosemary_variant1.yml) использует MT6785/G95 и 4.19. Дерево в **организации LineageOS** не делает автоматически **begonia официально поддерживаемым аппаратом LineageOS**; физически `rosemary` и `begonia` различаются сенсорами, дисплеем, питанием и другими DT/HAL. Пользовательский отчёт/пост о переносе 4.19 на begonia — **отдельное подтверждение**, не доказательство для любого 4.19 ZIP. В [Telegram @RedmiNote8ProUpdates](https://t.me/s/RedmiNote8ProUpdates) обнаружено сообщение автора, что он успешно портировал 4.19 и тестирует 1–2 недели [D; идентификация точного ROM/kernel commit/логов не проведена].

**Ещё одна важная деталь:** `linux-4.19.325` — основа Linux 4.19 с множеством vendor/backport патчей, а не доказательство, что в ядре присутствуют все функции Linux 5.x/6.x. Нельзя просто подменить 4.14 на 4.19 без согласования DTS, MTK HAL, firmware и boot/DTBO/vbmeta.

## 3. Почему «куча репозиториев» — не куча независимых драйверов

Разработчики создают `fork`/копию, берут коммиты из Android Common Kernel, OEM/LineageOS, upstream Linux, openELA, собственные патчи CPU/scheduler/power/graphics/DT/USB, затем добавляют root и компилируют. Поэтому 30 GitHub-репозиториев могут разделять **одну и ту же исходную 4.14/4.19 базу** с разницей в нескольких патчах. Имя `Power/Suzaku/Nova` — торговое имя патчсета, а **не** версия ядра.

Для определения реального происхождения:
1. `Makefile`: `VERSION/PATCHLEVEL/SUBLEVEL/EXTRAVERSION`.
2. `git remote -v`, `git show -s --format=fuller HEAD`, `git log --oneline --decorate`.
3. `git merge-base <branch> <upstream>`, `git log upstream..branch` и `git diff --stat upstream...branch` (только после определения общего предка; форки могут переписать историю). Не достаточно посмотреть лишь количество коммитов.
4. `arch/arm64/configs/*begonia*defconfig`, `arch/arm64/boot/dts/mediatek/`, `drivers/misc/mediatek`, `drivers/gpu`, `drivers/input`, `drivers/power`.
5. `.gitmodules`, подмодули/вендорные патчи и `.github/workflows`: отличать **submodule commit SHA** от плавающего `branch=legacy`, pinned releases от скачиваемого latest; фиксировать SHA каждого зависимого проекта.
6. Android `device` tree/manifest/vendor tree и `BOARD_KERNEL_IMAGE_NAME`, `TARGET_KERNEL_CONFIG`, recovery/AnyKernel3 install script; **успех GitHub Actions ≠ загрузка на устройстве**.
7. Для заявлений «tested»: фиксировать build hash, имя ROM и vendor, дату, hardware SKU/panel, kernel `uname`, наличие радио/звука/зарядки/OTA, ссылку на issue/log/test report; без этого указывать **claim only**.

## 4. Классификация root-экосистемы (с официальными источниками)

| Решение | Что изменяет и кто основной upstream | Совместимость для legacy begonia (4.14/4.19) |
|---|---|---|
| **Magisk**, [topjohnwu/Magisk](https://github.com/topjohnwu/Magisk), [официальный install guide](https://topjohnwu.github.io/Magisk/install.html) | Патчит **ramdisk/boot init** соответствующего `boot.img`, `init_boot.img`, `vendor_boot.img` или `recovery.img` **по фактической схеме устройства**; модули `systemless`, `su`, Zygisk | Практическая Android root-линия без необходимости собирать собственное ядро; **извлечь точный образ от работающей ROM и проверить ramdisk layout**. Не брать образ другой MIUI/ROM |
| **KernelSU (original)**, [tiann/KernelSU](https://github.com/tiann/KernelSU), [legacy non-GKI instructions](https://kernelsu.org/guide/how-to-integrate-for-non-gki.html) | Код `su` добавляется в ядро (kprobe/manual hook) | Важно: **официальная non-GKI инструкция объявлена архивной**; версия upstream **v0.9.5** — последняя из документированных там non-GKI. Нельзя автоматически применять latest original KernelSU к старому ядру |
| **KernelSU-Next**, [KernelSU-Next/KernelSU-Next](https://github.com/KernelSU-Next/KernelSU-Next), [non-GKI guide](https://github.com/KernelSU-Next/webpage/blob/main/docs/pages/how-to-integrate-for-non-gki.md) | Активный fork original KernelSU, ветка `legacy`, поддержка 4.x через **встроенную** компиляцию и hooks | Подходит для **исследования** 4.14/4.19; точная версия и патчи обязаны совпадать. Upstream README сообщает 4.19–5.4 как built-in, 5.10+ допускает GKI2 LKM/prebuilt. Не означает «на любом 4.19 работает из коробки» |
| **SukiSU Nova** (ранее SukiSU Ultra), [SukiSU-Nova/SukiSU-Nova](https://github.com/SukiSU-Nova/SukiSU-Nova), [integration](https://sukisu.org/guide/how-to-integrate) | Самостоятельный fork семейства KernelSU; KPM/доп. модули; старые ядра требуют собственной сборки | В README заявлена 4.14+ с ручной компиляцией [D]; отдельно проверять совместимость manager/kernel patches. Старые ссылки Ultra перенаправляют в Nova (проверено через GitHub/web 2026-11-21) |
| **APatch**, [bmax121/APatch](https://github.com/bmax121/APatch), [официальные docs](https://apatch.dev/what-is-apatch.html) | **KernelPatch** меняет ядро внутри `boot.img`; root не требует компиляции полного kernel tree, но требует поддерживаемой конфигурации (`CONFIG_KALLSYMS`) и целевого ARM64 | Официальные [требования](https://apatch.dev/install.html) называют kernel 3.18–6.12 и ARM64. Это **только заявленная общая совместимость**, не подтверждение patch/boot на MT6785 4.14/4.19; есть риск неудачной загрузки |
| **SUSFS**, [simonpunk/susfs4ksu](https://gitlab.com/simonpunk/susfs4ksu) | Патчи kernel VFS + часто userspace module для дополнительной модификации наблюдаемой файловой системы | **Не root**: add-on к KSU, выбирается ветка под kernel version (например `kernel-4.14`), структуру KSU и нужные backports |
| **NoMount**, [maxsteeel/nomount](https://github.com/maxsteeel/nomount) | Дополнительная kernel filesystem / mount функциональность, подмодуль NoVA | **Не root** сам по себе; проект/конфиг проверять отдельно |
| **AnyKernel3**, [osm0sis/AnyKernel3](https://github.com/osm0sis/AnyKernel3) | Упаковка и установка ядра; может распаковать/пересобрать `boot` и удерживать часть модификаций ramdisk | **Не root и не компилятор**; конкретный `anykernel.sh` обязан знать устройство и разметку; fork/ZIP без device check опасен |

**SUSFS, Zygisk, Play Integrity Fix, LSPosed, Shamiko, Mountify и KPM — не синонимы root:** относятся к разным слоям (ядровые хуки, модификация app process, модули, mount/маскировка, фреймворк). Смешивание нескольких `su`-движков может вызвать ошибки boot/SELinux/OTA и неожиданные политики безопасности. Никакие заявления о скрытии root не гарантируют совместимость банковских приложений.

### GKI vs non-GKI — не путать с GSI

- **GKI** = [Generic Kernel Image](https://source.android.com/docs/core/architecture/kernel/generic-kernel-image) — стандартная архитектура ядра Android с общим core и vendor modules; **не** [GSI](https://developer.android.com/topic/generic-system-image), универсальный **системный** образ Android.
- **Begonia на кастомном 4.14/4.19 Android ядре** — практический **legacy/non-GKI** сценарий. Наличие числа “4.19” **не** делает устройство GKI 1.0 автоматически; тип определяется его сборкой/ABI/структурой. Нельзя установить generic GKI kernel как замену конкретному begonia kernel без совместимых vendor modules, DTB и загрузки.
- **LKM** = Loadable Kernel Module, `.ko`; **built-in** = код скомпилирован в `Image.gz`, например `CONFIG_KSU=y`; **manual hook / kprobe** = разные стратегии перехвата операций ядра.
- **`CONFIG_KSU=y`** проверяет *намерение* встроить драйвер в образ при данной конфигурации, а не доказывает, что именно этот defconfig использовался в установленном телефоне.

## 5. Где реально взять инструменты и патчи (карта происхождения)

| Задача | Оригинальный автор/проект | Где именно применить на begonia |
|---|---|---|
| Stock драйверы MT6785 | [MiCode/Xiaomi_Kernel_OpenSource](https://github.com/MiCode/Xiaomi_Kernel_OpenSource) (P/Q/R ветки) | Отдельные драйверы / backport и сопоставление с vendor firmware |
| Общие Android kernel patches | [Android Common Kernel / AOSP](https://android.googlesource.com/kernel/common/), [Android kernel overview](https://source.android.com/docs/core/architecture/kernel) | cherry-pick только после проверки ABI/DT/конфликта с vendor патчами |
| Стабильные Linux patches | [kernel.org](https://kernel.org/) / [Linux stable](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git) | Поиск известных CVE/фиксов и backport, а не «сменить версию» строкой в Makefile |
| Android/MTK community base | [LineageOS/android_kernel_xiaomi_mt6785](https://github.com/LineageOS/android_kernel_xiaomi_mt6785), [xiaomi-mt6785-dev/android_kernel_xiaomi_mt6785](https://github.com/xiaomi-mt6785-dev/android_kernel_xiaomi_mt6785), [Saikrishna1504](https://github.com/Saikrishna1504/kernel_xiaomi_mt6785) | Для 4.19 / 4.14 с отдельным сравнением device tree |
| KernelSU core | [KernelSU-Next](https://github.com/KernelSU-Next/KernelSU-Next) `legacy`, [KernelSU original](https://github.com/tiann/KernelSU) | Integrated root source, не generic готовый boot.img |
| SUSFS / NoMount | [simonpunk/susfs4ksu](https://gitlab.com/simonpunk/susfs4ksu), [maxsteeel/nomount](https://github.com/maxsteeel/nomount) | Kernel patches **под конкретные версии**, на отдельной ветке |
| APatch / KernelPatch | [APatch](https://github.com/bmax121/APatch), [KernelPatch](https://github.com/bmax121/KernelPatch) | Эксперимент после извлечения **точного** boot.img и сохранения отката |
| Готовый builder for begonia | [WuXing90/KernelSU_Action_begonia](https://github.com/WuXing90/KernelSU_Action_begonia) (support 4.14/4.19), [Nova build script](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785/blob/main/nova-build.sh), [cvnertnc/Begonia-Kernel-Builder](https://github.com/cvnertnc/Begonia-Kernel-Builder) (архивирован) | Action/CI для компиляции, не доказательство boot safety. WuXing90 README говорит, что **device check отключён в AnyKernel ZIP** — дополнительный риск неправильной установки |
| Упаковка ядра | [osm0sis/AnyKernel3](https://github.com/osm0sis/AnyKernel3), project-specific fork | Раздел `boot`, ramdisk, DTB/DTBO; протестировать package script на *этом* устройстве |

### Пример реальной build supply chain: NoVA

```text
Nova-Kernels/kernel_xiaomi_mt6785 (4.14.356)
├── arch/arm64/configs/begonia_user_defconfig           → Non-KSU
├── arch/arm64/configs/begonia_user_ksu_defconfig       → KSU+SUSFS (manual hooks)
├── KernelSU (git submodule) → KernelSU-Next, legacy branch
├── NoMount (git submodule) → maxsteeel/nomount
├── nova-build.sh → AOSP Clang, Image.gz, mt6785.dtb, DTBO
└── AnyKernel3 fork → recovery/ZIP (NoVA vs NoVA-KSU)
```

Условие воспроизводимости: сохранять *SHA самого ядра*, *SHA подмодуля KernelSU*, *SHA NoMount*, версии компилятора, `defconfig`, хеши `Image`/`dtbo.img`/`ZIP`; branch `legacy` в `.gitmodules` сам по себе не гарантирует воспроизводимую сборку. Не запускать `curl|bash` из чужого репо без проверки и фиксации версии.

## 6. Какие патчи нам действительно нужны для Ubuntu Touch и postmarketOS

Важно различать **Android root patches** и **драйверы/функции Linux**:

| Цель | Что брать в первую очередь | Нужны ли Magisk/KernelSU? |
|---|---|---|
| Ubuntu Touch 24.04 / Halium 10, микрофон/RTC/энергосбережение | [UT device+kernel overlays](05-UBUNTU-TOUCH.md), [Droidian adaptation](06-DROIDIAN-POSTMARKETOS.md), HAL audio policy, MTK kernel drivers | **Нет**, root доступ в Linux/ADB/SSH решается другими средствами. KSU patch сам по себе не исправляет аппаратную ошибку |
| Новый Halium 11 | Android 11 vendor blobs + kernel tree + device tree + RIL/audio/graphics adaptation | **Нет**; root framework Android не является Halium dependency |
| Android кастомная ROM, kernel tuning | 4.14/4.19 kernel fork + device/vendor/DTB, отдельные KSU и Non-KSU build outputs | **Опционально**, как функциональность для пользователя/разработчика |
| postmarketOS/mainline | [Dinolek MT6785 mainline-based](03-KERNEL-HISTORY.md), DTS, regulators, audio/Wi-Fi/battery/modem драйверы | **Нет**, в чистом Linux `root` уже системная модель привилегий; Android KSU не применяется |

**Рекомендация для будущего проекта:** хранить в *информационном репозитории* таблицу источников и pinned commits; код порта/патчсеты держать в отдельных Git-ветках/форках, с CI и тест-протоколами. Не смешивать KSU/SUSFS, переход на 4.19, обновление vendor и новый Ubuntu Touch в одном эксперименте.

## 7. Что ещё не подтверждено и как закрыть пробел

1. **Доказательство, что конкретная 4.19 ветка работает на данном begonia**, а не только компилируется или используется на `rosemary`. Требуются device-tree commit, работающий boot.img, tested build+ROM hash, `uname -r` + dmesg, тесты экрана/зарядки/сенсоров/модема/камеры/USB.
2. **Родословная 4.19 порта MT6785**: сделать Git `merge-base`, `range-diff`, `diff --stat` между rosemary 4.19 tree, xiaomi-mt6785-dev и конкретной begonia ROM; узнать, кто перенёс экран, аккумулятор и прочие board specific nodes.
3. **Все KSU ZIP-версии для begonia**: связать Telegram/4PDA build post → SHA release download → `AnyKernel3/anykernel.sh` → kernel source SHA → `CONFIG_KSU` в реальном boot image. Название архива не доказательство.
4. **SukiSU Nova и APatch**: общая upstream поддержка старых ядер не равна протестированной интеграции MT6785. Нужны builds+logs.
5. **SUSFS**: fork/branch/patch revision и формат менеджера/пользовательского модуля; потенциальные конфликты `fs` с современными Android-ядрами.
6. **Security / updates**: статус OpenELA и бэкпортов CVE для выбранной 4.14/4.19, CONFIG_SECURITY_SELINUX, CONFIG_KPROBES/KALLSYMS, vendor-module ABI, доверие к сторонним builder-пайплайнам.

**Для будущих экспериментов на реальном телефоне:** сначала [18-DEVICE-PREFLIGHT-READONLY.md](18-DEVICE-PREFLIGHT-READONLY.md), резервные копии и идентификация текущего ROM. Не ставить root/ядро просто потому, что оно обозначено “KSU” и “begonia”.

## Primary sources and audit trail

- [Nova-Kernels source + build modes](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785/blob/main/nova-build.sh), [KSU defconfig](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785/blob/main/arch/arm64/configs/begonia_user_ksu_defconfig), [Non-KSU defconfig](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785/blob/main/arch/arm64/configs/begonia_user_defconfig), [submodules](https://github.com/Nova-Kernels/kernel_xiaomi_mt6785/blob/main/.gitmodules) [V 2026-11-21].
- [4.19 LineageOS Makefile](https://github.com/LineageOS/android_kernel_xiaomi_mt6785/blob/lineage-24.0/Makefile), [xiaomi-mt6785-dev active Makefile](https://github.com/xiaomi-mt6785-dev/android_kernel_xiaomi_mt6785/blob/lineage-24.0/Makefile), same tip `30485853fa89` in GitHub API 2026-11-21 [V].
- [Original KernelSU non-GKI warning](https://kernelsu.org/guide/how-to-integrate-for-non-gki.html), [KernelSU-Next compatibility matrix](https://github.com/KernelSU-Next/KernelSU-Next), [SukiSU-Nova current README](https://github.com/SukiSU-Nova/SukiSU-Nova), [APatch official requirements](https://apatch.dev/install.html), [Magisk installation](https://topjohnwu.github.io/Magisk/install.html), [AOSP GKI architecture](https://source.android.com/docs/core/architecture/kernel/generic-kernel-image).
- [WuXing90 action README](https://github.com/WuXing90/KernelSU_Action_begonia/blob/begonia-13.0/README_EN.md), [archived cvnertnc builder](https://github.com/cvnertnc/Begonia-Kernel-Builder), [simonpunk/susfs4ksu kernel-4.14 branch](https://gitlab.com/simonpunk/susfs4ksu/-/tree/kernel-4.14), [AnyKernel3](https://github.com/osm0sis/AnyKernel3).

*Время наблюдения: 2026-11-21, точная отметка UTC не фиксировалась; сведения о текущих HEAD могут устареть. Ни один драйвер или root-patch не признан проверенным на телефоне только по исходникам.*
