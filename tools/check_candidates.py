"""評估候選人名：扣掉既有詞表的長詞之後，真正還會命中幾次，並印出實際上下文。

只看 str.count 會高估——「香兒」多半是「愛香兒」的一部分。
這裡直接用與 build_data.py 相同的長詞優先比對，數候選詞真正吃到的位置。
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

BUILD = Path(__file__).resolve().parent / "build"
sys.path.insert(0, str(Path(__file__).resolve().parent))

import lexicon


def build_pattern(extra: list[str]) -> re.Pattern[str]:
    forms = {f for _t, _z, row in lexicon.iter_entities()
             for f in lexicon.surface_forms(row)} | set(extra)
    ordered = sorted(forms, key=lambda f: (-len(f), f))
    return re.compile("|".join(re.escape(f) for f in ordered))


def main() -> None:
    names = [n.strip() for n in sys.argv[1:] if n.strip()]
    if not names:
        print("用法：python check_candidates.py 名甲 名乙 …")
        return

    data = json.loads((BUILD / "chapters.json").read_text(encoding="utf-8"))
    paras = [(c["n"], p["text"]) for c in data["chapters"] for p in c["paragraphs"]]
    pattern = build_pattern(names)
    wanted = set(names)

    hits: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for ch, text in paras:
        for m in pattern.finditer(text):
            if m.group(0) in wanted:
                hits[m.group(0)].append(
                    (ch, text[max(0, m.start() - 14):m.start()]
                     + "⟪" + m.group(0) + "⟫" + text[m.end():m.end() + 14]))

    for name in names:
        rows = hits.get(name, [])
        raw = sum(t.count(name) for _c, t in paras)
        print(f"\n### {name}　實際命中 {len(rows)} 次（字串出現 {raw} 次）"
              f"　章回 {sorted({c for c, _ in rows})[:10]}")
        for _ch, ctx in rows[:3]:
            print(f"      …{ctx}…")


if __name__ == "__main__":
    main()
