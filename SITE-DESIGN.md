# Site design — the unified Recycling Empire site (Phase 6)

This document is the UI/UX contract for the static site that
[`tools/site-builder/build.py`](tools/site-builder/build.py) renders from `materials/` into
`docs/`. It is system-level (shared by every material) and follows the PLAYBOOK rules: plain
markdown stays the source of truth; the builder only presents it.

---

## 1. Design goals

1. **Read first.** The content is long-form, citation-heavy research. The UI exists to make a
   non-expert (the team, a reviewer, a funder) *finish* reading a method page — calm colors,
   one readable measure, no visual noise.
2. **Trust through labeling.** The four evidence labels are the project's identity. They get a
   permanent color system, a legend in the footer, and inline chips in text.
3. **The stop-condition is never hidden.** The metals gate (Cd/Pb/As/Hg) banner appears on the
   home page, every material dashboard, and the ranking page. It is part of the design, not a
   footnote.
4. **Zero-JavaScript-by-default.** The only JS is the search overlay and the table-of-contents
   highlight; every page works without it. No frameworks, no build dependencies beyond Python
   `markdown` + `PyYAML`.
5. **No monospace anywhere.** The user's explicit rule: mono fonts read as "developer tool",
   not research. Code spans, IDs, temperatures and numbers are set in Inter (tabular figures
   where alignment matters).

---

## 2. Typography

| Role | Font | Notes |
| --- | --- | --- |
| Display + headings (H1/H2, card titles, hero) | **Fraunces** (Google Fonts, variable, opsz 9-144) | Serif with warm, editorial character; pairs naturally with Inter; gives the knowledge base a "publication" voice |
| Body, UI, navigation, tables, chips | **Inter** (Google Fonts, 400/500/600/700) | The workhorse; `font-feature-settings: "cv11"` for a readable lowercase l; `"tnum"` (tabular numerals) on tables and metadata |
| Everything else (code, IDs, timestamps) | **Inter** — mono is banned | Code spans get a subtle paper-shade background instead of a font change |

- Load: one `display=swap` stylesheet, weights 400/500/600/700 only (fast).
- Fallbacks: `Inter, system-ui, -apple-system, "Segoe UI", sans-serif` and
  `"Fraunces", Georgia, "Times New Roman", serif`.
- Scale: H1 clamp(1.9rem→2.4rem) in Fraunces 600; H2 1.35rem Fraunces 600; body 1rem/1.7;
  long-form measure max 68ch; table text 0.92rem.

## 3. Color system

| Token | Value | Use |
| --- | --- | --- |
| `--paper` | `#FBFAF7` | page background (warm off-white) |
| `--card` | `#FFFFFF` | cards, tables, sidebar |
| `--ink` | `#1F2A24` | body text (deep green-black) |
| `--ink-soft` | `#5C6B62` | secondary text, captions, breadcrumbs |
| `--line` | `#E5E2D9` | hairlines, table borders |
| `--accent` | `#0E7C4A` | links, primary buttons, active nav (recycling green) |
| `--accent-ink` | `#0A5D38` | hover / active states |
| `--gate-bg` / `--gate-line` | `#FDF3E7` / `#E4B85C` | stop-condition banner (calm amber, not alarm red) |

### Evidence-label chips (the identity colors)

| Label | Chip |
| --- | --- |
| `source_supported` | green — `#E3F2EA` bg, `#0E7C4A` text |
| `ai_inference` | blue — `#E4EEFB` bg, `#1D5FBF` text |
| `ai_proposal` | amber — `#FCF1DF` bg, `#9A5B14` text |
| `parameter_not_located` | slate — `#ECEFF1` bg, `#546E7A` text |

Chips are pill-shaped, 0.78rem Inter 600, applied automatically by the builder wherever the
backticked label token appears in body text, and listed as a legend in every footer.

### Status badges

Method status (`draft`, `proposed`, `pending_deep_dive`, `primary-source-read`,
`experimentally-supported-in-source`) render as small bordered badges tinted from neutral to
green as evidence strength rises.

## 4. Information architecture

```
docs/
  index.html                          home: hero + material cards
  materials/cigarette-butts/
    index.html                        material dashboard (start here)
    ranking.html  registry.html  charter.html  glossary.html
    methods/index.html  methods/M-01…M-08.html  methods/cards.html
    inventions/index.html + 3 content pages
    reports/index.html + 2 report pages
    research/index.html + FINDINGS/manifest/transcripts (7 pages) + csv tables (3)
    sources/index.html (81-row table) + sources/<id>.html ×81
    state.html  log.html
    404.html
  assets/style.css  assets/site.js  assets/search-index.json  .nojekyll
```

URLs are stable and derived from file paths — a GitHub page and a site page share their slug,
so cross-links never rot.

## 5. Navigation model (easy navigation)

Three persistent layers + one overlay:

1. **Top bar** (sticky, every page): wordmark "Recycling Empire" → home; links **Materials**,
   **Charter & Playbook**, **About**; search button (`Ctrl/⌘-K`, also plain `/`).
