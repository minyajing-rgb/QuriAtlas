# QuriAtlas｜量子漫游

> A Smaller You, A Bigger Universe.  
> 从好奇出发，看见更大的宇宙。

**Live website / 已发布官网: https://quriatlas.saga1001.com/**

Current verified release: **0.6.0-atlantis-fullsite**. The existing GitHub Pages site and custom domain are configured. No new hosting or DNS setup is required to visit this release.

## What is live

Eleven independently addressable, bilingual pages:

| Page | Address |
|---|---|
| 首页 / Home | `index.html` |
| 量子基础 / Quantum basics | `explore.html` |
| 互动实验室 / Interactive lab | `lab.html` |
| 意识与现实 / Mind & reality | `mind.html` |
| 故事与人物 / Stories & people | `stories.html` |
| 游戏与探索 / Play & discover | `play.html` |
| 一起探索 / Explore together | `community.html` |
| 学习旅程 / Learning journey | `journey.html` |
| 证据书架 / Evidence library | `sources.html` |
| 关于 / About | `about.html` |
| 量子纠缠 / Entanglement | `entanglement.html` |

Use `?lang=zh` or `?lang=en` on each page. Original section URLs are redirected to their corresponding new pages.

The release integrates nine approved Atlantis/memo artworks from `assets/art/`, preserves the sourced 24-concept corpus and four interactive teaching models, and adds functioning knowledge challenges and local exploration notes. It does not load the old 520px hero image.

## Production acceptance

Verified on the real custom domain, not just a local DOM preview:
- **271 passed checks, zero failed checks**.
- All eleven pages in Chinese and English.
- Desktop, tablet and mobile widths: 1440, 768 and 390 px.
- Native artwork loading, route targets, search, concept dialogs, reading progress, SVG export, four experiments, language-state retention, quiz scoring, notebook persistence/export, mobile navigation and legacy deep links.

Report: [`qa/release-0.6.0.json`](qa/release-0.6.0.json)

Successful build and public verification: https://github.com/minyajing-rgb/QuriAtlas/actions/runs/35494686061

## Sources and build

- `site/app.js`: preserved corpus UI and scientific model engine.
- `site/release.js` and `site/release.css`: full-site routes, new-art layout and interactions.
- `site/en.json`: English corpus translations.
- `data/CURRENT.json`: canonical source pointer.
- `assets/art/`: approved original-size artwork and production crops.
- `build.py`: generates all eleven static HTML files and stages only public assets.
- `tests/e2e.py`: real browser acceptance checks.
- `.github/workflows/pages.yml`: build → local acceptance → deploy → custom-domain acceptance.

```bash
python build.py
python -m http.server 8080 --directory build/public
```

Open `http://localhost:8080/`.

## Scope and privacy

This is a sourced research preview, not an exhaustive survey or a claim that quantum physics establishes spiritual propositions. Atlantis scenes are fictional art, not accurate apparatus diagrams. The four experiments are explicitly labelled teaching models.

Explore Together is a **local notebook and discussion-prompts page**, not a public forum. Notes and reading progress remain in the browser unless the visitor chooses to export or share them. The site has no account, payment, public-posting or hosted AI-chat backend.

The canonical repository is `minyajing-rgb/QuriAtlas`; the former `Buddhist/quantum` copy is historical only.
