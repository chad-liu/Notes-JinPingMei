"""把紅樓夢展示版的前端改寫成《金瓶梅》知識圖譜。

這支腳本只做「一次性」的字串替換，改完後就以 index.html 等檔案為準；
留著它是為了說明每一處改動的理由，也方便日後從上游重新套用。
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def patch(name: str, pairs: list[tuple[str, str]], *, optional: tuple[str, ...] = ()) -> None:
    path = ROOT / name
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        if old not in text:
            if old in optional:
                continue
            raise SystemExit(f"[{name}] 找不到要替換的片段：{old[:70]}")
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
    print(f"  patched {name}")


INDEX = [
    # ---- 標題與 meta ----
    ("<title>紅樓夢知識圖譜</title>", "<title>金瓶梅知識圖譜</title>"),
    ('一個結合全文閱讀、檢索、命名實體、人物關係、共現分析與統計視覺化的《紅樓夢》數位研究平台。',
     '結合全文閱讀、檢索、實體標註、人物關係、共現分析與統計視覺化的《金瓶梅》（崇禎本）數位研究平台。'),
    ('content="紅樓夢知識圖譜"', 'content="金瓶梅知識圖譜"'),
    ('content="https://cclintw.github.io/red-chamber-dream/"',
     'content="https://chad-liu.github.io/Notes-JinPingMei/"'),
    ("<h1>紅樓夢知識圖譜</h1>", "<h1>金瓶梅知識圖譜</h1>"),

    # ---- 標記圖例：紅樓夢的「花」換成金瓶梅的「意象」----
    ('<button type="button" class="legend-badge" data-tag="flower" data-tag-state="background"><span class="swatch tag-flower"></span>花</button>',
     '<button type="button" class="legend-badge" data-tag="motif" data-tag-state="background"><span class="swatch tag-motif"></span>意象</button>'),

    # ---- 導覽列加上「延伸閱讀」----
    ('<button data-view="coGraph">共現圖</button>',
     '<button data-view="coGraph">共現圖</button>\n    <button data-view="people">人物列表</button>'),
    ('<button data-view="stats">統計</button>',
     '<button data-view="stats">統計</button>\n    <button data-view="articles">延伸閱讀</button>'),

    # ---- 檢索提示 ----
    ('placeholder="搜尋原文或詞頻，例如 寶玉、海棠、太虛幻境"',
     'placeholder="搜尋原文或詞頻，例如 西門慶、獅子街、銀子"'),
    ('''        <button type="button" class="search-example" data-search-example="寶玉">寶玉</button>
        <button type="button" class="search-example" data-search-example="黛玉">黛玉</button>
        <button type="button" class="search-example" data-search-example="寶釵">寶釵</button>
        <button type="button" class="search-example" data-search-example="怡紅公子">怡紅公子</button>
        <button type="button" class="search-example" data-search-example="怡紅院">怡紅院</button>
        <button type="button" class="search-example" data-search-example="海棠">海棠</button>
        <button type="button" class="search-example" data-search-example="大觀園">大觀園</button>''',
     '''        <button type="button" class="search-example" data-search-example="西門慶">西門慶</button>
        <button type="button" class="search-example" data-search-example="潘金蓮">潘金蓮</button>
        <button type="button" class="search-example" data-search-example="李瓶兒">李瓶兒</button>
        <button type="button" class="search-example" data-search-example="龐春梅">龐春梅</button>
        <button type="button" class="search-example" data-search-example="應伯爵">應伯爵</button>
        <button type="button" class="search-example" data-search-example="獅子街">獅子街</button>
        <button type="button" class="search-example" data-search-example="銀子">銀子</button>''',),
    ('<p>精確字串只查原文中完全出現的字串；實體擴展會依權威表與別名表擴展查詢，適合人物、地點、建築、花草等實體研究。</p>',
     '<p>精確字串只查原文中完全出現的字串；實體擴展會依人工詞表與別名表擴展查詢，'
     '例如查「潘金蓮」會一併找出「金蓮」「五娘」「六姐」，適合人物、地點、建築、意象等實體研究。</p>'),

    # ---- iframe 標題 ----
    ('title="紅樓夢人物社會網絡"', 'title="金瓶梅人物社會網絡"'),
    ('title="紅樓夢實體共現圖"', 'title="金瓶梅實體共現圖"'),

    # ---- 人物列表頁 ----
    ("""  <section id="stats" class="view">""",
     """  <section id="people" class="view">
    <article class="content">
      <h2>人物列表</h2>
      <p class="meta">詞表收錄的全部人物。點任一人可跳到瀏覽頁，看他的簡介、表記、共現與出處段落。</p>
      <div class="people-tabs">
        <button type="button" class="people-tab active" data-people-tab="cards">人物卡片</button>
        <button type="button" class="people-tab" data-people-tab="chart">關係簡圖</button>
      </div>
      <div id="peopleCards" class="people-pane active">
        <div class="people-controls">
          <input id="peopleSearch" placeholder="搜尋人名、別名或簡介，例如 妓女、守備、丫鬟">
          <select id="peopleSubtype" aria-label="身分"></select>
          <select id="peopleFamily" aria-label="陣營"></select>
          <select id="peopleSort" aria-label="排序">
            <option value="frequency">依出現次數</option>
            <option value="chapter">依出場回數</option>
            <option value="name">依名稱</option>
          </select>
        </div>
        <p id="peopleCount" class="meta"></p>
        <div id="peopleList" class="people-grid"></div>
      </div>
      <div id="peopleChart" class="people-pane">
        <p class="meta">依 1987 年手繪原圖轉繪，排列順序與原圖一致（由上而下、由左而右）。
          原圖右下角另有二名人物遭浮水印遮蔽，無法辨識，故從缺。
          <a id="peopleChartLink" target="_blank" rel="noopener">另開原圖</a></p>
        <div class="chart-zoom">
          <button type="button" class="active" data-chart-fit="fit">符合寬度</button>
          <button type="button" data-chart-fit="full">原寸</button>
        </div>
        <div class="chart-frame"><img id="peopleChartImg" alt="《金瓶梅》人物關係簡圖"></div>
      </div>
    </article>
  </section>

  <section id="stats" class="view">"""),

    # ---- 統計頁區塊標題 ----
    ('<h2>意象統計</h2><div id="motifStats"></div>',
     '<h2>意象統計</h2><div id="motifStats"></div>\n      <h2>關係與陣營</h2><div id="relationStats"></div>'),
    ('<h2>NER 類型統計</h2>', '<h2>實體類型統計</h2>'),

    # ---- 延伸閱讀區塊 ----
    ('<h2>探索：研究文章</h2>', '<h2>延伸閱讀</h2>\n      <p class="meta">以下書目是本站人物簡介與詮釋角度的主要參考。</p>'),

    # ---- 頁尾 ----
    ('<footer class="site-footer">本站為實驗性網站，使用 Codex 協作完成。</footer>',
     '<footer class="site-footer">《金瓶梅》崇禎本會校足本．全文一百回．'
     '版面與資料結構參考 <a href="https://github.com/cclintw/red-chamber-dream" target="_blank" rel="noopener">紅樓夢知識圖譜</a>。'
     '實體標註出自人工詞表，僅供研究參考。</footer>'),

    # ---- 章回 id 前綴 ----
    ("hongloumeng_ch", "jinpingmei_ch"),

    # ---- 載入延伸閱讀 ----
    ("""  if (viewId === 'stats') await ensureStats();""",
     """  if (viewId === 'stats') await ensureStats();
  if (viewId === 'people') await ensurePeople();
  if (viewId === 'articles') await ensureArticles();"""),
    ("""function showLoadError(err) {""",
     """async function ensurePeople() {
  if (state.peopleReady) return;
  [state.entityIndex, state.ebook] = await Promise.all([
    state.entityIndex ? Promise.resolve(state.entityIndex) : loadJson('data/basic_entity_index.json'),
    state.ebook ? Promise.resolve(state.ebook) : loadJson('data/ebook.json')
  ]);
  initPeople();
  state.peopleReady = true;
}

async function ensureArticles() {
  if (state.articlesReady) return;
  state.articles = await loadJson('data/articles.json');
  initArticles();
  state.articlesReady = true;
}

function showLoadError(err) {"""),

    # ---- 段落標記：加入意象色，詩詞段落保留斷行 ----
    ("""    const cls = ent.type === 'PERSON' ? 'person' : ['BUILDING','FAC'].includes(ent.type) ? 'building' : ['PLACE','GPE','LOC'].includes(ent.type) ? 'place' : ent.type === 'FLOWER' ? 'flower' : 'role';""",
     """    const cls = ent.type === 'PERSON' ? 'person' : ['BUILDING','FAC'].includes(ent.type) ? 'building' : ['PLACE','GPE','LOC'].includes(ent.type) ? 'place' : ent.type === 'MOTIF' ? 'motif' : 'role';"""),
    ("""ch.paragraphs.map(p => `<p id="${p.id}" data-paragraph-number="${p.n}">${renderMarkedParagraph(p)}</p>`).join('')""",
     """ch.paragraphs.map(p => `<p id="${p.id}" class="para-${p.kind || 'prose'}" data-paragraph-number="${p.n}">${renderMarkedParagraph(p)}</p>`).join('')"""),

    # ---- 共現分組 ----
    ("""  if (ent.type === 'FLOWER') return '花草共現';""",
     """  if (ent.type === 'MOTIF') return '意象共現';"""),
    ("""  const order = ['人物共現', '身份共現', '空間／建築共現', '地點共現', '花草共現'];""",
     """  const order = ['人物共現', '身份共現', '空間／建築共現', '地點共現', '意象共現'];"""),

    # ---- 實體面板：帶出人物簡介，段落原文改由 ebook 查表（索引不再重複存全文）----
    ("""function showEntity(key) {
  const item = state.entityIndex.entities[key]; if (!item) return;
  $('#reader').classList.remove('reader-right-collapsed');
  updateReaderPanelIcons();
  const paragraphs = item.paragraphs.slice(0, 80);
  $('#entityInfo').innerHTML = `<h3>${esc(item.label)}</h3><p class="meta">${esc(item.entity_type_zh)}｜出現 ${item.frequency} 次｜段落 ${item.paragraph_count} 段</p><p class="meta">表記：${esc(item.surface_forms.join('、'))}</p>${cooccurrenceSectionHtml(item.paragraphs.map(p => p.paragraph_id), new Set([key]))}<h4>段落</h4><ol class="entity-paragraphs">${paragraphs.map(p => `<li><a href="#" data-jump="${p.chapter_number}" data-pid="${p.paragraph_id}">第${p.chapter_number}回 第${p.paragraph_number}段</a><span class="paragraph-preview" title="${esc(paragraphPreview(p.text))}">${esc(paragraphPreview(p.text))}</span></li>`).join('')}</ol>`;
}""",
     """function entityText(paragraphId) {
  return paragraphMap().get(paragraphId)?.text || '';
}
function showEntity(key) {
  const item = state.entityIndex.entities[key]; if (!item) return;
  $('#reader').classList.remove('reader-right-collapsed');
  updateReaderPanelIcons();
  const paragraphs = item.paragraphs.slice(0, 80);
  const bio = item.bio ? `<p class="entity-bio">${esc(item.bio)}</p>` : '';
  $('#entityInfo').innerHTML = `<h3>${esc(item.label)}</h3><p class="meta">${esc(item.entity_type_zh)}｜出現 ${item.frequency} 次｜段落 ${item.paragraph_count} 段｜章回 ${item.chapter_count} 回</p><p class="meta">表記：${esc(item.surface_forms.join('、'))}</p>${bio}${cooccurrenceSectionHtml(item.paragraphs.map(p => p.paragraph_id), new Set([key]))}<h4>段落</h4><ol class="entity-paragraphs">${paragraphs.map(p => `<li><a href="#" data-jump="${p.chapter_number}" data-pid="${p.paragraph_id}">第${p.chapter_number}回 第${p.paragraph_number}段</a><span class="paragraph-preview" title="${esc(paragraphPreview(entityText(p.paragraph_id)))}">${esc(paragraphPreview(entityText(p.paragraph_id)))}</span></li>`).join('')}</ol>`;
}"""),

    # ---- 實體擴展檢索：改用 ebook 取原文 ----
    ("""      item.paragraphs.forEach(p => {
        const paragraphId = p.paragraph_id;
        const forms = item.surface_forms.filter(form => form && form !== q && p.text.includes(form));""",
     """      item.paragraphs.forEach(p => {
        const paragraphId = p.paragraph_id;
        const text = entityText(paragraphId);
        const forms = item.surface_forms.filter(form => form && form !== q && text.includes(form));"""),
    ("""          text: p.text,
          entity_forms: p.text.includes(q) ? [] : forms.length ? forms : [item.label]""",
     """          text,
          entity_forms: text.includes(q) ? [] : forms.length ? forms : [item.label]"""),

    # ---- 統計卡片：句子／token 換成字數與實體標註 ----
    ("""    ['章回', s.chapter_stats.length, statIcon('book')],
    ['段落', s.document.total_paragraphs, statIcon('paragraph')],
    ['句子', s.document.total_sentences, statIcon('quote')],
    ['token', s.document.total_tokens, statIcon('token')]""",
     """    ['章回', s.chapter_stats.length, statIcon('book')],
    ['段落', s.document.total_paragraphs, statIcon('paragraph')],
    ['字數', s.document.total_chars, statIcon('quote')],
    ['實體標註', s.document.total_occurrences, statIcon('token')]"""),
    ("""  renderChapterStats(s);
}""",
     """  renderChapterStats(s);
  renderRelationStats(s);
}"""),

    # ---- 類型與子類的中文名稱 ----
    ("""const entityTypeLabels = {
  PERSON:'人物', BUILDING:'建築／空間', FAC:'設施', GPE:'政區／地名', LOC:'地點', PLACE:'地點', TITLE_ROLE:'身份', FLOWER:'花草',
  CARDINAL:'數量詞', DATE:'日期', TIME:'時間', COLOR:'顏色', MOTIF:'意象', FOOD:'飲食', OBJECT:'物件', WORK_OF_ART:'作品',
  PLANT:'植物', ORG:'組織', ROOM_SPACE:'室內空間', ORDINAL:'序數', CLOTHING:'服飾', MONEY:'金錢', QUANTITY:'度量',
  NORP:'族群／身份群體', PRODUCT:'產品', EVENT:'事件', LANGUAGE:'語言', MEDICINE:'藥物', PERCENT:'百分比'
};
const subtypeLabels = {
  main_character:'主要人物', elder:'長輩', servant:'僕役', family_member:'家族成員', official:'官職人物',
  mansion:'府邸', residence:'居所', garden_space:'園林空間', temple:'寺廟', room:'房室',
  flower:'花', plant:'植物', title:'稱謂', role:'身份', kinship:'親屬稱謂'
};
const sourceLabels = {rule:'規則', 'ckip-albert-tiny':'CKIP', 'ckip-albert-tiny+rule':'CKIP＋規則', alias:'別名表'};""",
     """const entityTypeLabels = {
  PERSON:'人物', BUILDING:'建築／空間', PLACE:'地點', TITLE_ROLE:'身份', MOTIF:'意象'
};
const subtypeLabels = {
  main_character:'主要人物', consort:'妻妾', maid:'丫鬟', servant:'僕役', hanger_on:'幫閒',
  courtesan:'妓女優伶', official:'官員', merchant:'商賈夥計', clergy:'僧道醫卜',
  matchmaker:'媒婆牙婆', kin:'親族', other:'其他',
  mansion:'府邸', garden_space:'園林空間', room:'房室', temple:'寺觀', office:'官署',
  brothel:'妓館', street:'街市',
  county:'縣治', prefecture:'府治', province:'省分', capital:'京城', city:'城鎮', town:'市鎮', landmark:'地標',
  title:'稱謂', role:'身份', official_title:'官銜'
};
const familyLabels = {
  ximen:'西門府', chen:'陳家', hua:'花家', wu:'武家', han:'韓家',
  wangzhaoxuan:'王招宣府', zhou:'周守備府', courtesan:'院中', court:'官場',
  clergy:'僧道', other:'其他'
};
const relationLabels = {
  marriage:'婚配', kin:'親屬', romance:'私通情感', servant:'主僕',
  ally:'結拜幫閒', patron:'官場依附', conflict:'仇讎'
};
const sourceLabels = {lexicon:'人工詞表'};"""),
    ("""function zhSubtype(v) { return subtypeLabels[v] || v || '未分類'; }""",
     """function zhSubtype(v) { return subtypeLabels[v] || v || '未分類'; }
function zhFamily(v) { return familyLabels[v] || v || '其他'; }
function zhRelation(v) { return relationLabels[v] || v || '其他'; }"""),

    # ---- 統計圖說明文字 ----
    ("""'依人物表記總出現次數排序。'""", """'依人物所有表記（含別名、排行稱呼）的總出現次數排序。'"""),
    # 上游這裡直接沿用依加權度排序的清單，長條圖因此不是遞減的；出現次數榜要自己重排
    ("""  const people = s.person_social_top_nodes.slice(0, 15).map(row => ({label: row.name, value: row.frequency}));""",
     """  const people = s.person_social_top_nodes.slice().sort((a, b) => num(b.frequency) - num(a.frequency)).slice(0, 15).map(row => ({label: row.name, value: row.frequency}));"""),
    ("""${chartPanel('NER 類型占比', donutChart(byType), '類型名稱已轉為中文顯示。')}${chartPanel('NER 子類數量 Top 14', barChart(bySubtype, {color:'#16a34a'}), '依 NER 子類聚合統計。')}${chartPanel('NER 來源分布', donutChart(bySource), '來源包含 CKIP、規則與混合來源。')}""",
     """${chartPanel('實體類型占比', donutChart(byType), '人物、建築、地點、身份、意象五類的標註次數占比。')}${chartPanel('實體子類數量 Top 14', barChart(bySubtype, {color:'#16a34a'}), '依人物身分與空間類型聚合統計。')}"""),
    ("""  const bySource = sumBy(s.ner_summary, row => zhSource(row.source)).slice(0, 8).map((r, i) => ({...r, color: chartColors[(i + 3) % chartColors.length]}));\n""", ""),
    ("""'依意象標註出現次數排序。'""", """'酒色財氣的物質符號：銀子、春藥、汗巾、元宵、棺材等。'"""),
    ("""'將意象依花木、文藝、夢幻等類型聚合。'""", """'將意象依財、色、酒、藝、節候、死生、命數聚合。'"""),
    ("""'紅線為字數，藍線為段落數，呈現全 120 回的篇幅變化。'""",
     """'紅線為字數，藍線為段落數，呈現全 100 回的篇幅變化。'"""),
    ("""<text x="${w-pad-46}" y="${h-8}">第120回</text>""",
     """<text x="${w-pad-46}" y="${h-8}">第100回</text>"""),

    # ---- 新增：關係與陣營統計 ----
    ("""function initArticles() {""",
     """function renderRelationStats(s) {
  const relations = (s.relation_summary || []).map((row, i) => ({label: zhRelation(row.relation_type), value: num(row.count), color: chartColors[i % chartColors.length]}));
  const families = (s.family_summary || []).map(row => ({label: zhFamily(row.family), value: num(row.total_occurrences)}));
  $('#relationStats').innerHTML = `<div class="chart-grid">${chartPanel('語義關係類型占比', donutChart(relations), '人工整理的確定關係，與同段共現不同。')}${chartPanel('各陣營出現次數', barChart(families, {color:'#7c3aed'}), '依人物所屬家族／陣營彙總其出現次數。')}</div>`;
}
function peopleRows() {
  return Object.values(state.entityIndex.entities)
    .filter(e => e.entity_type === 'PERSON')
    .map(e => ({...e, subtypeZh: zhSubtype(e.subtype), familyZh: zhFamily(e.family)}));
}
function initPeople() {
  const rows = peopleRows();
  const fill = (sel, values, label) => {
    const seen = [...new Set(values)].sort((a, b) => a.localeCompare(b, 'zh-Hant'));
    $(sel).innerHTML = `<option value="">${label}</option>` +
      seen.map(v => `<option value="${esc(v)}">${esc(v)}</option>`).join('');
  };
  fill('#peopleSubtype', rows.map(r => r.subtypeZh), '全部身分');
  fill('#peopleFamily', rows.map(r => r.familyZh), '全部陣營');
  ['#peopleSearch', '#peopleSubtype', '#peopleFamily', '#peopleSort']
    .forEach(sel => $(sel).addEventListener('input', renderPeople));
  document.querySelectorAll('[data-people-tab]').forEach(btn => btn.addEventListener('click', () => {
    document.querySelectorAll('[data-people-tab]').forEach(b => b.classList.toggle('active', b === btn));
    const chart = btn.dataset.peopleTab === 'chart';
    $('#peopleCards').classList.toggle('active', !chart);
    $('#peopleChart').classList.toggle('active', chart);
    if (chart) loadPeopleChart();
  }));
  document.querySelectorAll('[data-chart-fit]').forEach(btn => btn.addEventListener('click', () => {
    document.querySelectorAll('[data-chart-fit]').forEach(b => b.classList.toggle('active', b === btn));
    $('#peopleChart').classList.toggle('chart-full', btn.dataset.chartFit === 'full');
  }));
  $('#peopleList').addEventListener('click', async e => {
    const card = e.target.closest('[data-person]');
    if (!card) return;
    await switchView('reader');
    showEntity(card.dataset.person);
  });
  renderPeople();
}
function loadPeopleChart() {
  const img = $('#peopleChartImg');
  if (img.getAttribute('src')) return;
  const url = 'data/' + encodeURIComponent('金瓶梅人物關係簡圖.svg');
  img.src = url;
  $('#peopleChartLink').href = url;
}
function renderPeople() {
  const q = $('#peopleSearch').value.trim();
  const sub = $('#peopleSubtype').value;
  const fam = $('#peopleFamily').value;
  const rows = peopleRows().filter(r =>
    (!sub || r.subtypeZh === sub) && (!fam || r.familyZh === fam) &&
    (!q || r.label.includes(q) || (r.bio || '').includes(q) ||
     r.surface_forms.some(f => f.includes(q))));
  const order = {
    frequency: (a, b) => b.frequency - a.frequency,
    chapter: (a, b) => b.chapter_count - a.chapter_count || b.frequency - a.frequency,
    name: (a, b) => a.label.localeCompare(b.label, 'zh-Hant')
  };
  rows.sort(order[$('#peopleSort').value] || order.frequency);
  $('#peopleCount').textContent = `共 ${rows.length} 人`;
  $('#peopleList').innerHTML = rows.map(r => {
    const alias = r.surface_forms.filter(f => f !== r.label);
    return `<button type="button" class="person-card" data-person="${esc(r.key)}">
      <span class="person-head"><span class="person-name">${esc(r.label)}</span>
      <span class="person-tag">${esc(r.subtypeZh)}</span><span class="person-tag">${esc(r.familyZh)}</span></span>
      <span class="person-meta">出現 ${r.frequency} 次｜段落 ${r.paragraph_count} 段｜章回 ${r.chapter_count} 回${alias.length ? `｜又作 ${esc(alias.join('、'))}` : ''}</span>
      ${r.bio ? `<span class="person-bio">${esc(r.bio)}</span>` : ''}
    </button>`;
  }).join('') || '<p class="meta">沒有符合的人物。</p>';
}
function initArticles() {"""),
]

GRAPH = [
    ("《紅樓夢》人物關係互動圖", "《金瓶梅》人物關係互動圖"),
    ("共現 + 主僕 / 婚姻 / 親屬等語義關係", "共現＋婚配／私通／主僕／幫閒／官場等語義關係"),
    ("紅樓夢人物關係 · co-occurrence + semantic relationship",
     "金瓶梅人物關係 · co-occurrence + semantic relationship"),
    # 節點分組顏色與名稱
    ("""const groupColors = {
  main_character: "#ff6b6b",
  family_elder: "#ffd36b",
  elder: "#ffd36b",
  maid: "#6bb8ff",
  family_member: "#7bd8a3",
  secondary: "#c7a6ff",
  servant: "#ccbfff",
  official: "#64d5ff",
  opening_character: "#8ee6a2",
  concubine: "#ffb65c",
  servant_concubine: "#ffb65c"
};
const groupNames = {
  main_character: "主要人物",
  family_elder: "長輩",
  elder: "長輩",
  maid: "丫鬟",
  family_member: "家族成員",
  secondary: "次要人物",
  servant: "僕役",
  official: "官員",
  opening_character: "開篇人物",
  concubine: "妾/姨娘",
  servant_concubine: "侍妾"
};""",
     """const groupColors = {
  main_character: "#ff6b6b",
  consort: "#ffb65c",
  maid: "#6bb8ff",
  servant: "#ccbfff",
  hanger_on: "#ffd36b",
  courtesan: "#ff9ad5",
  official: "#64d5ff",
  merchant: "#7bd8a3",
  clergy: "#a5b4fc",
  matchmaker: "#fca5a5",
  kin: "#8ee6a2",
  other: "#c7a6ff"
};
const groupNames = {
  main_character: "主要人物",
  consort: "妻妾",
  maid: "丫鬟",
  servant: "僕役",
  hanger_on: "幫閒",
  courtesan: "妓女優伶",
  official: "官員",
  merchant: "商賈夥計",
  clergy: "僧道醫卜",
  matchmaker: "媒婆牙婆",
  kin: "親族",
  other: "其他"
};"""),
    ("""const relationNames = {
  co_occurrence: "同段共現",
  family: "人物-家族",
  kin: "親屬",
  marriage: "婚姻/婚配",
  romance: "情感",
  servant: "主僕/僕役",
  ally: "友誼/同盟",
  conflict: "衝突",
  rival: "對照/競合"
};""",
     """const relationNames = {
  co_occurrence: "同段共現",
  family: "人物-陣營",
  kin: "親屬",
  marriage: "婚配",
  romance: "私通/情感",
  servant: "主僕",
  ally: "結拜/幫閒",
  patron: "官場依附",
  conflict: "仇讎"
};"""),
    ("""const familyColors = {
  rongguofu: "#ff6b6b",
  ningguofu: "#6bff95",
  xue: "#ffd36b",
  lin: "#80d4ff",
  shi: "#6bb8ff",
  zhen: "#8ee6a2",
  you: "#ffb65c",
  other: "#c7a6ff"
};
const familyNames = {
  rongguofu: "榮國府",
  ningguofu: "寧國府",
  xue: "薛家",
  lin: "林家",
  shi: "史家",
  zhen: "甄家",
  you: "尤氏",
  other: "其他"
};""",
     """const familyColors = {
  ximen: "#ff6b6b",
  chen: "#ffd36b",
  hua: "#6bff95",
  wu: "#80d4ff",
  han: "#ffb65c",
  wangzhaoxuan: "#c084fc",
  zhou: "#6bb8ff",
  courtesan: "#ff9ad5",
  court: "#64d5ff",
  clergy: "#a5b4fc",
  other: "#c7a6ff"
};
const familyNames = {
  ximen: "西門府",
  chen: "陳家",
  hua: "花家",
  wu: "武家",
  han: "韓家",
  wangzhaoxuan: "王招宣府",
  zhou: "周守備府",
  courtesan: "院中",
  court: "官場",
  clergy: "僧道",
  other: "其他"
};"""),
    # 陣營改由資料提供，不再靠 id 清單硬編
    ("""function inferFamily(id) {
  if (["person_jia_baoyu", "person_jia_mu", "person_wang_xifeng", "person_wang_furen", "person_li_wan", "person_jia_tanchun", "person_jia_zheng", "person_jia_lian", "person_ping_er", "person_yuanyang", "person_zijuan", "person_jia_yingchun", "person_qingwen", "person_she_yue", "person_jia_she", "person_jia_huan", "person_xueyan", "person_zhao_yiniang", "person_jia_lan", "person_qiuwen", "person_zhou_rui_jia", "person_jia_yuanchun", "person_lai_da", "person_jinchuan", "person_yuchuan", "person_siqi", "person_ruhua", "person_shishu", "person_xiren"].includes(id)) return "rongguofu";
  if (["person_you_shi", "person_jia_zhen", "person_jia_xichun", "person_jia_rong", "person_qin_keqing"].includes(id)) return "ningguofu";
  if (["person_xue_baochai", "person_xue_yima", "person_xiangling", "person_ying_er"].includes(id)) return "xue";
  if (["person_lin_daiyu", "person_lin_ruhai"].includes(id)) return "lin";
  if (id === "person_shi_xiangyun") return "shi";
  if (id === "person_zhen_shiyin") return "zhen";
  if (["person_you_erjie", "person_you_sanjie"].includes(id)) return "you";
  return "other";
}

function mergeData(network, relationships) {
  const nodes = network.nodes.map(n => ({ ...n, family: inferFamily(n.id) }));""",
     """function mergeData(network, relationships) {
  const nodes = network.nodes.map(n => ({ ...n, family: n.family || "other" }));"""),
    ('target_name: familyNames[n.family || "other"] || n.family || "其他",',
     'target_name: familyNames[n.family || "other"] || n.family || "其他",'),
    ('relation_label: "所屬家族/陣營",', 'relation_label: "所屬家族／陣營",'),
    # 金瓶梅的人物節點有 150 個，選項與門檻要放寬
    ('<label>最低共現權重 <input id="minWeight" type="number" min="1" value="40"></label>',
     '<label>最低共現權重 <input id="minWeight" type="number" min="1" value="20"></label>'),
    ('<select id="nodeLimit"><option>20</option><option selected>35</option><option>48</option></select>',
     '<select id="nodeLimit"><option>20</option><option>40</option><option selected>60</option><option>100</option><option>200</option><option>300</option></select>'),
    ('placeholder="輸入姓名（例：賈寶玉 / 林黛玉）"', 'placeholder="輸入姓名（例：西門慶 / 潘金蓮）"'),
    ('<span class="line-sample rel-marriage"></span> 婚姻/婚配', '<span class="line-sample rel-marriage"></span> 婚配'),
    ('<span class="line-sample rel-romance"></span> 情感', '<span class="line-sample rel-romance"></span> 私通／情感'),
    ('<span class="line-sample rel-servant"></span> 主僕/僕役', '<span class="line-sample rel-servant"></span> 主僕'),
    ('<span class="line-sample rel-ally"></span> 友誼/同盟', '<span class="line-sample rel-ally"></span> 結拜／幫閒'),
    ('<span class="line-sample rel-conflict"></span> 衝突', '<span class="line-sample rel-conflict"></span> 仇讎'),
    ('<label><input type="checkbox" class="edgeType" value="rival" checked><span class="line-sample rel-rival"></span> 對照/競合</label>',
     '<label><input type="checkbox" class="edgeType" value="patron" checked><span class="line-sample rel-patron"></span> 官場依附</label>'),
    ('<span class="line-sample rel-family"></span> 人物-家族', '<span class="line-sample rel-family"></span> 人物－陣營'),
    ('l.edge_source === "family" ? "人物-家族"', 'l.edge_source === "family" ? "人物－陣營"'),
]

CO_GRAPH = [
    ("《紅樓夢》實體共現圖", "《金瓶梅》實體共現圖"),
    ("依段落共現建立人物、身份、空間建築、地點、花草的關聯。邊權重為共同出現的段落數。",
     "依段落共現建立人物、身份、空間建築、地點、意象的關聯。邊權重為共同出現的段落數。"),
    ('placeholder="輸入實體，例如 寶玉、海棠、怡紅院"',
     'placeholder="輸入實體，例如 西門慶、銀子、獅子街"'),
    ('<label><input type="checkbox" value="FLOWER" checked> 花草</label>',
     '<label><input type="checkbox" value="MOTIF" checked> 意象</label>'),
    ("  FLOWER: {label: '花草', color: '#f472b6'}", "  MOTIF: {label: '意象', color: '#f472b6'}"),
    ("""  if (type === 'BUILDING' && label.endsWith('國府')) aliases.add(label.replace('國府', '府'));
""", ""),
]

CSS = [
    ("--accent: #b42318;", "--accent: #9f1239;"),
    ("nav button.active { background: #fee4e2; color: #912018; }",
     "nav button.active { background: #ffe4e6; color: #9f1239; }"),
    (".search-mode button.active { background: #fee4e2; color: #912018; }",
     ".search-mode button.active { background: #ffe4e6; color: #9f1239; }"),
    (".entity-flower { background: #fce7f3; }", ".entity-motif { background: #fce7f3; }"),
    ("#reader.tag-flower-underline .entity-flower { background: transparent; border-bottom-color: #db2777; }",
     "#reader.tag-motif-underline .entity-motif { background: transparent; border-bottom-color: #db2777; }"),
    ("    #reader.tag-flower-off .entity-flower { background: transparent; border-bottom-color: transparent; }",
     "    #reader.tag-motif-off .entity-motif { background: transparent; border-bottom-color: transparent; }"),
    (".swatch.tag-flower { --tag-color: #db2777; background: #fce7f3; border: 1px solid var(--tag-color); }",
     ".swatch.tag-motif { --tag-color: #db2777; background: #fce7f3; border: 1px solid var(--tag-color); }"),
    # 詩詞段落保留原書斷行；人物簡介樣式
    ("    .chapter-end { border: 0;",
     """    #readerContent p.para-verse { white-space: pre-wrap; text-indent: 0; margin-left: 2em; color: #334155; }
    .entity-bio { margin: 10px 0 4px; font-size: 13px; line-height: 1.7; color: #334155; border-left: 3px solid #fecdd3; padding-left: 10px; }
    #people.view.active { display: block; }
    #people .content { max-width: 1040px; margin: 0 auto; }
    .people-controls { display: grid; grid-template-columns: minmax(0, 2fr) repeat(3, minmax(0, 1fr)); gap: 10px; margin: 18px 0 12px; }
    .people-controls input, .people-controls select { padding: 9px 11px; }
    .people-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 12px; margin-bottom: 40px; }
    .person-card { display: grid; gap: 6px; text-align: left; font: inherit; border: 1px solid var(--border); border-radius: 8px; background: #fff; padding: 12px 14px; cursor: pointer; }
    .person-card:hover { border-color: #f9a8b4; background: #fffafb; }
    .person-head { display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap; }
    .person-name { font-family: "Noto Serif TC","Songti TC","PingFang TC","Microsoft JhengHei",serif; font-size: 19px; color: #1f2328; }
    .person-tag { border: 1px solid #e5e7eb; border-radius: 999px; padding: 1px 8px; font-size: 12px; color: #64748b; }
    .person-meta { font-size: 12px; line-height: 1.6; color: #64748b; }
    .person-bio { font-size: 13px; line-height: 1.7; color: #334155; }
    @media (max-width: 1024px) { .people-controls { grid-template-columns: 1fr 1fr; } }
    @media (max-width: 520px) { .people-controls { grid-template-columns: 1fr; } }
    .people-tabs { display: inline-flex; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; margin: 18px 0 2px; }
    .people-tab { border: 0; border-left: 1px solid var(--border); background: #fff; color: #64748b; padding: 8px 18px; cursor: pointer; font: inherit; font-size: 15px; }
    .people-tab:first-child { border-left: 0; }
    .people-tab.active { background: #ffe4e6; color: #9f1239; }
    .people-pane { display: none; }
    .people-pane.active { display: block; }
    #peopleChart .meta { margin: 14px 0 0; line-height: 1.7; }
    #peopleChart .meta a { color: #9f1239; }
    .chart-zoom { display: inline-flex; gap: 8px; margin: 10px 0 12px; }
    .chart-zoom button { border: 1px solid #d0d7de; background: #fff; border-radius: 999px; color: #64748b; cursor: pointer; padding: 4px 12px; font: inherit; font-size: 13px; }
    .chart-zoom button.active { border-color: #f9a8b4; color: #9f1239; }
    .chart-frame { border: 1px solid var(--border); border-radius: 8px; background: #fbf8f1; overflow: auto; max-height: 80vh; margin-bottom: 40px; }
    .chart-frame img { display: block; width: 100%; height: auto; }
    #peopleChart.chart-full .chart-frame img { width: 1800px; max-width: none; }
    .chapter-end { border: 0;"""),
]


GRAPH_CSS = [
    (".line-sample.rel-rival { border-color: #ffd166; border-top-style: dashed; }",
     ".line-sample.rel-patron { border-color: #ffd166; border-top-style: dashed; }"),
    (".link.rel-rival { stroke: #ffd166; stroke-dasharray: 8 4 2 4; }",
     ".link.rel-patron { stroke: #ffd166; stroke-dasharray: 8 4 2 4; }"),
]


def main() -> None:
    print("改寫前端：")
    patch("index.html", INDEX)
    patch("person_social_graph.html", GRAPH)
    patch("cooccurrence_graph.html", CO_GRAPH)
    patch("assets/index.css", CSS)
    patch("assets/person-social-graph.css", GRAPH_CSS)


if __name__ == "__main__":
    main()
