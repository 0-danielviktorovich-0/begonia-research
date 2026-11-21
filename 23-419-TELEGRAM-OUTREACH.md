# 23 — Begonia Linux 4.19: Telegram source provenance and developer contact

**Language:** English primary · [Раздел на русском](#по-русски--контекст-и-запрос).  
**Research date:** 2026-11-21. **Nothing was sent to the developer.** The author has not provided source code/boot image to this project yet.

## Public announcement: what was actually verified

| Field | Current evidence and confidence |
|---|---|
| Developer / self-identification | **@Saikrishna1504**, identified by a first-person post on [Redmi Note 8 Pro UPDATES](https://t.me/s/RedmiNote8ProUpdates). **High** for self-attribution in channel text. |
| Author's public Telegram contact | [t.me/saikrishna1504](https://t.me/saikrishna1504) — also linked from [GitHub profile Saikrishna1504](https://github.com/Saikrishna1504). **High** for public profile link, not proof of ownership beyond the author's consistent profile. |
| Date | Likely **2026-11-17** from [TG.ME channel archive](https://tg.me/redminote8proupdates) indexing the announcement as “Nov 17”. **Medium**: third-party feed index; exact original Telegram message timestamp/time zone not independently inspected. **NOT September 2026.** |
| Original post location | [Redmi Note 8 Pro UPDATES channel](https://t.me/s/RedmiNote8ProUpdates). Text confirmed via public search/index. A **post-specific t.me/channel/NUMBER permalink remains unverified**; do not invent one. |
| Screenshots | The owner recalls a screenshot of the running build. **Screenshot file/media not independently recovered**, so it is an open verification item; don't claim visual proof was analyzed. |
| Status | Developer says Linux v4.19 was successfully ported to **begonia**, tested by him for 1–2 weeks with apparently stable results. He explicitly **offered a test build to interested users** and requested meaningful bug reports. **[D] author-report, not independent bench test**. |
| Claimed benefits | New scheduler, native UClamp, easier BPF maintenance, native Codec2 (C2), fixed long-standing video-playback issues; separately VoWiFi, ViLTE and stock MIUI Camera on custom ROMs. **[D] claims only**, and the post does not prove those separate fixes all live in the very same kernel build. |
| Missing evidence | Source URL, exact branch/SHA, Linux sublevel, DTS/DTBO for actual begonia vs rosemary, defconfig, vendor base/Android version, compiler, boot/vendor ABI, reproducible build notes, source license and hardware matrix. |

**Critical technical point:** [LineageOS MT6785 Linux 4.19.325 kernel tree](https://github.com/LineageOS/android_kernel_xiaomi_mt6785) has a verified rosemary board DTS/defconfig. This **does not establish** that the author's claimed **begonia** forward-port uses the same exact tree or is publicly available. The author's own older [Power source](https://github.com/Saikrishna1504/kernel_xiaomi_mt6785) (checked main Makefile) was Linux **4.14.357-openela**, not a verified published 4.19 branch on 2026-11-21. See [03](03-KERNEL-HISTORY.md) and [22](22-KERNEL-FORWARD-PORT-AI-INTEGRITY-RU.md).

### Suggested short first DM in English (unsent)

Hi Sai! I saw your post in @RedmiNote8ProUpdates about getting Linux 4.19 running on the Redmi Note 8 Pro (begonia). Great to see the progress, especially the video playback fixes!

I'm researching begonia Linux ports (Ubuntu Touch/postmarketOS) and would love to study your approach and potentially help with testing. Would you be willing to share the kernel source repo/branch (or patches), defconfig/DTS, and which ROM/vendor base you tested? A link or the relevant commit SHA would be really helpful.

Thanks for your work!

### Optional technical follow-up if he responds positively (unsent)

Thank you! To reproduce this reliably, could you also share the precise kernel version and commit, the original 4.19 MT6785 base/fork, device-specific DTS/DTBO changes, compiler version, a link to any build instructions, matching boot image hashes, and known working/broken functions? I'm especially curious about display variants, charging/suspend, video playback, camera and radio. If the source is not public yet, is there a planned release and license? I can contribute reproducible tests and anonymized logs once a safe restore baseline is prepared.

## По-русски — контекст и запрос

**Автор:** @Saikrishna1504, [его профиль](https://t.me/saikrishna1504). **Канал:** [Redmi Note 8 Pro | UPDATES](https://t.me/s/RedmiNote8ProUpdates). **Дата:** вероятно **17 ноября 2026**, подтверждается только индексом стороннего TG.ME, время публикации и номер сообщения ещё не зафиксированы. Ранее в наших исследованиях ошибочно фигурировал сентябрь — это нужно исправлять при упоминании порта **4.19**. (Не путать с другой историей: Wi-Fi на ядре Linux 6.16.4 в отдельном проекте criollojoel10 действительно автором датирован **27 сентября 2026 года**.)

Разработчик заявляет, что запустил Linux 4.19 на begonia, тестировал около одной-двух недель, исправил воспроизведение видео и готов поделиться сборкой с участниками, которые смогут помочь тестированием. **Наличие открытого репозитория с этим конкретным портом пока не подтверждено.**

**Перевод первого сообщения для согласования:**

Привет, Сай! Я увидел твой пост в @RedmiNote8ProUpdates о запуске Linux 4.19 на Redmi Note 8 Pro (begonia). Здорово, что удалось добиться прогресса, особенно с исправлениями воспроизведения видео!

Я изучаю Linux-порты для begonia (Ubuntu Touch/postmarketOS), хотел бы разобраться в твоём подходе и, возможно, помочь с тестированием. Можешь поделиться ссылкой на исходники ядра и ветку (либо патчами), конфигурацией defconfig/DTS и информацией, на какой ROM/vendor-базе тестировалось ядро? Ссылка или SHA соответствующего коммита была бы очень полезна.

Спасибо за твою работу!

### Verification checklist after a reply

1. Link directly to the posted Telegram message and **save its unique post number/timestamp**. Do not infer it from adjacent posts.
2. Verify the reported repository and source commit with GitHub metadata; record license, fork origin and build configuration.
3. Compare with current 4.14 Power source, rosemary 4.19 tree and begonia DTS to understand exactly what changed.
4. Confirm results against a named ROM/kernel/vendor combination, logs, and hardware revision; no device-flashing before [18 — preflight](18-DEVICE-PREFLIGHT-READONLY.md).
5. If offered only a compiled image, request reproducible source/license and checksums before treating it as a usable project base. A private image is not evidence of public source release.

**Access / honesty:** original post text was indexed on the channel and on TG.ME. Full media, per-message permalink, all intermediate discussion and response from the developer **have not been collected or verified**. This is an outreach draft, not evidence that any message has been sent.
