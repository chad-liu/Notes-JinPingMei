"""稽核「婦人」在崇禎本裡究竟指誰。

結論：不是潘金蓮的專稱。「婦人」是敘事上指稱「當場那個女人」的慣用語，
隨場景轉換對象——潘金蓮約占六成，李瓶兒、王六兒各約一成。

方法上的一個教訓：不能用「往前找最近被點名的女性」來推定。
《金瓶梅》正是拿「婦人」去指**沒有被點名**的那位，所以最近的名字往往是同場的別人
（第三回的挨光場景若用該法，42 處會全判給王婆，實際上全指潘金蓮）。
底下改採「逐回抽樣讀上下文，判定各回主要指涉對象」，並把判定表寫在程式裡供覆核。

用法：
    python check_furen.py            # 各回次數、估算分布
    python check_furen.py 3 37 69    # 列出指定回的上下文抽樣
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

BOOK = Path(__file__).resolve().parent.parent / "data" / "ebook.json"
TERM = "婦人"

# 各回「婦人」的主要指涉對象，由逐回抽樣讀上下文判定。
# 未列入的回數多為零星出現或泛稱（「世上婦人」「眾婦人」「婦人科」）。
CHAPTER_REFERENT: dict[int, str] = {
    **{n: "潘金蓮" for n in (1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 27, 28, 29, 52,
                             58, 59, 72, 73, 74, 75, 76, 79, 80, 82, 83, 85, 86, 87, 88)},
    **{n: "李瓶兒" for n in (13, 14, 16, 17, 19, 20)},
    **{n: "王六兒" for n in (37, 38, 42, 50, 51, 61, 98, 99)},
    **{n: "宋蕙蓮" for n in (22, 23, 24, 25, 26)},
    **{n: "孟玉樓" for n in (7, 91, 92)},
    56: "常二嫂", 69: "林太太", 77: "賁四嫂", 90: "孫雪娥",
}


def load() -> list[tuple[int, str]]:
    book = json.loads(BOOK.read_text(encoding="utf-8"))
    return [(c["n"], p["text"]) for c in book["chapters"] for p in c["paragraphs"]]


def samples(paras: list[tuple[int, str]], chapters: list[int], per: int = 3) -> None:
    for n in chapters:
        rows = [(i, t) for ch, t in paras if ch == n
                for i in [m.start() for m in re.finditer(TERM, t)]]
        print(f"\n### 第{n}回（{len(rows)} 處）"
              f"　判定：{CHAPTER_REFERENT.get(n, '未列（零星或泛稱）')}")
        step = max(1, len(rows) // per)
        for i, t in rows[::step][:per]:
            print(f"    …{t[max(0, i - 50):i + 28]}…")


def main() -> None:
    paras = load()
    if len(sys.argv) > 1:
        samples(paras, [int(a) for a in sys.argv[1:]])
        return

    counts: dict[int, int] = {}
    for n, t in paras:
        c = t.count(TERM)
        if c:
            counts[n] = counts.get(n, 0) + c
    total = sum(counts.values())

    tally: dict[str, int] = {}
    for n, c in counts.items():
        key = CHAPTER_REFERENT.get(n, "其他／泛稱")
        tally[key] = tally.get(key, 0) + c

    print(f"「{TERM}」共 {total} 處，分布 {len(counts)} 回\n")
    print("依各回主要指涉對象估算：")
    for key, c in sorted(tally.items(), key=lambda kv: -kv[1]):
        print(f"   {key:<8} {c:>5} 處　{c / total * 100:5.1f}%")
    print(f"\n潘金蓮占 {tally.get('潘金蓮', 0) / total * 100:.1f}%——"
          f"若逕自併入潘金蓮，約 {total - tally.get('潘金蓮', 0)} 處會標錯，"
          "李瓶兒、王六兒、宋蕙蓮的場景會整段誤植。")
    print("\n各回次數：")
    line = "  ".join(f"{n}:{counts[n]}" for n in sorted(counts))
    print("   " + line)


if __name__ == "__main__":
    main()
