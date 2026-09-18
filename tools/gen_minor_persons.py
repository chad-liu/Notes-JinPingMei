"""依 data/金瓶梅人物關係.md 的名單，產生次要人物的詞表條目，附到 lexicon.py。

只收「全文確有出現、且逐一核對過上下文」的名字。
排除掉的多半是與花名、套語撞字的：海棠、芙蓉、荷花、臘梅、桃花兒是花，
「香兒」幾乎都是「丁香兒」「齊香兒」的一部分，「陳三」多半是宴席套語「湯陳三獻」，
「秋兒」則全被既有的「中秋兒」吃掉。

這支腳本是一次性的：跑完後就以 lexicon.py 為準，留著是為了說明這批條目怎麼來的。
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

# md 章節 → (subtype, family)：編寫下面 NEW_PERSONS 時的對照參考，
# 實際的 subtype/family 以每一條的手工核定為準。
SECTION_MAP = {
    "宋徽宗": ("official", "court"),
    "來往官僚": ("official", "court"),
    "陳洪一家": ("kin", "chen"),
    "陳經濟之友": ("other", "chen"),
    "親家": ("kin", "ximen"),
    "周守備一家": ("servant", "zhou"),
    "李通判之家": ("official", "court"),
    "王招宣府": ("servant", "wangzhaoxuan"),
    "來往親朋": ("kin", "ximen"),
    "各種來往人員": ("clergy", "clergy"),
    "韓道國一家": ("servant", "han"),
    "潘金蓮父母及有關人員": ("other", "other"),
    "武大郎一家": ("kin", "wu"),
    "李瓶兒前夫及親戚": ("kin", "hua"),
    "三院粉頭小優": ("courtesan", "courtesan"),
    "西門慶家奴婢、家僕": ("servant", "ximen"),
    "苗員外一家及與遇害有關人員": ("other", "other"),
    "其他人員": ("other", "other"),
    "無賴": ("other", "other"),
    "泰安州普靜寺及其他人員": ("clergy", "clergy"),
    "花子虛之奴": ("servant", "hua"),
    "王漢、李二": ("other", "han"),
    "梁山好漢": ("other", "other"),
}

# (人名, id, subtype, family, 簡介)
NEW_PERSONS: list[tuple[str, str, str, str, str]] = [
    # ---- 西門府奴婢、家僕 ----
    ("胡秀", "person_hu_xiu", "merchant", "han", "韓道國手下後生，替他押貨船往返杭州。"),
    ("王顯", "person_wang_xian", "merchant", "ximen", "西門慶緞子鋪後生，管取車稅銀兩。"),
    ("鐵棍兒", "person_tiegun", "servant", "ximen", "西門府小廝，第二十八回被西門慶糊塗打了一頓。"),
    ("小鸞", "person_xiaoluan", "maid", "ximen", "孟玉樓帶進西門府的小丫頭，與蘭香同侍。"),
    ("春燕", "person_chunyan", "servant", "ximen", "蘇州歌童，與春鴻同來，入府未久即死。"),
    ("翠兒", "person_cuier", "maid", "ximen", "後買入孫雪娥房中使喚的丫頭。"),
    ("僧寶兒", "person_sengbao", "servant", "ximen", "西門府小廝。"),
    ("倪鵬", "person_ni_peng", "merchant", "ximen", "字時遠，號桂巖，府庠生員，薦溫秀才入西門府為西席。"),
    ("水秀才", "person_shui_xiucai", "merchant", "ximen", "溫秀才之後受薦的西席人選。"),
    ("陳先生", "person_chen_xiansheng", "other", "other", "縣前代寫狀子的先生。"),
    # ---- 韓道國家 ----
    ("八老", "person_balao", "servant", "han", "韓道國家奴，末回往來傳話請客。"),
    ("錦兒", "person_jiner", "maid", "han", "王六兒買來使喚的丫頭。"),
    ("王漢", "person_wang_han", "servant", "han", "韓道國的小郎，隨他押銀往東京。"),
    # ---- 周守備府 ----
    ("月桂", "person_yuegui", "maid", "zhou", "春梅房中大丫鬟。"),
    ("玉堂", "person_yutang", "servant", "zhou", "守備府養娘，與金匱同抱金哥兒。"),
    ("金匱", "person_jingui", "servant", "zhou", "守備府養娘，抱奶金哥兒。"),
    ("蘭花", "person_lanhua", "maid", "zhou", "守備府小丫鬟。"),
    ("周仁", "person_zhou_ren", "servant", "zhou", "周守備府家人，管賞賜傳話。"),
    ("周宣", "person_zhou_xuan", "kin", "zhou", "周統制族弟，人稱二爺，末回看守宅子。"),
    # ---- 陳家 ----
    ("張氏", "person_zhangshi", "kin", "chen", "陳洪之妻、陳敬濟之母，末年母子相依。"),
    ("重喜兒", "person_chongxi", "servant", "chen", "陳家小廝。"),
    ("金錢兒", "person_jinqian", "servant", "chen", "陳家小廝。"),
    ("張世廉", "person_zhang_shilian", "kin", "chen", "陳洪之妹夫。"),
    ("楊大郎", "person_yang_dalang", "other", "chen", "陳敬濟的江湖友人，後同販貨落難。"),
    ("謝三郎", "person_xie_sanlang", "other", "chen", "陳敬濟之友。"),
    ("楊二郎", "person_yang_erlang", "other", "chen", "陳敬濟之友。"),
    ("陸二哥", "person_lu_erge", "other", "chen", "陳敬濟之友。"),
    # ---- 三院粉頭、小優 ----
    ("鄭春", "person_zheng_chun", "courtesan", "courtesan", "鄭奉之弟、鄭愛月之兄，小優兒，常入西門府彈唱。"),
    ("齊香兒", "person_qi_xianger", "courtesan", "courtesan", "二條巷齊家妓女，為王三官梳籠。"),
    ("洪四兒", "person_hong_sier", "courtesan", "courtesan", "清河妓女，常與齊香兒、董嬌兒同應局。"),
    ("韓玉釧", "person_han_yuchuan", "courtesan", "courtesan", "院中妓女，善彈琵琶。"),
    ("秦玉芝", "person_qin_yuzhi", "courtesan", "courtesan", "院中妓女。"),
    ("鄭嬌兒", "person_zheng_jiaoer", "courtesan", "courtesan", "鄭家妓女。"),
    ("董玉仙", "person_dong_yuxian", "courtesan", "courtesan", "院中妓女。"),
    ("呂賽兒", "person_lv_saier", "courtesan", "courtesan", "院中妓女。"),
    ("榮嬌兒", "person_rong_jiaoer", "courtesan", "courtesan", "院中妓女。"),
    ("消愁兒", "person_xiaochou", "courtesan", "courtesan", "韓金釧的姪女，年十三，善唱。"),
    ("薛存兒", "person_xue_cuner", "courtesan", "courtesan", "臨清私窠子。"),
    ("鄭媽媽", "person_zheng_mama", "courtesan", "courtesan", "鄭家妓院鴇母，鄭愛月之母。"),
    ("邵奉", "person_shao_feng", "courtesan", "courtesan", "小優兒，與吳惠、鄭春同班。"),
    ("邵謙", "person_shao_qian", "courtesan", "courtesan", "小優兒。"),
    ("王相", "person_wang_xiang", "courtesan", "courtesan", "小優兒，王桂之弟。"),
    ("王桂", "person_wang_gui", "courtesan", "courtesan", "小優兒，王相之兄。"),
    ("張美", "person_zhang_mei", "courtesan", "courtesan", "海鹽子弟，搬演戲文。"),
    ("徐順", "person_xu_shun", "courtesan", "courtesan", "海鹽子弟，搬演戲文。"),
    ("周順", "person_zhou_shun", "courtesan", "courtesan", "海鹽子弟，裝旦。"),
    ("袁琰", "person_yuan_yan", "courtesan", "courtesan", "海鹽子弟，貼旦。"),
    ("夏花兒", "person_xiahua", "maid", "ximen", "李嬌兒房中買來的丫頭。"),
    # ---- 朝廷權貴、官場 ----
    ("蔡攸", "person_cai_you", "official", "court", "蔡京之子，祥和殿學士，來保上東京即先見他。"),
    ("高安", "person_gao_an", "servant", "court", "蔡京府中管家，與翟謙分掌事務。"),
    ("王黼", "person_wang_fu", "official", "court", "當朝權臣，與楊戩同被劾拿送三法司。"),
    ("高俅", "person_gao_qiu", "official", "court", "太尉，朝中權貴。"),
    ("李邦彥", "person_li_bangyan", "official", "court", "朝中輔弼大臣。"),
    ("王燁", "person_wang_ye", "official", "court", "隴西公，總督京營八十萬禁軍。"),
    ("李太監", "person_li_taijian", "official", "court", "朝中太監。"),
    ("徐內相", "person_xu_neixiang", "official", "court", "清河一帶的內相。"),
    ("李內相", "person_li_neixiang", "official", "court", "清河一帶的內相。"),
    ("六黃公公", "person_liuhuang", "official", "court", "東京內相，王三官往東京磕頭的對象。"),
    ("楊盛", "person_yang_sheng", "official", "court", "楊戩名下幹辦。"),
    ("韓宗仁", "person_han_zongren", "official", "court", "楊戩名下府掾。"),
    ("趙弘道", "person_zhao_hongdao", "official", "court", "楊戩名下府掾。"),
    ("劉成", "person_liu_cheng", "official", "court", "楊戩名下班頭。"),
    ("胡四", "person_hu_si", "official", "court", "楊戩黨羽，與陳洪、西門慶同列彈章。"),
    ("董升", "person_dong_sheng", "official", "court", "王黼名下書辦官。"),
    ("王廉", "person_wang_lian", "official", "court", "王黼名下家人。"),
    ("黃玉", "person_huang_yu", "official", "court", "王黼名下班頭。"),
    ("李通判", "person_li_tongpan", "official", "court", "嚴州通判，李衙內之父。"),
    ("玉簪兒", "person_yuzan", "maid", "court", "李衙內房中丫頭，因妒孟玉樓被責賣。"),
    ("滿堂兒", "person_mantang", "servant", "court", "李通判家小廝。"),
    ("李知縣", "person_li_zhixian", "official", "court", "清河知縣。"),
    ("李達天", "person_li_datian", "official", "court", "陽穀知縣。"),
    ("樂和安", "person_yue_hean", "official", "court", "縣丞。"),
    ("夏恭基", "person_xia_gongji", "official", "court", "縣典史。"),
    ("錢勞", "person_qian_lao", "official", "court", "縣司吏，因武松案受責。"),
    ("陳文昭", "person_chen_wenzhao", "official", "court", "東平府尹，審武松案時力持公道。"),
    ("崔中書", "person_cui_zhongshu", "official", "court", "往來官員。"),
    ("胡師文", "person_hu_shiwen", "official", "court", "往來官員。"),
    ("賀千戶", "person_he_qianhu2", "official", "court", "往來武官。"),
    ("龔共", "person_gong_gong", "official", "court", "山東左佈政。"),
    ("何其高", "person_he_qigao", "official", "court", "山東左參政。"),
    ("陳四箴", "person_chen_sizhen", "official", "court", "山東右佈政。"),
    ("馮廷鵠", "person_feng_tinghu", "official", "court", "左參議。"),
    ("汪伯彥", "person_wang_boyan", "official", "court", "右參議。"),
    ("趙訥", "person_zhao_ne", "official", "court", "廉使。"),
    ("韓文光", "person_han_wenguang", "official", "court", "採訪使。"),
    ("陳正匯", "person_chen_zhenghui", "official", "court", "提學副使。"),
    ("凌雲翼", "person_ling_yunyi", "official", "court", "山東官員。"),
    ("韓邦奇", "person_han_bangqi", "official", "court", "山東官員。"),
    ("王士奇", "person_wang_shiqi", "official", "court", "青州府官。"),
    ("黃甲", "person_huang_jia", "official", "court", "登州府官。"),
    ("葉遷", "person_ye_qian", "official", "court", "萊州府官。"),
    ("李拱極", "person_li_gongji", "official", "court", "往來官員。"),
    ("錢斯成", "person_qian_sicheng", "official", "court", "往來官員。"),
    ("任良貴", "person_ren_lianggui", "official", "court", "往來官員。"),
    ("狄斯朽", "person_di_sixiu", "official", "court", "往來官員。"),
    ("狄斯彬", "person_di_sibin", "official", "court", "陽穀縣縣丞，河南舞陽人，為人剛直，查苗青一案。"),
    ("羅萬象", "person_luo_wanxiang", "official", "court", "往來官員。"),
    ("趙知府", "person_zhao_zhifu", "official", "court", "往來官員。"),
    ("侯石泉", "person_hou_shiquan", "official", "court", "往來官員。"),
    ("錢雲野", "person_qian_yunye", "official", "court", "往來官員。"),
    ("黃泰宇", "person_huang_taiyu", "official", "court", "往來官員。"),
    ("黃通判", "person_huang_tongpan", "official", "court", "審苗青一案的通判。"),
    ("高廉", "person_gao_lian", "official", "court", "本州知州，殷天錫的姊夫。"),
    ("丁相公", "person_ding_xianggong", "merchant", "other", "杭州販綢絹的客商，其子丁二官人號雙橋。"),
    # ---- 親朋 ----
    ("喬太太", "person_qiao_taitai", "kin", "ximen", "喬家女眷，出入西門府。"),
    ("吳大姨", "person_wu_dayi", "kin", "ximen", "吳家親眷。"),
    ("沈姨夫", "person_shen_yifu", "kin", "ximen", "西門府姻親。"),
    ("韓姨夫", "person_han_yifu", "kin", "ximen", "西門府姻親。"),
    ("鄭三姐", "person_zheng_sanjie", "kin", "ximen", "西門府女眷親戚。"),
    ("朱序班娘子", "person_zhu_xuban", "kin", "ximen", "序班朱家的娘子，西門府堂客。"),
    ("尚舉人娘子", "person_shang_juren", "kin", "ximen", "舉人尚家的娘子，西門府堂客。"),
    ("花大妗子", "person_hua_dajinzi", "kin", "hua", "花大舅之妻。"),
    ("姚二郎", "person_yao_erlang", "other", "wu", "武大死後收養迎兒的鄰人。"),
    ("白玉蓮", "person_bai_yulian", "other", "other", "潘金蓮在王招宣府時的同伴。"),
    ("王皇親", "person_wang_huangqin", "other", "other", "潘金蓮舊居的鄰家皇親。"),
    # ---- 醫卜僧道 ----
    ("何老人", "person_he_laoren", "clergy", "clergy", "清河老醫，何春泉之父。"),
    ("何春泉", "person_he_chunquan", "clergy", "clergy", "何老人之子，為西門慶診末疾。"),
    ("趙太醫", "person_zhao_taiyi", "clergy", "clergy", "清河庸醫，用藥荒唐。"),
    ("徐先生", "person_xu_xiansheng", "clergy", "clergy", "陰陽生，西門府喪葬擇日、開喪皆由他主持。"),
    ("祝道士", "person_zhu_daoshi", "clergy", "clergy", "泰安州道士。"),
    ("金宗明", "person_jin_zongming", "clergy", "clergy", "泰安州道人。"),
    ("郭守清", "person_guo_shouqing", "clergy", "clergy", "泰安州道童。"),
    ("雪洞禪師", "person_xuedong", "clergy", "clergy", "泰安州普靜寺禪師。"),
    # ---- 花家、王招宣府 ----
    ("天福兒", "person_tianfu", "servant", "hua", "花子虛家小廝。"),
    ("永定兒", "person_yongding", "servant", "wangzhaoxuan", "王招宣府小廝。"),
    # ---- 苗員外一案 ----
    ("翁八", "person_weng_ba", "other", "other", "揚州船家，與陳三同謀殺害苗天秀。"),
    ("樂三", "person_yue_san", "other", "other", "獅子街經紀，苗青逃匿其家。"),
    ("樂三嫂", "person_yue_sansao", "other", "other", "樂三之妻，與王六兒往來甚厚。"),
    ("黃美", "person_huang_mei", "other", "other", "苗天秀表兄，揚州舉人。"),
    ("刁七兒", "person_diao_qier", "other", "other", "苗天秀之妾。"),
    # ---- 無賴、其他 ----
    ("車淡", "person_che_dan", "other", "other", "清河潑皮，與韓二同鬧韓道國家。"),
    ("管世寬", "person_guan_shikuan", "other", "other", "清河潑皮。"),
    ("郝賢", "person_hao_xian", "other", "other", "清河潑皮。"),
    ("聶鉞兒", "person_nie_yue", "other", "other", "清河無賴。"),
    ("張小閒", "person_zhang_xiaoxian", "other", "other", "清河無賴。"),
    ("殷天錫", "person_yin_tianxi", "other", "other", "知州高廉的妻弟，仗勢橫行。"),
    ("石伯才", "person_shi_bocai", "other", "other", "泰安州一帶人物。"),
    ("陳宗美", "person_chen_zongmei", "other", "other", "泰安州一帶人物。"),
    ("小周兒", "person_xiao_zhouer", "other", "other", "篦頭待詔，替西門慶篦頭櫛發兼按摩。"),
    ("鄭紀", "person_zheng_ji", "servant", "ximen", "西門府打茶的小廝。"),
    ("張川兒", "person_zhang_chuaner", "other", "other", "清河閒漢。"),
    ("李逵", "person_li_kui", "other", "other", "梁山好漢，翠雲樓殺梁中書全家，李瓶兒因此攜財出走。"),
]

# 併入既有條目的別名（不另立實體）
ALIAS_PATCH = [("person_fu_huoji", "傅日新")]


def main() -> None:
    lines = ["", "# --------------------------------------------------------------------------",
             "# 次要人物",
             "#",
             "# 依 data/金瓶梅人物關係.md 的名單擴充，每個名字都在全文核對過上下文；",
             "# 與花名、套語撞字的一概不收（海棠、芙蓉、荷花、臘梅、桃花兒是花，",
             "# 「香兒」幾乎都是「丁香兒」「齊香兒」的一部分，「陳三」多是宴席套語",
             "# 「湯陳三獻」，「秋兒」則全被既有的「中秋兒」吃掉）。",
             "# 產生腳本：tools/gen_minor_persons.py",
             "# --------------------------------------------------------------------------",
             "",
             "PERSONS += ["]
    for name, pid, subtype, family, bio in NEW_PERSONS:
        lines.append(f'    {{"id": "{pid}", "name": "{name}", '
                     f'"subtype": "{subtype}", "family": "{family}",')
        lines.append(f'     "aliases": [], "bio": "{bio}"}},')
    lines.append("]")
    lines.append("")

    path = ROOT / "tools" / "lexicon.py"
    text = path.read_text(encoding="utf-8")
    marker = "\n# --------------------------------------------------------------------------\n# 建築／空間"
    assert marker in text
    text = text.replace(marker, "\n" + "\n".join(lines) + marker, 1)
    for pid, alias in ALIAS_PATCH:
        needle = f'"id": "{pid}"'
        i = text.index(needle)
        j = text.index('"aliases": [', i)
        k = text.index("]", j)
        inner = text[j + len('"aliases": ['):k]
        add = f'"{alias}"' if not inner.strip() else f'{inner}, "{alias}"'
        text = text[:j + len('"aliases": [')] + add + text[k:]
    path.write_text(text, encoding="utf-8")
    print(f"新增 {len(NEW_PERSONS)} 位人物，別名補丁 {len(ALIAS_PATCH)} 筆")


if __name__ == "__main__":
    main()
