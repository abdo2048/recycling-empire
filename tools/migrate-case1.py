#!/usr/bin/env python3
"""Migrate case 1 (cigarette butts) from the butt-lab archive into materials/cigarette-butts/.

One-time, idempotent migration executed by .github/workflows/site.yml (and runnable locally):
    python3 tools/migrate-case1.py /path/to/butt-lab-clone /path/to/recycling-empire

Moves the full TEXT knowledge base (plans, invention, ranking, registry, research shelf,
source metadata) byte-exact from butt-lab, performs the STATE/LOG migration surgery,
adds the missing INDEX row, and writes the material identity files. Heavy originals
(546 MB of document.pdf/html, text.md, figures/) stay in butt-lab — the frozen archive
that every site page links into. See materials/cigarette-butts/MIGRATION-NOTE.md.
"""
import os
import re
import shutil
import sys

BL = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "/tmp/butt-lab")
REPO = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else ".")
MAT = os.path.join(REPO, "materials", "cigarette-butts")

MATERIAL_YAML = '''# Material identity — filled at Phase 0 (2026-11-22 in butt-lab), migrated to this repo at Phase 6
name: "Cigarette butts"
slug: cigarette-butts
created: "2026-11-22"
status: active
version: v0.8
site_url: "https://abdo2048.github.io/recycling-empire/"  # live once GitHub Pages is enabled (Settings → Pages → Source: main, folder /docs); Cloudflare Pages with output dir docs/ works identically
priority_methods: [M-01-mego-wash, M-02-defenzo-solvent, M-03-unb-alkaline-pulping, M-04-keenat-dry-thermal, M-05-tchaomegot-sc-co2, M-06-terracycle-trade-secret, M-07-pyrolysis-triacetin, M-08-rmit-brick]
custom_ranking_factors: []  # the six standard factors are used as-is (see ranking.md)
stop_conditions:
  - "Metals gate (charter): Cd/Pb/As/Hg uncharacterised in a route's product means that route is on hold for product-facing work. M-08 fired bricks hold the only published pass (Kurmus Ch.5 leaching + Ch.6 PAH gates)."
  - "No physical trials (PLAYBOOK rule 7): desk research authorizes none; qualified facilities, risk assessment, lawful disposal and a named human actor are required for anything physical."
'''

MATERIAL_README = '''# Cigarette butts — knowledge base

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
'''

