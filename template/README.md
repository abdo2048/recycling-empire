# <Material name> — knowledge base

Cloned from `/template` at Phase 0. Work happens only inside this folder (PLAYBOOK golden rule 2).

## AI checklist (do in order)

1. Fill `material.yaml` (name, slug, created, version v0.0).
2. Initialize `STATE.md` (phase 0) and `LOG.md`.
3. Follow `/PLAYBOOK.md` phases 1-5. After every session, update STATE.md (before you stop) and append 1-3 lines to LOG.md.
4. Obey the golden rules and content labels in the PLAYBOOK; they bind every file you write.
5. When phases 1-5 are complete: set version `v1.0-candidate` in STATE.md and stop. Review rounds (Phase 7) are run by the operator.

## Folder map

```
sources/        one folder per source (document.pdf + text.md + SOURCE.md)
methods/        M-XX action plans + _cards.md summary cards
inventions/     INV-XX the AI's own methods
reviews/        round-N review folders (Phase 7)
proposals/      reviewer drafts in quarantine
lab-findings/   team experiment results (first-class evidence)
REGISTRY.md     one append-only entry per method
ranking.md      the six-factor scoring matrix + test-first list
material.yaml   identity + version metadata
STATE.md        the resume file (2-minute resume test)
LOG.md          append-only session log
```
