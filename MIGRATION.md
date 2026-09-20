# Migration from Buddhist repository

QuriAtlas became the **canonical standalone repository** for the quantum-physics product on 2026-09-20.

## Canonical now
- Product UI, bilingual content and interactions: this repository
- Quantum corpus pointer: `data/CURRENT.json`
- Quantum source dataset: `data/atlas.v0.1.json`
- Public generated HTML: `index.html`
- Website art direction: `STYLE_GUIDE.md`

## Migrated from
Legacy path: `minyajing-rgb/Buddhist/quantum/`

The old Buddhist copy is retained only as a historical migration snapshot until the standalone custom-domain rollout is complete. New quantum work should not be added there.

## Independence
This repository does not read files, APIs, pages, or data from the Buddhist repository at runtime or build time.
