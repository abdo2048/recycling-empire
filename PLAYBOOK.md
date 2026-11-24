# Recycling Empire — Playbook

A reusable system for turning "this waste material can maybe be recycled" into a browsable knowledge base of action plans that a real team can verify and test in qualified labs. Built by an AI researcher; judged by humans and other AIs after the build.

Case 1 (cigarette butts) currently lives in the [butt-lab](https://github.com/abdo2048/butt-lab) repository and migrates into `materials/cigarette-butts/` of this repo when complete.

Hand this file plus [START-A-NEW-MATERIAL.md](START-A-NEW-MATERIAL.md) to any AI with internet and file access. It runs one material through the phases below, inside one folder, updating one state file. That is the whole contract.

## Golden rules

1. **One repo, one site.** All materials live in `materials/<slug>/` of this repository. One build, one deploy, one URL; all materials browsable, with search across materials.
2. **Folder isolation.** An AI working on material X touches only `materials/X/`. Never another material's folder. Playbook and template changes go through a review round, not in-place edits.
3. **Plain markdown is the only source of truth.** No HTML cards, no plugin-only syntax, no `obsidian://` links inside content. Metadata lives in YAML frontmatter. The same files then render in Obsidian, on GitHub, and on the published site.
4. **STATE.md discipline.** Every session starts by reading `materials/<slug>/STATE.md` and ends by updating it — before stopping, and before starting any long step. The 2-minute resume test: a fresh AI must be able to answer "what phase, what task, what's next" from STATE.md alone. If it cannot, the previous session failed.
5. **Labeled gap-filling.** Where sources are silent, the AI fills gaps with concrete estimates (numbers, temperatures, ratios, times), each labeled, reasoned, and falsifiable. Vagueness is a defect, not safety. Safety comes from labels, safety notes, and rule 7.
6. **No invented measurements.** Measured values come only from sources or lab findings. Arithmetic is computed, not guessed. Unknown is not zero. Conflicting source values are both kept, never silently averaged.
7. **Desk research authorizes no physical trial.** No AI handles material, operates equipment, or enters a laboratory. Physical work requires qualified facilities, a risk assessment, lawful waste handling, and a named human actor.
8. **The endpoint rule.** A review round happens only if the previous round produced accepted changes or new evidence arrived (lab findings, new sources). A round with no accepted changes freezes the project at a stable version. Done means done.

## Content labels (mandatory on every non-trivial statement)

| Label | Meaning |
| --- | --- |
| `source_supported` | Stated by a cited primary source; include citation, units, mass basis. |
| `ai_inference` | Reasoned by the AI from sources; show the reasoning chain. |
| `ai_proposal` | Invented or estimated by the AI; testable assumption; needs reasoning + falsifier. |
| `parameter_not_located` | No number exists at the required basis; say what is missing and how to measure it. |

Secondhand claims count as `ai_inference` until checked against the primary source. Company self-report is not measurement. "Clean / safe / validated" are never claimed — the team's lab decides.

## Phases

### Phase 0 — Setup
Clone `template/` to `materials/<slug>/`; fill `material.yaml`; initialize STATE.md and LOG.md.

> **Prompt:** "You are the research AI for material <X>. Read PLAYBOOK.md fully, then materials/<slug>/STATE.md. Work only inside materials/<slug>/. Follow the phases in order. Update STATE.md before you stop."

### Phase 1 — Gather sources
Collect: patents of all statuses and jurisdictions (Google Patents; INPI/EPO/USPTO/WIPO for legal status), companies with no public patent, peer-reviewed papers, theses, reports, product/test documentation, and documented failures. Separate collectors from processors. "Patent not located in this search" proves neither absence nor trade secret.
Output: `sources/<source-id>/` per source — `document.pdf` (human-readable), `text.md` (AI-readable full text), `SOURCE.md` (metadata: title, authors, year, type, where found, URL, legal status if patent, access notes).
**Division of labor:** the AI may convert PDF to text if its tools allow; the operator may supply `text.md` directly — operator-supplied conversions are preferred when available. A missing `text.md` does not stall the phase: mark it, work from the PDF if readable, continue.

> **Prompt:** "Phase 1: find and shelve sources for <X> per PLAYBOOK Phase 1. Append every completed source to STATE.md Done; park next leads in Next up."

### Phase 2 — Method registry
`REGISTRY.md`: one append-only entry per method (id, name, source_type, assignee, mechanism_class, disclosed parameters, equipment, outputs, gaps, legal_status, citations, status). Mark each method priority or summary-card.

> **Prompt:** "Phase 2: build REGISTRY.md from the shelved sources. One append-only entry per method. Flag which methods deserve full action plans (priority) and which only summary cards."

### Phase 3 — Action plans
Priority methods: `methods/M-XX-<slug>.md` per `METHOD-TEMPLATE.md` — the disclosed protocol with numbers, equipment, the labeled gap-fill table, safety notes, and what the team must verify in lab. All other methods: one-paragraph summary cards in `methods/_cards.md` (what it is, status, why deprioritized). Nothing is lost; any card can be upgraded to a full plan later.

> **Prompt:** "Phase 3: write full action plans for the priority methods, one file per method, using METHOD-TEMPLATE.md. Every gap gets a labeled estimate with reasoning and a falsifier. Then write summary cards for the rest."

### Phase 4 — Invention
The AI designs its own method from the accumulated knowledge: `inventions/INV-XX-<slug>.md` — full recipe with numbers, every assumption `ai_proposal`, explicit relation to the sources it builds on, falsifiers, safety notes. An invention is not a claim of novelty or patentability.

> **Prompt:** "Phase 4: design one invented method for <X>, built from the gathered knowledge. Full recipe with numbers; every assumption labeled ai_proposal; falsifiers for the load-bearing claims; safety notes."

### Phase 5 — Ranking
`ranking.md`: every method scored 1-5 on the six standard factors (rubrics in the template), one-line justification per score, the ranked table, and the "test first" list for the team.

> **Prompt:** "Phase 5: fill ranking.md. Score every method on the six factors with justifications, rank them, and write the test-first list tied to the gap-fills each test confirms or kills."

### Phase 6 — Site
The site builder renders all `materials/` into one static site: a home page of material cards (from frontmatter), per-material sections, method pages, search. Deploy to Cloudflare Pages or Vercel free tier. Private access: repo invites, or Cloudflare Access in front of the site. (The builder ships with the first material migration — see MATERIALS.md.)

### Phase 7 — Review rounds (after the build)
Reviewers (AIs or humans) get a **focused brief** — format in `template/reviews/BRIEF-TEMPLATE.md`: specific files, specific questions, fixed output. They never edit the material in place and never receive a copy of the project. Output: `reviews/round-N-<reviewer>/` containing `brief.md`, `findings.md`, and (after the owner decides) `accepted.md`. The owner arbitrates; accepted items merge into the material; the version bumps in STATE.md. Reviewer-drafted new methods wait in `proposals/` until accepted. A round with nothing accepted freezes the version (endpoint rule).

## Tools a research AI needs

Web search; page fetching; Google Patents; PubMed / Google Scholar / journal sites; patent-office databases (INPI, EPO, USPTO, WIPO); company sites and press; PDF reading and text extraction; file read/write; a scratchpad for arithmetic — any numerical claim gets computed, not estimated.
Honest limits: paywalled papers give abstracts only until the operator supplies the PDF; trade secrets cannot be mined, only hypothesized with labels; nothing found online is "validated".

## Safety charter (condensed; binds every material)

Desk research authorizes no physical trial. Contaminated waste, chemicals, pressure, and emissions require qualified facilities, a risk assessment, lawful disposal, and a named human actor. No DIY pressure vessels. No clearance based on odor, appearance, or a single assay. Material-specific stop-conditions (cigarette butts: Cd/Pb/As/Hg uncharacterised means the route is on hold) live in the material's STATE.md and bind all work.

## File conventions

| Thing | Location |
| --- | --- |
| Methods (action plans) | `materials/<slug>/methods/M-XX-<slug>.md` (ids match REGISTRY.md) |
| Summary cards | `materials/<slug>/methods/_cards.md` |
| Inventions | `materials/<slug>/inventions/INV-XX-<slug>.md` |
| Sources | `materials/<slug>/sources/<source-id>/{document.pdf, text.md, SOURCE.md}` |
| Reviews | `materials/<slug>/reviews/round-N-<reviewer>/` |
| Reviewer drafts (quarantine) | `materials/<slug>/proposals/` |
| Team lab results | `materials/<slug>/lab-findings/` |
| State | `materials/<slug>/STATE.md` + `LOG.md` (append-only, 1-3 lines per session) |
| Versions | STATE.md `version:` field; v0.x while building, v1.0 = first complete reviewed version |
