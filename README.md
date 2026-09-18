# 金瓶梅知識圖譜

《金瓶梅》（崇禎本）全文一百回的數位研究平台。純 HTML／CSS／JavaScript 與靜態 JSON，
不需要後端、不需要資料庫，下載後打開 `index.html` 即可使用。

網站包含五個頁面：

- **瀏覽**：讀原文、切章回、看文內實體標註與詞頻資訊。點任一標記可看該實體的簡介、表記、共現與出處段落。
- **查詢**：精確字串與實體擴展兩種檢索。實體擴展會自動展開別名，查「潘金蓮」會一併找出「金蓮」「五娘」「六姐」。
- **人物關係圖**：150 位人物的共現網絡，疊上人工整理的婚配、私通、主僕、結拜、官場依附與仇讎關係，並依家族／陣營分群。
- **共現圖**：人物、身份、建築、地點、意象五類實體的段落共現網絡，可依章回篩選。
- **統計**：人物、實體類型、意象、章回篇幅、關係與陣營的視覺化。

## 使用方式

直接雙擊 `index.html` 即可。若瀏覽器限制本機檔案讀取，可在專案目錄執行：

```bash
python -m http.server 8788
```

再打開 <http://127.0.0.1:8788/>。

## 目錄說明

```text
.
├── index.html                  網站入口
├── person_social_graph.html    人物關係圖
├── cooccurrence_graph.html     實體共現圖
├── assets/                     樣式
├── vendor/                     D3.js
├── data/                       展示資料（JSON 與供 file:// 載入的 *.json.js）
├── books/                      原始電子書與參考書目（有版權，未入版控）
└── tools/                      資料建置腳本
```

## 資料建置

```bash
cd tools
python extract_text.py     # 從 EPUB 抽出一百回正文 -> tools/build/chapters.json
python check_lexicon.py    # 檢查詞表：零命中的表記、撞名的表記
python build_data.py       # 標註實體並產生 ../data/*.json
python resolve_glyphs.py   # 以詞話本比對缺字標記（考訂用，非必要步驟）
python write_glyph_list.py # 產生 ../data/修改字.txt
cd ..
node tools/smoke_test.js   # 驗證輸出是否符合前端讀取的欄位
```

- `tools/lexicon.py`：實體詞表。人物、建築、地點、身份、意象共 235 個實體、420 個表記，
  每個表記都先在全文中驗證過出現次數。
- `tools/relations.py`：186 筆人工整理的人物語義關係。
- `tools/patch_site.py`：把上游紅樓夢展示版改寫成金瓶梅版的一次性替換清單，留作改動記錄。

### 缺字處理

底本輸入時，凡國標碼表所缺的漢字一律寫成「［偏旁 部件］」，全書 71 種、177 處，
現已全部還原，正文不再留有任何「［　］」標記。對照表在 `tools/extract_text.py` 的
`MISSING_GLYPHS`，改一行再重跑 `extract_text.py` 與 `build_data.py` 即可生效。

- **依原刻字形還原** 60 種、163 處
- **原刻字形擴充H有收，但目前取通行字** 5 種、8 處
- **原刻字形查無，只能取通行字** 6 種、6 處

`data/修改字.txt` 是完整的考訂清單。考訂依據分三種：用 CJK IDS 部件資料庫反查、
字形與原註完全相符者標「構字」（`tools/ids_lookup.py`），以梅節夢梅館校本
《金瓶梅詞話》平行段落比對而得者標「詞話」（`tools/resolve_glyphs.py`），
由上下文成詞判定者標「辭例」。另以 ctext 的《金瓶梅第一奇書》（同屬崇禎本系統，
缺字逐一標成「●缺字：左「糸」右「堂」」）交叉印證過。

IDS 資料要用兩個來源：cjkvi-ids 只到擴充 F，而本書的缺字有十種落在擴充 H
（Unicode 15.0，2022 年才加入），得另外取 CHISE 上游的 `IDS-UCS-Ext-C…J`。
擴充 H 的字在 Windows 11 與新版 Chrome 顯示正常，舊系統或行動裝置可能顯示為方框。

## 資料來源

- 正文：`books/金瓶梅(崇禎本).epub`，崇禎本會校足本，王汝梅校，齊魯書社 1989 年版。
- 人物與關係：`data/金瓶梅人物關係.md`、`data/角色列表.txt`，並參考孟超《金瓶梅人物》等書。
- 版面與資料結構參考 [紅樓夢知識圖譜](https://github.com/cclintw/red-chamber-dream)。

## 注意事項

- 請保留完整資料夾結構，不要只複製 `index.html`。
- 實體標註出自人工詞表而非人工校讀全文，少數同名異指之處仍可能誤標，僅供研究參考。
- 原文為明代世情小說足本，內容包含大量情色與暴力描寫。
