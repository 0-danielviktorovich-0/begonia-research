# Repository architecture RFC 001 — clean root, bilingual knowledge base and durable evidence

**Status: CORE MIGRATION IMPLEMENTED IN A REVIEW BRANCH (2026-11-21); archive/cache/agent directory relocation DEFERRED.** Research snapshot: 2026-11-21.  
**Languages:** [English (source)](repository-refactor-plan.md) · [Русский (summary)](../../ru/architecture/repository-refactor-plan.md).  
**Repository:** [begonia-research](https://github.com/0-danielviktorovich-0/begonia-research).

## Problem and verified starting point

The repository root currently contains **38 files**, including **25 numbered research reports (00–24)**, `README.md`, `README.ru.md`, `INDEX.md`, source JSON and five CSV matrices. There are additional `docs/en/README.md`, `docs/ru/README.md` and `00-README.md` (an executive summary). These are separate functions, but `README` naming makes them look like redundant project entry points. Existing agents and link targets expect many reports at root. A mechanical bulk move without updating consumers would break the repo.

### Design principles

1. **One canonical root README.md**: a short, English-first GitHub landing page, prominent English/Русский switch and project status. No `README.ru.md` at root after migration. The original executive report `00-README.md` is a numbered *research article*, not the repository README.
2. **Content by locale, then domain:** `docs/en/<domain>/<NN-topic>.md` and `docs/ru/<domain>/<NN-topic>.md`. Number `NN` is a stable legacy topic/article identifier; a URL/filename is not the permanent machine ID.
3. **Single authoritative original per topic:** a full translation must be pinned to an original Git Blob SHA. Reports 19–22 are originally in Russian, reports 00–18 and 23–24 originally in English. Translation status is *source*, *full-draft*, *full-reviewed*, *digest* or *directory-only*. Do **not** infer source language from destination directory.
4. **Canonical data, generated views:** sources, topic IDs, firmware and kernel matrices live under `data/`. The EN/RU navigation pages are human interfaces over that data, never independently diverging fact databases.
5. **Preserve provenance and history:** use Git moves (`git mv`), keep exact source URLs/commit SHAs, move raw captures separately from curated reports, preserve original blob licenses. Use a published old→new migration table.
6. **Reproducible tests before merges:** check link targets and headings, Markdown fences, JSON/CSV schemas, localized topic coverage, stale translations, original source revision and workflows. A green link check is *not* a human translation review.
7. **Avoid editing active agent-owned files** until collaborators have updated their paths. Read/write bots use a stable machine index as interface.

## Proposed eventual layout

```text
begonia-research/
├── README.md                    # SINGLE GitHub landing README, EN + RU links
├── LICENSE                      # code license
├── LICENSE-DOCS                 # documentation license
├── NOTICE.md                    # attribution / third-party notices
├── .github/
│   ├── workflows/              # multilingual link/anchor/schema CI
│   └── CODEOWNERS              # optional reviewer ownership
├── docs/
│   ├── en/
│   │   ├── index.md            # English subject/search entry
│   │   ├── android/            # MIUI, CFW, custom ROMs, root, GSI
│   │   ├── kernels/            # vendor kernels, 4.19, mainline, hardware
│   │   ├── linux/              # Ubuntu Touch, Droidian, postmarketOS
│   │   ├── recovery/           # bootloader, BROM, backups, preflight
│   │   ├── research/           # audited findings, sources, evidence, contacts
│   │   ├── tools/              # AI, NetHunter, reverse engineering
│   │   └── architecture/       # repository structure, contributor rules
│   └── ru/
│       ├── index.md            # Russian subject/search entry
│       └── ...                 # same subject taxonomy; only verified coverage
├── data/
│   ├── catalog/                # canonical topics/sources and machine index
│   └── matrices/               # firmware, kernel, hardware, root provenance
├── i18n/                       # locale policy, status, glossary, translators' QA
├── research/
│   ├── evidence/               # immutable source snapshots and archive metadata
│   ├── cache/                  # automated crawls; generated, disposable
│   └── agent/                  # mission history, requirements, coverage, context
└── tools/                      # validators and data/index generators
```

There is **no requirement** to store code for whole external vendor kernels here. Their exact GitHub URLs/refs/hashes and license data are recorded; clone/submodule only for a *separate licensed reproduction project* when required.

## Proposed destination map for all 25 existing numbered reports

| Existing ID(s) at repository root | New locale/domain path(s) | Original language |
|---|---|---|
| 00, 01, 09, 17, 23, 24 | `docs/en/research/<legacy-basename>.md` | EN |
| 02, 10 | `docs/en/android/<legacy-basename>.md` | EN |
| 03, 04, 11, 14 | `docs/en/kernels/<legacy-basename>.md` | EN |
| 05, 06, 08, 15 | `docs/en/linux/<legacy-basename>.md` | EN |
| 07, 18 | `docs/en/recovery/<legacy-basename>.md` | EN |
| 12 | `docs/en/tools/<legacy-basename>.md` | EN |
| 13, 16 | `docs/en/android/<legacy-basename>.md` | EN |
| 19 | `docs/ru/android/19-ROM-TERMS-GLOSSARY-RU.md` | RU |
| 20, 21, 22 | `docs/ru/kernels/<legacy-basename>.md` | RU |

Translation files already in `docs/en/` move into matching subject directories; the RU digest of report 24 moves to `docs/ru/research/`. Avoid moving historical articles multiple times: initially keep legacy basenames and stable IDs to reduce churn, then consider descriptive slugs in a later, separately tested release.

| Current extra entry or machine artifact | Target | Rule |
|---|---|---|
| `README.md` | `README.md` | Rewrite as short GitHub landing page, never move |
| `README.ru.md` | merge unique introductory content into `docs/ru/index.md`; then remove root copy | **Remove only once every internal reference and the English root language switch are updated** |
| `docs/en/README.md`, `docs/ru/README.md` | `docs/en/index.md`, `docs/ru/index.md` | Rename so `README` has one specific meaning |
| `INDEX.md` | `docs/en/index.md` + source topic index in `data/catalog/` | Extract unique material; don't maintain three hand-edited indexes |
| `index.json`, `sources.json` | `data/catalog/` | Consumers must be switched before deleting legacy paths |
| five root CSV matrices | `data/matrices/` | Preserve CSV column schema, stable IDs and citation fields |
| `archive/` | `research/evidence/` | Preserve original capture timestamps and checksums |
| `_cache/` | `research/cache/` | Only after Hermes/crawlers no longer write the old path |
| `_context/` | `research/agent/` | Migrate requirements/mission history and update agent bootstrap |
| `i18n/catalog.json`, `i18n/topics.json` | `i18n/` initially | Do not move before validators and translation source tracking are updated |

**Migration map** should be generated and published as `data/catalog/path-migrations.json` with fields `old_path`, `new_path`, `stage`, `status`, `checked_links`, `blob_sha_before`, `blob_sha_after`. Path redirects on GitHub `blob/main/<path>` are **not guaranteed** simply because Git detected a rename. Preserve historical links via documented mapping and, if a public docs website is introduced, explicit HTTP redirects. Temporary one-line stubs at the old locations are a valid compatibility stage but contradict the final clean-root requirement.

## Safe implementation stages (small, reviewable commits)

**Stage A — baseline, no moves.** Snapshot tree/HEAD, enumerate ALL local links (including code fences/HTML references), every file reference in JSON/CSV, README entries, workflows, Hermes instructions and archived indices. Pin the old→new mapping and freeze active writers for the migration window. Add tests that fail on missing paths/anchors and invalid metadata. Include `README.ru.md`, `INDEX.md`, numbered report IDs in scope.

**Stage B — one README, navigation first.** Create localized `docs/{lang}/index.md`; incorporate the unique RU landing content; replace all internal `README.ru.md` links and delete the redundant root file. Keep `README.md` short; point to topic directories and relevant source catalog. Separate `00-README.md` from root README concept.

**Stage C — research reports in one atomic tree commit.** Move numbered articles by the mapping above, then rewrite *all relative Markdown hrefs from both moved sources and unmoved referrers*, including `README`, `INDEX`, `_context`, old in-article links and translation crosslinks. Validate SHA/translation-state data; update metadata and previous-source link mappings **in the same commit**. Git history is preserved via rename detection; do not bulk regenerate report text beyond the link rewrites.

**Stage D — structured data and historical evidence.** Move CSV/JSON only after changing every machine path consumer and workflow. Archive and cache/agent relocation are last because they may be consumed by active scraping agents. Keep independent verification against the original `sources.json` URL set (currently 244 unique values, 43 topic IDs, 25 source documents as of this RFC).

**Stage E — CI/review and deprecation.** Run `tools/check_i18n.py`, link+anchor checker over all Markdown/HTML, JSON/CSV validators, source-URL dedupe, content-equivalence assertions, source Blob SHA pin checks and both language browse tests. Check existing GitHub Actions pattern triggers after paths move. Only merge after validation, then optionally eliminate compatibility stubs to achieve the final clean root.

## Architectural quality gates

- Every `i18n/catalog.json` original path and every locale entry is present; any translation `derived_from_blob` equals the CURRENT content-addressed original Git Blob SHA.
- `index.json` stable IDs exactly equal localized `topics.json` IDs, before and after moving under `data/catalog/`.
- Source-URL list has exactly the same set as the pre-migration snapshot (any additions reviewed separately); no lost images or external firmware links.
- All Markdown relative paths resolve to existing files; all local heading fragments resolve, including Cyrillic headings; code fences stay unmodified.
- Search and navigation work both from the single root README and from the two language indexes; English and Russian labels are correct, no false full-translation states.
- Old URLs are tracked in the migration manifest; no silent disappearance of unique text or attribution.
- Do not rewrite kernel-versus-device support claims simply while moving documents.

## Kernel 4.19 evidence (verified independently for this RFC)

- [LineageOS kernel `lineage-23.2/Makefile`](https://github.com/LineageOS/android_kernel_xiaomi_mt6785/blob/lineage-23.2/Makefile): `VERSION = 4`, `PATCHLEVEL = 19`, `SUBLEVEL = 325` — **Linux 4.19.325**.
- [LineageOS kernel `lineage-24.0/Makefile`](https://github.com/LineageOS/android_kernel_xiaomi_mt6785/blob/lineage-24.0/Makefile): also **Linux 4.19.325**.
- [LineageOS `rosemary_defconfig`](https://github.com/LineageOS/android_kernel_xiaomi_mt6785/blob/lineage-24.0/arch/arm64/configs/rosemary_defconfig) sets DTBO image names to `mediatek/rosemary`. The upstream [LineageOS device record for Redmi Note 10S, rosemary](https://github.com/LineageOS/lineage_wiki/blob/main/_data/devices/rosemary_variant1.yml) explicitly selects the MT6785 4.19 kernel. A large recursive tree listing was **truncated**, so do not claim absolute proof that no begonia-related file exists anywhere in the whole repo.
- [Saikrishna's begonia device tree](https://github.com/Saikrishna1504/device_redmi_begonia/blob/axion/BoardConfig.mk) uses the **k419** config and dated Nov 13–15 patch history (see [research 24](../research/24-SAIKRISHNA1504-DEVICE-STACK-AUDIT.md)); the public local manifest still pins a Power **4.14.357** kernel. **Hence confirmed 4.19 sources for MT6785 family + published begonia migration work do not automatically equal a complete, reproducible 4.19 begonia kernel source/binary**.

## Decision

**Recommend this layout**, but implement in the phased order above with a migration audit and tests, not by deleting/creating all root files manually in one uncontrolled session. This RFC is a design proposal; it does **not** claim that the root has already been cleaned. Preserve owner/Hermes works in progress and do not force-update branches.

Document version 1, 2026-11-21.
