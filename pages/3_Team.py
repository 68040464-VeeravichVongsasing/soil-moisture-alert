# =========================================================
# หน้าคณะผู้จัดทำโครงการ (แยกจาก Dashboard) — ข้อมูลมาจาก README.md และส่วน "เกี่ยวกับโครงการ" เดิมของแอป
# =========================================================
import streamlit as st

import ui_helpers as ui

st.set_page_config(
    page_title="คณะผู้จัดทำ | Smart Farm Alert",
    page_icon=ui.get_page_icon(),
    layout="centered",
    initial_sidebar_state="auto",
)

ui.keep_control_state()

# ----- ข้อมูลจริงของโครงการ (แก้ที่นี่ที่เดียว) -----
PROJECT_TITLE = "การพัฒนาระบบ/แอปแจ้งเตือนความชื้นและรดน้ำอัตโนมัติ"
PROJECT_PERIOD = "29 มิ.ย. - 21 ต.ค. 2569"
GROUP_NAME = "กลุ่ม Python"
ADVISOR = "ผศ.ดร.ธนัท สมณคุปต์"
MEMBERS = [
    ("นายกนกพล เกตุจรุง", "Project Manager (PM)"),
    ("นายวีรวิชญ์ วงค์ษาสิงห์", "Programmer"),
    ("นายธนธร สืบกระแสร์", "Programmer"),
    ("นายจิรภัทร จำนงศิลป์", "Graphic & UI"),
    ("นายธเนศ แต้โนนฝาว", "Report & Slide Presentation"),
]
REFERENCES = [
    "data.go.th — สถิติภูมิอากาศรายวัน",
    "กรมอุตุนิยมวิทยา (TMD) — ข้อมูลอุณหภูมิและปริมาณน้ำฝน",
    "กรมวิชาการเกษตร / กรมส่งเสริมการเกษตร — อัตราการระเหยน้ำ (Evapotranspiration) "
    "ของไม้ผลเฉลี่ย 3.8-5.7 มม./วัน",
]

TEAM_CSS = """
.stApp { font-family: 'Plus Jakarta Sans', 'Noto Sans Thai', -apple-system, sans-serif;
    background: radial-gradient(circle at 90% 0%, rgba(46,92,70,.10), transparent 30%), #F5F7F5; }
.block-container { max-width: 760px; padding: 1.2rem 1rem 3rem 1rem; }
.team-hero { position: relative; overflow: hidden; text-align: center; color: #fff; padding: 30px 20px 26px;
    border-radius: 28px; background: linear-gradient(145deg, #315F49 0%, #183C2B 100%);
    box-shadow: 0 18px 40px rgba(31,66,49,.22); animation: fadeUp .6s both; }
.team-hero::after { content: "🌿"; position: absolute; right: 14px; top: 2px; font-size: 6.5rem; opacity: .12; transform: rotate(12deg); }
.team-icon { width: 88px; height: 88px; border-radius: 24px; box-shadow: 0 12px 28px rgba(0,0,0,.35); animation: floatY 4s ease-in-out infinite; }
.team-title { font-size: clamp(1.35rem, 5vw, 1.7rem); font-weight: 800; margin: 16px 0 4px; color: #fff; }
.team-sub { font-size: .85rem; color: rgba(255,255,255,.78); margin: 0; }
.sec-title { display: flex; align-items: center; gap: 9px; margin: 28px 2px 12px; color: #17231D; font-size: 1.05rem; font-weight: 800; }
.sec-title .ico { width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; border-radius: 10px; background: #E7F1EB; }
.member-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 12px; }
.m-card { display: flex; align-items: center; gap: 13px; background: #fff; border: 1px solid #E7ECE8; border-radius: 20px;
    padding: 14px 16px; box-shadow: 0 8px 24px rgba(20,50,35,.05); transition: transform .2s ease, box-shadow .2s ease; animation: fadeUp .6s both; }
.m-card:hover { transform: translateY(-4px); box-shadow: 0 14px 30px rgba(20,50,35,.13); }
.m-card:nth-child(1) { animation-delay: .10s; } .m-card:nth-child(2) { animation-delay: .18s; }
.m-card:nth-child(3) { animation-delay: .26s; } .m-card:nth-child(4) { animation-delay: .34s; }
.m-card:nth-child(5) { animation-delay: .42s; }
.avatar { width: 46px; height: 46px; border-radius: 50%; flex-shrink: 0; display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem; background: linear-gradient(135deg, #E7F1EB, #CFE6D8); }
.m-name { color: #17231D; font-weight: 700; font-size: .95rem; line-height: 1.35; }
.m-role { display: inline-block; margin-top: 5px; padding: 2px 10px; border-radius: 999px; background: #E7F1EB;
    color: #2E5C46; font-size: .75rem; font-weight: 700; }
.advisor { border: 1.5px solid #8CAF99; background: linear-gradient(135deg, #FFFFFF, #F1F8F3); animation-delay: .1s; }
.info-card { background: #fff; border: 1px solid #E7ECE8; border-radius: 22px; padding: 6px 20px 14px;
    box-shadow: 0 8px 24px rgba(20,50,35,.05); animation: fadeUp .6s .2s both; }
.info-label { color: #7B867F; font-size: .75rem; font-weight: 600; margin-top: 14px; }
.info-value { color: #17231D; font-size: .93rem; font-weight: 600; margin-top: 2px; line-height: 1.55; }
.ref-list { color: #34443B; font-size: .85rem; line-height: 1.65; padding-left: 18px; margin: 6px 0 4px; }
"""

ui.inject_shell_css()
st.markdown(f"<style>{TEAM_CSS}</style>", unsafe_allow_html=True)
ui.render_sidebar("team")

members_html = "".join(
    f"<div class='m-card'><div class='avatar'>👤</div>"
    f"<div><div class='m-name'>{name}</div><div class='m-role'>{role}</div></div></div>"
    for name, role in MEMBERS
)
refs_html = "".join(f"<li>{r}</li>" for r in REFERENCES)

st.markdown(
    "<div class='team-hero'>"
    f"{ui.icon_html('team-icon', small=True)}"
    "<div class='team-title'>คณะผู้จัดทำโครงการ</div>"
    "<p class='team-sub'>Smart Farm Alert</p>"
    "</div>"
    "<div class='sec-title'><div class='ico'>👥</div>คณะผู้จัดทำ</div>"
    f"<div class='member-grid'>{members_html}</div>"
    "<div class='sec-title'><div class='ico'>🎓</div>อาจารย์ที่ปรึกษา</div>"
    f"<div class='m-card advisor'><div class='avatar'>🎓</div><div><div class='m-name'>{ADVISOR}</div>"
    "<div class='m-role'>อาจารย์ที่ปรึกษาโครงการ</div></div></div>"
    "<div class='sec-title'><div class='ico'>📋</div>ข้อมูลโครงการ</div>"
    "<div class='info-card'>"
    f"<div class='info-label'>ชื่อโครงการ</div><div class='info-value'>{PROJECT_TITLE}</div>"
    f"<div class='info-label'>ระยะเวลาดำเนินการ</div><div class='info-value'>{PROJECT_PERIOD}</div>"
    f"<div class='info-label'>ผู้จัดทำ</div><div class='info-value'>{GROUP_NAME}</div>"
    "<div class='info-label'>อ้างอิงข้อมูลและแนวคิดการจำลอง</div>"
    f"<ul class='ref-list'>{refs_html}</ul>"
    "</div>",
    unsafe_allow_html=True,
)
