"""用 CJK IDS（部件描述）資料庫，依「［偏旁 部件］」反查 Unicode 字。

資料來源：https://github.com/cjkvi/cjkvi-ids （ids.txt，衍生自 CHISE IDS Database）
第一次執行會把 ids.txt 下載到 tools/build/。

用法：
    python ids_lookup.py            # 查詞表裡所有標記
    python ids_lookup.py 扌 欒       # 直接查某組部件
"""

from __future__ import annotations

import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

BUILD = Path(__file__).resolve().parent / "build"
IDS_FILE = BUILD / "ids.txt"
IDS_URL = "https://raw.githubusercontent.com/cjkvi/cjkvi-ids/master/ids.txt"

# 描述符本身不是部件
OPERATORS = set("⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻")
# 原註用的字形與 IDS 裡的部件寫法有出入，先正規化
ALIASES = {
    "屍": "尸",
    "糹": "糸", "纟": "糸",
    "衤": "衣", "忄": "心", "氵": "水", "灬": "火",
    "釒": "金", "钅": "金",
    "飠": "食", "饣": "食",
    "艹": "艸", "艸": "艸",
    "扌": "手", "犭": "犬", "阝": "阜",
    "𧾷": "足",          # 足作偏旁時的字形，IDS 多寫成這個
    "蟲": "虫",
    "⺼": "月", "肉": "月",
    "訁": "言", "讠": "言",
    "釆": "采",
    "爭": "争", "為": "為",   # IDS 用的是「争」這類字形
}


def load() -> dict[str, list[str]]:
    if not IDS_FILE.exists():
        BUILD.mkdir(parents=True, exist_ok=True)
        print(f"下載 {IDS_URL} …")
        urllib.request.urlretrieve(IDS_URL, IDS_FILE)
    table: dict[str, list[str]] = {}
    for line in IDS_FILE.read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or "\t" not in line:
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        table[parts[1]] = parts[2:]
    return table


def expand(ids: str, table: dict[str, list[str]], depth: int = 2) -> set[str]:
    """回傳這個 IDS 的部件集合；必要時把部件再拆一層，以容忍寫法差異。"""
    out = set()
    for ch in ids:
        if ch in OPERATORS or ch == "&":
            continue
        out.add(ch)
        out.add(ALIASES.get(ch, ch))
        if depth > 0:
            for sub in table.get(ch, []):
                if sub != ch and len(sub) > 1:
                    out |= expand(sub, table, depth - 1)
    return out


def search(components: list[str], table: dict[str, list[str]]) -> list[tuple[str, str, int]]:
    """找出部件涵蓋 components 的字，依部件數（愈精簡愈可能是正解）排序。"""
    want = {ALIASES.get(c, c) for c in components}
    hits = []
    for char, forms in table.items():
        if len(char) != 1:
            continue
        for ids in forms:
            if ids == char:
                continue
            direct = {ALIASES.get(c, c) for c in ids if c not in OPERATORS and c != "&"}
            if want <= direct:
                hits.append((char, ids, len(direct)))
                break
        else:
            for ids in forms:
                if want <= expand(ids, table):
                    hits.append((char, ids, len(expand(ids, table))))
                    break
    hits.sort(key=lambda h: (h[2], ord(h[0])))
    return hits


def describe(char: str) -> str:
    return f"{char} U+{ord(char):04X}"


def main() -> None:
    table = load()
    print(f"IDS 資料庫 {len(table):,} 字\n")

    if len(sys.argv) > 1:
        for char, ids, n in search(sys.argv[1:], table)[:12]:
            print(f"  {describe(char)}  {ids}  （{n} 部件）")
        return

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from write_glyph_list import APPLIED, NOT_FOUND

    groups = [("已還原", APPLIED), ("查無", NOT_FOUND)]
    for title, rows in groups:
        print(f"===== {title} =====")
        for marker, glyph, _common, _basis, _note in rows:
            body = marker.strip("［］")
            if "”" in body or "“" in body:      # 以文字敘述的條目無法反查
                print(f"  {marker:<14} （文字敘述，略）")
                continue
            comps = list(body)
            hits = search(comps, table)[:4]
            shown = "、".join(f"{describe(c)}{ids}" for c, ids, _ in hits) or "查無"
            mark = ""
            if glyph and hits:
                mark = " ✓" if glyph == hits[0][0] else (
                    " ~" if glyph in [h[0] for h in hits] else " ！與現用不同")
            print(f"  {marker:<14} 現用 {glyph or '－':<2} → {shown}{mark}")
        print()


if __name__ == "__main__":
    main()
