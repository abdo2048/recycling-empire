# Start a new material project

One page. Do this in order.

## Human (operator) steps

1. Copy `template/` to `materials/<slug>/` (slug = short kebab-case name, e.g. `coffee-grounds`).
2. Open a session with any AI that has internet and file access to this repository.

## AI instructions (paste into the AI session)

> You are the research AI for material <NAME>. Read `/PLAYBOOK.md` fully, then `/materials/<slug>/STATE.md`. Work ONLY inside `/materials/<slug>/`. Follow the phases in order (0 Setup, 1 Gather, 2 Registry, 3 Action plans, 4 Invention, 5 Ranking). Obey the golden rules and the labeling rules. Update STATE.md before you stop and before any long step. When the phase set is complete, say so and stop — review rounds come later.

## Choosing priorities

- Pick 5-10 priority methods for full action plans (Phase 3); everything else gets a summary card.
- Priorities favor: viability at the team's scale, evidence strength, product usefulness, legal status.

## When is a material "done" (first version)

- All priority methods have action plans with labeled gap-fills
- One invented method exists
- `ranking.md` filled and the test-first list written
- STATE.md says so with version `v1.0-candidate` — then review rounds (Phase 7), then the owner freezes the version

## Reminder for the operator

- You may supply `sources/<id>/text.md` conversions yourself; operator-supplied conversions are preferred over AI conversion when available.
- Arbitration of review rounds is yours: mark accepted/rejected items in each round's `accepted.md`.
- Lab results from the team go to `lab-findings/` and automatically justify a new review round.
