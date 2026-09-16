import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="탈출! 거지 클리커",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# Game data
# -----------------------------
STAGES = [
    {"name": "시골 탈출", "place": "🌾 시골", "goal": 1_000_000},
    {"name": "길거리 탈출", "place": "🚶 인도 (side walk)", "goal": 5_000_000},
    {"name": "반지하 탈출", "place": "🏚️ 반지하", "goal": 50_000_000},
    {"name": "1층 탈출", "place": "🏠 1층 집", "goal": 250_000_000},
    {"name": "지방도시 탈출", "place": "🏢 지방도시 아파트", "goal": 1_250_000_000},
]

def init_game():
    if "money" not in st.session_state:
        st.session_state.money = 0
    if "stage" not in st.session_state:
        st.session_state.stage = 0
    if "click_power" not in st.session_state:
        st.session_state.click_power = 1_000
    if "multi_click" not in st.session_state:
        st.session_state.multi_click = 1
    if "power_level" not in st.session_state:
        st.session_state.power_level = 0
    if "multi_level" not in st.session_state:
        st.session_state.multi_level = 0
    if "message" not in st.session_state:
        st.session_state.message = ""
    if "last_gain" not in st.session_state:
        st.session_state.last_gain = 0
    if "game_clear" not in st.session_state:
        st.session_state.game_clear = False

init_game()

def won_stage():
    return st.session_state.money >= STAGES[st.session_state.stage]["goal"]

def click_game():
    gain = st.session_state.click_power * st.session_state.multi_click
    st.session_state.money += gain
    st.session_state.last_gain = gain
    if won_stage():
        st.session_state.message = f"🎉 {STAGES[st.session_state.stage]['name']} 클리어!"
    else:
        st.session_state.message = ""

def buy_power():
    cost = int(1_000 * (1.5 ** st.session_state.power_level))
    if st.session_state.money >= cost:
        st.session_state.money -= cost
        st.session_state.click_power += 1_000
        st.session_state.power_level += 1
        st.session_state.message = "💪 클릭당 수입이 +1,000원 증가했습니다!"
    else:
        st.session_state.message = "💸 돈이 부족합니다!"

def buy_multi():
    cost = int(1_000 * (1.5 ** st.session_state.multi_level))
    if st.session_state.money >= cost:
        st.session_state.money -= cost
        st.session_state.multi_click += 1
        st.session_state.multi_level += 1
        st.session_state.message = "⚡ 한 번 클릭할 때 적용되는 클릭 수가 +1 증가했습니다!"
    else:
        st.session_state.message = "💸 돈이 부족합니다!"

def next_stage():
    if won_stage() and st.session_state.stage < len(STAGES) - 1:
        st.session_state.stage += 1
        st.session_state.message = f"🚪 다음 단계: {STAGES[st.session_state.stage]['name']}"
        st.session_state.last_gain = 0
    elif won_stage() and st.session_state.stage == len(STAGES) - 1:
        st.session_state.game_clear = True

def reset_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

stage = STAGES[st.session_state.stage]
goal = stage["goal"]
progress = min(st.session_state.money / goal, 1.0)

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.stApp {
    background: #f5ead8;
}

