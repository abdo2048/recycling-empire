# Recycling Empire

One knowledge base, one website, every recycling material we study. Each material gets its own folder of sources, method action plans, invented methods, and rankings — built by an AI following the [PLAYBOOK](PLAYBOOK.md), reviewed by humans and other AIs after the build, and testable in qualified labs.

## How it is organized

```
PLAYBOOK.md               the reusable system (phases, rules, labels, review system)
START-A-NEW-MATERIAL.md   how a new material project starts
MATERIALS.md              registry of all material projects
SITE-DESIGN.md            the UI/UX contract for the unified site
template/                 skeleton cloned for each new material
materials/<slug>/         one folder per material (all the content)
tools/site-builder/       renders materials/ → docs/ (the static site)
docs/                     the built site (GitHub Pages / Cloudflare Pages serve this)
```

Design principles (why it looks like this): one repo and one site for all materials; folder-level isolation so any AI can work on any material without touching others; plain markdown with frontmatter so the same files render in Obsidian, on GitHub, and on the published site; labeled AI gap-filling so every missing parameter becomes a concrete, challengeable estimate; one state file per material so interrupted work always resumes correctly; review rounds with an endpoint rule so the work can actually finish.

## Current status

See [MATERIALS.md](MATERIALS.md). Case 1 — cigarette butts — completed Phases 1-5 in the [butt-lab repository](https://github.com/abdo2048/butt-lab) (now the frozen archive of heavy source originals) and migrated into `materials/cigarette-butts/` at Phase 6 together with the first build of the unified site. The old reader (butt-lab.am6.workers.dev) is retired once the unified site goes live.

## The site

Built by `python3 tools/site-builder/build.py` into `docs/`; served by GitHub Pages (Settings → Pages → branch `main`, folder `/docs`) or Cloudflare Pages (output dir `docs`). Typography: Inter + Fraunces; the four evidence labels have a permanent color system; the metals stop-condition banner appears on the home page, dashboards, and ranking. Full spec: [SITE-DESIGN.md](SITE-DESIGN.md).

## For the team

Read the cigarette-butt material on the deployed site (link in MATERIALS.md) or directly here in the repo. Team lab results go to `materials/<slug>/lab-findings/` and are treated as first-class evidence.
