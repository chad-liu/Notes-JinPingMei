"""從 data/金瓶梅人物關係.md 抽出所有人名，核對全文出現次數，找出詞表還沒收的。

md 的章節結構本身就帶著身分資訊（「## 周守備一家」「## 三院粉頭小優」），
所以連同章節路徑一起輸出，供編寫詞表時判定 subtype 與 family。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = Path(__file__).resolve().parent / "build"
sys.path.insert(0, str(Path(__file__).resolve().parent))

import lexicon

MD = ROOT / "data" / "金瓶梅人物關係.md"
# 條列項可能是「- 名字」或「- **關係**：名甲、名乙」
BULLET = re.compile(r"^\s*-\s+(.*)$")
BOLD_KEY = re.compile(r"^\*\*(.+?)\*\*[：:]\s*(.*)$")
NAME_OK = re.compile(r"^[㐀-鿿\U00020000-\U0003ffff]{2,5}$")


def parse_md() -> list[tuple[str, str, str]]:
    """回傳 (章節路徑, 角色欄位, 人名)。"""
    rows: list[tuple[str, str, str]] = []
    heads: dict[int, str] = {}
    for line in MD.read_text(encoding="utf-8").splitlines():
        h = re.match(r"^(#{2,4})\s+(.*)$", line)
        if h:
            level = len(h.group(1))
            heads[level] = h.group(2).strip()
            for deeper in list(heads):
                if deeper > level:
                    del heads[deeper]
            continue
        b = BULLET.match(line)
        if not b:
            continue
        body = b.group(1).strip()
        role = ""
        k = BOLD_KEY.match(body)
        if k:
            role, body = k.group(1), k.group(2)
        path = " / ".join(heads[k] for k in sorted(heads))
        for name in re.split(r"[、,，]", body):
            name = name.strip().strip("*")
            if NAME_OK.match(name):
                rows.append((path, role, name))
    return rows


def main() -> None:
    data = json.loads((BUILD / "chapters.json").read_text(encoding="utf-8"))
    full = "".join(p["text"] for c in data["chapters"] for p in c["paragraphs"])

    known: dict[str, str] = {}
    for _t, _zh, row in lexicon.iter_entities():
        for form in lexicon.surface_forms(row):
            known[form] = row["id"]

    rows = parse_md()
    seen: set[str] = set()
    new: list[tuple[int, str, str, str]] = []
    zero: list[str] = []
    for path, role, name in rows:
        if name in seen:
            continue
        seen.add(name)
        if name in known:
            continue
        n = full.count(name)
        if n:
            new.append((n, name, path, role))
        else:
            zero.append(name)

    new.sort(key=lambda r: -r[0])
    print(f"md 收錄人名 {len(seen)} 個；詞表已收 "
          f"{sum(1 for n in seen if n in known)}；"
          f"未收而全文有出現 {len(new)}；未收且全文查無 {len(zero)}")
    print("\n== 未收、全文有出現（依次數排序）==")
    for n, name, path, role in new:
        print(f"{n:>5}  {name:<6} {role:<6} {path}")
    print(f"\n== 未收且全文查無 {len(zero)} 個 ==")
    print("  " + "、".join(zero))


if __name__ == "__main__":
    main()
