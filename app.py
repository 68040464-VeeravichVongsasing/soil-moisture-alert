# =========================================================
# หน้า Home (หน้าแรกก่อนเข้าใช้งาน) — ไฟล์หลักของแอป (Main file path บน Streamlit Cloud = app.py)
# หน้า Dashboard อยู่ที่ pages/2_Dashboard.py และคณะผู้จัดทำอยู่ที่ pages/3_Team.py
# =========================================================
import streamlit as st

import ui_helpers as ui

st.set_page_config(
    page_title="Smart Farm Alert",
    page_icon=ui.get_page_icon(),
    layout="centered",
    initial_sidebar_state="collapsed",
)

# หน้านี้ไม่แตะฐานข้อมูล ไม่เริ่มรดน้ำ และไม่เปลี่ยนค่าควบคุมใด ๆ
ui.keep_control_state()

HOME_CSS = """
#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"], [data-testid="stExpandSidebarButton"], [data-testid="stStatusWidget"] { display: none !important; }
.stApp { font-family: 'Plus Jakarta Sans', 'Noto Sans Thai', -apple-system, sans-serif;
    background: linear-gradient(160deg, #0F3A27 0%, #1B5B3E 45%, #0B2C1E 100%); background-size: 220% 220%;
    animation: bgShift 16s ease-in-out infinite; }
@keyframes bgShift { 0% { background-position: 0% 0%; } 50% { background-position: 100% 100%; } 100% { background-position: 0% 0%; } }
.block-container { max-width: 460px; padding: 0 1.2rem 2rem; }
.bubbles { position: fixed; inset: 0; overflow: hidden; pointer-events: none; z-index: 0; }
.bubbles span { position: absolute; bottom: -140px; border-radius: 50%; background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.12); animation: rise linear infinite; }
.bubbles span:nth-child(1) { left: 8%;  width: 46px;  height: 46px;  animation-duration: 19s; animation-delay: 0s; }
.bubbles span:nth-child(2) { left: 24%; width: 90px;  height: 90px;  animation-duration: 26s; animation-delay: 4s; }
.bubbles span:nth-child(3) { left: 46%; width: 30px;  height: 30px;  animation-duration: 17s; animation-delay: 8s; }
.bubbles span:nth-child(4) { left: 63%; width: 70px;  height: 70px;  animation-duration: 23s; animation-delay: 2s; }
.bubbles span:nth-child(5) { left: 80%; width: 40px;  height: 40px;  animation-duration: 20s; animation-delay: 10s; }
.bubbles span:nth-child(6) { left: 92%; width: 110px; height: 110px; animation-duration: 30s; animation-delay: 6s; }
@keyframes rise { 0% { transform: translateY(0) scale(1); opacity: 0; } 10% { opacity: 1; }
    100% { transform: translateY(-120vh) scale(1.4); opacity: 0; } }
.home-hero { position: relative; z-index: 2; text-align: center; color: #fff; padding-top: 15vh; }
.icon-wrap { position: relative; display: inline-block; animation: floatY 4s ease-in-out infinite; }
.icon-wrap::before, .icon-wrap::after { content: ""; position: absolute; inset: -10px; border-radius: 40px;
    border: 2px solid rgba(150,240,185,.5); animation: ring 2.8s ease-out infinite; }
.icon-wrap::after { animation-delay: 1.4s; }
@keyframes ring { 0% { transform: scale(.92); opacity: .85; } 100% { transform: scale(1.4); opacity: 0; } }
.home-icon { position: relative; width: 150px; height: 150px; border-radius: 36px; display: block;
    box-shadow: 0 18px 44px rgba(0,0,0,.45), 0 0 60px rgba(80,220,140,.28); }
.home-title { font-size: clamp(2rem, 9vw, 2.7rem); font-weight: 800; margin: 28px 0 6px; color: #fff;
    letter-spacing: -.5px; text-shadow: 0 2px 14px rgba(0,0,0,.35); animation: fadeUp .7s .15s both; }
.home-th { font-size: 1.08rem; font-weight: 600; margin: 0 0 12px; color: #E3F6E9; animation: fadeUp .7s .3s both; }
.home-desc { font-size: .93rem; line-height: 1.7; color: rgba(255,255,255,.85); margin: 0 auto 30px;
    max-width: 340px; animation: fadeUp .7s .45s both; }
div.stButton { position: relative; z-index: 2; animation: fadeUp .7s .6s both; }
div.stButton > button { min-height: 58px; border-radius: 999px !important; font-family: inherit;
    font-size: 1.15rem !important; font-weight: 800 !important; transition: transform .2s ease, filter .2s ease; }
div.stButton > button * { color: inherit !important; }
div.stButton > button[kind="primary"], button[data-testid="stBaseButton-primary"] { position: relative; overflow: hidden;
    background: linear-gradient(135deg, #2FB574, #168A4F); color: #fff;
    border: 1px solid rgba(255,255,255,.3); animation: btnPulse 2.4s ease-in-out infinite; }
@keyframes btnPulse { 0%, 100% { box-shadow: 0 12px 30px rgba(0,0,0,.35), 0 0 0 0 rgba(80,220,140,.45); }
    50% { box-shadow: 0 12px 30px rgba(0,0,0,.35), 0 0 0 12px rgba(80,220,140,0); } }
div.stButton > button[kind="primary"]::after, button[data-testid="stBaseButton-primary"]::after { content: ""; position: absolute;
    top: 0; left: -120%; width: 55%; height: 100%; background: linear-gradient(100deg, transparent, rgba(255,255,255,.38), transparent);
    animation: shine 3.2s ease-in-out infinite; }
@keyframes shine { 0% { left: -120%; } 60%, 100% { left: 150%; } }
div.stButton > button:hover { transform: translateY(-3px) scale(1.02); filter: brightness(1.08); }
div.stButton > button:active { transform: scale(.97); }
.home-tag { position: relative; z-index: 2; text-align: center; color: rgba(255,255,255,.6); font-size: .78rem;
    margin-top: 34px; letter-spacing: .04em; animation: fadeUp .7s .9s both; }
"""

st.markdown(f"<style>{ui.FONT_IMPORT}{ui.KEYFRAMES}{HOME_CSS}</style>", unsafe_allow_html=True)

st.markdown(
    "<div class='bubbles'><span></span><span></span><span></span><span></span><span></span><span></span></div>"
    "<div class='home-hero'>"
    f"<div class='icon-wrap'>{ui.icon_html('home-icon')}</div>"
    "<h1 class='home-title'>Smart Farm Alert</h1>"
    f"<p class='home-th'>{ui.APP_NAME_TH}</p>"
    "<p class='home-desc'>ติดตามความชื้นในดิน ตั้งเกณฑ์ และสั่งรดน้ำอัตโนมัติ ได้ในหน้าจอเดียว</p>"
    "</div>",
    unsafe_allow_html=True,
)

if st.button("▶  เริ่มใช้งาน", type="primary", use_container_width=True):
    st.switch_page(ui.PAGE_DASHBOARD)

st.markdown(f"<div class='home-tag'>{ui.TAGLINE}</div>", unsafe_allow_html=True)
