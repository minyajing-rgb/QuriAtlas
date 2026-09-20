/* Production state, accessibility and responsive drawing. No new backend. */
'use strict';
window.QURI_SOURCE_COMMIT = document.querySelector('meta[name="quri-source-commit"]').content;
const _switchLanguage = switchLang;
switchLang = function(next) {
  const box = document.getElementById('notebook');
  const draft = box ? box.value : null;
  const start = box ? box.selectionStart : 0, end = box ? box.selectionEnd : 0;
  _switchLanguage(next);
  const nextBox = document.getElementById('notebook');
  if (nextBox && draft !== null) {
    nextBox.value = draft;
    nextBox.setSelectionRange(start, end);
  }
  decoratePage();
};
function decoratePage() {
  document.querySelectorAll('.q-mobile-menu a').forEach(a => {
    if (a.pathname.split('/').pop() === (PAGE === 'home' ? 'index.html' : PAGE + '.html')) a.setAttribute('aria-current', 'page');
  });
  const menu = document.querySelector('.q-mobile-menu');
  if (menu) {
    menu.id = 'mobile-navigation';
    document.querySelector('[data-q="menu"]').setAttribute('aria-controls', menu.id);
  }
  document.querySelectorAll('.q-art').forEach(img => {
    img.draggable = false;
    img.dataset.role = 'illustration';
  });
}
// Keep a tab's experiment state across page visits; notebook remains explicitly
// saved to localStorage only when the visitor presses "Save locally".
function rememberExperiment() {
  if (PAGE !== 'lab') return;
  try {
    sessionStorage.setItem('quri-lab-v1', JSON.stringify({lab, phase, visibility, detector, width, theta, hits, pairs}));
  } catch (_) { /* Privacy modes may block browser storage. */ }
}
function restoreExperiment() {
  if (PAGE !== 'lab') return;
  try {
    const state = JSON.parse(sessionStorage.getItem('quri-lab-v1') || 'null');
    if (!state || typeof state !== 'object') return;
    if (labIds.includes(state.lab) && location.hash !== '#bell') lab = state.lab;
    const number = (key, min, max, fallback) => Number.isFinite(state[key]) ? Math.max(min, Math.min(max, state[key])) : fallback;
    phase = number('phase',0,360,0); visibility = number('visibility',0,100,100);
    width = number('width',.3,2,.7); theta = number('theta',0,90,45);
    detector = state.detector === true;
    hits = Array.isArray(state.hits) ? state.hits.filter(p => Array.isArray(p) && p.length === 2 && p.every(Number.isFinite) && p[0]>=60 && p[0]<=760 && p[1]>=235 && p[1]<=304).slice(0,10000) : [];
    pairs = state.pairs && ['a','b','same'].every(k => Number.isInteger(state.pairs[k]) && state.pairs[k] >= 0 && state.pairs[k] <= 1000) ? state.pairs : null;
    renderLab();
  } catch (_) { /* Ignore malformed previous-session state. */ }
}
window.addEventListener('pagehide', rememberExperiment);
const _drawExperiment = drawLab;
drawLab = function() {
  _drawExperiment();
  const canvas = document.getElementById('experiment');
  if (canvas) canvas.dataset.renderScale = String(canvas.width / 820);
};
let repaintTimer;
window.addEventListener('resize', () => {
  clearTimeout(repaintTimer);
  repaintTimer = setTimeout(() => { if (PAGE === 'lab') drawLab(); }, 180);
});
document.addEventListener('keydown', e => {
  if (e.key !== 'Escape') return;
  const menu = document.querySelector('.q-mobile-menu');
  if (menu && !menu.hidden) {
    menu.hidden = true;
    const button = document.querySelector('[data-q="menu"]');
    button.setAttribute('aria-expanded','false'); button.focus();
  }
});
decoratePage(); restoreExperiment();
if (PAGE === 'lab') drawLab();
