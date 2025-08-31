import pandas as pd
import streamlit as st

import random
import time

from data import pav_ja


# ==============================
# セッション初期化
# ==============================
def init_session_state():
    st.session_state.game_started =False
    st.session_state.remaining = []
    st.session_state.history = []

def set_history() -> pd.DataFrame:
    df = pd.DataFrame(st.session_state.history, columns=["これまでに出たパビリオン"])
    df.index = df.index + 1
    df.index.name = 'No.'
    return df    

# ==============================
# ページコンフィグ
# ==============================
st.set_page_config(
    page_title="大阪万博2025 パビリオンルーレット",
    page_icon="🎡",
    layout="wide",
)

# ==============================
# CSSでいい感じのデザイン（生成AI出力）
# ==============================
st.markdown(
"""
<style>
/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap');

.stApp {
    background-color: #f9f9f9;
    font-family: 'Noto Sans JP', sans-serif;
}

/* =========================
   タイトル・サブタイトル
   ========================= */
h1 {
    text-align: center;
    color: #ff4d4f;
    font-size: 6vw; /* 画面幅の6%に自動調整 */
    font-weight: 900;
    margin-bottom: 0.5em;
    display: block;
}

h2, h3 {
    text-align: center;
    font-weight: 700;
    color: #1890ff;
    font-size: 4vw;
}

/* =========================
   ルーレット文字
   ========================= */
.roulette-text {
    font-size: 4vw;
    min-font-size: 18px;
    max-font-size: 36px;
    color: #52c41a;
    text-align: center;
    font-weight: 700;
    white-space: nowrap;      /* 改行禁止 */
    overflow-x: auto;         /* 横スクロール */
    display: block;
}

/* =========================
   テーブル
   ========================= */
.dataframe {
    border: none;
    border-radius: 12px;
    background-color: #fff;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    width: 100% !important;
    overflow-x: auto;
    padding: 0.5em;
}

/* =========================
   区切り線
   ========================= */
hr {
    border: 1px solid #eee;
    margin: 2em 0;
}

/* =========================
   スマホレスポンシブ
   ========================= */
@media (max-width: 768px) {
    h1 { font-size: 6vw !important; }
    h2 { font-size: 5vw !important; }
    h3 { font-size: 4.5vw !important; }
    button[kind="primary"] { width: 100% !important; font-size: 1em !important; padding: 0.6em !important; }
    .dataframe { font-size: 0.85em !important; }
    .roulette-text { font-size: 6vw !important; }
}
</style>
""",
unsafe_allow_html=True
)

# ==============================
# タイトル
# ==============================
st.title("🔴 大阪万博2025 🔵")
st.title("パビリオンルーレット")

# ==============================
# ゲーム開始前設定
# ==============================
if not "game_started" in st.session_state and not "remaining" in st.session_state and not "history" in st.session_state:
    init_session_state()

if not st.session_state.game_started:
    st.subheader("🔍 ルーレットで出したいパビリオンの種類を選択してね！")
    st.write("") # 改行

    foreign_pavilions = st.checkbox("🌍 海外パビリオン", True)
    japan_pavilions = st.checkbox("🗾 国内パビリオン", True)
    signature_pavilions = st.checkbox("⭐ シグネチャーパビリオン", True)

    if st.button("🚀 ゲームを開始する", type="primary", width="stretch"):
        selected_pavilions = []
        if foreign_pavilions:
            selected_pavilions += pav_ja.foreign_pavilions
        if japan_pavilions:
            selected_pavilions += pav_ja.japan_pavilions
        if signature_pavilions:
            selected_pavilions += pav_ja.signature_pavilions

        st.session_state.remaining = selected_pavilions.copy()
        st.session_state.game_started = True
        st.rerun()

# ==============================
# ゲーム開始
# ==============================
else:
    # 画面placeholderで先に構成
    st.subheader("スタートを押して、出たパビリオンを地図で探そう！")
    roulette_button_ph = st.empty()
    remain_count_ph = st.empty()
    roulette_result_ph = st.empty()

    st.write("---")
    st.write("📜 これまでに出たパビリオン:")
    chosen_placeholder = st.empty()

    st.write("---")
    roulette_reset_ph = st.empty()

    # 残り回数
    remain_count_ph.write(f"残り：{len(st.session_state.remaining)}回")

    # 過去の結果
    if st.session_state.history:
        chosen_placeholder.table(set_history())
    else:
        chosen_placeholder.write("無し")

    # リセットボタン
    if roulette_reset_ph.button("🔄 リセット", width="stretch"):
        init_session_state()
        st.rerun()

    # スタートボタン
    all__pavilions = pav_ja.all_pavilions
    if roulette_button_ph.button("🎰 スタート", type="primary", width="stretch"):
        if st.session_state.remaining:
            # ルーレット演出
            for i in range(15):
                roulette_result_ph.write(
                    # 残りのパビリオンでルーレットすると、残り1の時に回らないので、全てのパビリオンで回す
                    f"<h2 style='text-align:center; color:#00a0e9;'>{random.choice(all__pavilions)}</h2>",
                    unsafe_allow_html=True
                )
                time.sleep(0.05 + i*0.02)

            chosen = random.choice(st.session_state.remaining)
            roulette_result_ph.write(
                f"<h1 style='text-align:center; color:#e60012;'> {chosen} ",
                unsafe_allow_html=True
            )

            st.session_state.remaining.remove(chosen)
            st.session_state.history.append(chosen)
        else:
            roulette_result_ph.warning("すべてのパビリオンが出ました！ゲーム終了です 🎉")