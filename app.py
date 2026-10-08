import streamlit as st
import database
import pandas as pd
from datetime import datetime
import random
import time
from utils import check_watering_condition

# =========================================================
# 1. CONSTANTS & PAGE CONFIG
# =========================================================
MAX_MOISTURE = 90.0
MIN_MOISTURE = 10.0
DEFAULT_MOISTURE = 59.0
LOG_EVERY_N_STEPS = 3   # ระหว่างรดน้ำ บันทึกลง DB ทุก N รอบ (ลดขนาด DB)
CHART_POINTS = 50       # จำนวนจุดข้อมูลที่แสดงในกราฟ

st.set_page_config(
    page_title="Smart Farm Alert",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 2. CUSTOM UI / CSS (UPGRADED)
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background: radial-gradient(circle at 90% 0%, rgba(46,92,70,.08), transparent 28%), #F5F7F5;
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
}

.block-container {
    max-width: 760px;
    padding: 1.2rem 1rem 3rem 1rem;
}

/* Banner */
.app-banner {
    position: relative;
    overflow: hidden;
    min-height: 150px;
    padding: 24px;
    border-radius: 26px;
    margin-bottom: 16px;
    display: flex;
    align-items: flex-end;
    color: white;
    background: linear-gradient(135deg, rgba(12,66,44,.90), rgba(27,91,62,.68)), 
                url("https://images.unsplash.com/photo-1592982537447-6f29910d681e?q=80&w=1200&auto=format&fit=crop");
    background-color: #1a4f36; /* Fallback color */
    background-size: cover;
    background-position: center;
    box-shadow: 0 14px 35px rgba(20,70,48,.18);
}

.app-banner::after {
    content: "🌿";
    position: absolute;
    right: 18px;
    top: 8px;
    font-size: 6rem;
    opacity: .12;
    transform: rotate(12deg);
}

.banner-icon {
    width: 52px; height: 52px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 16px;
    background: rgba(255,255,255,.16);
    border: 1px solid rgba(255,255,255,.18);
    backdrop-filter: blur(8px);
    font-size: 1.8rem; flex-shrink: 0;
}

.banner-title {
    margin: 0;
    font-size: clamp(1.35rem, 5vw, 1.75rem);
    font-weight: 800; line-height: 1.1;
}

.banner-subtitle {
    margin: 6px 0 0 0; color: rgba(255,255,255,.78); font-size: .85rem;
}

.section-title {
    display: flex; align-items: center; gap: 9px;
    margin: 20px 2px 10px; color: #17231D;
    font-size: 1.05rem; font-weight: 800;
}

.section-title .icon {
    width: 32px; height: 32px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 10px; background: #E7F1EB;
}

/* Hero Card */
.hero-card {
    position: relative; overflow: hidden;
    padding: 24px; border-radius: 28px; color: white;
    background: linear-gradient(145deg, #315F49 0%, #183C2B 100%);
    box-shadow: 0 18px 40px rgba(31,66,49,.22);
}

.hero-graphic {
    position: absolute; right: 10px; top: 25px;
    font-size: 6.5rem; opacity: 0.85;
    filter: drop-shadow(0 15px 20px rgba(0,0,0,0.3));
    z-index: 1; animation: float 3.5s ease-in-out infinite;
}

@keyframes float {
    0% { transform: translateY(0px) scale(1); }
    50% { transform: translateY(-12px) scale(1.02); }
    100% { transform: translateY(0px) scale(1); }
}

.hero-top {
    position: relative; z-index: 2;
    display: flex; align-items: center; justify-content: space-between;
}

.hero-label {
    color: rgba(255,255,255,.85); font-size: .9rem; font-weight: 600;
}

.live-pill {
    display: flex; align-items: center; gap: 6px;
    padding: 6px 10px; border-radius: 999px;
    background: rgba(255,255,255,.11); border: 1px solid rgba(255,255,255,.10);
    font-size: .72rem; color: rgba(255,255,255,.9);
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 currentColor; }
    70% { box-shadow: 0 0 0 6px rgba(255,255,255,0); }
    100% { box-shadow: 0 0 0 0 rgba(255,255,255,0); }
}

.live-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: currentColor; animation: pulse 2s infinite;
}

.moisture-row {
    position: relative; z-index: 2;
    display: flex; align-items: baseline; gap: 5px; margin: 8px 0 4px;
}

.moisture-value {
    font-size: clamp(4.2rem, 17vw, 6.5rem); line-height: .95; font-weight: 800; letter-spacing: -2px;
}

.moisture-unit {
    font-size: 2rem; font-weight: 700; color: rgba(255,255,255,.65);
}

.status-row {
    position: relative; z-index: 2; display: flex; align-items: center;
    gap: 10px; font-size: .95rem; font-weight: 600; margin-top: 5px;
}