2. **Material sidebar** (left, sticky on all `materials/<slug>/` pages, collapsed to a
   horizontal chip-row under the top bar on mobile):
   *Overview · Ranking · Methods (8) · Registry · Invention · Reports · Sources (81) ·
   Research · Charter · Glossary · State & log* — the full map is always one click away.
3. **"On this page"** (right rail on wide screens, only on long pages): H2-level TOC from the
   markdown, with scroll-spy highlighting; collapses under the content on narrow screens.
4. **Search overlay**: client-side, index prebuilt at generation time (`search-index.json`,
   page titles + headings + text, sources included). Scores title > heading > body; results
   grouped by section; Esc closes; fully keyboard-navigable.

Every page also carries: **breadcrumbs** (Home › Cigarette butts › Methods › M-01), and
**prev/next pagers** inside sequential groups (methods in registry order, sources alphabetical).

## 6. The reading journey (designed path)

The material dashboard is the journey's hub. Its "Start here" block prescribes one order:

1. **Overview** (dashboard) — what this material is, its version, phase, stop-condition.
2. **Ranking** — the verdict: Table A top routes, why M-08 leads (the only published metals-gate
   pass), the test-first list. *If you read one page, read this.*
3. **Final reports** — the evidence boundary in full prose (batch-01 synthesis; validation &
   open questions).
4. **Methods M-01…M-08** — the action plans, in ranking order, each with its status badge and
   gap-fill chips.
5. **INV-01** — the invented route that turns the field's missing mass balances into the
   deliverable; its falsifier ledger and red-team placeholder (Phase 7).
6. **Sources** — the 81-document shelf, each with metadata and archive links.
7. **Charter, glossary, state & log** — the rules and the record.

Each step's card states what you will learn and how long it takes ("short read", "deep read"),
so the reader can enter anywhere without losing the thread.

## 7. Page templates

- **Home**: hero (one sentence + two buttons: *Browse materials*, *Read the playbook*), material
  cards (name, one-line blurb, version/phase badge, counts), footer legend.
- **Material dashboard**: identity card (name, version, status, site URL, priority methods),
  stop-condition banner, "Start here" journey cards, shelf counters (sources / methods /
  inventions / cards), ranking snapshot (top 3 rows of Table A), test-first preview,
  phase-progress strip, migration note link.
- **Method page**: spec-sheet grid rendered from the fenced metadata block (id, name, family,
  status, version, sources), body with H2 sections + right-rail TOC, prev/next among methods,
  label chips inline, archive links rewritten automatically.
- **Ranking page**: the three tables verbatim with sticky first column, zebra rows, tabular
  numerals; gates explained above the tables; test-first list as numbered cards.
- **Sources index**: 81-row table (id, figures, original → archive, AI text → archive raw,
  detail page) with a filter box and type-filter chips, client-side only.
- **Source detail**: SOURCE.md content (or, for the 49 sources without SOURCE.md, an honest
  auto-stub: id, figures count, links to the archive folder and text.md) + callout
  "Full document lives in the butt-lab archive".
- **Reports / research / charter / glossary / state / log**: plain article template with TOC.

## 8. Components inventory

cards (material, journey, stat), chips (evidence labels), badges (status), banners
(stop-condition), spec-sheet grid, tables (sticky header, zebra, tabular figures), callouts
(archive links, caveat notes), breadcrumbs, TOC rail, pagers, search overlay, footer legend,
404 page with the material map.

## 9. Accessibility & responsiveness

- WCAG AA contrast on every token pair (paper/ink 13.9:1; chips ≥ 4.6:1).
- Keyboard: visible focus rings (2px accent offset), search fully operable, skip-to-content link.
- Breakpoints: ≥1200px full three-column; 800-1200px two-column (TOC hides); <800px single
  column (sidebar → horizontal chips; tables scroll horizontally with sticky first column).
- `prefers-reduced-motion` disables all transitions; no animation elsewhere.
- Semantic HTML throughout (`nav`, `main`, `article`, `aside`); one H1 per page; descriptive
  link text (never "here").

## 10. Performance

Single CSS file (~15 KB), single JS file (~8 KB), fonts via Google Fonts with `display=swap`
and system fallbacks, search index ≤ 500 KB, no framework, no images required for pages (the
archive holds the figures). Every page renders instantly from the CDN.

## 11. Build & deploy

```
python3 tools/site-builder/build.py        # renders materials/ → docs/ (deterministic; safe to re-run)
```

- **GitHub Pages (chosen default)**: Settings → Pages → Source: *Deploy from a branch*, branch
  `main`, folder `/docs`. Site: `https://abdo2048.github.io/recycling-empire/`.
- **Cloudflare Pages (equivalent alternative)**: connect the repo, build command none, output
  dir `docs`. Private access later: Cloudflare Access in front of the domain (PLAYBOOK Phase 6).
- After the build, commit both `materials/` (source of truth) and `docs/` (rendered output);
  MATERIALS.md and the material's `material.yaml` hold the live URL.
