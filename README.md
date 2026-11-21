# begonia-research

**Xiaomi Redmi Note 8 Pro · `begonia` · MediaTek Helio G90T / MT6785**

**Languages:** **[English — technical index](docs/en/index.md)** · **[Русский — каталог исследований](docs/ru/index.md)** · [Русский обзор проекта](docs/ru/overview.md)

Research and evidence index for porting **Ubuntu Touch, Droidian, postmarketOS, Halium and mainline Linux** to begonia, together with Android ROMs, kernels, recovery, vendor blobs and device security. This is a **research repository, not a ready-to-flash image**.

## Start here

- [Executive research summary](docs/en/research/00-README.md) — device fundamentals, findings, open limitations.
- [Master technical topic map](docs/en/research/master-topic-index.md) — precise topic → owner document + section navigation.
- [Primary sources & provenance](docs/en/research/01-SOURCES.md) — source dates, credibility, developer repositories.
- [November 2026 kernel/ROM source verification](docs/en/research/begonia-kernel-and-rom-evidence-2026-11.md) — pinned branches, Git SHAs, 4.14 vs. 4.19 findings.
- [Linux porting roadmap](docs/en/linux/08-DEVELOPMENT-ROADMAP.md) · [Ubuntu Touch](docs/en/linux/05-UBUNTU-TOUCH.md) · [mainline roadmap](docs/en/kernels/14-MAINLINE-UPGRADE-PATH.md).
- [Safety, recovery & preflight](docs/en/recovery/07-RECOVERY-SAFETY.md) · [Read-only device checks](docs/en/recovery/18-DEVICE-PREFLIGHT-READONLY.md).

## Repository layout

| Directory | Purpose |
|---|---|
| [`docs/en/`](docs/en/index.md) and [`docs/ru/`](docs/ru/index.md) | Language-based topical documentation; originals and translations are distinguished |
| [`data/catalog/`](data/catalog/) | Source/topic JSON, migration manifest and machine-readable indexes |
| [`data/matrices/`](data/matrices/) | Kernel, firmware, driver and developer-source comparison tables |
| [`i18n/`](i18n/README.md) | Translation review status, search labels, terminology and provenance |
| [`archive/`](archive/README.md) | Offline evidence copies; third-party copyright remains with original authors |
| [`_context/`](_context/CONTEXT.md), [`_cache/`](_cache/) | Original agent research context and captured material (relocation deferred) |
| [`tools/`](tools/README.md) | Validation, link audit and archive generation scripts |

## Evidence & caution

**Do not equate Android 16 / LineageOS 23.2 with Linux 4.19.** Public begonia kernel trees verified on 2026-11-21 include Linux **4.14**, while some 4.19 references concern configs or community-reported experimental ports. See the [pinned source audit](docs/en/research/begonia-kernel-and-rom-evidence-2026-11.md). No device was flashed by this research.

The previous root paths moved to `docs/` and `data/`. For old bookmarks, consult the [old→new path migration manifest](data/catalog/path-migrations.json); GitHub URL redirects are **not guaranteed**.

**Contributing:** keep English as the international default and Russian as a first-class language; always link original code, dates, SHAs, known limitations and translation states. Run `python3 tools/check_i18n.py` before sending changes.

## Licensing

Code: [MIT](LICENSE). Original research text/data: [CC BY-SA 4.0](LICENSE-DOCS). Third-party source captures are not relicensed; see [NOTICE](NOTICE.md).
