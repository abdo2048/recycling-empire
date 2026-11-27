# Materials registry

| Material | Slug | Status | Version | Lives in | Site |
| --- | --- | --- | --- | --- | --- |
| Cigarette butts | cigarette-butts | active — Phase 6 (site built; Phase 7 review rounds next) | v0.8-migration | this repo: [materials/cigarette-butts/](materials/cigarette-butts/) (heavy originals frozen in [butt-lab](https://github.com/abdo2048/butt-lab)) | [Unified site](https://abdo2048.github.io/recycling-empire/) (GitHub Pages from `docs/`; old reader retired) |

Notes:
- Case 1 (cigarette butts) completed Phases 1-5 in butt-lab and migrated here at Phase 6 (2026-11-26) together with the first build of the unified site — see its [MIGRATION-NOTE.md](materials/cigarette-butts/MIGRATION-NOTE.md).
- The site is built by [tools/site-builder/build.py](tools/site-builder/build.py) from `materials/`; the design contract is [SITE-DESIGN.md](SITE-DESIGN.md).
- New materials start from [START-A-NEW-MATERIAL.md](START-A-NEW-MATERIAL.md).
- A material is frozen when a review round produces no accepted changes (PLAYBOOK endpoint rule); its row status becomes `frozen vX.Y`.
