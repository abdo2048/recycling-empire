# Cigarette butts — knowledge base

Case 1 of the Recycling Empire. Migrated from the [butt-lab](https://github.com/abdo2048/butt-lab)
archive at Phase 6 (2026-11-26); this folder is the canonical home. Work happens only inside this
folder (PLAYBOOK golden rule 2).

## What is here

A desk investigation into cigarette-butt recycling: **82 sourced documents**, **30 registered
methods**, **8 full action plans** (M-01-M-08), **1 invented route** (INV-01), and the **Phase 5
ranking** of 36 items on six factors with a test-first list — all under the Gap-fill labeling
system (`source_supported` / `ai_inference` / `ai_proposal` / `parameter_not_located`) and the
metals stop-condition (Cd/Pb/As/Hg uncharacterised = product-facing work on hold).

## Folder map

```
material.yaml      identity + version + priority methods + stop conditions
STATE.md           the resume file (2-minute resume test)
LOG.md             append-only session log
charter.md         research charter v2 (the gap-filling flip)
GLOSSARY.md        plain-words vocabulary
ranking.md         six-factor scoring matrix + test-first list
registry/          methods.yaml (30 entries) + methods-old.yaml (backup)
methods/           M-01..M-08 action plans + _cards.md (22 cards) + research/ (arena shelf)
inventions/        INV-01 split-loop refinery + hypotheses + batch-02 proposals + TEMPLATE
reports/final/     batch-01 synthesis + validation & open questions
sources/           INDEX.md (82 rows) + per-source SOURCE.md metadata
MIGRATION-NOTE.md  what moved, what stayed in the butt-lab archive, why
```

The heavy originals (document.pdf/html, text.md, figures/) live in the frozen
[butt-lab archive](https://github.com/abdo2048/butt-lab); see
[MIGRATION-NOTE.md](MIGRATION-NOTE.md). Site: [https://abdo2048.github.io/recycling-empire/](https://abdo2048.github.io/recycling-empire/)
(GitHub Pages from `docs/`, built by [tools/site-builder/build.py](../../../tools/site-builder/build.py)).

## Status

- Version **v0.8-migration** — Phases 1-5 complete, Phase 6 (site) built, **Phase 7 review rounds next**
  (INV-01's red-team section is intentionally empty and waits for them; ranking.md v0.1 is review-eligible).
- Stop-condition banner applies everywhere until product metals are measured: **one ICP-MS pass
  re-totals the top of the ranking table**.
