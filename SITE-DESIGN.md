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
  long-form measure max 68ch; table text 0.85-0.9rem.

## 3. The writing system (readability contract)

The prose framework every page follows, so a reader with no or moderate domain expertise can
scan a page before committing to reading it. It is plain-language writing with BLUF ("bottom
line up front"), applied to research pages:

1. **Answer first.** Every section opens with its conclusion — a bolded lead ("**The route in
   one paragraph.** …") or a short lede. Background never comes before the answer.
2. **One idea per paragraph.** At most ~3 sentences; a paragraph carrying two ideas is split,
   and a paragraph longer than ~5 sentences becomes a list or a table.
3. **Parallel facts become bullet lists**, each bullet opened by a **bold lead-in**
   ("**Tar/PAH/semi-polars — polarity-graded extraction.** …"); **sequences become numbered
   lists**; **comparisons become tables** (e.g. INV-01 § 1: registry entries vs. what the
   invention does instead).
4. **Claim, then evidence, in the same block.** The first sentence carries the claim; the
   numbers, source anchors and caveats follow immediately — never a paragraph later.
5. **Labels ride with the claim they qualify.** An evidence tag sits directly after the
   sentence it grades (hover/focus shows the canonical charter definition); never clustered
   at the end of a paragraph.
6. **Units and anchors every time.** Every number carries its unit and its source anchor
   ("35.4 g/L measured in dark liquor (M-03)").
7. **One concept, one name.** Terms are used consistently and point to the glossary on first
   use; synonyms are avoided.
8. **Falsifiers are explicit.** Where a claim could be killed, the page names the test that
   would kill it.

The builder enforces the structural half mechanically: lists that directly follow a paragraph
line are re-spaced so they render as lists (`normalize_lists`), generated tables get the
data-table style with bare-number cells centered (`enhance_tables`), and long measures stay
capped at 68ch.

## 4. Color system

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

### Evidence labels (the identity colors)

| Label | Color |
| --- | --- |
| `source_supported` | green text `#0E7C4A` |
| `ai_inference` | blue text `#1D5FBF` |
| `ai_proposal` | amber text `#9A5B14` |
| `parameter_not_located` | slate text `#546E7A` |

In body text labels render as **inline colored text with a dashed underline** — not pill
chips — applied automatically by the builder wherever the backticked label token appears.
Hovering (or keyboard-focusing) a label shows a tooltip with the canonical charter wording
for that label; a `title` attribute carries the same text natively. The footer legend uses
the same treatment, so the legend doubles as an explainer. The tinted backgrounds stay in
the system for status badges and the phase strip.

### Status badges

Method status (`draft`, `proposed`, `pending_deep_dive`, `primary-source-read`,
`experimentally-supported-in-source`) render as small bordered badges tinted from neutral to
green as evidence strength rises.

## 5. Information architecture

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

## 6. Navigation model (easy navigation)

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

## 7. The reading journey (designed path)

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

## 8. Page templates

- **Home**: hero (one sentence + two buttons: *Browse materials*, *Read the playbook*), material
  cards (name, one-line blurb, version/phase badge, counts), footer legend.
- **Material dashboard**: identity card (name, version, status, site URL, priority methods),
  stop-condition banner, "Start here" journey cards, shelf counters (sources / methods /
  inventions / cards), ranking snapshot (top 3 rows of Table A), test-first preview,
  phase-progress strip, migration note link.
- **Method page**: spec-sheet grid rendered from the fenced metadata block (id, name, family,
  status, version, sources), body with H2 sections + right-rail TOC, prev/next among methods,
  evidence labels inline (colored text + tooltip), archive links rewritten automatically.
- **Ranking page**: the three tables verbatim with the data-table style (borders, zebra rows,
  tinted header, tabular numerals, centered score columns); the 8+-column score tables get a
  960px minimum width, scroll horizontally inside a rounded frame with the identity column
  pinned and a guaranteed 250px note column; gates explained above the tables; test-first
  list as numbered cards.
- **Sources index**: 81-row table (id, figures, original → archive, AI text → archive raw,
  detail page) with a filter box and type-filter chips, client-side only.
- **Source detail**: SOURCE.md content (or, for the 49 sources without SOURCE.md, an honest
  auto-stub: id, figures count, links to the archive folder and text.md) + callout
  "Full document lives in the butt-lab archive".
- **Reports / research / charter / glossary / state / log**: plain article template with TOC.

## 9. Components inventory

cards (material, journey, stat), evidence-label tags with tooltips, badges (status), banners
(stop-condition), spec-sheet grid, data tables (bordered frame, zebra, tinted header, pinned
identity column, tabular figures), callouts (archive links, caveat notes), breadcrumbs, TOC
rail, pagers, search overlay, footer legend, 404 page with the material map.

## 10. Accessibility & responsiveness

- WCAG AA contrast on every token pair (paper/ink 13.9:1; label and badge colors ≥ 4.5:1).
- Keyboard: visible focus rings (2px accent offset), search fully operable, skip-to-content link.
- Breakpoints: ≥1200px full three-column; 800-1200px two-column (TOC hides); <800px single
  column (sidebar → horizontal chips; tables scroll horizontally with sticky first column).
- `prefers-reduced-motion` disables all transitions; no animation elsewhere.
- Semantic HTML throughout (`nav`, `main`, `article`, `aside`); one H1 per page; descriptive
  link text (never "here").

## 11. Performance

Single CSS file (~15 KB), single JS file (~8 KB), fonts via Google Fonts with `display=swap`
and system fallbacks, search index ≤ 500 KB, no framework, no images required for pages (the
archive holds the figures). Every page renders instantly from the CDN.

## 12. Build & deploy

```
python3 tools/site-builder/build.py        # renders materials/ → docs/ (deterministic; safe to re-run)
```

- **GitHub Pages (chosen default)**: Settings → Pages → Source: *Deploy from a branch*, branch
  `main`, folder `/docs`. Site: `https://abdo2048.github.io/recycling-empire/`.
- **Cloudflare Pages (equivalent alternative)**: connect the repo, build command none, output
  dir `docs`. Private access later: Cloudflare Access in front of the domain (PLAYBOOK Phase 6).
- After the build, commit both `materials/` (source of truth) and `docs/` (rendered output);
  MATERIALS.md and the material's `material.yaml` hold the live URL.