MIGRATION_NOTE = '''# Migration note — cigarette-butts → recycling-empire (Phase 6, 2026-11-26)

Case 1 completed its research in the [butt-lab](https://github.com/abdo2048/butt-lab) repository
(sessions 1-10, Phases 1-5) and this folder is now its **canonical home**. One repo, one site
(PLAYBOOK golden rule 1): from now on, work happens only here, and the unified site is built
from `materials/` by [tools/site-builder/build.py](../../../tools/site-builder/build.py).

## What moved here

The entire text knowledge base, byte-exact from butt-lab:

| Content | Files |
| --- | --- |
| Identity + state | `material.yaml`, `STATE.md`, `LOG.md`, `README.md`, `MIGRATION-NOTE.md` |
| Rules + vocabulary | `charter.md` (v2), `GLOSSARY.md` |
| Phase 5 ranking | `ranking.md` (36 items, six factors, test-first list) |
| Phase 2 registry | `registry/methods.yaml` (30 entries, sync-corrected) + `registry/methods-old.yaml` (immutable backup) |
| Phase 3 action plans | `methods/M-01` … `methods/M-08` (v0.1-v0.5) + `methods/_cards.md` (22 cards) |
| Arena research shelf | `methods/research/2026-11-25-arena/` — FINDINGS 1/2, MANIFEST, README, 5 transcripts, 3 csv |
| Phase 4 invention | `inventions/INV-01-split-loop-refinery.md` + candidate hypotheses + batch-02 proposals + TEMPLATE |
| Final reports | `reports/final/batch-01-synthesis.md`, `reports/final/validation-and-open-questions.md` |
| Source metadata | `sources/INDEX.md` (82 rows — one row added for defenzo-2020-materials during migration), `sources/README.md`, `sources/links.json`, and all 32 `sources/<id>/SOURCE.md` files |

Migration content fixes (recorded in the INDEX footer): the `espr-2021-challenges-review` row
pointed at a stale `ese-2021-challenges-review/` folder name (a butt-lab-era defect) and
`defenzo-2020-materials` had a folder + SOURCE.md but no INDEX row — both corrected during
migration; count corrected 81 → 82.

## What stayed in butt-lab (the frozen archive)

The heavy shelf cannot travel through the API-based migration path (per-file push limit ~1 MB;
the archive is 546 MB). It stays in [butt-lab](https://github.com/abdo2048/butt-lab), which is
now a **read-only archive**:

- `sources/<id>/document.pdf` / `document.html` — the originals (humans read these)
- `sources/<id>/text.md` — the AI-readable conversions (4.7 MB)
- `sources/<id>/figures/` — extracted images
- `methods/research/2026-11-25-arena/attempts/` + `cdx/` — raw fetch artifacts behind the FINDINGS
- `publication/` — the old reader's data layer (superseded by the unified site)
- all historical dirs (`archive/`, `docs/`, `state/`, `tools/`, `mcp/`, `operator/`, …)

Every migrated file and every generated site page resolves links into the archive:
originals link to `https://github.com/abdo2048/butt-lab/tree/main/<path>` and AI-readable text
links to `https://raw.githubusercontent.com/abdo2048/butt-lab/main/<path>`. The builder does
this rewrite automatically (see `tools/site-builder/build.py`).

## Why this split is safe

- The **record of knowledge** (plans, rankings, registry, invention, reports, source metadata) is
  complete here and self-contained — nothing on the site needs the binaries to be understood.
- The **originals** are immutable published documents; a frozen public archive repo is a stable
  link target, and each document also exists in a second copy under the operator's control
  (butt-materials / local machine).
- If a full byte-level move is ever wanted, a single local operation completes it:
  `git clone https://github.com/abdo2048/butt-lab && cp -r butt-lab/sources/* recycling-empire/materials/cigarette-butts/sources/` —
  the builder already handles both layouts (it links locally when a file exists in the folder).

## Reader retirement

The old reader at `https://butt-lab.am6.workers.dev/` (Cloudflare Worker over `publication/`)
is superseded by the unified site. Decommissioning the Worker is an operator step: it serves a
frozen snapshot and stays up until the operator switches it off. [MATERIALS.md](../../../MATERIALS.md)
records the change.
'''

