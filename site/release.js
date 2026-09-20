/* QuriAtlas full-site release. Reuses the sourced corpus and tested model engine. */
'use strict';
const RELEASE='0.6.0-atlantis-fullsite';
const PAGE=document.body.dataset.page||'home';
const legacyRender=render;
const pages={
 home:['首页','Home','home'],explore:['量子基础','Quantum Basics','basics'],lab:['互动实验室','Interactive Lab','lab'],
 mind:['意识与现实','Mind & Reality','mind'],stories:['故事与人物','Stories & People','stories'],
 play:['游戏与探索','Play & Discover','play'],community:['一起探索','Explore Together','community'],
 journey:['学习旅程','Learning Journey','journey'],sources:['证据书架','Evidence Library','stories'],
 about:['关于量子漫游','About QuriAtlas','community'],entanglement:['量子纠缠','Quantum Entanglement','entanglement']
};
const pageUrl=(p,hash='')=>(p==='home'?'index':p)+'.html?lang='+lang+hash;
const icons={
 atom:'<ellipse cx="24" cy="24" rx="20" ry="8"/><ellipse cx="24" cy="24" rx="20" ry="8" transform="rotate(60 24 24)"/><ellipse cx="24" cy="24" rx="20" ry="8" transform="rotate(120 24 24)"/><circle cx="24" cy="24" r="2" fill="currentColor"/>',
 lab:'<path d="M18 5h12m-9 0v15L10 39q-2 4 3 4h22q5 0 3-4L27 20V5M16 29h16"/><circle cx="24" cy="35" r="1"/>',
 orbit:'<circle cx="24" cy="24" r="13"/><ellipse cx="24" cy="24" rx="23" ry="8" transform="rotate(-25 24 24)"/>',
 book:'<path d="M24 12q-7-6-19-3v31q12-3 19 3 7-6 19-3V9q-12-3-19 3v31"/>',
 play:'<path d="M14 14h20q6 0 8 8l3 13q1 8-6 6l-9-9H18l-9 9q-7 2-6-6l3-13q2-8 8-8Z"/><path d="M10 23h10m-5-5v10m17-6h1m4 5h1"/>',
 people:'<circle cx="24" cy="14" r="7"/><path d="M11 42V33q0-11 13-11t13 11v9ZM9 14a6 6 0 0 0 0 12M39 14a6 6 0 0 1 0 12M6 29q-5 2-4 12h6m34-12q5 2 4 12h-6"/>',
 arrow:'<path d="M8 24h31M29 14l10 10-10 10"/>',
 search:'<circle cx="20" cy="20" r="12"/><path d="m29 29 12 12"/>'
};
function icon(k){return '<svg class="q-icon" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+(icons[k]||icons.atom)+'</svg>'}
function logo(){return `<a class="q-brand" href="${pageUrl('home')}">${icon('atom')}<span><b>${t('量子漫游','QuriAtlas')}</b><small>${t('QURIATLAS · EXPLORE A BRIGHTER TOMORROW','EXPLORE A BRIGHTER TOMORROW')}</small></span></a>`}
function header(){return `<a class="sr-only" href="#page-content">${t('跳到正文','Skip to content')}</a><header class="q-header"><div class="q-width q-header-row">${logo()}<nav class="q-nav" aria-label="${t('主导航','Main navigation')}">${[['home','首页','Home'],['explore','探索','Explore'],['lab','实验室','Lab'],['stories','故事','Stories'],['community','一起探索','Together'],['about','关于','About']].map(([p,z,e])=>`<a href="${pageUrl(p)}" ${PAGE===p?'aria-current="page"':''}>${t(z,e)}</a>`).join('')}</nav><div class="q-tools"><button class="q-search-button" data-q="search" aria-label="${t('搜索知识','Search the atlas')}">${icon('search')}</button><div class="lang"><button data-lang="zh" lang="zh-CN" aria-pressed="${lang==='zh'}">中文</button><button data-lang="en" lang="en" aria-pressed="${lang==='en'}">EN</button></div><button class="q-menu-button" data-q="menu" aria-expanded="false" aria-label="${t('打开菜单','Open menu')}">☰</button></div></div><nav class="q-mobile-menu" hidden>${Object.entries(pages).map(([p,n])=>`<a href="${pageUrl(p)}">${t(n[0],n[1])}</a>`).join('')}</nav></header>`}
const portalSpec=[['explore','atom','从好奇开始','Start with curiosity'],['lab','lab','改变一个条件','Change one condition'],['mind','orbit','区分体验与证据','Wonder meets evidence'],['stories','book','发现背后的故事','Ideas have a history'],['play','play','在乐趣中学习','Learn by playing'],['community','people','交流你的发现','Share your discoveries']];
function portals(){return `<nav class="q-portals q-width" aria-label="${t('探索入口','Explore the atlas')}">${portalSpec.map(([p,i,z,e])=>`<a href="${pageUrl(p)}">${icon(i)}<span><b>${t(pages[p][0],pages[p][1])}</b><small>${t(z,e)}</small></span><span class="portal-arrow">→</span></a>`).join('')}</nav>`}
function art(key,klass='',eager=false){return `<img class="q-art ${klass}" src="assets/art/${key}-crop.webp?v=6" alt="${t('亚特兰蒂斯主题原创场景：','Original Atlantis-inspired scene: ')}${esc(key)}" ${eager?'fetchpriority="high"':'loading="lazy"'} decoding="async">`}
function tile(p,z,e,extra=''){return `<a class="q-tile ${extra}" href="${pageUrl(p)}">${art(pages[p][2])}<span class="q-tile-caption"><small>${t(z,e)}</small><b>${t(pages[p][0],pages[p][1])}</b><span>${icon('arrow')}</span></span></a>`}
function homeHero(){return `<section class="q-home-hero"><picture><source media="(max-width:700px)" srcset="assets/art/home-crop.webp?v=6"><img class="q-hero-image" src="assets/art/home-scene.webp?v=6" width="1672" height="760" fetchpriority="high" alt="${t('未来亚特兰蒂斯、年轻探索者与 memo 猫','Futuristic Atlantis, a young explorer, and memo cat')}"></picture><div class="q-hero-copy"><span class="q-eyebrow">EXPLORE · UNDERSTAND · CREATE</span><h1>${t('从好奇出发，<br>看见更大的宇宙','A Smaller You,<br>A Bigger Universe.')}</h1><p class="q-subtitle">${t('A Smaller You, A Bigger Universe.','Stay curious. Follow the evidence.')}</p><p class="q-hero-desc">${t('让故事带你走近量子世界。<br>让实验把好奇变成理解。','Let stories open a door to the quantum world.<br>Let experiments turn curiosity into understanding.')}</p><div class="actions"><a class="btn primary" href="${pageUrl('explore')}">${t('开始探索','Start Exploring')} →</a><a class="btn" href="${pageUrl('lab')}">${icon('lab')}${t('进入实验室','Enter the Lab')}</a></div><p class="q-caption">${t('同一个星球 · 更明亮的明天','SAME PLANET · A BRIGHTER TOMORROW')}</p></div></section>`}
function home(){return `${homeHero()}${portals()}<div class="q-width q-home-content"><div class="q-home-panels"><a class="q-lab-feature" href="${pageUrl('lab')}">${art('lab')}<div><small>INTERACTIVE LAB</small><h2>${t('动手探索，<br>看见量子世界','Experiment.<br>Discover something new.')}</h2><span class="btn">${t('开始实验','Start experimenting')} →</span></div></a><div class="q-journey-panel"><div class="q-mini-heading"><b>${t('三段探索旅程','Your learning journey')}</b><a href="${pageUrl('journey')}">${t('查看路线','See the path')} →</a></div><div class="q-three">${[['explore','basics','01','认知','Explore'],['lab','lab','02','体验','Experience'],['journey','journey','03','创造','Create']].map(([p,k,n,z,e])=>`<a class="q-mini-tile" href="${pageUrl(p)}">${art(k)}<span>${n}<b>${t(z,e)}</b></span></a>`).join('')}</div></div><div class="q-featured"><div class="q-mini-heading"><b>${t('精选内容','Featured')}</b><a href="${pageUrl('sources')}">${t('追到来源','Trace sources')} →</a></div><a class="q-featured-main" href="${pageUrl('entanglement')}">${art('entanglement')}<b>${t('量子纠缠：<br>比想象更奇妙的关联','Entanglement:<br>a stranger connection')}</b></a><a class="q-featured-row" href="${pageUrl('mind')}">${art('mind')}<span>${t('量子与意识，怎样认真讨论？','How do we discuss quantum and mind?')}</span>→</a><a class="q-featured-row" href="${pageUrl('stories')}">${art('stories')}<span>${t('遇见改变世界的问题','Meet questions that changed the world')}</span>→</a></div></div><div class="q-facts">${[[24,'概念笔记','Concept notes'],[4,'互动模型','Interactive models'],[20,'来源入口','Source entries'],[3,'学习路线','Learning paths'],[2,'语言','Languages']].map(([n,z,e])=>`<div><b>${n}</b><span>${t(z,e)}</span></div>`).join('')}<div class="q-fact-note">${t('保持好奇<br>也看见证据','Stay curious.<br>Follow the evidence.')}</div></div><div class="q-section-title"><small>FIND YOUR NEXT QUESTION</small><h2>${t('不同的好奇，同一个宇宙。','Different curiosity. Same universe.')}</h2></div><div class="q-topic-grid">${tile('explore','认识微观世界','Meet the quantum world')}${tile('mind','好奇，不走捷径','Wonder, without shortcuts')}${tile('stories','思想与发现','Stories behind the ideas')}${tile('play','用挑战检验理解','Challenge your intuition')}${tile('community','记录、分享、一起探索','Reflect, share, explore together')}${tile('journey','让好奇走得更远','Take curiosity further')}</div></div>`}
const descriptions={
 explore:['没有公式门槛。从一个问题出发，循着图解找到证据。','No equations required to begin. Follow a question through explanations to evidence.'],
 lab:['四个模型，四种观察世界的新方式。选择实验，亲手改变条件。','Four models. Four ways to question your intuition. Choose one and change a condition.'],
 mind:['好奇心可以很大；关于物理机制的结论，需要具体证据。','Wonder can be expansive. Claims about physical mechanisms need specific evidence.'],
 stories:['每一个答案之前，都有人认真问过一个问题。','Before every answer, someone asked a better question.'],
 play:['先做判断，再揭晓解释。用一场小挑战检查自己的理解。','Make a prediction, then uncover the explanation. Test your intuition.'],
 community:['记录自己的发现，带着一个好问题，与朋友开启讨论。','Record what you discover. Start a conversation with a better question.'],
 journey:['先看见，再动手，最后用自己的语言把它讲清楚。','Explore an idea, try it out, then explain it in your own words.'],
 sources:['不是“有论文”就等于“已证实”。继续追问来源究竟支持什么。','A paper is not automatically proof. Ask exactly what a source supports.'],
 about:['一个属于好奇者的量子学习空间。科学与想象，各有自己的位置。','A quantum learning space for curious minds. Science and imagination, each in its place.'],
 entanglement:['从普通相关，到能够接受检验的非经典关联。','From ordinary correlation to nonclassical relationships we can test.']
};
function innerHero(){const p=pages[PAGE];return `<section class="q-inner-hero q-width"><div><a class="q-breadcrumb" href="${pageUrl('home')}">${t('首页','Home')} /</a><span class="q-eyebrow">EXPLORE · UNDERSTAND · CREATE</span><h1>${t(p[0],p[1])}</h1><p>${t(...descriptions[PAGE])}</p><a class="btn primary" href="#page-content">${t('开始阅读与探索','Explore this page')} ↓</a></div>${art(p[2],'q-inner-scene',true)}</section>`}
function quizData(){return [
 ['Q004','一次只发一个粒子，很多次之后还能出现干涉条纹吗？','Can interference emerge after many one-at-a-time detections?', ['可以，适当条件下可以','不可以，必须同时发射'],['Yes, under suitable conditions','No, particles must arrive together'],0],
 ['Q008','量子测量一定需要有意识的人盯着仪器吗？','Does a quantum measurement require a conscious person watching?', ['一定需要','标准计算不要求如此'],['Yes, always','Not in the standard calculation'],1],
 ['Q016','仅靠纠缠，能发送可控制的超光速消息吗？','Can entanglement alone send a controllable faster-than-light message?', ['能','不能'],['Yes','No'],1],
 ['Q009','一般量子态的不确定度乘积一定等于 ℏ/2 吗？','Must every quantum state attain an uncertainty product of ℏ/2?', ['不一定，通常是不等式','任何量子态都取等号'],['No, the general relation is an inequality','Yes, all states attain equality'],0],
 ['Q010','自旋可以完全解释成小球绕轴旋转吗？','Is spin fully described as a little ball rotating?', ['可以','不可以'],['Yes','No'],1],
 ['Q021','存在一种脑内量子机制提案，就等于该机制已证实吗？','Does a proposed quantum brain mechanism mean it is established?', ['不等于','等于'],['No','Yes'],0]
]}
let answers={};
function quiz(){return `<section class="q-width q-workspace" id="quiz"><div class="q-section-title"><small>THE CURIOSITY CHALLENGE</small><h2>${t('你的直觉，准备好了吗？','Ready to question your intuition?')}</h2><p>${t('6 个判断题。每题都有解释和对应概念。','Six questions, each with an explanation and a concept to explore.')}</p></div><div class="q-quiz-grid">${quizData().map((d,i)=>`<article class="q-question"><small>0${i+1} / 06</small><h3>${t(d[1],d[2])}</h3><div class="q-answer-options">${t(d[3],d[4]).map((a,j)=>`<button class="btn" data-quiz="${i}" data-choice="${j}" ${answers[i]!==undefined?'disabled':''}>${esc(a)}</button>`).join('')}</div><div class="q-answer" id="answer-${i}" role="status">${answers[i]!==undefined?answerHtml(i):''}</div></article>`).join('')}</div><p class="q-quiz-score" aria-live="polite"></p><button class="btn" data-q="reset-quiz">${t('再挑战一次','Try again')}</button></section>`}
function answerHtml(i){const d=quizData()[i],ok=answers[i]===d[5];return `<b>${ok?t('判断正确 ✓','Correct ✓'):t('换个角度看 →','A different perspective →')}</b><p>${esc(entry(d[0]).summary)}</p><button class="step" data-entry="${d[0]}">${t('查看解释与来源','Open explanation and sources')} →</button>`}
function updateQuiz(){const el=$('#quiz');if(!el)return;el.outerHTML=quiz();const done=Object.keys(answers).length;$('#quiz .q-quiz-score').textContent=t('已完成 ','Completed ')+done+'/6 · '+t('正确 ','Correct ')+Object.entries(answers).filter(([i,a])=>a===quizData()[i][5]).length}
function notebook(){return `<section class="q-width q-workspace"><div class="q-note-layout"><div><span class="q-eyebrow">CURIOSITY, IN YOUR OWN WORDS</span><h2>${t('把今天的发现留下来。','Make the discovery your own.')}</h2><p>${t('这是一份只存于当前浏览器的学习手记，不是公共论坛，也不会自动上传。写好后可导出或分享给朋友。','This notebook stays in this browser. It is not a public forum and is not uploaded automatically. Export or share it with a friend.')}</p><div class="q-prompts">${['今天哪个解释改变了你的直觉？','哪个说法需要更多证据？','下一次实验，你想改变什么？'].map((z,i)=>`<button class="step" data-prompt="${i}">${t(z,['What changed your intuition today?','Which claim needs more evidence?','What would you change in the next experiment?'][i])}</button>`).join('')}</div></div><div class="q-notebook"><label for="notebook">${t('我的探索手记','My exploration notebook')}</label><textarea id="notebook" rows="9" maxlength="12000" placeholder="${t('一个问题，一次发现……','A question. A discovery…')}">${esc(stored('quri-notebook',''))}</textarea><div class="actions"><button class="btn primary" data-q="save-note">${t('保存到本机','Save locally')}</button><button class="btn" data-q="export-note">${t('导出手记','Export note')}</button><button class="btn" data-q="share-note">${t('分享','Share')}</button></div><p id="note-status" role="status"></p></div></div></section>`}
function about(){return `<section class="q-width q-workspace"><div class="q-editorial"><span class="q-eyebrow">STAY CURIOUS. FOLLOW THE EVIDENCE.</span><h2>${t('一座有证据入口的想象之城。','A city of imagination, with a trail of evidence.')}</h2><p>${t('QuriAtlas 把量子力学入门内容、图解与互动模型放在同一个学习空间。你可以从现象开始，也可以从意识、现实或灵性相关问题进入，再逐层追到原始解释和来源。','QuriAtlas brings introductory quantum physics, visual explanations, and interactive models into one learning space. Begin with an experiment or a question about consciousness and reality, then trace the reasoning and its sources.')}</p><h3>${t('科学与艺术的边界','Science and art have different roles')}</h3><p>${t('亚特兰蒂斯、星球、探索者和 memo 猫是网站的虚构美术世界。场景、发光球体和装饰性图案不是实际实验装置或量子态的准确图像。实验区另外标注模型与假设；意识讨论分别说明理论、诠释和个人体验。','Atlantis, the planets, the explorer, and memo cat form a fictional visual world. The glowing spheres and decorative motifs are not accurate depictions of apparatus or quantum states. The lab states its model assumptions, while the consciousness pages distinguish theory, interpretation, and personal experience.')}</p><h3>${t('当前收录与隐私','Collection status and privacy')}</h3><p>${t('当前为 24 个概念、20 个来源入口、4 个教学模型的研究预览，不声称全网穷尽或专家审稿完成。阅读进度、语言与手记保存在本机；没有账号、支付、公共发帖或后台 AI 对话服务。','This research preview contains 24 concepts, 20 source entries, and four teaching models. It is not an exhaustive survey or a completed expert review. Progress, language, and notebook data stay in your browser; there are no accounts, payments, public posts, or hosted AI chat.')}</p><div class="actions"><a class="btn primary" href="${pageUrl('sources')}">${t('查看来源','Read the sources')} →</a><a class="btn" href="${pageUrl('journey')}">${t('选择学习路线','Choose a learning path')} →</a></div></div></section>`}
function entanglement(){return `<section class="q-width q-workspace"><div class="q-editorial"><span class="q-eyebrow">FROM CURIOSITY TO A TESTABLE QUESTION</span>${['Q014','Q015','Q016','Q017'].map(id=>{const e=entry(id);return `<article class="q-essay"><h2>${esc(e.title)}</h2><p>${esc(e.summary)}</p><div class="note"><b>${t('解释的边界','Limits of the explanation')}</b>${esc(e.limit)}</div><p class="small">${srcLinks(e.source_ids)}</p><button class="btn" data-entry="${id}">${t('继续深入','Go deeper')} →</button></article>`}).join('')}<a class="btn primary" href="${pageUrl('lab','#bell')}">${t('亲手调整贝尔模型','Explore the Bell model')} →</a></div></section>`}
function footer(){return `<footer class="q-footer"><div class="q-width"><div class="q-footer-main">${logo()}<nav>${[['journey','学习旅程','Learning journey'],['sources','证据书架','Sources'],['about','方法与隐私','Method & privacy'],['community','探索手记','Notebook']].map(([p,z,e])=>`<a href="${pageUrl(p)}">${t(z,e)}</a>`).join('')}</nav><button class="btn quiet" data-action="motion" aria-pressed="${still}">${still?t('动效：关','Motion: off'):t('动效：开','Motion: on')}</button></div><p>${t('艺术场景为虚构视觉；实验为教学模型。保持好奇，也看见证据。','Fictional artistic scenes. Educational scientific models. Stay curious. Follow the evidence.')}</p><small>QuriAtlas × memo · <span id="release-version">${RELEASE}</span> · ${t('研究预览','Research preview')}</small></div></footer>`}
function retargetLinks(){const map={home:'home',learn:'journey',atlas:'explore',lab:'lab',bridge:'mind',history:'stories',sources:'sources',filters:'explore'};$$('#page-content a[href^="#"]').forEach(a=>{const id=a.getAttribute('href').slice(1);if(map[id]&&map[id]!==PAGE)a.href=pageUrl(map[id],'#'+id)});}
render=function(){
 legacyRender();
 const legacyMain=$('#home');legacyMain.id='legacy-home';legacyMain.hidden=true;
 const contentByPage={explore:['atlas'],lab:['lab'],mind:['bridge'],stories:['history'],journey:['learn'],sources:['sources']};
 const selected=(contentByPage[PAGE]||[]).map(id=>legacyMain.querySelector('#'+id));
 const homeMarkup=PAGE==='home'?home():innerHero();
 $('#app').innerHTML=header()+homeMarkup+`<main id="page-content" tabindex="-1"></main>`+footer();
 $('#app').appendChild(legacyMain);
 const main=$('#page-content');selected.forEach(s=>main.appendChild(s));
 if(PAGE==='play')main.innerHTML=quiz();
 if(PAGE==='community')main.innerHTML=notebook()+`<div class="q-width q-community-links">${tile('lab','和朋友试一个实验','Try an experiment together')}${tile('sources','让讨论有据可循','Ground the conversation in sources')}${tile('journey','选择下一条路线','Choose your next path')}</div>`;
 if(PAGE==='about')main.innerHTML=about();
 if(PAGE==='entanglement')main.innerHTML=entanglement();
 if(PAGE==='journey')main.insertAdjacentHTML('beforeend',notebook());
 if(PAGE==='home')main.innerHTML='';
 if(PAGE==='lab'&&location.hash==='#bell'){lab='bell';renderLab();}
 if(PAGE==='play')updateQuiz();
 retargetLinks();window.QURI_BUILD=RELEASE;document.documentElement.dataset.release=RELEASE;
 document.title=t(pages[PAGE][0]+'｜量子漫游 QuriAtlas',pages[PAGE][1]+' | QuriAtlas');
};
document.addEventListener('click',async ev=>{
 const b=ev.target.closest('[data-q],[data-quiz],[data-prompt]');if(!b)return;
 if(b.dataset.quiz!==undefined){answers[+b.dataset.quiz]=+b.dataset.choice;updateQuiz();return;}
 if(b.dataset.prompt!==undefined){const txt=b.textContent;const box=$('#notebook');box.value+=(box.value?'\n\n':'')+txt+'\n';box.focus();return;}
 const status=$('#note-status');
 switch(b.dataset.q){
 case'menu':{const menu=$('.q-mobile-menu');menu.hidden=!menu.hidden;b.setAttribute('aria-expanded',String(!menu.hidden));break;}
 case'search':if(PAGE==='explore'){$('#search').scrollIntoView({behavior:still?'auto':'smooth',block:'center'});$('#search').focus()}else location.href=pageUrl('explore','#filters');break;
 case'reset-quiz':answers={};updateQuiz();break;
 case'save-note':try{localStorage.setItem('quri-notebook',$('#notebook').value);status.textContent=t('已保存在当前浏览器。','Saved in this browser.')}catch{status.textContent=t('浏览器不允许存储，请使用导出。','Storage is unavailable. Export your note instead.')}break;
 case'export-note':{const blob=new Blob([$('#notebook').value],{type:'text/plain;charset=utf-8'});const u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download='QuriAtlas-notebook.txt';a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);break;}
 case'share-note':try{const text=$('#notebook').value;if(navigator.share)await navigator.share({title:'QuriAtlas',text,url:'https://quriatlas.saga1001.com/'});else {await navigator.clipboard.writeText(text);status.textContent=t('已复制，可粘贴分享。','Copied. Paste it to share.')}}catch(e){status.textContent=t('未完成分享；手记仍保留，可使用导出。','Sharing was not completed. Your note is still here; export it instead.')}break;
 }
});
const oldDraw=drawLab;
drawLab=function(){oldDraw();const c=$('#experiment');if(c){const dpr=Math.min(devicePixelRatio||1,2);c.setAttribute('data-render-scale','1.5');}};
render();
// Resolve legacy section URLs only once. Language preferences are kept in the query.
if(PAGE==='home'&&['#sources','#atlas','#lab','#bridge','#history','#learn'].includes(location.hash)){
 const m={'#sources':'sources','#atlas':'explore','#lab':'lab','#bridge':'mind','#history':'stories','#learn':'journey'};location.replace(pageUrl(m[location.hash],location.hash));
}
requestAnimationFrame(()=>{if(location.hash){const target=document.getElementById(location.hash.slice(1));if(target&&!target.closest('[hidden]'))target.scrollIntoView({behavior:'instant'})}});
