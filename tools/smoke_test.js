// 驗證 data/*.json 是否符合 index.html 與兩張圖表頁面實際讀取的欄位。
// 用法：node tools/smoke_test.js
const fs = require('fs');
const path = require('path');

const DATA = path.join(__dirname, '..', 'data');
const read = name => JSON.parse(fs.readFileSync(path.join(DATA, name), 'utf8'));

let failed = 0;
function check(label, ok, detail = '') {
  if (ok) {
    console.log(`  ok    ${label}`);
  } else {
    failed += 1;
    console.log(`  FAIL  ${label}${detail ? ' — ' + detail : ''}`);
  }
}

const ebook = read('ebook.json');
const index = read('basic_entity_index.json');
const stats = read('statistics.json');
const network = read('person_social_network.json');
const rels = read('person_relationships.json');
const search = read('search_index.json');
const articles = read('articles.json');

console.log('ebook.json');
check('章回 100 回', ebook.chapters.length === 100);
check('章回 id 格式與 data-jump 相符',
  ebook.chapters.every(c => c.id === `jinpingmei_ch${String(c.n).padStart(3, '0')}`));
check('每回都有回目與段落',
  ebook.chapters.every(c => c.title && c.title.length > 4 && c.paragraphs.length > 0));

const paragraphs = new Map();
for (const ch of ebook.chapters) for (const p of ch.paragraphs) paragraphs.set(p.id, p);
check('段落 id 不重複',
  paragraphs.size === ebook.chapters.reduce((n, c) => n + c.paragraphs.length, 0));
check('段落有 kind（詩詞段落靠它保留斷行）',
  [...paragraphs.values()].every(p => p.kind === 'prose' || p.kind === 'verse'));

let offsetBad = null;
for (const p of paragraphs.values()) {
  let cur = 0;
  for (const e of p.entities) {
    if (e.start < cur || e.end > p.text.length || p.text.slice(e.start, e.end) !== e.text) {
      offsetBad = `${p.id} ${e.text}@${e.start}`;
      break;
    }
    cur = e.end;
  }
  if (offsetBad) break;
}
check('實體位移遞增、不重疊、切片與原字串相符', offsetBad === null, offsetBad || '');
check('實體標註欄位齊全（renderMarkedParagraph 需要）',
  [...paragraphs.values()].every(p => p.entities.every(e =>
    e.key && e.label && e.type && e.type_zh && typeof e.start === 'number')));
check('實體類型只有五種（對應五個圖例）',
  [...new Set([...paragraphs.values()].flatMap(p => p.entities.map(e => e.type)))]
    .sort().join(',') === 'BUILDING,MOTIF,PERSON,PLACE,TITLE_ROLE');

console.log('\nbasic_entity_index.json');
const entities = index.entities;
check('ebook 中的每個 key 都在實體索引裡',
  [...paragraphs.values()].every(p => p.entities.every(e => entities[e.key])));
check('索引欄位齊全（showEntity 需要）',
  Object.values(entities).every(e =>
    e.label && e.entity_type_zh && typeof e.frequency === 'number' &&
    typeof e.paragraph_count === 'number' && typeof e.chapter_count === 'number' &&
    Array.isArray(e.surface_forms) && Array.isArray(e.paragraphs) &&
    Array.isArray(e.cooccurrences)));
check('索引列出的段落 id 都存在（entityText 要查得到原文）',
  Object.values(entities).every(e => e.paragraphs.every(p => paragraphs.has(p.paragraph_id))));
check('共現對象都是已知實體',
  Object.values(entities).every(e => e.cooccurrences.every(c => entities[c.key])));
check('人物都有簡介',
  Object.values(entities).filter(e => e.entity_type === 'PERSON').every(e => e.bio));

console.log('\nsearch_index.json');
check('檢索段落數與 ebook 相同', search.documents.length === paragraphs.size);
check('檢索原文與 ebook 一致',
  search.documents.every(d => paragraphs.get(d.id)?.text === d.text));

console.log('\nperson_social_network.json');
const nodeIds = new Set(network.nodes.map(n => n.id));
check('節點都帶 family（關係圖分群靠它）',
  network.nodes.every(n => n.family && n.name && typeof n.weighted_degree === 'number'));
check('邊的兩端都是已知節點',
  network.links.every(l => nodeIds.has(l.source) && nodeIds.has(l.target)));
check('節點數與 metadata 相符', network.nodes.length === network.metadata.node_count);

console.log('\nperson_relationships.json');
check('語義關係兩端都在網絡節點內',
  rels.relationships.every(r => nodeIds.has(r.source) && nodeIds.has(r.target)));
check('沒有被略過的關係', rels.skipped.length === 0, JSON.stringify(rels.skipped).slice(0, 120));
const relTypes = new Set(rels.relationships.map(r => r.relation_type));
const known = new Set(['kin', 'marriage', 'romance', 'servant', 'ally', 'patron', 'conflict']);
check('關係類型都有中文對照', [...relTypes].every(t => known.has(t)), [...relTypes].join(','));

console.log('\nstatistics.json');
check('統計卡片四個數字都在',
  ['total_paragraphs', 'total_chars', 'total_occurrences'].every(k => typeof stats.document[k] === 'number') &&
  stats.chapter_stats.length === 100);
check('章回統計欄位齊全',
  stats.chapter_stats.every(c => c.chapter_number && c.title && c.paragraph_count && c.char_count));
check('人物 Top 15 有 frequency 與 weighted_degree',
  stats.person_social_top_nodes.length >= 15 &&
  stats.person_social_top_nodes.every(n => n.name && n.frequency >= 0));
check('實體類型統計欄位齊全',
  stats.ner_summary.every(r => r.entity_type && r.subtype && typeof r.count === 'number'));
check('意象統計欄位齊全',
  stats.motif_summary.length > 0 &&
  stats.motif_summary.every(r => r.subtype && r.motif_type && typeof r.count === 'number'));
check('關係／陣營統計存在',
  stats.relation_summary.length > 0 && stats.family_summary.length > 0);

console.log('\narticles.json');
check('延伸閱讀有資料', articles.articles.length > 0 &&
  articles.articles.every(a => a.title && a.abstract));

console.log('\n*.json.js 對照');
for (const name of fs.readdirSync(DATA).filter(f => f.endsWith('.json'))) {
  const js = path.join(DATA, `${name}.js`);
  if (!fs.existsSync(js)) { check(`${name}.js 存在`, false); continue; }
  const src = fs.readFileSync(js, 'utf8');
  check(`${name}.js 註冊了正確的鍵`, src.includes(`window.DEMO_JSON["data/${name}"]`));
}

console.log(failed ? `\n${failed} 項未通過` : '\n全部通過');
process.exit(failed ? 1 : 0);
