# QuriAtlas 0.6.0 — native-art full-site integration

Target domain: https://quriatlas.saga1001.com/

## Scope shipped by this release
- Eleven independently addressable HTML pages: home, quantum basics, lab, mind & reality, stories, play, explore together, journey, sources, about and entanglement.
- Nine approved artworks reused from assets/art, with native-resolution desktop and mobile crops. No rejected 520px hero or third-party expiring image URLs are used.
- Original corpus, 24 concepts, 20 source entries, bilingual explanations and four teaching models preserved. Scientific evidence boundaries remain visible.
- Working concept search, detail dialogs, reading progress, SVG export, language switching, six-question knowledge challenge and local notebook export/share.
- Main navigation no longer labels the source list as a community. Explore Together is explicitly a local notebook and discussion-prompts page, not a public forum.
- Chinese and English pages share a single source renderer. URL parameters and old section deep links remain supported.

## Verification
The deployment workflow tests all eleven pages in both languages at 1440, 768 and 390 px; checks native image loading, core interactions and the production domain. Successful HTTP checks are archived at qa/release-0.6.0.json after deployment. Do not claim a successful release merely because the source commit exists.

## Boundaries
This release does not implement authentication, a multiplayer/public forum, hosted AI chat, payments, or exhaustive quantum research. Artwork is a fictional visual setting, not a representation of real equipment. The content is a sourced research preview.
