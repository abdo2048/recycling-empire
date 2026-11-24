# Recycling Empire

One knowledge base, one website, every recycling material we study. Each material gets its own folder of sources, method action plans, invented methods, and rankings — built by an AI following the [PLAYBOOK](PLAYBOOK.md), reviewed by humans and other AIs after the build, and testable in qualified labs.

## How it is organized

```
PLAYBOOK.md               the reusable system (phases, rules, labels, review system)
START-A-NEW-MATERIAL.md   how a new material project starts
MATERIALS.md              registry of all material projects
template/                 skeleton cloned for each new material
materials/<slug>/         one folder per material (all the content)
```

Design principles (why it looks like this): one repo and one site for all materials; folder-level isolation so any AI can work on any material without touching others; plain markdown with frontmatter so the same files render in Obsidian, on GitHub, and on the published site; labeled AI gap-filling so every missing parameter becomes a concrete, challengeable estimate; one state file per material so interrupted work always resumes correctly; review rounds with an endpoint rule so the work can actually finish.

## Current status

See [MATERIALS.md](MATERIALS.md). Case 1 — cigarette butts — is being completed in the [butt-lab repository](https://github.com/abdo2048/butt-lab) (live reader: https://butt-lab.am6.workers.dev/) and will migrate into `materials/cigarette-butts/` when done, together with the first deploy of the unified site.

## For the team

Until migration, read the cigarette-butt material in butt-lab (link above). After migration, everything is browsable here and on the deployed site. Team lab results go to `materials/<slug>/lab-findings/` and are treated as first-class evidence.