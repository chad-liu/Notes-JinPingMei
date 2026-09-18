"""《金瓶梅》人物語義關係表。

與「同段共現」不同，這裡是人工整理的確定關係：婚配、親屬、私通、主僕、
結拜幫閒、官場往來與仇讎。資料來源為 data/金瓶梅人物關係.md 與小說情節。

每筆：(來源, 對象, 關係類型, 關係標籤, 說明)
關係類型：marriage 婚配／kin 親屬／romance 私通情感／servant 主僕／
          ally 結拜幫閒／patron 官場依附／conflict 仇讎
"""

from __future__ import annotations

X = "person_ximen_qing"

RELATIONS: list[tuple[str, str, str, str, str]] = [
    # ---- 西門慶的妻妾 ----------------------------------------------------
    (X, "person_chenshi", "marriage", "元配", "西門慶先頭渾家，早逝。"),
    (X, "person_wu_yueniang", "marriage", "正室（填房）", "吳千戶之女，繼室，人稱大娘。"),
    (X, "person_li_jiaoer", "marriage", "第二房妾", "妓院出身，應伯爵做媒。"),
    (X, "person_zhuo_diuer", "marriage", "第三房妾", "南街窠子卓二姐，入門未久即亡。"),
    (X, "person_meng_yulou", "marriage", "第三房妾", "布商楊宗錫遺孀，薛嫂做媒。"),
    (X, "person_sun_xuee", "marriage", "第四房妾", "陳氏陪嫁丫頭收房。"),
    (X, "person_pan_jinlian", "marriage", "第五房妾", "毒殺武大郎後偷娶進門。"),
    (X, "person_li_pinger", "marriage", "第六房妾", "花子虛之妻，攜家產改嫁。"),
    (X, "person_pang_chunmei", "romance", "收房丫頭", "潘金蓮薦於西門慶。"),

    # ---- 西門慶的私通對象 ------------------------------------------------
    (X, "person_song_huilian", "romance", "私通", "來旺之妻，因私通得寵。"),
    (X, "person_wang_liuer", "romance", "包占", "韓道國之妻。"),
    (X, "person_lin_taitai", "romance", "私通", "文嫂牽線，王招宣府貴婦。"),
    (X, "person_ruyier", "romance", "私通", "官哥奶媽，瓶兒死後頂替其位。"),
    (X, "person_bensi_sao", "romance", "私通", "賁四之妻。"),
    (X, "person_li_guijie", "romance", "梳攏包占", "麗春院名妓。"),
    (X, "person_zheng_aiyue", "romance", "包占", "鄭家妓院名妓。"),
    (X, "person_wu_yiner", "romance", "應酬", "妓女，拜李瓶兒為乾娘。"),
    (X, "person_shutong", "romance", "男寵", "書房小廝，因貌美受寵。"),

    # ---- 西門慶家的親屬 --------------------------------------------------
    (X, "person_ximen_dajie", "kin", "父女", "西門慶與陳氏所生。"),
    (X, "person_guange", "kin", "父子", "李瓶兒所生，未滿週歲夭折。"),
    (X, "person_xiaoge", "kin", "父子", "吳月娘所生，書末出家。"),
    ("person_li_pinger", "person_guange", "kin", "母子", "官哥為瓶兒所生。"),
    ("person_wu_yueniang", "person_xiaoge", "kin", "母子", "孝哥為月娘所生。"),
    ("person_wu_yueniang", "person_wu_dajiu", "kin", "兄妹", "吳大舅為月娘之兄。"),
    ("person_wu_yueniang", "person_wu_erjiu", "kin", "姊弟", "吳二舅為月娘之弟。"),
    ("person_wu_dajiu", "person_wu_dajinzi", "marriage", "夫妻", "吳大舅與吳大妗子。"),
    ("person_pan_jinlian", "person_pan_laolao", "kin", "母女", "潘姥姥為金蓮之母。"),
    ("person_meng_yulou", "person_yang_zongxi", "marriage", "前夫", "玉樓原為楊宗錫之妻。"),
    ("person_meng_yulou", "person_yang_guniang", "kin", "姑姪媳", "楊姑娘力主玉樓改嫁。"),
    ("person_meng_yulou", "person_zhang_si", "kin", "舅甥媳", "張四舅欲阻玉樓改嫁圖財。"),
    ("person_yang_guniang", "person_zhang_si", "conflict", "口角", "楊姑娘氣罵張四舅。"),
    ("person_meng_yulou", "person_meng_erjiu", "kin", "兄妹", "孟二舅為玉樓兄弟。"),
    ("person_li_jiaoer", "person_li_guijie", "kin", "姑姪", "李桂姐為李嬌兒姪女。"),
    ("person_li_jiaoer", "person_li_ming", "kin", "兄妹", "李銘為李嬌兒之兄。"),
    (X, "person_qiao_daohu", "kin", "兒女親家", "官哥與喬大戶之女結親。"),

    # ---- 陳家 ------------------------------------------------------------
    ("person_chen_jingji", "person_ximen_dajie", "marriage", "夫妻", "陳敬濟娶西門大姐。"),
    ("person_chen_jingji", "person_chen_hong", "kin", "父子", "陳洪為敬濟之父。"),
    (X, "person_chen_jingji", "kin", "翁婿", "敬濟因父案寄居西門府。"),
    ("person_chen_jingji", "person_pan_jinlian", "romance", "私通", "全書後半的核心姦情。"),
    ("person_chen_jingji", "person_pang_chunmei", "romance", "私通", "春梅在守備府收留敬濟。"),
    ("person_chen_jingji", "person_feng_jinbao", "marriage", "續娶", "臨清妓女。"),
    ("person_chen_jingji", "person_ge_cuiping", "marriage", "續娶", "守備府作媒。"),
    ("person_chen_jingji", "person_han_aijie", "romance", "情緣", "愛姐為敬濟守志。"),
    ("person_chen_jingji", "person_zhang_sheng", "conflict", "仇殺", "張勝受春梅指使殺敬濟。"),
    ("person_chen_jingji", "person_sun_xuee", "conflict", "仇怨", "雪娥唆打陳敬濟。"),

    # ---- 花家 ------------------------------------------------------------
    ("person_hua_zixu", "person_li_pinger", "marriage", "夫妻", "瓶兒原為子虛之妻。"),
    ("person_hua_zixu", "person_hua_taijian", "kin", "叔姪", "花太監家產由子虛承繼。"),
    ("person_hua_zixu", "person_hua_dajiu", "kin", "兄弟", "曾為爭產打官司。"),
    (X, "person_hua_zixu", "ally", "結拜兄弟", "十兄弟之一，卻遭西門慶吞其家財。"),
    ("person_li_pinger", "person_jiang_zhushan", "marriage", "招贅", "子虛死後短暫入贅。"),
    (X, "person_jiang_zhushan", "conflict", "報復", "西門慶使草裡蛇邏打蔣竹山。"),
    ("person_li_pinger", "person_liang_zhongshu", "marriage", "前夫", "大名府梁中書。"),
    ("person_li_pinger", "person_yingchun", "servant", "主僕", "迎春為瓶兒貼身丫頭。"),
    ("person_li_pinger", "person_xiuchun", "servant", "主僕", "繡春為瓶兒房中丫頭。"),
    ("person_li_pinger", "person_feng_mama", "servant", "主僕", "馮媽媽替瓶兒看房傳話。"),
    ("person_li_pinger", "person_wu_yiner", "kin", "乾母女", "吳銀兒拜瓶兒為乾娘。"),

    # ---- 武家 ------------------------------------------------------------
    ("person_wu_dalang", "person_pan_jinlian", "marriage", "夫妻", "金蓮原為武大之妻。"),
    ("person_wu_dalang", "person_wu_song", "kin", "兄弟", "武松為武大之弟。"),
    ("person_wu_dalang", "person_yinger", "kin", "父女", "迎兒為武大之女。"),
    ("person_pan_jinlian", "person_wu_song", "romance", "求歡不成", "金蓮挑逗武松被拒。"),
    ("person_wu_song", "person_pan_jinlian", "conflict", "殺嫂", "武松殺嫂祭兄。"),
    ("person_wu_song", X, "conflict", "仇讎", "歸來時西門慶已死。"),
    ("person_wu_song", "person_wang_po", "conflict", "仇殺", "王婆與金蓮同死於武松刀下。"),
    ("person_wang_po", "person_pan_jinlian", "ally", "撮合設計", "縣前街茶坊撮合並獻毒計。"),
    (X, "person_wang_po", "ally", "撮合設計", "王婆為西門慶設十分光計。"),
    ("person_wang_po", "person_wang_chaoer", "kin", "母子", "王潮兒為王婆之子。"),
    ("person_wu_dalang", "person_yunge", "ally", "通風報信", "鄆哥報信助武大捉姦。"),
    ("person_yunge", "person_wang_po", "conflict", "鬧茶坊", "鄆哥義憤鬧王婆茶坊。"),
    (X, "person_hejiu", "patron", "行賄", "何九受賄瞞下武大屍證。"),
    ("person_wu_song", "person_li_waizhuan", "conflict", "誤打致死", "武松誤打李皂隸。"),

    # ---- 韓家 ------------------------------------------------------------
    ("person_han_daoguo", "person_wang_liuer", "marriage", "夫妻", "靠妻與西門慶的關係得利。"),
    ("person_han_daoguo", "person_han_aijie", "kin", "父女", "愛姐為韓家之女。"),
    ("person_han_daoguo", "person_han_er", "kin", "兄弟", "韓二為道國之弟。"),
    ("person_wang_liuer", "person_han_er", "romance", "叔嫂私通", "書中屢次點出。"),
    (X, "person_han_daoguo", "patron", "東家夥計", "絨線鋪夥計。"),
    ("person_han_aijie", "person_zhai_qian", "marriage", "妾", "愛姐入翟府為妾。"),
    ("person_wang_liuer", "person_wangjing", "kin", "姑姪", "王經為六兒姪兒。"),

    # ---- 王招宣府 --------------------------------------------------------
    ("person_lin_taitai", "person_wang_sanguan", "kin", "母子", "王三官為林太太之子。"),
    ("person_lin_taitai", "person_wang_zhaoxuan", "marriage", "夫妻", "招宣死後林太太守寡。"),
    (X, "person_wang_sanguan", "kin", "義父子", "三官拜西門慶為義父，稱其四泉。"),
    ("person_wang_sanguan", "person_li_guijie", "romance", "嫖妓", "被鄭愛月連環計拆散。"),
    (X, "person_wen_sao", "ally", "牽線", "文嫂替西門慶勾搭林太太。"),
    ("person_lin_taitai", "person_wen_sao", "ally", "牽線", "文嫂往來招宣府。"),

    # ---- 周守備府 --------------------------------------------------------
    ("person_zhou_shoubei", "person_pang_chunmei", "marriage", "妾後扶正", "春梅生子扶正為夫人。"),
    ("person_zhou_shoubei", "person_sun_erniang", "marriage", "妾", "守備府側室。"),
    ("person_zhou_shoubei", "person_zhang_sheng", "servant", "主僕", "守備府家丁。"),
    ("person_zhou_shoubei", "person_li_an", "servant", "主僕", "守備府家丁。"),
    ("person_pang_chunmei", "person_zhou_yi", "romance", "私通", "守備出征後縱情。"),
    ("person_pang_chunmei", "person_sun_xuee", "conflict", "仇怨", "春梅用計整治孫雪娥。"),
    ("person_pang_chunmei", "person_pan_jinlian", "ally", "主僕情誼", "春梅厚葬金蓮。"),

    # ---- 西門府主僕 ------------------------------------------------------
    (X, "person_daian", "servant", "主僕", "最得力的心腹小廝。"),
    (X, "person_pingan", "servant", "主僕", "看門小廝。"),
    (X, "person_laiwang", "servant", "主僕", "家僕，後遞解徐州。"),
    (X, "person_laibao", "servant", "主僕", "管事家僕，常往東京。"),
    (X, "person_laixing", "servant", "主僕", "家僕。"),
    (X, "person_laijue", "servant", "主僕", "家僕。"),
    (X, "person_laizhao", "servant", "主僕", "家僕。"),
    (X, "person_qintong", "servant", "主僕", "小廝。"),
    (X, "person_huatong", "servant", "主僕", "小廝。"),
    (X, "person_chunhong", "servant", "主僕", "蘇州歌童。"),
    (X, "person_wangjing", "servant", "主僕", "收用的小廝。"),
    (X, "person_fu_huoji", "patron", "東家夥計", "生藥鋪老夥計。"),
    (X, "person_gan_huoji", "patron", "東家夥計", "絨線鋪夥計。"),
    (X, "person_ben_si", "patron", "東家夥計", "管工程與鋪面。"),
    (X, "person_cui_ben", "patron", "東家夥計", "緞子鋪夥計。"),
    (X, "person_wen_bigu", "patron", "西席", "代筆書啟往來。"),
    (X, "person_wu_dianen", "patron", "提攜", "受西門慶保薦得官。"),
    ("person_laiwang", "person_song_huilian", "marriage", "夫妻", "蕙蓮為來旺之妻。"),
    ("person_laiwang", "person_sun_xuee", "romance", "私通", "西門慶死後同逃。"),
    ("person_laizhao", "person_yizhangqing", "marriage", "夫妻", "一丈青為來昭之妻。"),
    ("person_laixing", "person_huixiang", "marriage", "夫妻", "惠祥為來興之妻。"),
    ("person_laijue", "person_huiyuan", "marriage", "夫妻", "惠元為來爵之妻。"),
    ("person_ben_si", "person_bensi_sao", "marriage", "夫妻", "賁四嫂為賁四之妻。"),
    ("person_daian", "person_bensi_sao", "romance", "私通", "主僕同槽共食。"),
    ("person_daian", "person_xiaoyu", "marriage", "夫妻", "月娘撮合成親。"),
    ("person_wu_yueniang", "person_daian", "kin", "義母子", "月娘認玳安為子，改名西門安。"),
    ("person_wu_yueniang", "person_xiaoyu", "servant", "主僕", "小玉為月娘貼身丫頭。"),
    ("person_wu_yueniang", "person_yuxiao", "servant", "主僕", "玉簫為月娘房中丫鬟。"),
    ("person_yuxiao", "person_shutong", "romance", "有染", "書童與玉簫私情。"),
    ("person_pan_jinlian", "person_pang_chunmei", "servant", "主僕", "春梅轉為伺候金蓮。"),
    ("person_pan_jinlian", "person_chunmei_qiuju", "servant", "主僕", "秋菊屢遭凌虐。"),
    ("person_pang_chunmei", "person_chunmei_qiuju", "conflict", "凌虐", "春梅與金蓮共同責打秋菊。"),
    ("person_meng_yulou", "person_lanxiang", "servant", "主僕", "蘭香為玉樓房中丫鬟。"),
    ("person_sun_xuee", "person_zhongqiu", "servant", "主僕", "中秋兒為雪娥丫鬟。"),
    ("person_pan_jinlian", "person_sun_xuee", "conflict", "仇怨", "金蓮激打孫雪娥。"),
    ("person_pan_jinlian", "person_li_pinger", "conflict", "妒恨", "因官哥出生結怨。"),
    ("person_pan_jinlian", "person_song_huilian", "conflict", "設計陷害", "金蓮設計害來旺以除蕙蓮。"),
    ("person_pan_jinlian", "person_li_jiaoer", "conflict", "對頭", "李嬌兒與雪娥同為金蓮對頭。"),
    ("person_song_huilian", "person_song_ren", "kin", "父女", "宋仁告官反被問罪。"),
    ("person_song_huilian", "person_jiang_cong", "marriage", "前夫", "廚役蔣聰。"),
    ("person_ruyier", "person_guange", "servant", "乳母", "官哥的奶媽。"),
    ("person_ruyier", "person_xiaoge", "servant", "乳母", "瓶兒死後改侍孝哥。"),

    # ---- 結拜十兄弟與幫閒 -------------------------------------------------
    (X, "person_ying_bojue", "ally", "結拜兄弟", "十兄弟中排行第二，幫閒領班。"),
    (X, "person_xie_xida", "ally", "結拜兄弟", "十兄弟之一。"),
    (X, "person_zhu_shinian", "ally", "結拜兄弟", "十兄弟之一。"),
    (X, "person_sun_guazui", "ally", "結拜兄弟", "十兄弟之一。"),
    (X, "person_chang_zhijie", "ally", "結拜兄弟", "十兄弟中排行老九。"),
    (X, "person_bai_laiguang", "ally", "結拜兄弟", "十兄弟之一。"),
    (X, "person_yun_lishou", "ally", "結拜兄弟", "十兄弟之一。"),
    (X, "person_bu_zhidao", "ally", "結拜兄弟", "開篇即亡，由花子虛遞補。"),
    ("person_ying_bojue", "person_xie_xida", "ally", "幫閒同伴", "兩人常相伴出入。"),
    ("person_ying_bojue", "person_li_jiaoer", "ally", "做媒", "伯爵為西門慶說合李嬌兒。"),
    ("person_ying_bojue", "person_li_guijie", "ally", "引薦", "引西門慶入麗春院。"),

    # ---- 官場依附 --------------------------------------------------------
    (X, "person_cai_jing", "patron", "認乾爺", "西門慶靠蔡京鑽營得官。"),
    (X, "person_zhai_qian", "patron", "東京門路", "蔡府管家，互通聲氣。"),
    ("person_cai_jing", "person_zhai_qian", "servant", "主僕", "翟謙為蔡京管家。"),
    (X, "person_xia_tixing", "ally", "同僚", "提刑所正副千戶。"),
    (X, "person_he_qianhu", "ally", "同僚", "接替夏提刑。"),
    ("person_he_qianhu", "person_he_taijian", "kin", "叔姪", "何太監為何千戶之叔。"),
    (X, "person_cai_zhuangyuan", "patron", "饋贈", "蔡狀元受贈後為西門慶行方便。"),
    (X, "person_an_chen", "ally", "官場往來", "安進士屢借西門府設席。"),
    (X, "person_song_yushi", "patron", "官場往來", "巡按御史，受西門慶招待。"),
    (X, "person_jing_dujian", "ally", "同僚酒友", "清河都監。"),
    (X, "person_huang_taiwei", "patron", "接駕", "山東接駕，西門慶藉此揚名。"),
    (X, "person_zhu_taiwei", "patron", "參見", "東京權貴。"),
    (X, "person_zeng_yushi", "conflict", "參劾", "曾御史上本參劾西門慶枉法受贓。"),
    ("person_cai_jing", "person_zeng_yushi", "conflict", "貶斥", "蔡京一黨反貶曾御史。"),
    ("person_chen_hong", "person_yang_jian", "patron", "黨羽", "陳洪為楊提督黨羽。"),
    (X, "person_miao_qing", "patron", "受賄枉法", "西門枉法受贓放走苗青。"),
    ("person_miao_qing", "person_miao_tianxiu", "conflict", "謀主奪財", "苗青殺主。"),
    ("person_miao_tianxiu", "person_antong", "servant", "主僕", "安童告官為主伸冤。"),
    ("person_li_yanei", "person_meng_yulou", "marriage", "續娶", "玉樓改嫁李衙內。"),
    ("person_zhang_erguan", "person_li_jiaoer", "marriage", "改嫁", "嬌兒拐財改嫁張二官。"),

    # ---- 僧道術士醫者 ----------------------------------------------------
    (X, "person_hu_seng", "patron", "求藥", "胡僧贈春藥，種下死因。"),
    (X, "person_wu_shenxian", "patron", "相面", "冰鑑定終身。"),
    ("person_li_pinger", "person_pan_daoshi", "patron", "禳解", "法遣黃巾力士。"),
    ("person_li_pinger", "person_huang_zhenren", "patron", "薦亡", "發牒薦亡。"),
    ("person_li_pinger", "person_ren_yiguan", "patron", "診病", "任醫官屢次診治。"),
    ("person_li_pinger", "person_hu_taiyi", "patron", "誤診", "胡太醫用藥不對症。"),
    ("person_wu_yueniang", "person_wang_guzi", "patron", "求子", "王姑子替月娘求子。"),
    ("person_wu_yueniang", "person_xue_guzi", "patron", "宣卷", "薛姑子佛口談經。"),
    ("person_wang_guzi", "person_xue_guzi", "conflict", "爭施主", "兩尼爭奪西門府香火。"),
    ("person_xiaoge", "person_pujing", "kin", "師徒", "普靜幻度孝哥兒出家。"),
    ("person_chen_jingji", "person_ren_daoshi", "kin", "師徒", "敬濟拜任道士為師。"),
    ("person_chen_jingji", "person_wang_xingan", "ally", "義助", "王杏庵義恤貧兒。"),
    ("person_chen_jingji", "person_liu_er", "conflict", "毆鬥", "劉二大酒樓撒潑。"),
    ("person_wang_liuer", "person_liu_er", "conflict", "醉罵", "劉二醉罵王六兒。"),

    # ---- 媒婆牙婆 --------------------------------------------------------
    (X, "person_xue_sao", "ally", "說媒", "說娶孟玉樓、賣春梅。"),
    ("person_meng_yulou", "person_xue_sao", "ally", "說媒", "薛嫂做媒。"),
    ("person_meng_yulou", "person_tao_mama", "ally", "說媒", "陶媽媽說合改嫁李衙內。"),
    ("person_pang_chunmei", "person_xue_sao", "ally", "發賣", "月娘令薛嫂賣春梅。"),

    # ---- 妓院 ------------------------------------------------------------
    ("person_li_guijie", "person_li_sanma", "kin", "母女", "李三媽為麗春院鴇母。"),
    ("person_li_guijie", "person_li_guiqing", "kin", "姊妹", "桂卿為桂姐之姊。"),
    ("person_li_guijie", "person_wu_yueniang", "kin", "乾母女", "桂姐拜月娘為乾娘。"),
    ("person_zheng_aiyue", "person_zheng_aixiang", "kin", "姊妹", "鄭家姊妹同在院中。"),
    ("person_zheng_aiyue", "person_wang_sanguan", "romance", "往來", "巧施連環計。"),
]