.status-dot {
    width: 10px; height: 10px; border-radius: 50%; animation: pulse 2s infinite;
}

.moisture-bar {
    position: relative; z-index: 2; height: 8px; margin-top: 20px;
    border-radius: 999px; background: rgba(255,255,255,.13); overflow: hidden;
}

.moisture-fill {
    height: 100%; border-radius: 999px; background: rgba(255,255,255,.85);
    box-shadow: 0 0 12px rgba(255,255,255,.3); transition: width 0.4s ease-out;
}

.moisture-threshold-marker {
    position: absolute; top: -1px; bottom: -1px; width: 3px;
    background: #FCA5A5; border-radius: 2px; z-index: 3;
    box-shadow: 0 0 6px rgba(252,165,165,0.8);
}

.hero-alert {
    position: relative; z-index: 2; display: flex; align-items: center; gap: 12px;
    margin-top: 18px; padding: 14px 16px; border-radius: 16px;
    background: rgba(14, 38, 27, 0.45); border: 1px solid rgba(255,255,255,.12);
    backdrop-filter: blur(8px); font-size: .85rem; font-weight: 500; line-height: 1.4;
}

@keyframes spin-slow { 100% { transform: rotate(360deg); } }
.icon-spin { display: inline-block; animation: spin-slow 3s linear infinite; }

