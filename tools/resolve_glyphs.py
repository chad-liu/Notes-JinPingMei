"""考訂崇禎本裡「［偏旁 部件］」缺字標記對應的 Unicode 字。

方法：拿 books/ 裡梅節夢梅館校本《金瓶梅詞話》當旁證。
詞話本用的是真正的 Unicode 字，兩個版本雖非同一系統，多數句子仍可對上。
對每一處標記，取前後文到詞話本裡找「前文＋任一字＋後文」，
逐步縮短窗格直到找到唯一解；找不到或候選不唯一的就留白，由人工判讀。

輸出 tools/build/glyph_candidates.tsv，供 data/修改字.txt 整理之用。
"""

from __future__ import annotations

import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
BUILD = Path(__file__).resolve().parent / "build"
CIHUA = ["金瓶梅詞話(1)", "金瓶梅詞話(2)", "金瓶梅詞話(3)"]
MARKER_RE = re.compile(r"［[^］]{1,20}］")

# 兩個版本的標點與異體字不同，比對前一律正規化掉
PUNCT = "“”‘’「」『』，。、！？：；（）〔〕《》〈〉…—·．,.!?:;()[]"


def normalize(text: str) -> str:
    text = re.sub(r"\s+", "", text)
    return "".join(c for c in text if c not in PUNCT)


def load_cihua() -> str:
    parts = []
    for name in CIHUA:
        zf = zipfile.ZipFile(ROOT / "books" / f"{name}.epub")
        for entry in sorted(n for n in zf.namelist() if re.search(r"\.x?html?$", n)):
            parts.append(BeautifulSoup(zf.read(entry), "html.parser").get_text("\n", strip=True))
    return normalize("\n".join(parts))


def load_chongzhen() -> list[tuple[int, str]]:
    """回傳 (回數, 正規化後的段落) —— 直接從 EPUB 讀，不受缺字還原影響。"""
    import json
    data = json.loads((BUILD / "chapters.json").read_text(encoding="utf-8"))
    return [(c["n"], p["text"]) for c in data["chapters"] for p in c["paragraphs"]]


def candidates(cihua: str, before: str, after: str) -> set[str]:
    """在詞話本中找「before + 單字 + after」，回傳中間那個字的所有可能。"""
    if not before and not after:
        return set()
    pattern = re.compile(f"{re.escape(before)}(.){re.escape(after)}")
    return {m.group(1) for m in pattern.finditer(cihua)}


def resolve(cihua: str, left: str, right: str) -> tuple[str, str]:
    """由長到短嘗試窗格，回傳 (字, 判定依據)。"""
    for width in range(8, 1, -1):
        before, after = left[-width:], right[:width]
        if len(before) < width or len(after) < width:
            continue
        found = candidates(cihua, before, after)
        if len(found) == 1:
            return found.pop(), f"雙側{width}字"
    # 單側比對：前文較長時比後文可靠
    for width in range(10, 3, -1):
        before = left[-width:]
        if len(before) < width:
            continue
        found = candidates(cihua, before, "")
        if len(found) == 1:
            return found.pop(), f"前文{width}字"
    for width in range(10, 3, -1):
        after = right[:width]
        if len(after) < width:
            continue
        found = candidates(cihua, "", after)
        if len(found) == 1:
            return found.pop(), f"後文{width}字"
    return "", ""


def main() -> None:
    cihua = load_cihua()
    print(f"詞話本 {len(cihua):,} 字")
    paragraphs = load_chongzhen()

    occurrences: dict[str, list[tuple[int, str, str]]] = defaultdict(list)
    for chapter, text in paragraphs:
        clean = normalize(text)
        for m in MARKER_RE.finditer(clean):
            # 同段其他標記會干擾比對，一律換成單一佔位符再切窗格
            left = MARKER_RE.sub("〇", clean[:m.start()])
            right = MARKER_RE.sub("〇", clean[m.end():])
            occurrences[m.group(0)].append((chapter, left, right))

    rows = []
    for marker, places in sorted(occurrences.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        votes: Counter[str] = Counter()
        basis: dict[str, str] = {}
        for _chapter, left, right in places:
            glyph, how = resolve(cihua, left, right)
            if glyph and glyph != "〇" and not MARKER_RE.match(glyph):
                votes[glyph] += 1
                basis.setdefault(glyph, how)
        best, count = (votes.most_common(1)[0] if votes else ("", 0))
        rows.append({
            "marker": marker,
            "total": len(places),
            "glyph": best,
            "agree": count,
            "basis": basis.get(best, ""),
            "others": "、".join(f"{g}×{n}" for g, n in votes.most_common()[1:]),
            "chapters": sorted({c for c, _, _ in places}),
        })

    BUILD.mkdir(parents=True, exist_ok=True)
    out = BUILD / "glyph_candidates.tsv"
    with out.open("w", encoding="utf-8") as fh:
        fh.write("marker\ttotal\tglyph\tagree\tbasis\tothers\tchapters\n")
        for r in rows:
            fh.write(f"{r['marker']}\t{r['total']}\t{r['glyph']}\t{r['agree']}\t"
                     f"{r['basis']}\t{r['others']}\t{','.join(map(str, r['chapters']))}\n")

    hit = sum(1 for r in rows if r["glyph"])
    print(f"標記 {len(rows)} 種、{sum(r['total'] for r in rows)} 處；"
          f"詞話本比對出 {hit} 種")
    for r in rows:
        mark = r["glyph"] or "？"
        extra = f"  其他候選：{r['others']}" if r["others"] else ""
        print(f"  {r['marker']:<12} ×{r['total']:<3} -> {mark}  "
              f"({r['agree']}/{r['total']} {r['basis']}){extra}")
    print(f"\n-> {out}")


if __name__ == "__main__":
    main()
