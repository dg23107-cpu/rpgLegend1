import streamlit as st
import streamlit.components.v1 as components
import time

# =========================================================
# 거지 탈출 RPG - Streamlit Clicker
# =========================================================

st.set_page_config(
    page_title="거지 탈출 RPG",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

GOAL = 50_000_000

DEFAULT = {
    "money": 0,
    "total_money": 0,
    "click_power": 1,
    "income": 0,
    "income_level": 0,
    "click_level": 0,
    "floor": 1,
    "escape": False,
    "message": "길거리에서 시작했습니다. 클릭해서 돈을 모아보세요!",
    "owned": {
        "신문지": 0,
        "자판기": 0,
        "손수레": 0,
        "작은가게": 0,
        "알바생": 0,
        "매니저": 0,
    },
}

for key, value in DEFAULT.items():
    if key not in st.session_state:
        st.session_state[key] = value.copy() if isinstance(value, dict) else value

INCOME_ITEMS = [
    ("신문지", "📰", 10_000, 1, "거리에서 꾸준히 수입을 얻습니다."),
    ("자판기", "🥤", 50_000, 7, "작은 자동 수입원이 생깁니다."),
    ("손수레", "🛒", 250_000, 35, "판매를 시작해 수입이 늘어납니다."),
    ("작은가게", "🏪", 1_000_000, 120, "작은 가게에서 안정적으로 돈을 법니다."),
    ("알바생", "🧑‍🔧", 5_000_000, 650, "알바생이 일을 도와줍니다."),
    ("매니저", "👔", 20_000_000, 3_000, "가게 운영을 맡아줍니다."),
]

FLOORS = [
    ("길거리", "🧺"),
    ("골목", "🏘️"),
    ("시장", "🏪"),
    ("도심", "🏙️"),
]

# 화면 전체를 고정해 세로 스크롤이 생기지 않도록 합니다.
st.markdown(
    """
<style>
html, body, [data-testid="stAppViewContainer"], .stApp {
    overflow: hidden !important;
    height: 100vh !important;
}
[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {
    display: none !important;
}
.block-container {
    max-width: 1500px !important;
    height: 100vh !important;
    padding: 8px 16px !important;
    overflow: hidden !important;
}
iframe {
    border: 0 !important;
    width: 100% !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- 버튼 액션 ----------
action = st.query_params.get("action", "")
token = st.query_params.get("n", "")

if token and token != st.session_state.get("_last_action_token", ""):
    st.session_state["_last_action_token"] = token

    if action == "click":
        st.session_state.money += st.session_state.click_power
        st.session_state.total_money += st.session_state.click_power
        st.session_state.message = (
            f"💰 +{st.session_state.click_power:,}원! 계속 모아보세요."
        )

    elif action == "buy_income":
        idx = int(st.query_params.get("idx", "-1"))
        if 0 <= idx < len(INCOME_ITEMS):
            name, icon, base_price, add_income, desc = INCOME_ITEMS[idx]
            owned = st.session_state.owned[name]
            price = int(base_price * (1.28 ** owned))

            if st.session_state.money >= price:
                st.session_state.money -= price
                st.session_state.income += add_income
                st.session_state.owned[name] += 1
                st.session_state.message = (
                    f"{icon} {name} 구매 완료! 초당 수입 +{add_income:,}원"
                )
            else:
                st.session_state.message = (
                    f"❗ {name} 구매에는 {price:,}원이 필요합니다."
                )

    elif action == "upgrade_click":
        price = int(25_000 * (1.55 ** st.session_state.click_level))
        if st.session_state.money >= price:
            st.session_state.money -= price
            st.session_state.click_level += 1
            st.session_state.click_power += 1
            st.session_state.message = "⚡ 클릭 능력이 +1 올랐습니다!"
        else:
            st.session_state.message = f"❗ 클릭 강화에는 {price:,}원이 필요합니다."

    elif action == "upgrade_income":
        price = int(100_000 * (1.65 ** st.session_state.income_level))
        if st.session_state.money >= price:
            st.session_state.money -= price
            st.session_state.income_level += 1
            st.session_state.income = max(1, int(st.session_state.income * 1.25))
            st.session_state.message = "📈 전체 자동 수입이 25% 증가했습니다!"
        else:
            st.session_state.message = f"❗ 수입 강화에는 {price:,}원이 필요합니다."

    elif action == "floor":
        if st.session_state.floor >= 4:
            st.session_state.message = "🏁 최종층입니다. 목표 금액을 모아 탈출하세요!"
        elif st.session_state.money >= 1_000_000:
            st.session_state.money -= 1_000_000
            st.session_state.floor += 1
            st.session_state.message = (
                f"🚪 {st.session_state.floor}층으로 이동했습니다!"
            )
        else:
            st.session_state.message = "❗ 다음 층 이동에는 1,000,000원이 필요합니다."

    elif action == "escape":
        if st.session_state.money >= GOAL:
            st.session_state.escape = True
            st.session_state.message = "🎉 탈출 성공! 드디어 자유를 얻었습니다!"
        else:
            st.session_state.message = f"❗ 탈출에는 {GOAL:,}원이 필요합니다."

    elif action == "reset":
        for key, value in DEFAULT.items():
            st.session_state[key] = value.copy() if isinstance(value, dict) else value
        st.session_state.message = "🔄 처음부터 다시 시작합니다!"

money = st.session_state.money
progress = min(100, money / GOAL * 100)
floor_name, floor_icon = FLOORS[st.session_state.floor - 1]

def esc(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

def game_link(action_name, label, extra=""):
    timestamp = str(int(time.time() * 1_000_000))
    url = f"?action={action_name}&n={timestamp}{extra}"
    return f"""<a class="game-btn" href="{url}" onclick="playSound(event)">{label}</a>"""

shop_cards = ""
for i, (name, icon, base_price, add_income, desc) in enumerate(INCOME_ITEMS):
    owned = st.session_state.owned[name]
    price = int(base_price * (1.28 ** owned))
    shop_cards += f"""
    <div class="shop-card">
        <div class="shop-top">
            <div class="item-icon">{icon}</div>
            <div class="item-info">
                <div class="item-name">{esc(name)}</div>
                <div class="item-desc">{esc(desc)}</div>
            </div>
            <div class="owned">Lv.{owned}</div>
        </div>
        {game_link("buy_income", f"💰 {price:,}원 · 수입 +{add_income:,}/초", f"&idx={i}")}
    </div>
    """

click_price = int(25_000 * (1.55 ** st.session_state.click_level))
income_price = int(100_000 * (1.65 ** st.session_state.income_level))

if st.session_state.escape:
    result_box = """
    <div class="escape-success">
        <div class="success-title">🎉 탈출 성공!</div>
        <div class="success-text">목표 금액을 모아 자유를 얻었습니다.</div>
    </div>
    """
else:
    result_box = f"""
    <div class="goal-box">
        <div class="goal-title">🎯 탈출 목표</div>
        <div class="goal-money">{money:,} / {GOAL:,}원</div>
        <div class="progress"><div class="progress-in" style="width:{progress:.2f}%"></div></div>
        <div class="goal-text">목표 금액을 모으면 탈출할 수 있습니다.</div>
    </div>
    """

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing:border-box; }}
html, body {{
    margin:0; padding:0; width:100%; height:100%;
    overflow:hidden;
    font-family:Arial, "Noto Sans KR", sans-serif;
    color:#171717;
    background:#f7ecd9;
}}
.wrap {{
    width:100%; height:100%;
    padding:6px 8px;
    display:flex; flex-direction:column; gap:7px;
}}
.header {{
    height:48px; flex:0 0 48px;
    display:flex; align-items:center; justify-content:space-between;
}}
.logo {{ font-size:27px; font-weight:900; color:#4b2d1d; }}
.logo span {{ font-size:24px; margin-right:6px; }}
.stats {{ display:flex; gap:7px; }}
.stat {{
    background:#fffaf0; border:2px solid #d9b778;
    border-radius:12px; padding:5px 12px; min-width:135px;
}}
.stat-label {{ font-size:10px; font-weight:700; color:#555; }}
.stat-value {{ font-size:16px; font-weight:900; color:#171717; }}
.main {{
    min-height:0; flex:1;
    display:grid; grid-template-columns:1.04fr .96fr; gap:8px;
}}
.panel {{
    min-height:0; background:#fffaf1;
    border:3px solid #d4a25c; border-radius:17px;
    padding:9px; overflow:hidden;
}}
.left {{
    display:grid; grid-template-rows:112px 1fr 40px; gap:7px;
}}
.character {{
    border-radius:13px;
    background:linear-gradient(#d8efcf,#b8ddac);
    border:2px solid #9dbb8e;
    position:relative; overflow:hidden;
    display:flex; align-items:center; justify-content:center;
}}
.cloud {{ position:absolute; font-size:29px; opacity:.8; }}
.c1 {{left:5%; top:8px}} .c2 {{right:8%; top:18px}}
.scene {{ font-size:67px; z-index:2; }}
.sign {{
    position:absolute; bottom:5px; left:9px;
    background:#fff7df; border:2px solid #a9783d;
    border-radius:8px; padding:4px 8px;
    font-size:10px; font-weight:800;
}}
.money-area {{
    min-height:0; display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    background:#fff5c9; border:2px dashed #dba12b;
    border-radius:14px; padding:7px;
}}
.money-title {{font-size:12px;font-weight:800;color:#555}}
.money {{font-size:34px;font-weight:1000;color:#171717;letter-spacing:-1px}}
.income {{font-size:11px;font-weight:800;color:#27652d;margin-bottom:5px}}
.game-btn {{
    display:flex; align-items:center; justify-content:center;
    text-decoration:none; color:#fff !important;
    background:#171a20; border:3px solid #9b682e;
    border-radius:11px; min-height:39px;
    font-size:13px; font-weight:900;
    transition:transform .08s, filter .08s;
}}
.game-btn:hover {{filter:brightness(1.12);transform:translateY(-1px)}}
.game-btn:active {{transform:scale(.98)}}
.click-btn {{min-height:53px;font-size:19px;background:#2b211c}}
.actions {{display:grid;grid-template-columns:1fr 1fr;gap:6px}}
.right {{
    display:grid; grid-template-rows:30px 1fr auto; gap:7px;
}}
.shop-title {{display:flex;justify-content:space-between;align-items:center}}
.shop-title h2 {{margin:0;color:#4b2e1e;font-size:19px}}
.shop-title span {{font-size:10px;color:#555;font-weight:700}}
.shop-list {{
    min-height:0; overflow:hidden;
    display:grid; grid-template-columns:1fr 1fr; gap:6px;
}}
.shop-card {{
    background:#fffdf8; border:2px solid #d8c19a;
    border-radius:10px; padding:6px;
    min-width:0; display:flex; flex-direction:column; justify-content:space-between;
}}
.shop-top {{display:flex;align-items:center;gap:6px;min-height:38px}}
.item-icon {{
    width:35px;height:35px;border-radius:9px;
    background:#e8f1d8;display:flex;align-items:center;justify-content:center;font-size:21px;
}}
.item-info {{min-width:0;flex:1}}
.item-name {{font-size:13px;font-weight:900;color:#171717}}
.item-desc {{font-size:9px;color:#555;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.owned {{font-size:10px;font-weight:900;color:#7b4c21}}
.shop-card .game-btn {{min-height:28px;border-width:2px;border-radius:7px;font-size:10px;margin-top:4px}}
.goal-box {{
    background:#fff3bb;border:2px solid #dda126;border-radius:11px;padding:6px 10px;
}}
.goal-title {{font-size:11px;font-weight:900;color:#5d3a17}}
.goal-money {{font-size:14px;font-weight:1000;color:#171717}}
.progress {{height:6px;background:#eadcae;border-radius:8px;overflow:hidden;margin:3px 0}}
.progress-in {{height:100%;background:#d98c20;border-radius:8px}}
.goal-text {{font-size:9px;color:#444}}
.escape-success {{
    background:#fff0b3;border:2px solid #dda126;border-radius:11px;
    padding:7px;text-align:center;
}}
.success-title {{font-size:17px;font-weight:1000;color:#51351d}}
.success-text {{font-size:10px;font-weight:800;color:#333}}
.message {{
    flex:0 0 27px; display:flex;align-items:center;
    background:#fffaf0;border:1px solid #d9c8a9;border-radius:8px;
    padding:3px 9px; font-size:10px;font-weight:800;color:#333;
    overflow:hidden;white-space:nowrap;text-overflow:ellipsis;
}}
.footer {{
    flex:0 0 24px; display:flex;align-items:center;
    justify-content:space-between;font-size:9px;color:#666;
}}
.reset {{min-width:145px;min-height:25px !important;font-size:10px !important;border-width:2px !important}}
@media (max-width:900px) {{
    .wrap {{padding:4px;gap:4px}}
    .header {{height:40px;flex-basis:40px}}
    .logo {{font-size:20px}}
    .stat {{min-width:92px;padding:4px 7px}}
    .stat-value {{font-size:13px}}
    .main {{gap:4px}}
    .panel {{padding:6px;border-radius:12px}}
    .left {{grid-template-rows:85px 1fr 35px}}
    .scene {{font-size:49px}}
    .money {{font-size:25px}}
    .shop-list {{grid-template-columns:1fr}}
    .item-desc {{display:none}}
    .shop-card .game-btn {{min-height:26px;font-size:9px}}
    .game-btn {{min-height:34px;font-size:10px}}
    .click-btn {{min-height:45px;font-size:15px}}
    .footer {{display:none}}
}}
</style>
</head>
<body>
<div class="wrap">
    <div class="header">
        <div class="logo"><span>🛒</span>거지 탈출 RPG</div>
        <div class="stats">
            <div class="stat">
                <div class="stat-label">현재 장소</div>
                <div class="stat-value">{floor_icon} {floor_name}</div>
            </div>
            <div class="stat">
                <div class="stat-label">초당 수입</div>
                <div class="stat-value">💵 {st.session_state.income:,}원</div>
            </div>
        </div>
    </div>

    <div class="main">
        <div class="panel left">
            <div class="character">
                <div class="cloud c1">☁️</div>
                <div class="cloud c2">☁️</div>
                <div class="scene">🧑‍🦲🪣</div>
                <div class="sign">🏠 {floor_name}에서 살아남기!</div>
            </div>

            <div class="money-area">
                <div class="money-title">현재 가진 돈</div>
                <div class="money">💰 {money:,}원</div>
                <div class="income">자동 수입 +{st.session_state.income:,}원/초</div>
                {game_link("click", f"💸 돈 벌기  +{st.session_state.click_power:,}원")}
                <div style="height:5px"></div>
                <div class="actions">
                    {game_link("upgrade_click", f"⚡ 클릭 강화 · {click_price:,}원")}
                    {game_link("upgrade_income", f"📈 수입 강화 · {income_price:,}원")}
                </div>
            </div>

            <div class="actions">
                {game_link("floor", "🚪 다음 층 이동")}
                {game_link("escape", "🎯 탈출하기")}
            </div>
        </div>

        <div class="panel right">
            <div class="shop-title">
                <h2>🛍️ 상점</h2>
                <span>구매하면 자동 수입 증가</span>
            </div>
            <div class="shop-list">{shop_cards}</div>
            {result_box}
        </div>
    </div>

    <div class="message">📢 {esc(st.session_state.message)}</div>
    <div class="footer">
        <div>※ 거지키우기에서 영감을 받은 귀여운 클리커 RPG</div>
        {game_link("reset", "🔄 처음부터 다시")}
    </div>
</div>

<script>
let audioCtx = null;

function playSound(event) {
    event.preventDefault();
    const target = event.currentTarget;

    try {
        if (!audioCtx) {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        if (audioCtx.state === "suspended") {
            audioCtx.resume();
        }

        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();

        osc.type = "sine";
        osc.frequency.setValueAtTime(520, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(
            780, audioCtx.currentTime + 0.06
        );

        gain.gain.setValueAtTime(0.06, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(
            0.001, audioCtx.currentTime + 0.09
        );

        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.09);

        setTimeout(function() {
            window.parent.location.href = target.href;
        }, 65);
    } catch (e) {
        window.parent.location.href = target.href;
    }
}
</script>
</body>
</html>
"""

components.html(html, height=700, scrolling=False)
