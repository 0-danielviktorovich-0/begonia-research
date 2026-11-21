# Localization and translation policy — begonia-research

**Language entry points:** [English](../docs/en/index.md) · [Русский](../docs/ru/index.md). Machine registries: [catalog.json](catalog.json), [topics.json](topics.json).

## 1. Supported languages and content policy

- The repository's **default international UI, machine identifiers and future documentation language is English (en)**. Every original research topic remains readable in its original language.
- **Russian (ru) is a first-class supported language**: a complete navigable directory, localized titles, search terms, controlled vocabulary, and explicitly declared translation coverage.
- **Legacy source-language exception:** chapters 19–22 were authored in Russian first. They remain authoritative technical originals **until** a full English translation is completed and independently reviewed. Do not silently switch the source of truth or discard the Russian text.
- Chapters 00–18 were authored in English. The Russian navigation is available now; a full technical RU translation is *not* implied by localized titles or abstracts.
- A mixed-language document with a few headings translated is not a "full translation".
- **No personal device information:** neither locale includes real IMEI, serials, NVRAM, tokens, credentials or identifying logs. Bilingual text is not "personal data" replication; keep it documentation only.

The clean-root, bilingual repository layout is **already in use**. The [EN architecture plan](../docs/en/architecture/repository-refactor-plan.md), [RU architecture plan](../docs/ru/architecture/repository-refactor-plan.md), and [old→new file manifest](../data/catalog/path-migrations.json) document the completed migration and its original paths.

## 2. File layout and stable IDs

- Root: a short international **[README.md](../README.md)**, licenses and the project notice. Long technical chapters live under [docs/en/](../docs/en/index.md) or [docs/ru/](../docs/ru/index.md), grouped by domain.
- Language indexes: **[docs/en/index.md](../docs/en/index.md)** and **[docs/ru/index.md](../docs/ru/index.md)**; each topic is discoverable in both languages, even when its full translation is still pending.
- Full translated chapters and shorter digests live within `docs/{lang}/{domain}/`. Chapter 19 has a full English translation draft; English pages for chapters 20–22 are digests, **not full translations**.
- **[catalog.json](catalog.json)** records source language, source Git Blob SHA when known, localized pages, translation coverage, and review state.
- **[topics.json](topics.json)** uses the same stable topic IDs as **[data/catalog/index.json](../data/catalog/index.json)** and supplies localized names, search aliases, and source pointers. Search labels do not copy the underlying technical claims.
- Machine IDs remain **lowercase ASCII / kebab-case** and are **never translated**. Changes to stable file paths require updating links, indexes and the migration map.
- Preserve external source URLs and GitHub permalinks; ensure all **relative Markdown links and section anchors** resolve to the relocated pages.

## 3. Professional translation requirements

For every full translation:

1. **Semantic completeness:** every section, heading, table row, list item, number, qualification, uncertainty marker, risk note and primary-source citation must be preserved. Do not add undocumented performance or compatibility guarantees.
2. **Technical integrity:** preserve version numbers, kernel flags (CONFIG_*), filesystem paths, commit SHA, device codenames (begonia, rosemary), recovery partition names, command arguments, error messages, code snippets and names of upstream projects exactly. Translate *surrounding explanations*, not commands.
3. **Terminology:** consult [TERMINOLOGY.md](TERMINOLOGY.md). Translate natural-language descriptions; retain internationally searchable aliases on first use: e.g. загрузчик (bootloader), дерево устройств (Device Tree), исходники ядра (kernel source).
4. **Style:** English concise and technically precise; Russian idiomatic professional Russian, not literal calques. Avoid unsupported absolutes: “works on all devices”, “bricked phones are always recoverable”, “root never detected”.
5. **Evidence preservation:** maintain direct links, original post numbers, dates, [V]/[D]/[I]/[U] confidence labels and **reporting distinctions** (upstream claim vs firsthand test vs independent reproduction). Do not convert historical mentions into present-tense capabilities.
6. **Markdown QA:** internal and external link targets; fenced code; headings; tables, Unicode UTF-8, anchors; no malformed local links after path relocation.
7. **Bilingual discoverability:** titles, table-of-contents labels and searchable aliases should be localized; search by hardware identifiers should return the same topic in both languages.
8. **License/attribution:** translations of our text follow LICENSE-DOCS (CC BY-SA 4.0); quotations remain attributed to their owners. Do not copy large passages of outside forum material in translation.
9. **Review:** compare source and translation paragraph-by-paragraph; verify all numeric claims, exact code snippets and citations; if not reviewed, mark it **draft** and clearly label that on the page.
10. **Source drift:** record the SHA-1 **Git Blob ID** (not commit SHA) of the source file used for translation. If it changes, translation becomes **outdated** until diffs are reviewed. This check can run automatically via scripts.

## 4. Translation-state vocabulary (no implicit completion)

- **source**: original, authoritative full technical text in that language.
- **full-draft**: full translation prepared, not fully human/technical reviewed; content should remain labelled as draft.
- **full-reviewed**: fully checked against a specific source blob and accepted.
- **digest**: useful localized technical abstract/landing page; explicitly **not** a translation of every paragraph.
- **directory-only**: localized title and descriptive index entry linked to a full report in another language.
- **missing**: no localized material yet. Do not fabricate a page or report a translation as done.

Only **source** and **full-reviewed** may be described as complete and technically reviewed. A full-draft page should state its reviewer status and revision.

## 5. Workflow for an AI contributor

1. Read [CONTEXT.md](../_context/CONTEXT.md), this policy, [TERMINOLOGY.md](TERMINOLOGY.md), [catalog.json](catalog.json) and the corresponding original file. A translator **must not** use a short digest as the only source for a full translation.
2. Choose one topic ID. Pin exact source Git Blob SHA and last observed research source dates; write to its canonical locale path.
3. Draft the **complete** translation with matching section numbers and preserved table dimensions. If not complete, publish as **digest**, not as full.
4. Run spelling/terminology, compare critical figures and source URLs. Keep a list of unresolved ambiguities and technical claims that need an expert.
5. Validate with [check_i18n.py](../tools/check_i18n.py). Status becomes **full-reviewed** only after content-level review, not because CI passes.
6. Update catalog/topics, both language directories, README language switch; add a changelog entry when changing a reviewed translation. Avoid gratuitous edits to original evidence documents solely to reorganize translations.
7. When the original changes, mark affected translation stale; no automatic silent updates of translations without human review.

## 6. Quality gates

A scheduled or pull-request check can validate JSON schema-ish integrity, path existence, stable-ID uniqueness, language switch targets, source SHA currency and local Markdown links. **CI cannot determine whether a translation is idiomatic or factually equivalent**; reviewer evidence must be recorded separately.

**Scope:** this is a foundation for multilingual documentation. It does **not** claim that all research chapters have already received complete two-language translations.

Established: 2026-11-21. Project language codes: BCP 47 en / ru.
