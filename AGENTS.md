# Instructions for AI coding and research agents

This repository is a **research and evidence knowledge base** for Redmi Note 8 Pro / begonia / MT6785, not a flashable ROM or live device controller. Treat `README.md`, [the evidence contract](_context/CONTEXT.md), [requirements](_context/REQUIREMENTS.md), [tool policy](tools/README.md), and [the English index](docs/en/index.md) as authoritative entry points. English is the main international technical language; Russian is first-class; label English digests, full translations and originals accurately.

## First read for kernel work

1. [Kernel Lab architecture](docs/en/tools/kernel-lab-autonomous-debugging.md) and [bounded agent mission](docs/en/tools/kernel-lab-agent-mission.md).
2. [Recovery safety](docs/en/recovery/07-RECOVERY-SAFETY.md) and [read-only inventory](docs/en/recovery/18-DEVICE-PREFLIGHT-READONLY.md).
3. Exact device kernel and recovery source history, branches and evidence.
4. The **official upstream Linux** [AI coding assistant policy](https://github.com/torvalds/linux/blob/master/Documentation/process/coding-assistants.rst), [coding style](https://docs.kernel.org/process/coding-style.html), and [patch submission guide](https://docs.kernel.org/process/submitting-patches.html) when working on upstream-bound patches. An AI must never forge a human `Signed-off-by` / DCO.

## Non-negotiable engineering rules

- Distinguish **VERIFIED SOURCE**, **HOST-TESTED**, **DEVICE-TESTED**, **INFERRED**, and **UNKNOWN**. Add source URLs, date, branch, commit SHA and limitations; never invent working hardware capabilities.
- One canonical fact per owner document. Link rather than copy; put machine-readable matrices under `data/` and indexed documentation under `docs/en/` or `docs/ru/`.
- Do not confuse an Android version with kernel version. The tested Axion 2.9 NOESIS boot on Linux 4.19.325 is a device observation; its exact public reproducible source is still unverified in this repo.
- **No unapproved writes to an actual device:** no flashing, formatting, erasing, unlocking, AVB/anti-rollback changes, bootloader exploits or partition writes. Read-only inventory and isolated mocked tests are the default. A separate explicit user authorization and a human-reviewed Hardware Test Gate are necessary before any dangerous operations.
- Never erase/reset raw crash logs before a hash-verified first-failure capture. Crash data may contain private material; do not upload raw dumps or device identifiers to public issues, logs or model prompts by default.
- Preserve a known-good recovery/boot image and exact source/build manifest. Do not treat compilation success as boot success.
- Prefer deterministic scripts with bounded retries, an emergency stop, dry-run and explicit reasoned failures. A connector or agent must not have unrestricted root access to the host or arbitrary USB ports.
- No arbitrary kernel memory addresses, unchecked UART voltage assumptions, hidden production debug interfaces, blind Kconfig dependency enabling or universal BROM unbrick guarantees.
- Never place secrets, auth tokens, sensitive serials, personal file paths or private crash dumps in committed docs.

## Git and quality

Use a dedicated branch and reviewable PR for research. Keep only the expected files in scope, record commands/output and report unverified areas. Run existing repository audits / i18n checks where available. Do not silently alter source-derived facts or overwrite other agents' work. The single-writer principle from `tools/README.md` applies.

**Task entry:** [Kernel Lab agent mission](docs/en/tools/kernel-lab-agent-mission.md).