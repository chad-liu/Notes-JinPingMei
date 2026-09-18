"""檢查詞表：列出零命中的表記，以及可能被長詞吃掉的重疊表記。"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import lexicon

BUILD = Path(__file__).resolve().parent / "build"


def main() -> None:
    data = json.loads((BUILD / "chapters.json").read_text(encoding="utf-8"))
    full = "".join(p["text"] for c in data["chapters"] for p in c["paragraphs"])

    seen: dict[str, str] = {}
    zero: list[str] = []
    dup: list[str] = []
    counts: Counter[str] = Counter()

    for entity_type, _zh, row in lexicon.iter_entities():
        for form in lexicon.surface_forms(row):
            n = full.count(form)
            counts[f"{row['id']}::{form}"] = n
            if n == 0:
                zero.append(f"{entity_type} {row['name']} <- {form}")
            if form in seen and seen[form] != row["id"]:
                dup.append(f"{form}: {seen[form]} vs {row['id']}")
            seen[form] = row["id"]

    print(f"實體總數 {sum(1 for _ in lexicon.iter_entities())}，表記總數 {len(counts)}")
    print(f"\n== 零命中 {len(zero)} ==")
    for line in zero:
        print("  ", line)
    print(f"\n== 表記撞名 {len(dup)} ==")
    for line in dup:
        print("  ", line)

    print("\n== 出現次數最低的 25 個有效表記 ==")
    for key, n in sorted((kv for kv in counts.items() if kv[1]), key=lambda kv: kv[1])[:25]:
        print(f"   {n:>5}  {key}")


if __name__ == "__main__":
    main()