STATE_EDITS = [
    ("# STATE — cigarette-butts (case 1; lives in butt-lab until migration to recycling-empire)",
     "# STATE — cigarette-butts (materials/cigarette-butts/ in recycling-empire; migrated from butt-lab 2026-11-26)"),
    ("Updated: 2026-11-26 (session 10) | Phase: 5 complete (ranking.md + registry pass) | Version: v0.8-pre-migration",
     "Updated: 2026-11-26 (session 11) | Phase: 6 complete (migration + unified site build) | Version: v0.8-migration"),
    ("Nothing mid-flight. Session 10 completed Phase 5: ranking.md written (36 items scored on the six standard factors), test-first list fixed, registry/methods.yaml corrections pass applied (cards-ledger queue + status syncs; validator constraints respected). Phase 6 next — migration to recycling-empire/materials/cigarette-butts/.",
     "Nothing mid-flight. Session 11 executed Phase 6: the finished material migrated to recycling-empire/materials/cigarette-butts/ (the full text knowledge base), the unified static site built (tools/site-builder/build.py -> docs/, design per SITE-DESIGN.md: Inter + Fraunces, label chips, client-side search), and the old butt-lab reader marked retired pending Worker decommission. Heavy source originals (546 MB of document.pdf/html, text.md, figures/) remain in butt-lab as the frozen archive; every migrated file and every site page links into it (see MIGRATION-NOTE.md)."),
    ("## Done\n- Phase 1 (2026-11-22)",
     "## Done\n- 2026-11-26 (session 11): **Phase 6 — migration + unified site.** materials/cigarette-butts/ created in recycling-empire: material.yaml filled; charter, GLOSSARY, ranking, registry/methods.yaml (+methods-old backup), M-01..M-08 + _cards.md, INV-01 + candidate-hypotheses + batch-02 proposals + TEMPLATE, reports/final pair, arena research shelf (FINDINGS 1/2 + MANIFEST + README + 5 transcripts + 3 csv), sources/INDEX + README + links.json + all 32 SOURCE.md metadata files. INDEX defects fixed in passing (stale ese-2021 folder link; missing defenzo row; count 81 -> 82). SITE-DESIGN.md written (IA, navigation, reading journey, Inter + Fraunces typography, no-mono rule, label color system, accessibility). Site builder tools/site-builder/build.py renders all materials/ into docs/ (~110 pages, client-side search). Deploy = GitHub Pages from docs/ or Cloudflare Pages output dir docs/; old reader superseded (Worker decommission is an operator step).\n- Phase 1 (2026-11-22)"),
    ("""## Next up (in order)
1. Phase 6 — migrate finished material to recycling-empire/materials/cigarette-butts/; build unified site; retire old reader
2. Phase 7 — review rounds after the build (INV-01's red-team section is intentionally empty and waits for these; ranking.md v0.1 is review-eligible too)
3. Optional pre-migration checks: sources/INDEX.md final sort pass; registry/methods-old.yaml untouched (immutable backup)""",
     """## Next up (in order)
1. Operator: enable GitHub Pages (Settings -> Pages -> Source: main, folder /docs) or point Cloudflare Pages at the repo with output dir docs/ — the site then goes live at the material.yaml site_url
2. Operator: decommission the old reader worker butt-lab.am6.workers.dev (superseded by the unified site)
3. Phase 7 — review rounds after the build (INV-01's red-team section is intentionally empty and waits for these; ranking.md v0.1 is review-eligible too)
4. Future materials start from START-A-NEW-MATERIAL.md in recycling-empire"""),
    ("""## Where things live (this repo, transitional)
sources/ | registry/methods.yaml | reports/final/ | inventions/ | methods/ (M-01..M-08 + _cards.md) | ranking.md | GLOSSARY.md | charter.md
System + template: https://github.com/abdo2048/recycling-empire (PLAYBOOK.md)
Historical provenance — do NOT read to resume: archive/, docs/, state/, tools/, mcp/, .superpowers/, operator/, reports/ (except final/), .github/workflows""",
     """## Where things live (post-migration)
Canonical home: this folder (materials/cigarette-butts/ of recycling-empire) — charter, GLOSSARY, ranking, registry/, methods/ (M-01..M-08 + _cards.md + research/), inventions/, reports/final/, sources/ (INDEX + README + links.json + per-source SOURCE.md metadata), STATE/LOG, MIGRATION-NOTE.
Frozen archive (originals): https://github.com/abdo2048/butt-lab holds the heavy shelf (82 x document.pdf/html, text.md, figures/, publication/, historical dirs). Site pages and migrated files link into it; butt-lab is read-only from now on.
Site: docs/ in recycling-empire, built by tools/site-builder/build.py, design spec in SITE-DESIGN.md.
Historical provenance — do NOT read to resume: butt-lab archive/, docs/, state/, tools/, mcp/, .superpowers/, operator/, reports/ (except final/), .github/workflows"""),
]

LOG_APPEND = ("\n- 2026-11-26 | Phase 6 (session 11) | Migration executed: the material text knowledge base moved to "
              "recycling-empire/materials/cigarette-butts/ (charter, glossary, ranking, registry, M-01..M-08 + cards, "
              "INV-01 + hypotheses + batch-02, reports/final, arena research shelf, sources INDEX/README/links + 32 "
              "SOURCE.md). Heavy originals (546 MB) stay in butt-lab as the frozen archive and are linked from the "
              "site (MIGRATION-NOTE.md). INDEX defects fixed in passing (stale ese-2021 link; missing defenzo row; "
              "81 -> 82). Unified site built by tools/site-builder/build.py -> docs/ (Inter + Fraunces, no mono; "
              "label chips; material dashboard; client-side search). SITE-DESIGN.md records the UI/UX plan. Old "
              "reader marked retired; Worker decommission is an operator step. Phase 7 next.\n")


