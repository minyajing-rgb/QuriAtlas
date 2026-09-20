# QuriAtlas / 量子漫游 — 域名与部署交接

## Standalone site

- Canonical repository: `minyajing-rgb/QuriAtlas`
- Source: `site/`
- Canonical corpus pointer: `data/CURRENT.json`
- Generated public HTML: `index.html`
- Hero artwork: `assets/hero-atlantis.webp`
- Build + browser QA + Pages workflow: `.github/workflows/pages.yml`
- Chinese: `?lang=zh`
- English: `?lang=en`

QuriAtlas is now independent from the Buddhist repository at runtime and build time.

## GitHub Pages

The repository has a complete GitHub Actions Pages workflow. A repository admin must enable the new repository once:

**Settings → Pages → Source → GitHub Actions**

The connected GitHub integration can write code and Actions workflows but GitHub rejects programmatic creation of a new Pages site with `Resource not accessible by integration`. This is a repository setting, not a website-code failure.

After the setting is enabled, rerun `Build test deploy QuriAtlas`. The workflow will:
1. build `index.html`;
2. run browser interaction QA;
3. stage only public files;
4. deploy GitHub Pages;
5. re-open the public URL and verify the current build.

Expected default Pages host after enablement:
`https://minyajing-rgb.github.io/QuriAtlas/`

## Custom domain later

For a subdomain managed in Aliyun DNS, first add the Custom domain in **this QuriAtlas repository's** GitHub Pages settings, then add the DNS record GitHub asks for.

For a normal GitHub Pages subdomain setup, the DNS CNAME target is the GitHub Pages host, not a URL path. Do not put `https://` or `/QuriAtlas/` in a CNAME value.

Do not bind the old Buddhist repository to the new QuriAtlas domain.

## Acceptance checklist

- HTTPS works.
- Chinese / English switching works and persists.
- 24 concept cards and source trails render.
- Four interactive physics models work.
- memo / Atlantis hero artwork loads.
- Knowledge map filters and SVG export work.
- Mobile width has no horizontal overflow.
- Custom domain opens the QuriAtlas root, not a Buddhist subdirectory.

## Official GitHub references

- Publishing source: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- Custom domain: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
