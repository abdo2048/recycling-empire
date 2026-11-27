# Migration note — cigarette-butts → recycling-empire (Phase 6, 2026-11-26)

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
