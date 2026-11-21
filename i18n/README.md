# Localization and translation policy — begonia-research

**Language entry points:** [English](../docs/en/README.md) · [Русский](../docs/ru/README.md). Machine registries: [catalog.json](catalog.json), [topics.json](topics.json).

## 1. Terminology

- **i18n** (*internationalization*, i + 18 letters + n): engineer a knowledge base so more than one language can be supported.
- **l10n** (*localization*, l + 10 letters + n): adapt the actual text, terminology, search metadata and links to each language.
- **n8n** is an automation/orchestration product, *not* the name of the translation architecture. It could optionally automate synchronization, but is not required.
- **t9n** can informally mean translation, but is not a substitute for i18n/l10n workflow controls.

## 2. Language contract

- The repository's **default international UI, machine identifiers and future documentation language is English (en)**. Every original research topic remains readable in its original language.
- **Russian (ru) is a first-class supported language**: a complete navigable directory, localized titles, search terms, controlled vocabulary, and explicitly declared translation coverage.
- **Legacy source-language exception:** chapters 19–22 were authored in Russian first. They remain authoritative technical originals **until** a full English translation is completed and independently reviewed. Do not silently switch the source of truth or discard the Russian text.
- Chapters 00–18 were authored in English. The Russian navigation is available now; a full technical RU translation is *not* implied by localized titles or abstracts.
- A mixed-language document with a few headings translated is not a "full translation".
- **No personal device information:** neither locale includes real IMEI, serials, NVRAM, tokens, credentials or identifying logs. Bilingual text is not "personal data" replication; keep it documentation only.

## 3. File layout, migration and stable IDs

- Root: **README.md (EN)**, **README.ru.md (RU)**, existing original reports 00–22, INDEX.md/index.json and sources.json.
- Human indexes: **docs/en/README.md** and **docs/ru/README.md**; each topic is discoverable in both languages even if its full translation is pending.
- Full translations: **docs/{lang}/{id}-{stable-slug}.md**; English translation of chapter 19 is the first exemplar.
- English digests for Russian originals (20–22) are in docs/en/; they carry prominent **DIGEST, NOT FULL TRANSLATION** notices and direct links to originals.
- **catalog.json**: one entry per original report; original-language, Blob SHA of the source snapshot when known, all localized pages, translation status, review state.
- **topics.json**: human-friendly titles/search aliases for every existing stable topic ID from root index.json, with the same IDs and original document pointers. These labels are not copies of the underlying claims.
- Machine identifier format remains **lowercase ASCII / kebab-case** and is **never translated**. Filenames and Git refs are immutable interface identifiers. Changing a slug requires redirect or compatibility alias.
- **Absolute URLs** and GitHub issue permalinks are preserved; adjust **relative Markdown links** after moving a translated page to docs/en or docs/ru.

## 4. Professional translation requirements

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

## 5. Translation-state vocabulary (no implicit completion)

- **source**: original, authoritative full technical text in that language.
- **full-draft**: full translation prepared, not fully human/technical reviewed; content should remain labelled as draft.
- **full-reviewed**: fully checked against a specific source blob and accepted.
- **digest**: useful localized technical abstract/landing page; explicitly **not** a translation of every paragraph.
- **directory-only**: localized title and descriptive index entry linked to a full report in another language.
- **missing**: no localized material yet. Do not fabricate a page or report a translation as done.

Only **source** and **full-reviewed** may be described as complete and technically reviewed. A full-draft page should state its reviewer status and revision.

## 6. Workflow for an AI contributor

1. Read [CONTEXT.md](../_context/CONTEXT.md), this policy, [TERMINOLOGY.md](TERMINOLOGY.md), [catalog.json](catalog.json) and the corresponding original file. A translator **must not** use a short digest as the only source for a full translation.
2. Choose one topic ID. Pin exact source Git Blob SHA and last observed research source dates; write to its canonical locale path.
3. Draft the **complete** translation with matching section numbers and preserved table dimensions. If not complete, publish as **digest**, not as full.
4. Run spelling/terminology, compare critical figures and source URLs. Keep a list of unresolved ambiguities and technical claims that need an expert.
5. Validate with [check_i18n.py](../tools/check_i18n.py). Status becomes **full-reviewed** only after content-level review, not because CI passes.
6. Update catalog/topics, both language directories, README language switch; add a changelog entry when changing a reviewed translation. Avoid gratuitous edits to original evidence documents solely to reorganize translations.
7. When the original changes, mark affected translation stale; no automatic silent updates of translations without human review.

## 7. Quality gates

A scheduled or pull-request check can validate JSON schema-ish integrity, path existence, stable-ID uniqueness, language switch targets, source SHA currency and local Markdown links. **CI cannot determine whether a translation is idiomatic or factually equivalent**; reviewer evidence must be recorded separately.

**Scope:** this is a foundation for multilingual documentation. It does **not** claim that all 23 long reports have already received complete two-language translations.

Established: 2026-11-21. Project language codes: BCP 47 en / ru.
