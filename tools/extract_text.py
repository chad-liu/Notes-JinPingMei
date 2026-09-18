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
    "［入日］": "㒲",
    "［走多］": "趍",
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


def main() -> None:
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
            if kind == "verse" and paras and paras[-1]["kind"] == "verse":
                paras[-1]["text"] += "\n" + text
            else:
                paras.append({"n": 0, "text": text, "kind": kind})

    chapters.sort(key=lambda c: c["n"])
    for ch in chapters:
        for i, para in enumerate(ch["paragraphs"], 1):
            para["n"] = i

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
