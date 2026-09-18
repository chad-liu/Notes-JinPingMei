"""從《金瓶梅（崇禎本）》EPUB 抽出一百回正文，輸出 chapters.json。

輸出格式：
{
  "meta": {...},
  "chapters": [
    {"n": 1, "title": "西門慶熱結十弟兄　武二郎冷遇親哥嫂",
     "paragraphs": [{"n": 1, "text": "...", "kind": "prose|verse"}]}
  ]
}
"""

from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

from bs4 import BeautifulSoup

EPUB = Path(r"D:\Notes-JinPingMei\books\金瓶梅(崇禎本).epub")
OUT = Path(__file__).resolve().parent / "build" / "chapters.json"

# 底本輸入時，國標碼表所缺的漢字一律以「［偏旁 部件］」註明。
# 這裡把已考訂出對應 Unicode 字的還原回去；未列入的仍維持原樣。
MISSING_GLYPHS = {
    # 罵詈、動作
    "［入日］": "㒲",     # 賊㒲孃的
    "［走多］": "趍",     # 趕、驅
    "［扌芻］": "搊",     # 攙扶
    "［足麗］": "躧",     # 踩、踏
    "［足鹿］": "蹗",     # 同上，崇禎本另一寫法
    "［扌昝］": "揝",     # 握、攥
    "［扌歷］": "攊",
    "［扌扉］": "𢵞",     # 擊、撞
    "［扌寨］": "㩟",
    "［屍從］": "㞞",
    "［分鹿］": "麄",     # 粗
    "［足孝］": "踍",
    "［馬婁］": "䮫",
    # 情態、身體
    "［歹帶］": "殢",     # 殢雨尤雲
    "［髟參］": "鬖",     # 黑鬖鬖
    "［悤頁］": "顖",     # 顖門。原註「悤」當為「恖」
    "［疒羅］": "癳",
    "［毛俞］": "毹",     # 氈毹
    "［毛戊］": "毧",     # 原註「戊」當為「戎」
    "［兀王］": "尪",     # 尪羸。原註「兀」當為「尢」
    # 言語、聲響
    "［口樂］": "嚛",     # 歎詞
    "［口舌］": "咶",     # 咭咶
    "［耳吉］": "聐",     # 聐聒
    "［門爭］": "䦟",
    "［門乍］": "䦛",
    # 器物、服飾、飲食
    "［糹至］": "絰",     # 孝絰
    "［囗扁］": "匾",     # 匾金補子。原註作囗，實為匚
    "［秋瓦］": "甃",     # 石甃
    "［石乞］": "矻",     # 矻磴
    "［竹貢］": "篢",     # 虛篢
    "［“蝶”“蟲”改“火”］": "煠",  # 油炸（原註為「蝶」字蟲旁改火）
    # 名物
    "［百大百］": "奭",   # 吳神仙名奭
    "［竹錢］": "籛",     # 彭籛
    "［宛鳥］": "鵷",     # 鵷鷺
    "［魚肖］": "鮹",     # 辭當作「鮫綃」
}

CHAPTER_RE = re.compile(r"^第([零一二三四五六七八九十百]+)回$")
APPENDIX_MARK = "附錄"
DIGITS = {"零": 0, "一": 1, "二": 2, "三": 3, "四": 4,
          "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def zh_number(text: str) -> int:
    """把「二十一」「一百」這類中文數字轉成整數。"""
    if text == "一百":
        return 100
    if "十" in text:
        head, _, tail = text.partition("十")
        return (DIGITS[head] if head else 1) * 10 + (DIGITS[tail] if tail else 0)
    return DIGITS[text]


def clean(text: str) -> str:
    """去掉 PDF 轉檔殘留的換行空白，還原缺字標記，保留原書全形標點。"""
    text = text.replace("\u3000", "")
    text = re.sub(r"\s+", "", text)
    for marker, glyph in MISSING_GLYPHS.items():
        text = text.replace(marker, glyph)
    return text.strip()


def spine_files(zf: zipfile.ZipFile) -> list[str]:
    opf = zf.read("content.opf").decode("utf-8")
    items = dict(re.findall(r'<item[^>]*id="([^"]+)"[^>]*href="([^"]+)"', opf))
    order = re.findall(r'<itemref[^>]*idref="([^"]+)"', opf)
    return [items[i] for i in order if i in items]


def parse_chapters() -> list[dict]:
    """解析 EPUB，回傳依回數排序的章回清單。"""
    zf = zipfile.ZipFile(EPUB)
    chapters: list[dict] = []
    current: dict | None = None
    pending_title: list[str] = []
    stop = False

    for name in spine_files(zf):
        if stop:
            break
        soup = BeautifulSoup(zf.read(name), "html.parser")
        body = soup.find("body")
        if body is None:
            continue
        for p in body.find_all("p"):
            raw = p.get_text(" ", strip=True)
            text = clean(raw)
            if not text:
                continue
            if text == APPENDIX_MARK:
                stop = True
                break
            m = CHAPTER_RE.match(text)
            if m:
                current = {"n": zh_number(m.group(1)), "title": "", "paragraphs": []}
                chapters.append(current)
                pending_title = []
                continue
            if current is None:
                continue
            klass = " ".join(p.get("class") or [])
            if not current["title"] or len(pending_title) < 2:
                # 回目兩句分行排版，收滿兩句才算標題完成
                if "calibre3" in klass and len(pending_title) < 2:
                    pending_title.append(text)
                    current["title"] = "　".join(pending_title)
                    continue
            kind = "verse" if "calibre10" in klass else "prose"
            paras = current["paragraphs"]
            if paras and paras[-1]["text"].count("［") > paras[-1]["text"].count("］"):
                # 缺字標記被排版切斷在兩個 <p> 之間，接回上一段再還原
                paras[-1]["text"] = clean(paras[-1]["text"] + text)
            elif kind == "verse" and paras and paras[-1]["kind"] == "verse":
                paras[-1]["text"] += "\n" + text
            else:
                paras.append({"n": 0, "text": text, "kind": kind})

    chapters.sort(key=lambda c: c["n"])
    for ch in chapters:
        for i, para in enumerate(ch["paragraphs"], 1):
            para["n"] = i
    return chapters


def main() -> None:
    chapters = parse_chapters()

    meta = {
        "document_id": "jinpingmei",
        "title": "金瓶梅",
        "edition": "崇禎本（張竹坡評本系統）會校足本",
        "author": "蘭陵笑笑生",
        "source_file": EPUB.name,
        "language": "zh-Hant",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps({"meta": meta, "chapters": chapters}, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )

    total_p = sum(len(c["paragraphs"]) for c in chapters)
    total_c = sum(len(p["text"]) for c in chapters for p in c["paragraphs"])
    missing = [i for i in range(1, 101) if i not in {c["n"] for c in chapters}]
    print(f"chapters={len(chapters)} paragraphs={total_p} chars={total_c} missing={missing}")
    for ch in chapters[:3] + chapters[-2:]:
        print(f'  第{ch["n"]}回 {ch["title"]} ({len(ch["paragraphs"])} 段)')


if __name__ == "__main__":
    main()
