---
name: product-acceptance
description: Independently inspect every page, feature, state and flow against PRD, rendered mockups and architecture; fix/retest before owner review and verify actual live versions after authorized releases.
metadata:
  standard_version: 1.0.0
---
# Acceptance, not a build-success label
Read product-definition and full approved inputs. Record exact commit/build/environment/URL/browser/device/viewport/locale. All concrete pages, nested branches, tabs/modals/states are the denominator; PASS/FAIL/BLOCKED/NA_WITH_REASON, untested never PASS.
Open actual desktop/mobile screenshots against mockups and inspect layout/hierarchy/spacing/type/color/contrast/original images/readability/controls/overlap/clipping/zoom/focus/reduced motion. DOM overflow and builder claims are not visual review. Exercise every CTA and success/error/empty/loading/timeout/permission/cancel/back/refresh/deep-link/storage-denied/repeat path. Observe actual outcomes and applicable auth/RLS/data/API/model/form/payment safely; no unauthorized side effects or permission weakening.
Defects need severity, reproduction, expected/actual, evidence, fixing commit and RETEST. Review real visitor value and architecture/privacy/languages/performance/SEO. Fix/retest regressions. No internal acceptance with incomplete coverage, uninspected pixels, open P0/P1 or unaccepted P2.
Separate implemented, preview-tested, internally accepted, owner-reviewed, deployed and live-verified. Only after authorized release inspect actual live version/hash, pages and critical flows. Preview evidence is not live evidence. Preserve old site where requested. Deliver self-checked candidate only; progress stays NOT_READY until passed. Do not keep asking the owner to request review or doing more backups instead.
Full standard/templates: minyajing-rgb/GGC-AI-Spirituality-Research @ b50cc78567641341419c45a5759811b70f9d0456, .agents/skills/product-acceptance/SKILL.md and skills/product-delivery/.