.block-container {
    max-width: 1050px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

.game-title {
    text-align: center;
    font-family: 'Jua', sans-serif;
    font-size: 3.1rem;
    color: #5b3a29;
    margin-bottom: 0.1rem;
    text-shadow: 2px 2px 0px #fff;
}

.subtitle {
    text-align: center;
    color: #765944;
    margin-bottom: 1rem;
}

.money-card {
    background: #fff8e9;
    border: 3px solid #d4aa70;
    border-radius: 22px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 5px 0 #b98b56;
}

.money-label {
    color: #876344;
    font-weight: 700;
}

.money-value {
    color: #4c2d1c;
    font-size: 2.3rem;
    font-weight: 900;
}

.scene {
    position: relative;
    min-height: 310px;
    border: 4px solid #8e6846;
    border-radius: 25px;
    overflow: hidden;
    box-shadow: 0 7px 0 #6d4a31;
    margin: 15px 0;
}

.scene h2 {
    position: absolute;
    left: 22px;
    top: 12px;
    z-index: 2;
    background: rgba(255,255,255,.78);
    padding: 8px 15px;
    border-radius: 15px;
    color: #503522;
}

.scene-0 {
    background:
      linear-gradient(#8dc9ed 0 52%, #8ebc58 52% 72%, #9c713e 72%);
}
.scene-1 {
    background:
      linear-gradient(#a9d8ee 0 47%, #777 47% 52%, #c4c4c4 52% 100%);
}
.scene-2 {
    background:
      linear-gradient(#b9d9ea 0 35%, #777 35% 45%, #604b43 45% 100%);
}
.scene-3 {
    background:
      linear-gradient(#b9d8ea 0 38%, #c6b39b 38% 100%);
}
.scene-4 {
    background:
      linear-gradient(#8fc8e6 0 40%, #a8a8a8 40% 48%, #b9b9b9 48% 100%);
}

.scene::after {
    content: "☁️   ☁️        ☁️";
    position: absolute;
    top: 45px;
    left: 80px;
    font-size: 30px;
    opacity: .8;
}

.character {
    position: absolute;
    left: 50%;
    bottom: 25px;
    transform: translateX(-50%);
    font-size: 105px;
    z-index: 3;
    filter: drop-shadow(0 5px 2px rgba(0,0,0,.25));
    user-select: none;
}

.object {
    position: absolute;
    font-size: 70px;
    bottom: 28px;
    z-index: 2;
    user-select: none;
}
.obj-left { left: 8%; }
.obj-right { right: 8%; }

.click-hint {
    text-align: center;
    color: #79553b;
    font-weight: 700;
    margin-top: 5px;
}

.shop-title {
    color: #573823;
    font-family: 'Jua', sans-serif;
    font-size: 1.8rem;
    margin-top: 12px;
}

.shop-card {
    background: #fffaf0;
    border: 2px solid #d9bc8e;
    border-radius: 18px;
    padding: 15px;
    min-height: 145px;
}

.progress-wrap {
    background: #ddc8a7;
    border-radius: 20px;
    height: 24px;
    overflow: hidden;
    border: 2px solid #9e7a50;
}
.progress-bar {
    height: 100%;
    background: #e6a83d;
    border-radius: 18px;
    transition: width .25s ease;
}

.float {
    animation: fadeUp 1.1s ease-out forwards;
    text-align: center;
    font-size: 2rem;
    font-weight: 900;
    color: #c8751a;
    text-shadow: 1px 1px white;
}
@keyframes fadeUp {
    0% { opacity: 1; transform: translateY(0) scale(1); }
    100% { opacity: 0; transform: translateY(-55px) scale(1.15); }
}

.clear-box {
    background: #fff4c8;
    border: 3px solid #d79d31;
    border-radius: 20px;
    padding: 18px;
    text-align: center;
    margin: 10px 0;
}

div.stButton > button {
    border-radius: 14px;
    font-weight: 800;
    border: 2px solid #9b6e3c;
}

div.stButton > button[kind="primary"] {
    background: #e49b35;
    color: white;
    min-height: 70px;
    font-size: 1.35rem;
    box-shadow: 0 5px 0 #a96d24;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="game-title">💰 탈출! 거지 클리커</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">클릭해서 돈을 벌고, 가난에서 한 단계씩 탈출하세요!</div>', unsafe_allow_html=True)

# Top stats
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        f'<div class="money-card"><div class="money-label">현재 자산</div>'
        f'<div class="money-value">₩{st.session_state.money:,}</div></div>',
        unsafe_allow_html=True
    )
with c2:
    st.markdown(
        f'<div class="money-card"><div class="money-label">클릭 1회 수입</div>'
        f'<div class="money-value">₩{st.session_state.click_power * st.session_state.multi_click:,}</div></div>',
        unsafe_allow_html=True
    )
with c3:
    st.markdown(
        f'<div class="money-card"><div class="money-label">현재 스테이지</div>'
        f'<div class="money-value">{st.session_state.stage + 1} / 5</div></div>',
        unsafe_allow_html=True
    )

# Scene
scene_objects = [
    ("🌳", "🌾"),
    ("🏪", "🚏"),
    ("🪟", "🚪"),
    ("🛋️", "🚪"),
    ("🏢", "🚗"),
]
st.markdown(
    f'<div class="scene scene-{st.session_state.stage}">'
    f'<h2>Stage {st.session_state.stage + 1} · {stage["name"]}</h2>'
    f'<div class="object obj-left">{scene_objects[st.session_state.stage][0]}</div>'
    f'<div class="object obj-right">{scene_objects[st.session_state.stage][1]}</div>'
    f'<div class="character">🧍</div>'
    f'</div>',
    unsafe_allow_html=True
)

st.markdown(f'<div class="click-hint">{stage["place"]} · 목표: ₩{goal:,}</div>', unsafe_allow_html=True)

# Progress
st.markdown(
    f'<div class="progress-wrap"><div class="progress-bar" style="width:{progress*100:.1f}%"></div></div>',
    unsafe_allow_html=True
)
st.caption(f"진행도 {progress*100:.1f}% · ₩{st.session_state.money:,} / ₩{goal:,}")

# Floating money effect + sound
if st.session_state.last_gain:
    components.html(
        f"""
        <div class="float">+₩{st.session_state.last_gain:,}</div>
        <script>
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        try {{
            const ctx = new AudioContext();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = "sine";
            osc.frequency.value = 720;
            gain.gain.setValueAtTime(0.045, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.12);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start();
            osc.stop(ctx.currentTime + 0.12);
        }} catch(e) {{}}
        </script>
        """,
        height=65,
    )

if st.session_state.message:
    st.info(st.session_state.message)

# Main click button
_, mid, _ = st.columns([1, 2, 1])
with mid:
    if st.button("💰 돈 벌기!  +₩{:,.0f}".format(st.session_state.click_power * st.session_state.multi_click),
                 type="primary", use_container_width=True):
        click_game()
        st.rerun()

# Shop
st.markdown('<div class="shop-title">🛒 상점</div>', unsafe_allow_html=True)
s1, s2 = st.columns(2)

power_cost = int(1_000 * (1.5 ** st.session_state.power_level))
multi_cost = int(1_000 * (1.5 ** st.session_state.multi_level))

with s1:
    st.markdown(
        f'<div class="shop-card"><b>💵 수입 증가</b><br>'
        f'클릭당 +1,000원<br>현재: +₩{st.session_state.click_power:,}<br>'
        f'레벨: {st.session_state.power_level}<br>'
        f'<b>가격: ₩{power_cost:,}</b></div>',
        unsafe_allow_html=True
    )
    if st.button("수입 +1,000원 구매", use_container_width=True, key="power"):
        buy_power()
        st.rerun()

with s2:
    st.markdown(
        f'<div class="shop-card"><b>⚡ 추가 클릭</b><br>'
        f'한 번 클릭할 때 +1회 적용<br>'
        f'현재 클릭 배수: ×{st.session_state.multi_click}<br>'
        f'레벨: {st.session_state.multi_level}<br>'
        f'<b>가격: ₩{multi_cost:,}</b></div>',
        unsafe_allow_html=True
    )
    if st.button("추가 클릭 +1 구매", use_container_width=True, key="multi"):
        buy_multi()
        st.rerun()

# Stage clear
if won_stage():
    if st.session_state.stage < 4:
        st.markdown(
            f'<div class="clear-box"><b>🎉 {stage["name"]} 성공!</b><br>'
            f'목표 금액 ₩{goal:,}을 넘었습니다.</div>',
            unsafe_allow_html=True
        )
        if st.button(f"🚪 {STAGES[st.session_state.stage + 1]['name']}로 이동", use_container_width=True):
            next_stage()
            st.rerun()
    else:
        st.session_state.game_clear = True

if st.session_state.game_clear:
    st.balloons()
    st.success("🏆 모든 스테이지를 클리어했습니다! 이제 완전한 탈출입니다!")
    st.markdown("### 🌟 최종 자산: ₩{:,.0f}".format(st.session_state.money))

st.divider()
left, right = st.columns([3, 1])
with left:
    st.caption("※ 게임의 기본 구조와 클릭 방식은 '거지키우기'에서 영감을 받아 제작한 클리커 게임입니다.")
with right:
    if st.button("🔄 처음부터 다시", use_container_width=True):
        reset_game()
