# Reconciliation of concurrent main history before refactor merge (2026-11-21)

The original refactor was based on Git commit `563a710658a6600896809fc0bbc21b84f768d6b0`. Before merging PR #4, `main` advanced to `b28589a677ec7472aa7d847f67e1b7a76abd7a3b` (16 additional commits). The comparison showed changes in exactly five tracked paths. A two-parent merge of the latest main history into the refactor branch retains **both** histories, with conflict resolution in the refactored tree.

| Changed path on concurrent main | Resolution in the cleaned structure |
|---|---|
| `03-KERNEL-HISTORY.md` | Integrated the updated moved-source and Linux 4.19 provenance caveat into [kernel history](../kernels/03-KERNEL-HISTORY.md) |
| `16-ROOT-METHODS.md` | Integrated new direct-evidence details while retaining the separate NoMount/Play Integrity caveats in [root methods](../android/16-ROOT-METHODS.md) |
| `20-KERNEL-419-ROOT-ECOSYSTEM-RU.md` | The new main contained unresolved Git conflict markers; kept the clean, locally linked [Russian source document](../../ru/kernels/20-KERNEL-419-ROOT-ECOSYSTEM-RU.md). Historical alternatives remain accessible in Git history |
| `INDEX.md` | The new main contained nested conflict markers; retained the complete [clean master index](master-topic-index.md) and integrated Russian root/kernel links |
| `README.md` | Preserved new Russian root-provenance navigation in the [clean landing page](../../../README.md) |

The automatic migration audit compares all 41 moved files and pre-refactor blobs against the pinned original Git commit. Seven byte-identical historical navigation and source snapshots are preserved in [archive/legacy](../../../archive/README.md). CI also rejects unresolved Git conflict markers in active Markdown. External URL reachability and device flashing are outside these checks.