def main():
    assert os.path.isdir(os.path.join(BL, "sources")), f"butt-lab clone not found at {BL}"
    os.makedirs(MAT, exist_ok=True)

    def cp(src_rel, dst_rel=None):
        s = os.path.join(BL, src_rel)
        d = os.path.join(MAT, (dst_rel or src_rel).replace("/", os.sep))
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(s, d)

    # 1. text knowledge base
    for f in ["charter.md", "GLOSSARY.md", "ranking.md"]:
        cp(f)
    cp("registry/methods.yaml")
    cp("registry/methods-old.yaml")
    for f in sorted(os.listdir(os.path.join(BL, "methods"))):
        if f.endswith(".md"):
            cp(f"methods/{f}")
    R = "methods/research/2026-11-25-arena"
    for sub in ["FINDINGS.md", "FINDINGS-2.md", "MANIFEST.md", "README.md"]:
        cp(f"{R}/{sub}")
    for t in ["arena_agent.md", "arena_gpt_luna_search.md", "kimi3_nvidia.md", "obsidian as website.md", "qwen.md"]:
        cp(f"{R}/transcripts/{t}")
    for c in ["brigade_totals_growth_curve.csv", "mass_figures.csv", "butt_mass_triangulation.csv"]:
        cp(f"{R}/csv/{c}")
    for f in ["INV-01-split-loop-refinery.md", "TEMPLATE.md", "candidate-hypotheses-01.md",
              "scientist-inventor-batch-02-proposals.md"]:
        cp(f"inventions/{f}")
    cp("reports/final/batch-01-synthesis.md")
    cp("reports/final/validation-and-open-questions.md")
    cp("sources/INDEX.md")
    cp("sources/README.md")
    cp("sources/links.json")
    n_src = 0
    for root, dirs, files in os.walk(os.path.join(BL, "sources")):
        for f in files:
            if f == "SOURCE.md":
                cp(os.path.relpath(os.path.join(root, f), BL))
                n_src += 1

    # 2. INDEX fixes (stale folder link; missing defenzo row; count)
    idx_path = os.path.join(MAT, "sources", "INDEX.md")
    idx = open(idx_path, encoding="utf-8").read().replace("ese-2021-challenges-review", "espr-2021-challenges-review")
    idx = idx.replace("81 documents, one folder each", "82 documents, one folder each")
    defrow = "| `defenzo-2020-materials` | — (original not yet shelved; open access via PMC, see SOURCE.md) | — | — |\n"
    m = re.search(r"(\| `cu2o-ag2moo4-2024-photocatalyst`[^\n]*\n)", idx)
    if m and "`defenzo-2020-materials` |" not in idx:
        idx = idx[:m.end()] + defrow + idx[m.end():]
    idx += ("\n_Session 11 (migration, 2026-11-26): 3 stale folder links corrected "
            "(ese-2021-challenges-review -> espr-2021-challenges-review); the heavy originals now live in "
            "the frozen butt-lab archive and all site pages link there. Row added for `defenzo-2020-materials` "
            "(folder + SOURCE.md existed since session 2 but the row was missing; original not yet shelved). "
            "Count corrected 81 -> 82._\n")
    open(idx_path, "w", encoding="utf-8").write(idx)

    # 3. STATE.md surgery
    state = open(os.path.join(BL, "STATE.md"), encoding="utf-8").read()
    for old, new in STATE_EDITS:
        assert old in state, f"STATE anchor not found: {old[:60]!r}"
        state = state.replace(old, new)
    open(os.path.join(MAT, "STATE.md"), "w", encoding="utf-8").write(state)

    # 4. LOG.md append
    log = open(os.path.join(BL, "LOG.md"), encoding="utf-8").read().rstrip("\n")
    log += LOG_APPEND
    open(os.path.join(MAT, "LOG.md"), "w", encoding="utf-8").write(log)

    # 5. identity files
    open(os.path.join(MAT, "material.yaml"), "w", encoding="utf-8").write(MATERIAL_YAML)
    open(os.path.join(MAT, "README.md"), "w", encoding="utf-8").write(MATERIAL_README)
    open(os.path.join(MAT, "MIGRATION-NOTE.md"), "w", encoding="utf-8").write(MIGRATION_NOTE)

    total = sum(os.path.getsize(os.path.join(r, f)) for r, d, fs in os.walk(MAT) for f in fs)
    print(f"migration OK: {n_src} SOURCE.md files, material folder {total / 1024:.0f} KB")


if __name__ == "__main__":
    main()