/* Mini Cards */
.mini-grid {
    display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 12px;
}
.mini-card {
    padding: 16px; border-radius: 20px; background: white;
    border: 1px solid #E7ECE8; box-shadow: 0 8px 24px rgba(20,50,35,.04);
}
.mini-label { color: #7B867F; font-size: .75rem; font-weight: 600; }
.mini-value { margin-top: 5px; color: #17231D; font-size: 1.3rem; font-weight: 800; }
.mini-sub { margin-top: 2px; color: #5A665E; font-size: .7rem; font-weight: 500; }

/* Streamlit Containers (Modern Target via keys) */
div.st-key-control_card {
    padding: 20px; border-radius: 24px; background: white;
    border: 1px solid #E6EBE7; box-shadow: 0 8px 24px rgba(20,50,35,.055);
}
div.st-key-chart_card {
    padding: 20px 16px 10px; border-radius: 24px; background: white;
    border: 1px solid #E6EBE7; box-shadow: 0 8px 24px rgba(20,50,35,.055);
}

/* Streamlit overrides */
div.stButton > button {
    min-height: 50px; border-radius: 16px !important; border: 1px solid #E1E8E3 !important;
    background: white !important; color: #203027 !important; font-weight: 700 !important;
    box-shadow: 0 4px 12px rgba(20,50,35,.04) !important; transition: all .2s ease !important;
}
div.stButton > button:hover {
    border-color: #8CAF99 !important; transform: translateY(-2px); box-shadow: 0 6px 16px rgba(20,50,35,.08) !important;
}
div.stButton > button:active { transform: scale(.97); }

@media (max-width: 600px) {
    .block-container { padding: .5rem .75rem 2.5rem; }
    .hero-graphic { font-size: 5.5rem; right: -5px; top: 20px; }
    .hero-card { padding: 20px; border-radius: 24px; }
    .moisture-value { font-size: 4.5rem; }
    .banner-title { font-size: 1.3rem; }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. DATABASE INITIALIZATION & STATE RECOVERY
# =========================================================
database.init_db()

# ดึงค่าล่าสุดจาก DB แทนการ Hardcode 59% ทุกครั้ง
if "moisture" not in st.session_state:
    conn = database.get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT moisture_level FROM sensor_data ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if row:
            st.session_state.moisture = float(row[0])
        else:
            st.session_state.moisture = DEFAULT_MOISTURE
    except Exception:
        st.session_state.moisture = DEFAULT_MOISTURE
    finally:
        conn.close()

if "pump_on" not in st.session_state:
    st.session_state.pump_on = False

if "auto_mode" not in st.session_state:
    st.session_state.auto_mode = True

if "threshold" not in st.session_state:
    st.session_state.threshold = 40.0

if "water_steps" not in st.session_state:
    st.session_state.water_steps = 0


# =========================================================
# 4. DATABASE LOGGER (WITH ERROR HANDLING)
# =========================================================
def log_to_db(status_msg, log_sensor=True):
    conn = database.get_conn()
    try:
        cursor = conn.cursor()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if log_sensor:
            cursor.execute(
                "INSERT INTO sensor_data (timestamp, moisture_level) VALUES (?, ?)",
                (current_time, st.session_state.moisture)
            )

        if status_msg:
            cursor.execute(
                "INSERT INTO watering_logs (start_time, status, mode) VALUES (?, ?, ?)",
                (current_time, status_msg, "Auto" if st.session_state.auto_mode else "Manual")
            )
        conn.commit()
    finally:
        conn.close()


def emergency_stop():
    """ใช้เป็น on_click callback เพื่อให้แก้ค่า key ของ widget (auto_mode) ได้อย่างปลอดภัย"""
    st.session_state.pump_on = False
    st.session_state.auto_mode = False  # ปิด Auto ไปด้วย ป้องกันปั๊มเปิดซ้ำทันที
    log_to_db("หยุดปั๊มฉุกเฉิน")


# =========================================================
# 5. BUSINESS LOGIC & STATUS CALCULATION
# =========================================================
# ย้ายการเช็กเงื่อนไขมาไว้ตรงนี้ เพื่อให้ Auto Mode ทำงานทันทีเมื่อขยับเกณฑ์ Slider
if st.session_state.auto_mode and not st.session_state.pump_on:
    if check_watering_condition(st.session_state.moisture, st.session_state.threshold, st.session_state.auto_mode):
        st.session_state.pump_on = True
        log_to_db("ปั๊มทำงานอัตโนมัติ", log_sensor=False)  # ค่าความชื้นถูกบันทึกไปแล้ว ไม่ต้องซ้ำ

if st.session_state.pump_on:
    status_text = "กำลังรดน้ำ (Watering)"
    status_color = "#93C5FD" # ฟ้า
    alert_icon = "<span class='icon-spin'>🔄</span>"
    alert_msg = "ระบบกำลังรดน้ำแปลงเกษตร..."
    alert_bg = "rgba(37, 99, 235, 0.35)"
elif st.session_state.moisture < st.session_state.threshold:
    status_text = "วิกฤต (Critical)"
    status_color = "#FCA5A5" # แดง
    alert_icon = "⚠️"
    alert_msg = f"ความชื้นต่ำกว่าเกณฑ์ {st.session_state.threshold:.0f}% ดินแห้งเกินไป!"
    alert_bg = "rgba(220, 38, 38, 0.35)"
else:
    status_text = "ระดับปกติ (Normal)"
    status_color = "#86EFAC" # เขียวอ่อน
    alert_icon = "✨"
    alert_msg = "สภาพดินเหมาะสม ไม่จำเป็นต้องรดน้ำ"
    alert_bg = "rgba(14, 38, 27, 0.45)"

moisture_percent = max(0, min(100, st.session_state.moisture))


# =========================================================
# 6. APP BANNER & HERO MOISTURE CARD
# =========================================================
st.markdown("""
<div class="app-banner">
    <div class="banner-icon">🌱</div>
    <div style="margin-left:15px; position:relative; z-index:2;">
        <h1 class="banner-title">Smart Farm Alert</h1>
        <p class="banner-subtitle">ระบบแจ้งเตือนความชื้นและรดน้ำอัตโนมัติ</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="hero-card">
    <div class="hero-graphic">💧</div>
    <div class="hero-top">
        <span class="hero-label">ความชื้นในดิน (Moisture)</span>
        <div class="live-pill" style="color:{status_color}; border-color: {status_color}40;">
            <span class="live-dot" style="color:{status_color};"></span> LIVE
        </div>
    </div>
    <div class="moisture-row">
        <span class="moisture-value">{st.session_state.moisture:.0f}</span>
        <span class="moisture-unit">%</span>
    </div>
    <div class="status-row">
        <span class="status-dot" style="background:{status_color}; color:{status_color};"></span>
        <span>{status_text}</span>
    </div>
    <div class="moisture-bar">
        <div class="moisture-fill" style="width:{moisture_percent}%;"></div>
        <div class="moisture-threshold-marker" style="left:{st.session_state.threshold}%;"></div>
    </div>
    <div class="hero-alert" style="background:{alert_bg};">
        <span style="font-size:1.2rem;">{alert_icon}</span>
        <span>{alert_msg}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 7. MINI STATUS CARDS
# =========================================================
pump_status = "ON" if st.session_state.pump_on else "OFF"
pump_text = "กำลังทำงาน" if st.session_state.pump_on else "พร้อมใช้งาน"

st.markdown(f"""
<div class="mini-grid">
    <div class="mini-card">
        <div class="mini-label">🎯 เกณฑ์ตั้งต้น</div>
        <div class="mini-value">{st.session_state.threshold:.0f}%</div>
        <div class="mini-sub">ระบบออโต้จะทำงาน</div>
    </div>
    <div class="mini-card">
        <div class="mini-label">💦 ปั๊มน้ำ</div>
        <div class="mini-value" style="color: {'#3B82F6' if st.session_state.pump_on else '#17231D'};">{pump_status}</div>
        <div class="mini-sub">{pump_text}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 8. CONTROL PANEL (Using Containers & Keys properly)
# =========================================================
st.markdown("""
<div class="section-title">
    <div class="icon">⚙️</div>
    แผงควบคุมระบบ (Control Panel)
</div>
""", unsafe_allow_html=True)

with st.container(key="control_card"):
    st.toggle("🤖 โหมดรดน้ำอัตโนมัติ (Auto Mode)", key="auto_mode")
    st.slider("เกณฑ์การรดน้ำอัตโนมัติ (%)", min_value=20.0, max_value=80.0, step=5.0, key="threshold")

st.write("")
col1, col2 = st.columns(2, gap="small")

with col1:
    # Disable ปุ่มจำลองเวลา ถ้าปั๊มทำงานอยู่
    if st.button("☀️ จำลองเวลา (ดินแห้ง)", use_container_width=True, disabled=st.session_state.pump_on):
        st.session_state.moisture -= random.uniform(5.0, 10.0)
        if st.session_state.moisture < MIN_MOISTURE:
            st.session_state.moisture = MIN_MOISTURE
        log_to_db(None)
        st.rerun()

with col2:
    if not st.session_state.auto_mode:
        button_text = "🛑 ปิดปั๊มน้ำ (Stop)" if st.session_state.pump_on else "💦 เปิดปั๊มน้ำ (Manual)"
        if st.button(button_text, use_container_width=True):
            st.session_state.pump_on = not st.session_state.pump_on
            log_to_db("สั่งเปิดปั๊ม (Manual)" if st.session_state.pump_on else "สั่งปิดปั๊ม (Manual)")
            st.rerun()
    else:
        # ระบบหยุดฉุกเฉิน
        if st.session_state.pump_on:
            st.button("🛑 ปิดฉุกเฉิน", use_container_width=True, on_click=emergency_stop)
        else:
            st.button("🔒 ล็อกการกด Manual", disabled=True, use_container_width=True)

# =========================================================
# 9. HISTORY CHART (With proper DB connection handling)
# =========================================================
st.markdown("""
<div class="section-title">
    <div class="icon">📈</div>
    ประวัติความชื้นย้อนหลัง
</div>
""", unsafe_allow_html=True)

conn = database.get_conn()
try:
    df = pd.read_sql_query(
        "SELECT timestamp, moisture_level FROM sensor_data ORDER BY id DESC LIMIT ?",
        conn,
        params=(CHART_POINTS,)
    )
finally:
    conn.close()

with st.container(key="chart_card"):
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")
        df.set_index("timestamp", inplace=True)
        st.line_chart(df, y="moisture_level", height=220, color="#315F49", use_container_width=True)
    else:
        st.caption("ยังไม่มีข้อมูลความชื้นสำหรับแสดงผล")

# =========================================================
# 10. PROJECT INFORMATION
# =========================================================
st.write("")
with st.expander("ℹ️ เกี่ยวกับโครงการและคณะผู้จัดทำ"):
    st.markdown("""
### 🌱 Smart Farm Alert
**การพัฒนาระบบ/แอปแจ้งเตือนความชื้นและรดน้ำอัตโนมัติ**

**ระยะเวลาดำเนินการ:** 29 มิ.ย. - 21 ต.ค. 2569

**อาจารย์ที่ปรึกษา**
- ผศ.ดร.ธนัท สมณคุปต์

**ผู้จัดทำ (กลุ่ม Python)**
1. นายกนกพล เกตุจรุง — Project Manager
2. นายวีรวิชญ์ วงค์ษาสิงห์ — Programmer
3. นายธนธร สืบกระแสร์ — Programmer
4. นายจิรภัทร จำนงศิลป์ — Graphic
5. นายธเนศ แต้โนนฝาว — Report / Slide

**อ้างอิงข้อมูลและแนวคิดการจำลอง**
- data.go.th — สถิติภูมิอากาศรายวัน
- กรมอุตุนิยมวิทยา (TMD) — ข้อมูลอุณหภูมิและปริมาณน้ำฝน
- กรมวิชาการเกษตร / กรมส่งเสริมการเกษตร — อัตราการระเหยน้ำ (Evapotranspiration) ของไม้ผลเฉลี่ย 3.8-5.7 มม./วัน
""")

# =========================================================
# 11. AUTOMATIC WATERING ANIMATION LOOP
# =========================================================
if st.session_state.pump_on:
    time.sleep(0.4)
    st.session_state.moisture += random.uniform(2.0, 5.0)
    st.session_state.water_steps += 1

    if st.session_state.moisture >= MAX_MOISTURE:
        st.session_state.moisture = MAX_MOISTURE
        st.session_state.pump_on = False
        st.session_state.water_steps = 0
        log_to_db("ปั๊มหยุดอัตโนมัติ (ความชื้นเต็ม)")
    elif st.session_state.water_steps % LOG_EVERY_N_STEPS == 0:
        log_to_db(None)  # บันทึกกราฟให้ไต่ระดับขึ้น (ทุก N รอบ)

    st.rerun()