# --------------------------------------------------------------------------
# 次要人物
#
# 只收書中明確交代的關係：親屬、主僕、同班、共謀、依附。
# 章回裡只是同時在場而無明文關係的一律不補——那已由同段共現呈現。
# --------------------------------------------------------------------------

RELATIONS += [
    # ---- 周守備府 ----
    ("person_pang_chunmei", "person_yuegui", "servant", "主僕", "月桂為春梅房中大丫鬟。"),
    ("person_pang_chunmei", "person_lanhua", "servant", "主僕", "蘭花為守備府小丫鬟。"),
    ("person_zhou_shoubei", "person_yutang", "servant", "主僕", "玉堂為府中養娘。"),
    ("person_zhou_shoubei", "person_jingui", "servant", "主僕", "金匱為府中養娘。"),
    ("person_yutang", "person_jingui", "ally", "同事", "兩人同抱奶金哥兒。"),
    ("person_zhou_shoubei", "person_zhou_ren", "servant", "主僕", "周仁為府中家人。"),
    ("person_zhou_shoubei", "person_zhou_xuan", "kin", "族兄弟", "周宣為周統制族弟，人稱二爺。"),
    ("person_zhou_xuan", "person_ge_cuiping", "ally", "同守宅", "末回與葛翠屏、韓愛姐同看守宅子。"),

    # ---- 李通判之家 ----
    ("person_li_tongpan", "person_li_yanei", "kin", "父子", "李衙內為李通判之子。"),
    ("person_li_yanei", "person_yuzan", "servant", "主僕", "玉簪兒為李衙內房中丫頭。"),
    ("person_yuzan", "person_meng_yulou", "conflict", "妒忌", "玉簪兒妒孟玉樓，被責發賣。"),
    ("person_li_tongpan", "person_mantang", "servant", "主僕", "滿堂兒為李通判家小廝。"),

    # ---- 陳家 ----
    ("person_chen_hong", "person_zhangshi", "marriage", "夫妻", "張氏為陳洪之妻。"),
    ("person_zhangshi", "person_chen_jingji", "kin", "母子", "敬濟參見父靈後與母親張氏磕頭。"),
    ("person_chen_hong", "person_zhang_shilian", "kin", "妹夫", "張世廉為陳洪妹夫。"),
    ("person_chen_hong", "person_chongxi", "servant", "主僕", "重喜兒為陳家小廝。"),
    ("person_chen_hong", "person_jinqian", "servant", "主僕", "金錢兒為陳家小廝。"),
    ("person_chen_jingji", "person_yang_dalang", "ally", "交遊", "同販貨往來的江湖友人。"),
    ("person_chen_jingji", "person_xie_sanlang", "ally", "交遊", "陳敬濟之友。"),
    ("person_chen_jingji", "person_yang_erlang", "ally", "交遊", "陳敬濟之友。"),
    ("person_chen_jingji", "person_lu_erge", "ally", "交遊", "陳敬濟之友。"),

    # ---- 韓道國一家 ----
    ("person_han_daoguo", "person_balao", "servant", "主僕", "八老為韓家家奴。"),
    ("person_wang_liuer", "person_jiner", "servant", "主僕", "錦兒為王六兒買來的丫頭。"),
    ("person_han_daoguo", "person_wang_han", "servant", "主僕", "王漢為韓道國的小郎。"),
    ("person_han_daoguo", "person_hu_xiu", "patron", "東家後生", "胡秀替韓道國押貨船。"),
    ("person_hu_xiu", "person_ximen_qing", "patron", "東家後生", "自杭州回來向西門慶回話。"),

    # ---- 院中粉頭、小優 ----
    ("person_zheng_aiyue", "person_zheng_chun", "kin", "兄妹", "鄭春為鄭愛月之兄。"),
    ("person_zheng_aiyue", "person_zheng_mama", "kin", "母女", "鄭媽媽為鄭家鴇母。"),
    ("person_zheng_aixiang", "person_zheng_chun", "kin", "兄妹", "同為鄭家子女。"),
    ("person_qi_xianger", "person_wang_sanguan", "romance", "梳籠", "王三官梳籠齊香兒。"),
    ("person_qi_xianger", "person_hong_sier", "ally", "同應局", "與董嬌兒三人常同應西門府酒席。"),
    ("person_hong_sier", "person_dong_jiaoer", "ally", "同應局", "同赴西門府應局。"),
    ("person_han_jinchuan", "person_xiaochou", "kin", "姑姪", "消愁兒為韓金釧姪女。"),
    ("person_wang_gui", "person_wang_xiang", "kin", "兄弟", "王相為王桂之弟。"),
    ("person_li_ming", "person_zheng_chun", "ally", "同班小優", "與吳惠、邵奉同班承應。"),
    ("person_zheng_chun", "person_shao_feng", "ally", "同班小優", "同赴西門府彈唱。"),
    ("person_zheng_chun", "person_wang_xiang", "ally", "同班小優", "鄭春引王相見西門慶。"),
    ("person_li_ming", "person_shao_qian", "ally", "同班小優", "與韓佐同來磕頭。"),
    ("person_zhang_mei", "person_xu_shun", "ally", "海鹽子弟", "同挑戲箱搬演戲文。"),
    ("person_zhou_shun", "person_yuan_yan", "ally", "海鹽子弟", "一裝旦、一貼旦。"),

    # ---- 朝廷、官場 ----
    ("person_cai_jing", "person_cai_you", "kin", "父子", "蔡攸為蔡京之子，祥和殿學士。"),
    ("person_cai_jing", "person_gao_an", "servant", "主僕", "高安為蔡京府管家。"),
    ("person_gao_an", "person_zhai_qian", "ally", "同府管家", "二人分掌蔡府事務。"),
    ("person_yang_jian", "person_yang_sheng", "patron", "黨羽", "楊戩名下幹辦。"),
    ("person_yang_jian", "person_han_zongren", "patron", "黨羽", "楊戩名下府掾。"),
    ("person_yang_jian", "person_zhao_hongdao", "patron", "黨羽", "楊戩名下府掾。"),
    ("person_yang_jian", "person_liu_cheng", "patron", "黨羽", "楊戩名下班頭。"),
    ("person_yang_jian", "person_hu_si", "patron", "黨羽", "與陳洪、西門慶同列彈章。"),
    ("person_wang_fu", "person_dong_sheng", "patron", "黨羽", "王黼名下書辦官。"),
    ("person_wang_fu", "person_wang_lian", "patron", "黨羽", "王黼名下家人。"),
    ("person_wang_fu", "person_huang_yu", "patron", "黨羽", "王黼名下班頭。"),
    ("person_wang_fu", "person_yang_jian", "ally", "同被劾", "二人同被拿送三法司。"),
    ("person_cai_jing", "person_gao_qiu", "ally", "同朝", "同列輔弼，朝儀同班。"),
    ("person_cai_jing", "person_li_bangyan", "ally", "同朝", "同列輔弼。"),
    ("person_huang_taiwei", "person_wang_ye", "ally", "同朝", "隴西公與太尉同至。"),
    ("person_wang_sanguan", "person_liuhuang", "patron", "磕頭", "王三官往東京與六黃公公磕頭。"),

    # 第六十五回，山東各級官員同赴廳參黃太尉
    ("person_huang_taiwei", "person_gong_gong", "patron", "廳參", "山東左佈政。"),
    ("person_huang_taiwei", "person_he_qigao", "patron", "廳參", "山東左參政。"),
    ("person_huang_taiwei", "person_chen_sizhen", "patron", "廳參", "山東右佈政。"),
    ("person_huang_taiwei", "person_feng_tinghu", "patron", "廳參", "左參議。"),
    ("person_huang_taiwei", "person_wang_boyan", "patron", "廳參", "右參議。"),
    ("person_huang_taiwei", "person_zhao_ne", "patron", "廳參", "廉使。"),
    ("person_huang_taiwei", "person_han_wenguang", "patron", "廳參", "採訪使。"),
    ("person_huang_taiwei", "person_chen_zhenghui", "patron", "廳參", "提學副使。"),
    ("person_huang_taiwei", "person_wang_shiqi", "patron", "廳參", "青州府官。"),
    ("person_huang_taiwei", "person_huang_jia", "patron", "廳參", "登州府官。"),
    ("person_huang_taiwei", "person_ye_qian", "patron", "廳參", "萊州府官。"),
    ("person_huang_taiwei", "person_zhang_shuye", "patron", "廳參", "與八府官同行廳參之禮。"),

    # 陽穀、清河兩縣的官吏
    ("person_li_datian", "person_yue_hean", "ally", "同僚", "知縣與縣丞。"),
    ("person_li_datian", "person_xia_gongji", "ally", "同僚", "知縣與典史。"),
    ("person_li_datian", "person_qian_lao", "ally", "同僚", "知縣與司吏。"),
    ("person_chen_wenzhao", "person_wu_song", "patron", "審讞", "東平府尹審武松案時力持公道。"),
    ("person_chen_wenzhao", "person_qian_lao", "conflict", "問責", "痛責司吏錢勞二十板。"),
    ("person_chen_xiansheng", "person_wu_song", "ally", "代書", "替武松寫告狀。"),
    ("person_gao_lian", "person_yin_tianxi", "kin", "郎舅", "殷天錫為知州高廉的妻弟。"),
    ("person_di_sibin", "person_miao_qing", "conflict", "查案", "陽穀縣丞狄斯彬查苗青一案。"),
    ("person_hu_shiwen", "person_di_sibin", "patron", "調委", "東平府尹胡師文調委狄斯彬查辦。"),
    ("person_hu_shiwen", "person_ximen_qing", "ally", "相交", "府尹胡師文與西門慶相交，為苗青案迴護。"),
    ("person_huang_taiwei", "person_hu_shiwen", "patron", "廳參", "東平府知府。"),
    ("person_huang_taiwei", "person_xu_song", "patron", "廳參", "東昌府知府。"),
    ("person_huang_taiwei", "person_ling_yunyi", "patron", "廳參", "兗州府知府。"),
    ("person_huang_taiwei", "person_han_bangqi", "patron", "廳參", "徐州府知府。"),
    ("person_huang_taiwei", "person_lei_qiyuan", "patron", "廳參", "兵備副使。"),
    ("person_huang_mei", "person_miao_qing", "conflict", "行文追究", "開封府通判黃美接安童告狀，行文追究苗青。"),
    ("person_antong", "person_huang_mei", "ally", "告狀", "安童走東京投開封府黃通判具訴。"),

    # ---- 苗員外一案 ----
    ("person_miao_tianxiu", "person_weng_ba", "conflict", "謀主", "船家翁八與陳三合謀殺主。"),
    ("person_miao_qing", "person_weng_ba", "ally", "同謀", "苗青買通船家下手。"),
    ("person_miao_qing", "person_yue_san", "ally", "窩藏", "苗青逃匿經紀樂三家。"),
    ("person_yue_san", "person_yue_sansao", "marriage", "夫妻", "樂三嫂為樂三之妻。"),
    ("person_yue_sansao", "person_wang_liuer", "ally", "往來", "兩家住鄰，所交極厚。"),
    ("person_miao_tianxiu", "person_huang_mei", "kin", "表兄弟", "黃美為苗天秀表兄。"),
    ("person_miao_tianxiu", "person_diao_qier", "marriage", "妾", "刁七兒為苗天秀之妾。"),
    ("person_weng_ba", "person_antong", "conflict", "行兇", "翁八一悶棍打落安童入水。"),

    # ---- 西門府 ----
    ("person_meng_yulou", "person_xiaoluan", "servant", "主僕", "小鸞隨玉樓過門，與蘭香同侍。"),
    ("person_sun_xuee", "person_cuier", "servant", "主僕", "翠兒買入雪娥房中使喚。"),
    ("person_li_jiaoer", "person_xiahua", "servant", "主僕", "夏花兒為李嬌兒房中丫頭。"),
    ("person_ximen_qing", "person_chunyan", "servant", "主僕", "與春鴻同為蘇州歌童。"),
    ("person_chunhong", "person_chunyan", "ally", "同來歌童", "二人同時進府，春燕早死。"),
    ("person_ximen_qing", "person_tiegun", "servant", "主僕", "西門府小廝。"),
    ("person_ximen_qing", "person_sengbao", "servant", "主僕", "西門府小廝。"),
    ("person_ximen_qing", "person_zheng_ji", "servant", "主僕", "府中打茶的小廝。"),
    ("person_ximen_qing", "person_wang_xian", "patron", "東家後生", "緞子鋪後生，管取車稅銀兩。"),
    ("person_ni_peng", "person_wen_bigu", "ally", "薦舉", "倪秀才薦溫必古入西門府為西席。"),
    ("person_ximen_qing", "person_ni_peng", "patron", "延請", "西門慶延倪秀才引薦西席。"),
    ("person_ximen_qing", "person_shui_xiucai", "patron", "延請", "溫秀才之後受薦的西席人選。"),
    ("person_ximen_qing", "person_xiao_zhouer", "patron", "承應", "篦頭待詔小周兒替他篦頭櫛發。"),

    # ---- 花家、王招宣府 ----
    ("person_hua_zixu", "person_tianfu", "servant", "主僕", "天福兒為花家小廝。"),
    ("person_wang_sanguan", "person_yongding", "servant", "主僕", "永定兒為招宣府小廝。"),

    # ---- 醫卜、術士 ----
    ("person_he_laoren", "person_he_chunquan", "kin", "父子", "何春泉為何老人之子。"),
    ("person_ximen_qing", "person_he_chunquan", "patron", "診病", "西門慶末疾請何春泉來看。"),
    ("person_ximen_qing", "person_zhao_taiyi", "patron", "診病", "清河庸醫，用藥荒唐。"),
    ("person_ximen_qing", "person_xu_xiansheng", "patron", "擇日", "陰陽生徐先生主西門府喪葬擇日、開喪。"),
    ("person_li_pinger", "person_xu_xiansheng", "patron", "擇日", "瓶兒之喪由徐先生批書。"),

    # ---- 親朋 ----
    ("person_qiao_daohu", "person_qiao_taitai", "kin", "家眷", "喬家女眷。"),
    ("person_wu_yueniang", "person_wu_dayi", "kin", "親眷", "吳家親戚。"),
    ("person_wu_yueniang", "person_shen_yifu", "kin", "姻親", "西門府姻親。"),
    ("person_wu_yueniang", "person_han_yifu", "kin", "姻親", "西門府姻親。"),
    ("person_wu_yueniang", "person_zheng_sanjie", "kin", "親眷", "西門府女眷親戚。"),
    ("person_wu_yueniang", "person_zhu_xuban", "kin", "堂客", "序班朱家娘子，西門府堂客。"),
    ("person_wu_yueniang", "person_shang_juren", "kin", "堂客", "舉人尚家娘子，西門府堂客。"),
    ("person_hua_dajiu", "person_hua_dajinzi", "marriage", "夫妻", "花大妗子為花大舅之妻。"),

    # ---- 其他 ----
    ("person_pan_jinlian", "person_bai_yulian", "ally", "同伴", "同在王招宣府時的夥伴。"),
    ("person_pan_jinlian", "person_wang_huangqin", "kin", "鄰家", "潘金蓮舊居的鄰家皇親。"),
    ("person_yinger", "person_yao_erlang", "patron", "收養", "武大死後迎兒寄養姚二郎家。"),
    ("person_han_er", "person_che_dan", "ally", "同夥", "與管世寬、郝賢同鬧韓道國家。"),
    ("person_che_dan", "person_guan_shikuan", "ally", "同夥", "清河潑皮。"),
    ("person_che_dan", "person_hao_xian", "ally", "同夥", "清河潑皮。"),
    ("person_liang_zhongshu", "person_li_kui", "conflict", "屠戮", "李逵翠雲樓殺梁中書全家老小。"),
    ("person_li_pinger", "person_li_kui", "conflict", "亂離", "瓶兒因翠雲樓之變攜財出走。"),
]

# 補上原詞表就有、關係卻漏列的幾位
RELATIONS += [
    ("person_ximen_qing", "person_laian", "servant", "主僕", "西門府小廝。"),
    ("person_ximen_qing", "person_qitong", "servant", "主僕", "西門府小廝。"),
    ("person_ximen_qing", "person_huixiu", "servant", "主僕", "西門府僕婦。"),
    ("person_chen_hong", "person_chen_ding", "servant", "主僕", "陳定為陳家僕人。"),
    ("person_zhou_shoubei", "person_zhou_zhong", "servant", "主僕", "周忠為守備府老家人。"),
    ("person_qiao_daohu", "person_qiao_wutaitai", "kin", "家族長輩", "喬家長輩，出入西門府。"),
    ("person_ximen_qing", "person_liu_taijian", "ally", "往來", "西門慶赴磚廠劉太監莊上設席。"),
    ("person_ximen_qing", "person_xue_taijian", "ally", "往來", "薛太監與劉太監同赴西門府酒席。"),
]
