# QuriAtlas｜量子漫游

> A Smaller You, A Bigger Universe.  
> 从好奇出发，看见更大的宇宙。

QuriAtlas 是独立的双语量子物理互动知识站。项目已从 `minyajing-rgb/Buddhist` 中拆出，不再依赖佛典项目的部署结构。

## Product
- 中文 / English 一键切换
- 量子物理入门知识地图
- 4 个可操作实验模型：双缝、干涉、不确定性、Bell/纠缠
- 意识 / 现实 / 灵性相关主张的证据边界
- 可追溯来源
- Atlantis-inspired future world + memo cat visual system

## Structure
```
/
  index.html             # generated public site
  build.py
  site/
    app.js
    style.css
    mobile.css
    en.json
  data/
    CURRENT.json
    atlas.v0.1.json
  assets/
    hero-atlantis.webp
    knowledge-map.svg
  tests/
    e2e.py
  .github/workflows/pages.yml
```

## Local
```bash
python build.py
python -m http.server 8080
```

Then open http://localhost:8080/

## Publishing
GitHub Actions builds and browser-tests the repository root on every relevant push. The new repository still needs its one-time GitHub Pages setting enabled by a repository admin: **Settings → Pages → Source: GitHub Actions**. The workflow detects that setting and deploys automatically once enabled. Custom-domain DNS is intentionally not set yet.

## Research status
The public product is a research preview. The current corpus is a sourced seed set, not an exhaustive survey and not a claim that quantum physics proves spiritual propositions.


## Current implementation
- UI build: `0.4.0-atlantis-cinematic`
- Hero: cinematic Atlantis scene occupying the majority of the desktop visual area
- Live HTML HUD overlays: superposition / entanglement / enter lab
- memo cat integrated into the world scene
- Research method copied into `skills/global-knowledge-atlas/`
- Legacy Buddhist quantum folder points here and is no longer canonical
