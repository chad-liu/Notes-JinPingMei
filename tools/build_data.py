"""把 chapters.json 加上詞表標註，產生知識圖譜網站所需的全部 JSON。

輸出到 ../data/：
  ebook.json                  全文＋段落層級實體標註
  search_index.json           全文檢索用段落表
  basic_entity_index.json     實體索引（詞頻、段落、共現）
  entity_chapter_summary.json 實體 × 章回次數
  entity_paragraph_index.json 實體 → 段落對照
  person_social_network.json  人物共現網絡
  person_relationships.json   人工整理的語義關係
  statistics.json             統計頁資料
  articles.json               延伸閱讀

每個 JSON 另存一份 *.json.js，讓網站以 file:// 直接開啟也能載入。
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import lexicon
import relations

ROOT = Path(__file__).resolve().parent.parent
BUILD = Path(__file__).resolve().parent / "build"
OUT = ROOT / "data"
DOC = "jinpingmei"

SENTENCE_END = "。！？；"
MAX_COOCCURRENCE = 40         # 單一實體保留的共現對象數


def build_matcher() -> tuple[re.Pattern[str], dict[str, dict]]:
    """把所有表記編成一個長詞優先的正規式，並回傳表記 → 實體的對照表。"""
    form_map: dict[str, dict] = {}
    for entity_type, type_zh, row in lexicon.iter_entities():
        for form in lexicon.surface_forms(row):
            form_map.setdefault(form, {
                "key": row["id"],
                "label": row["name"],
                "type": entity_type,
                "type_zh": type_zh,
            })
    forms = sorted(form_map, key=lambda f: (-len(f), f))
    pattern = re.compile("|".join(re.escape(f) for f in forms))
    return pattern, form_map


def utf16_table(text: str) -> list[int] | None:
    """字碼位索引 → UTF-16 碼元索引的對照表。

    段落若含 BMP 以外的字（如「𢵞」U+22D5E），Python 算一個字、
    JavaScript 的 slice 算兩個碼元，其後的標記位移會整個錯開。
    全段都在 BMP 內時回傳 None，照原索引即可。
    """
    if max(map(ord, text), default=0) < 0x10000:
        return None
    table, acc = [], 0
    for ch in text:
        table.append(acc)
        acc += 2 if ord(ch) > 0xFFFF else 1
    table.append(acc)
    return table


def annotate(chapters: list[dict], pattern, form_map) -> None:
    """就地把每段文字掃出實體，寫入 paragraph['entities']。"""
    counter = 0
    for ch in chapters:
        for para in ch["paragraphs"]:
            hits = []
            table = utf16_table(para["text"])
            for m in pattern.finditer(para["text"]):
                info = form_map[m.group(0)]
                counter += 1
                hits.append({
                    "id": f"{DOC}_ne{counter:07d}",
                    "key": info["key"],
                    "label": info["label"],
                    "type": info["type"],
                    "type_zh": info["type_zh"],
                    "text": m.group(0),
                    "start": table[m.start()] if table else m.start(),
                    "end": table[m.end()] if table else m.end(),
                })
            para["entities"] = hits


def dump(name: str, payload: dict) -> None:
    path = OUT / name
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    path.write_text(text, encoding="utf-8")
    (OUT / f"{name}.js").write_text(
        "window.DEMO_JSON = window.DEMO_JSON || {};\n"
        f'window.DEMO_JSON["data/{name}"] = {text};\n',
        encoding="utf-8",
    )
    print(f"  {name:<32} {path.stat().st_size/1024:>9,.0f} KB")


def main() -> None:
    source = json.loads((BUILD / "chapters.json").read_text(encoding="utf-8"))
    meta, chapters = source["meta"], source["chapters"]

    pattern, form_map = build_matcher()
    annotate(chapters, pattern, form_map)

    entity_meta = {row["id"]: (etype, zh, row)
                   for etype, zh, row in lexicon.iter_entities()}

    # ---- ebook / search_index -------------------------------------------
    ebook_chapters = []
    search_docs = []
    paragraph_meta: dict[str, dict] = {}
    for ch in chapters:
        chapter_id = f"{DOC}_ch{ch['n']:03d}"
        paragraphs = []
        for para in ch["paragraphs"]:
            pid = f"{DOC}_p{len(paragraph_meta) + 1:05d}"
            paragraph_meta[pid] = {
                "chapter_number": ch["n"],
                "chapter_title": ch["title"],
                "paragraph_number": para["n"],
                "text": para["text"],
                "entities": para["entities"],
            }
            paragraphs.append({
                "id": pid, "n": para["n"], "kind": para["kind"],
                "text": para["text"], "entities": para["entities"],
            })
            search_docs.append({
                "id": pid, "chapter_id": chapter_id, "chapter_number": ch["n"],
                "chapter_title": ch["title"], "paragraph_number": para["n"],
                "text": para["text"],
            })
        ebook_chapters.append({
            "id": chapter_id, "n": ch["n"], "title": ch["title"], "paragraphs": paragraphs,
        })

    OUT.mkdir(parents=True, exist_ok=True)
    print("輸出 data/：")
    dump("ebook.json", {"meta": meta, "chapters": ebook_chapters})
    dump("search_index.json", {"documents": search_docs})

    # ---- 統計每個實體 ----------------------------------------------------
    freq: Counter[str] = Counter()
    forms_used: dict[str, Counter[str]] = defaultdict(Counter)
    para_ids: dict[str, list[str]] = defaultdict(list)
    chapter_hits: dict[tuple[str, int], int] = Counter()
    chapters_of: dict[str, set[int]] = defaultdict(set)
    cooccur: dict[str, Counter[str]] = defaultdict(Counter)
    person_edges: Counter[tuple[str, str]] = Counter()
    person_edge_chapters: dict[tuple[str, str], set[int]] = defaultdict(set)

    for pid, info in paragraph_meta.items():
        seen = []
        for ent in info["entities"]:
            freq[ent["key"]] += 1
            forms_used[ent["key"]][ent["text"]] += 1
            chapter_hits[(ent["key"], info["chapter_number"])] += 1
            chapters_of[ent["key"]].add(info["chapter_number"])
            if ent["key"] not in seen:
                seen.append(ent["key"])
        for key in seen:
            para_ids[key].append(pid)
        for a, b in combinations(seen, 2):
            cooccur[a][b] += 1
            cooccur[b][a] += 1
        persons = [k for k in seen if entity_meta[k][0] == "PERSON"]
        for a, b in combinations(sorted(persons), 2):
            person_edges[(a, b)] += 1
            person_edge_chapters[(a, b)].add(info["chapter_number"])

    # ---- basic_entity_index ---------------------------------------------
    entities = {}
    for key, (etype, zh, row) in entity_meta.items():
        if not freq[key]:
            continue
        entities[key] = {
            "key": key,
            "label": row["name"],
            "entity_type": etype,
            "entity_type_zh": zh,
            "entity_key": key,
            "canonical_name": row["name"],
            "subtype": row.get("subtype", ""),
            "family": row.get("family", ""),
            "bio": row.get("bio", ""),
            "frequency": freq[key],
            "paragraph_count": len(para_ids[key]),
            "chapter_count": len(chapters_of[key]),
            "surface_forms": [f for f, _ in forms_used[key].most_common()],
            "paragraphs": [{
                "chapter_number": paragraph_meta[pid]["chapter_number"],
                "paragraph_id": pid,
                "paragraph_number": paragraph_meta[pid]["paragraph_number"],
            } for pid in para_ids[key]],
            "cooccurrences": [{
                "key": other,
                "label": entity_meta[other][2]["name"],
                "type": entity_meta[other][0],
                "type_zh": entity_meta[other][1],
                "count": n,
            } for other, n in cooccur[key].most_common(MAX_COOCCURRENCE)],
        }
    dump("basic_entity_index.json", {
        "metadata": {
            "included_types": sorted({e["entity_type"] for e in entities.values()}),
            "entity_count": len(entities),
            "occurrence_count": sum(freq.values()),
            "note": "實體以人工詞表比對，長詞優先、不重疊。",
        },
        "entities": entities,
    })

    # ---- entity_chapter_summary / entity_paragraph_index -----------------
    dump("entity_chapter_summary.json", {"rows": [
        {"entity_key": key, "name": entity_meta[key][2]["name"],
         "entity_type": entity_meta[key][0], "chapter_number": n, "count": c}
        for (key, n), c in sorted(chapter_hits.items(), key=lambda kv: (kv[0][0], kv[0][1]))
    ]})
    dump("entity_paragraph_index.json", {"rows": [
        {"entity_key": key, "paragraph_count": len(pids), "paragraph_ids": pids}
        for key, pids in sorted(para_ids.items())
    ]})

    # ---- person_social_network ------------------------------------------
    person_keys = [k for k in entities if entity_meta[k][0] == "PERSON"]
    degree: Counter[str] = Counter()
    weighted: Counter[str] = Counter()
    for (a, b), w in person_edges.items():
        degree[a] += 1
        degree[b] += 1
        weighted[a] += w
        weighted[b] += w
    nodes = [{
        "id": k, "name": entities[k]["label"], "type": "PERSON",
        "subtype": entity_meta[k][2].get("subtype", "other"),
        "family": entity_meta[k][2].get("family", "other"),
        "bio": entity_meta[k][2].get("bio", ""),
        "frequency": freq[k], "chapter_count": len(chapters_of[k]),
        "paragraph_count": len(para_ids[k]),
        "degree": degree[k], "weighted_degree": weighted[k],
    } for k in person_keys]
    nodes.sort(key=lambda n: -n["weighted_degree"])
    links = [{
        "source": a, "target": b,
        "source_name": entities[a]["label"], "target_name": entities[b]["label"],
        "relation_type": "co_occurrence", "weight": w,
        "shared_paragraph_count": w, "chapter_count": len(person_edge_chapters[(a, b)]),
    } for (a, b), w in person_edges.most_common()]
    dump("person_social_network.json", {
        "metadata": {
            "network_type": "person_social_network", "node_type": "PERSON",
            "edge_relation": "co_occurrence", "edge_scope": "paragraph",
            "node_count": len(nodes), "edge_count": len(links),
            "note": "邊代表同段共現，不等於親屬或情感關係。",
        },
        "nodes": nodes, "links": links,
    })

    # ---- person_relationships -------------------------------------------
    rels, skipped = [], []
    for i, (src, dst, rtype, label, note) in enumerate(relations.RELATIONS, 1):
        if src not in entities or dst not in entities:
            skipped.append({"source": src, "target": dst, "relation_type": rtype,
                            "label": label, "reason": "missing_node"})
            continue
        rels.append({
            "relation_id": f"{DOC}_pr{i:04d}",
            "source": src, "target": dst,
            "source_name": entities[src]["label"], "target_name": entities[dst]["label"],
            "relation_type": rtype, "relation_label": label,
            "direction": "undirected", "confidence": 0.95,
            "source_method": "manual_v1", "note": note,
        })
    dump("person_relationships.json", {"relationships": rels, "skipped": skipped})

    # ---- statistics ------------------------------------------------------
    chapter_stats = []
    for ch in ebook_chapters:
        chars = sum(len(p["text"]) for p in ch["paragraphs"])
        chapter_stats.append({
            "chapter_id": ch["id"], "chapter_number": ch["n"], "title": ch["title"],
            "paragraph_count": len(ch["paragraphs"]), "char_count": chars,
        })
    total_sentences = sum(
        sum(1 for _ in re.finditer(f"[{SENTENCE_END}]", p["text"]))
        for ch in ebook_chapters for p in ch["paragraphs"])
    total_chars = sum(c["char_count"] for c in chapter_stats)

    ner_summary = []
    for etype, zh, rows in lexicon.ALL_GROUPS:
        by_subtype: dict[str, list[str]] = defaultdict(list)
        for row in rows:
            if freq[row["id"]]:
                by_subtype[row.get("subtype", "other")].append(row["id"])
        for subtype, keys in by_subtype.items():
            ner_summary.append({
                "entity_type": etype, "subtype": subtype, "source": "lexicon",
                "count": sum(freq[k] for k in keys),
                "unique_surface_count": sum(len(forms_used[k]) for k in keys),
                "unique_entity_count": len(keys),
            })

    motif_keys = [k for k in entities if entity_meta[k][0] == "MOTIF"]
    motif_summary = [{
        "motif_key": k, "motif_type": entity_meta[k][2].get("subtype", ""),
        "subtype": entities[k]["label"], "count": freq[k],
        "surface_forms": "|".join(entities[k]["surface_forms"]),
    } for k in sorted(motif_keys, key=lambda k: -freq[k])]
    motif_chapter_summary = [{
        "chapter_number": n, "motif_key": key,
        "motif_type": entity_meta[key][2].get("subtype", ""),
        "subtype": entity_meta[key][2]["name"], "count": c,
    } for (key, n), c in sorted(chapter_hits.items()) if entity_meta[key][0] == "MOTIF"]

    node_by_id = {n["id"]: n for n in nodes}
    dump("statistics.json", {
        "document": {
            **meta,
            "total_chapters": len(chapter_stats),
            "total_paragraphs": len(paragraph_meta),
            "total_sentences": total_sentences,
            "total_chars": total_chars,
            "total_entities": len(entities),
            "total_occurrences": sum(freq.values()),
        },
        "chapter_stats": chapter_stats,
        "ner_summary": sorted(ner_summary, key=lambda r: -r["count"]),
        "entity_occurrence_summary": [{
            "entity_key": k, "canonical_name": e["label"], "entity_type": e["entity_type"],
            "subtype": e["subtype"], "total_occurrences": e["frequency"],
            "chapter_count": e["chapter_count"],
            "first_chapter": min(chapters_of[k]), "last_chapter": max(chapters_of[k]),
            "surface_forms": "|".join(e["surface_forms"]),
        } for k, e in sorted(entities.items(), key=lambda kv: -kv[1]["frequency"])],
        "motif_summary": motif_summary,
        "motif_chapter_summary": motif_chapter_summary,
        "person_social_top_nodes": nodes[:30],
        "person_social_top_edges": [{
            "edge_id": f"{DOC}_edge{i:06d}", **link,
        } for i, link in enumerate(links[:50], 1)],
        "relation_summary": sorted(
            [{"relation_type": t, "count": c} for t, c in
             Counter(r["relation_type"] for r in rels).items()],
            key=lambda r: -r["count"]),
        "family_summary": sorted(
            [{"family": f, "person_count": c,
              "total_occurrences": sum(node_by_id[n]["frequency"] for n in nodes_in)}
             for f, (c, nodes_in) in {
                 fam: (len(group), group) for fam, group in
                 {fam: [n["id"] for n in nodes if n["family"] == fam]
                  for fam in {n["family"] for n in nodes}}.items()}.items()],
            key=lambda r: -r["total_occurrences"]),
    })

    dump("articles.json", {"articles": [
        {"id": "article_hou_wenyong", "title": "沒有神的所在：私房閱讀《金瓶梅》",
         "author": "侯文詠", "year": "2009", "tags": ["導讀", "人性"],
         "abstract": "從人性與慾望的角度重讀《金瓶梅》，指出這是一部沒有神、只有人的小說。",
         "links": []},
        {"id": "article_sun_shuyu", "title": "金瓶梅的藝術：凡夫俗子的寶卷",
         "author": "孫述宇", "year": "1978", "tags": ["文學研究", "敘事"],
         "abstract": "分析《金瓶梅》如何以寶卷式的因果框架承載市井人物的世情書寫。",
         "links": []},
        {"id": "article_ning_zongyi", "title": "《金瓶梅》十二講",
         "author": "寧宗一", "year": "2010", "tags": ["導讀", "講座"],
         "abstract": "十二個主題切入，談作者、版本、人物與明代社會的橫斷面。",
         "links": []},
        {"id": "article_ma_ruifang", "title": "趣話《金瓶梅》",
         "author": "馬瑞芳", "year": "2011", "tags": ["導讀", "人物"],
         "abstract": "以說書體逐回細說《金瓶梅》的人物性格與情節轉折。",
         "links": []},
        {"id": "article_meng_chao", "title": "金瓶梅人物",
         "author": "孟超", "year": "1948", "tags": ["人物論"],
         "abstract": "為書中主要人物各立專章，是本站人物簡介的主要參考。",
         "links": []},
    ]})

    print(f"\n章回 {len(chapter_stats)}　段落 {len(paragraph_meta)}　字數 {total_chars:,}")
    print(f"實體 {len(entities)}　標註 {sum(freq.values()):,} 處　"
          f"人物節點 {len(nodes)}　共現邊 {len(links)}　語義關係 {len(rels)}（略過 {len(skipped)}）")
    print("\n出現次數前 15 名：")
    for k, n in freq.most_common(15):
        print(f"   {n:>6}  {entity_meta[k][1]}　{entity_meta[k][2]['name']}")


if __name__ == "__main__":
    main()
