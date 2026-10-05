import streamlit as st
import database
import pandas as pd
import random
from datetime import datetime

# 1. ตั้งค่าหน้าจอ (ต้องอยู่บรรทัดแรก)
st.set_page_config(page_title="ระบบแจ้งเตือนและรดน้ำอัตโนมัติ", layout="centered")

# 2. เรียกใช้การสร้างฐานข้อมูล
database.init_db()

# --- ตั้งค่า Session State (ตัวแปรเก็บสถานะชั่วคราวขณะเปิดเว็บ) ---
if 'moisture' not in st.session_state:
    st.session_state.moisture = 55.0  # ค่าความชื้นเริ่มต้น
if 'pump_on' not in st.session_state:
    st.session_state.pump_on = False
if 'auto_mode' not in st.session_state:
    st.session_state.auto_mode = True
if 'threshold' not in st.session_state:
    st.session_state.threshold = 40.0

def simulate_sensor():
    """จำลองการเปลี่ยนแปลงความชื้นเมื่อเวลาผ่านไป"""
    if st.session_state.pump_on:
        # ถ้ารดน้ำ ความชื้นเพิ่ม
        st.session_state.moisture += random.uniform(5.0, 10.0)
        if st.session_state.moisture >= 90.0:
            st.session_state.moisture = 90.0
            if st.session_state.auto_mode:
                st.session_state.pump_on = False # ออโต้ปิดเมื่อชื้นพอ
    else:
        # ถ้าไม่รดน้ำ ความชื้นลดลง
        st.session_state.moisture -= random.uniform(2.0, 5.0)
        if st.session_state.moisture <= 10.0:
            st.session_state.moisture = 10.0

    # Auto mode เช็กความชื้น
    if st.session_state.auto_mode and st.session_state.moisture < st.session_state.threshold:
        st.session_state.pump_on = True

    # บันทึกข้อมูลลงฐานข้อมูล (SQLite)
    conn = database.get_conn()
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # บันทึกความชื้น
    cursor.execute("INSERT INTO sensor_data (timestamp, moisture_level) VALUES (?, ?)", 
                   (current_time, st.session_state.moisture))
    
    # บันทึกประวัติรดน้ำ (ถ้าปั๊มทำงาน)
    if st.session_state.pump_on:
        cursor.execute("INSERT INTO watering_logs (start_time, status, mode) VALUES (?, ?, ?)",
                       (current_time, "กำลังรดน้ำ", "Auto" if st.session_state.auto_mode else "Manual"))
        
    conn.commit()
    conn.close()


# --- หน้าจอ UI ---
st.title("🌱 ระบบแจ้งเตือนและรดน้ำอัตโนมัติ")
st.markdown("ระบบติดตามค่าความชื้นในดินและควบคุมปั๊มน้ำ")
st.divider()

# FR-01: ส่วนแสดงค่าความชื้น
st.header("💧 สถานะความชื้นปัจจุบัน")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="ความชื้นในดิน", 
              value=f"{st.session_state.moisture:.1f} %", 
              delta="- ลดลง" if not st.session_state.pump_on else "+ เพิ่มขึ้น",
              delta_color="normal" if st.session_state.pump_on else "inverse")
with col2:
    status = "กำลังรดน้ำ 💦" if st.session_state.pump_on else "ปิด 🛑"
    st.metric(label="สถานะปั๊มน้ำ", value=status)

st.divider()

# FR-02: ส่วนแจ้งเตือน
st.header("🔔 การแจ้งเตือน")
if st.session_state.moisture < st.session_state.threshold:
    st.error(f"⚠️ ความชื้นต่ำกว่าเกณฑ์ ({st.session_state.threshold}%) ระบบต้องการน้ำ!")
elif st.session_state.pump_on:
    st.info("ℹ️ ระบบกำลังรดน้ำแปลงเกษตร")
else:
    st.success("✅ ระดับความชื้นอยู่ในเกณฑ์ปกติ")

st.divider()

# FR-03 & FR-04: ส่วนควบคุม
st.header("⚙️ ควบคุมระบบรดน้ำ")
st.session_state.auto_mode = st.toggle("🤖 เปิดระบบรดน้ำอัตโนมัติ (Auto Mode)", value=st.session_state.auto_mode)
st.session_state.threshold = st.slider("ตั้งเกณฑ์ความชื้นที่ต้องการรดน้ำ (%)", min_value=20.0, max_value=80.0, value=st.session_state.threshold, step=5.0)

if not st.session_state.auto_mode:
    button_text = "ปิดปั๊มน้ำ" if st.session_state.pump_on else "เปิดปั๊มน้ำ"
    if st.button(f"💦 {button_text} (Manual)"):
        st.session_state.pump_on = not st.session_state.pump_on
        st.rerun() # รีเฟรชหน้าจอเพื่ออัปเดตสถานะปุ่ม
else:
    st.info("โหมด Manual ถูกปิดการใช้งาน (ต้องปิด Auto Mode ก่อน)")

st.markdown("---")
# ปุ่มจำลองการทำงาน (เพื่อให้เห็นภาพการเปลี่ยนแปลง)
if st.button("⏳ จำลองเวลาผ่านไป (อัปเดตข้อมูล)"):
    simulate_sensor()
    st.rerun()

# FR-05: ดูกราฟ
st.header("📈 ประวัติความชื้นย้อนหลัง")
conn = database.get_conn()
df = pd.read_sql_query("SELECT timestamp, moisture_level FROM sensor_data ORDER BY id DESC LIMIT 20", conn)
conn.close()

if not df.empty:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    df.set_index('timestamp', inplace=True)
    st.line_chart(df)
else:
    st.info("ยังไม่มีข้อมูลประวัติความชื้น (กด 'จำลองเวลาผ่านไป' เพื่อสร้างข้อมูล)")
