# 23 — Begonia Linux 4.19: Telegram source provenance and developer contact

> **New GitHub evidence (2026-11-21):** the developer's [device_redmi_begonia@axion](https://github.com/Saikrishna1504/device_redmi_begonia/tree/axion) contains six **dated 13–15 Nov** transition commits documented in [24](24-SAIKRISHNA1504-DEVICE-STACK-AUDIT.md), including [switch to k419 + vendor/begonia.config](https://github.com/Saikrishna1504/device_redmi_begonia/commit/d78e16d11686806b1f0b24c6b3c149255a950ac0). The [public manifest](https://github.com/Saikrishna1504/local_manifests/blob/udc/mt6785.xml) still pins `kernel_xiaomi_mt6785@main` **4.14.357**, while the actual `vendor/begonia.config` fragment was not found in the checked LineageOS 4.19 tree. **Ask specifically for his working 4.19 kernel repo/commit and config fragment**; the existence of userspace patches is stronger evidence than the earlier post alone but not a complete reproducible kernel package.

**Language:** English primary · [Раздел на русском](#по-русски--контекст-и-запрос).  
**Research date:** 2026-11-21. **Nothing was sent to the developer.** The author has not provided source code/boot image to this project yet.

## Public announcement: what was actually verified

| Field | Current evidence and confidence |
|---|---|
| Developer / self-identification | **@Saikrishna1504**, identified by a first-person post on [Redmi Note 8 Pro UPDATES](https://t.me/s/RedmiNote8ProUpdates). **High** for self-attribution in channel text. |
| Author's public Telegram contact | [t.me/saikrishna1504](https://t.me/saikrishna1504) — also linked from [GitHub profile Saikrishna1504](https://github.com/Saikrishna1504). **High** for public profile link, not proof of ownership beyond the author's consistent profile. |
| Date | Likely **2026-11-17** from [TG.ME channel archive](https://tg.me/redminote8proupdates) indexing the announcement as “Nov 17”. **Medium**: third-party feed index; exact original Telegram message timestamp/time zone not independently inspected. **NOT September 2026.** |
| Original post location | [Redmi Note 8 Pro UPDATES channel](https://t.me/s/RedmiNote8ProUpdates). Text confirmed via public search/index. A **post-specific link is recorded in other repo reports**: [Redmi Note 8 Pro UPDATES post #1657](https://t.me/RedmiNote8ProUpdates/1657), cited in [03-KERNEL-HISTORY.md](../kernels/03-KERNEL-HISTORY.md) and [16-ROOT-METHODS.md](../android/16-ROOT-METHODS.md). This auditor independently found the announcement text in the public channel view, but the permalink endpoint itself is not accessible from this browsing environment; status: **previously captured by collaborators, not revalidated here**. |
| Screenshots | The owner recalls a screenshot of the running build. **Screenshot file/media not independently recovered in this auditor's environment**, so it is an open verification item; don't claim visual proof was analyzed. |
| Status | Developer says Linux v4.19 was successfully ported to **begonia**, tested by him for 1–2 weeks with apparently stable results. He explicitly **offered a test build to interested users** and requested meaningful bug reports. **[D] author-report, not independent bench test**. |
| Claimed benefits | New scheduler, native UClamp, easier BPF maintenance, native Codec2 (C2), fixed long-standing video-playback issues; separately VoWiFi, ViLTE and stock MIUI Camera on custom ROMs. **[D] claims only**, and the post does not prove those separate fixes all live in the very same kernel build. |
| Missing evidence | Source URL, exact branch/SHA, Linux sublevel, DTS/DTBO for actual begonia vs rosemary, defconfig, vendor base/Android version, compiler, boot/vendor ABI, reproducible build notes, source license and hardware matrix. |

**Critical technical point:** [LineageOS MT6785 Linux 4.19.325 kernel tree](https://github.com/LineageOS/android_kernel_xiaomi_mt6785) has a verified rosemary board DTS/defconfig. This **does not establish** that the author's claimed **begonia** forward-port uses the same exact tree or is publicly available. The author's own older [Power source](https://github.com/Saikrishna1504/kernel_xiaomi_mt6785) (checked main Makefile) was Linux **4.14.357-openela**, not a verified published 4.19 branch on 2026-11-21. See [03](../kernels/03-KERNEL-HISTORY.md) and [22](../../ru/kernels/22-KERNEL-FORWARD-PORT-AI-INTEGRITY-RU.md).

### GitHub source-release check (2026-11-21)

The developer's publicly listed [kernel_xiaomi_mt6785 repository](https://github.com/Saikrishna1504/kernel_xiaomi_mt6785) currently exposes only **main** and **kaeru** branches in the directly checked GitHub branch listing. Their previously inspected Makefile identifies the 4.14.357-openela Power line; **there is no 4.19-named branch in this particular public repository at observation time**. This does **not** prove the 4.19 project is unpublished everywhere: it could live in a different repository, an unindexed branch, a private tree or as a pending patch series. Ask the author for the authoritative source rather than guessing from an unrelated MT6785/rosemary tree.

### Suggested short first DM in English (unsent)

Hi Sai! I saw your post in @RedmiNote8ProUpdates about getting Linux 4.19 running on the Redmi Note 8 Pro (begonia). Great to see the progress, especially the video playback fixes!

I'm researching begonia Linux ports (Ubuntu Touch/postmarketOS) and would love to study your approach and potentially help with testing. Would you be willing to share the kernel source repo/branch (or patches), defconfig/DTS, and which ROM/vendor base you tested? A link or the relevant commit SHA would be really helpful.

Thanks for your work!

### Optional technical follow-up if he responds positively (unsent)

Thank you! To reproduce this reliably, could you also share the precise kernel version and commit, the original 4.19 MT6785 base/fork, device-specific DTS/DTBO changes, compiler version, a link to any build instructions, matching boot image hashes, and known working/broken functions? I'm especially curious about display variants, charging/suspend, video playback, camera and radio. If the source is not public yet, is there a planned release and license? I can contribute reproducible tests and anonymized logs once a safe restore baseline is prepared.

## По-русски — контекст и запрос

**Автор:** @Saikrishna1504, [его профиль](https://t.me/saikrishna1504). **Канал:** [Redmi Note 8 Pro | UPDATES](https://t.me/s/RedmiNote8ProUpdates). **Дата:** вероятно **17 ноября 2026**, подтверждается только индексом стороннего TG.ME, время публикации пока не перепроверено; номер поста [#1657](https://t.me/RedmiNote8ProUpdates/1657) уже сохранён в отчётах 03 и 16. Ранее в наших исследованиях ошибочно фигурировал сентябрь — это нужно исправлять при упоминании порта **4.19**. (Не путать с другой историей: Wi-Fi на ядре Linux 6.16.4 в отдельном проекте criollojoel10 действительно автором датирован **27 сентября 2026 года**.)

Разработчик заявляет, что запустил Linux 4.19 на begonia, тестировал около одной-двух недель, исправил воспроизведение видео и готов поделиться сборкой с участниками, которые смогут помочь тестированием. **Наличие открытого репозитория с этим конкретным портом пока не подтверждено.**

**Перевод первого сообщения для согласования:**

Привет, Сай! Я увидел твой пост в @RedmiNote8ProUpdates о запуске Linux 4.19 на Redmi Note 8 Pro (begonia). Здорово, что удалось добиться прогресса, особенно с исправлениями воспроизведения видео!

Я изучаю Linux-порты для begonia (Ubuntu Touch/postmarketOS), хотел бы разобраться в твоём подходе и, возможно, помочь с тестированием. Можешь поделиться ссылкой на исходники ядра и ветку (либо патчами), конфигурацией defconfig/DTS и информацией, на какой ROM/vendor-базе тестировалось ядро? Ссылка или SHA соответствующего коммита была бы очень полезна.

Спасибо за твою работу!

### Verification checklist after a reply

1. Link directly to the posted Telegram message and **save its unique post number/timestamp**. Do not infer it from adjacent posts.
2. Verify the reported repository and source commit with GitHub metadata; record license, fork origin and build configuration.
3. Compare with current 4.14 Power source, rosemary 4.19 tree and begonia DTS to understand exactly what changed.
4. Confirm results against a named ROM/kernel/vendor combination, logs, and hardware revision; no device-flashing before [18 — preflight](../recovery/18-DEVICE-PREFLIGHT-READONLY.md).
5. If offered only a compiled image, request reproducible source/license and checksums before treating it as a usable project base. A private image is not evidence of public source release.

**Access / honesty:** original post text was indexed on the channel and on TG.ME. Full media, independent revalidation of post-specific permalink #1657, all intermediate discussion and response from the developer **have not been collected or verified in this audit**. This is an outreach draft, not evidence that any message has been sent.
