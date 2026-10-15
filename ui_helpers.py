"""ตัวช่วยกลางของแอป Smart Farm Alert (ธีม, เมนูข้าง, ไอคอน)
ไฟล์นี้เกี่ยวกับการแสดงผลเท่านั้น ไม่แตะ logic ของ Dashboard"""
import base64
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

# พาธหน้าต่าง ๆ (เทียบกับไฟล์หลัก app.py)
PAGE_HOME = "app.py"
PAGE_DASHBOARD = "pages/2_Dashboard.py"
PAGE_TEAM = "pages/3_Team.py"

APP_NAME_TH = "ระบบแจ้งเตือนความชื้นและรดน้ำอัตโนมัติ"
TAGLINE = "Smart Farming for a Better Tomorrow"

FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800"
    "&family=Noto+Sans+Thai:wght@400;500;600;700&display=swap');"
)

KEYFRAMES = """
@keyframes fadeUp { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: none; } }
@keyframes floatY { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-7px); } }
"""


def get_page_icon():
    """ไอคอนแท็บเบราว์เซอร์ ถ้าไม่มีไฟล์จะใช้อีโมจิ 🌱 แทน"""
    icon_path = ASSETS_DIR / "app_icon.png"
    if icon_path.exists():
        try:
            from PIL import Image  # มากับ streamlit อยู่แล้ว
            return Image.open(icon_path)
        except Exception:
            pass
    return "🌱"


@st.cache_data(show_spinner=False)
def image_data_uri(filename):
    """อ่านรูปจากโฟลเดอร์ assets แล้วแปลงเป็น data URI (ใช้ได้ทั้งในเครื่องและ Streamlit Cloud)
    ถ้าไม่มีไฟล์จะคืนค่า None"""
    path = ASSETS_DIR / filename
    if not path.exists():
        return None
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def icon_html(css_class, small=False):
    uri = image_data_uri("app_icon_sm.png" if small else "app_icon.png") or image_data_uri("app_icon.png")
    if uri:
        return f'<img class="{css_class}" src="{uri}" alt="Smart Farm Alert"/>'
    return '<div style="font-size:3rem">🌱</div>'


def keep_control_state():
    """กันค่า Auto Mode / เกณฑ์ความชื้นถูกรีเซ็ตเมื่อสลับไปหน้า Home/Team แล้วกลับมา
    (Streamlit จะลบค่าของ widget ที่ไม่ได้แสดงในหน้านั้น การกำหนดค่าซ้ำจะทำให้ค่าถูกเก็บไว้)"""
    for key in ("auto_mode", "threshold"):
        if key in st.session_state:
            st.session_state[key] = st.session_state[key]


# ---------- CSS ส่วนกลางสำหรับหน้า Dashboard และคณะผู้จัดทำ (เมนูซ้ายสีเขียวเข้ม) ----------
SHELL_CSS = """
#MainMenu, footer, [data-testid="stMainMenu"], [data-testid="stAppDeployButton"], .stDeployButton,
[data-testid="stToolbarActions"], [data-testid="stStatusWidget"], [data-testid="stDecoration"] { display: none !important; }
header[data-testid="stHeader"] { visibility: visible !important; background: transparent !important; box-shadow: none !important; }
[data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapsedControl"] button {
    background: #183C2B !important; color: #fff !important; border-radius: 12px !important;
}
[data-testid="stExpandSidebarButton"] *, [data-testid="stSidebarCollapsedControl"] button * { color: #fff !important; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #183C2B 0%, #0F2A1D 100%) !important; border-right: none !important; }
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebarCollapseButton"] button, [data-testid="stSidebarCollapseButton"] svg { color: rgba(255,255,255,.85) !important; }
.sb-brand { text-align: center; padding: 6px 6px 18px; border-bottom: 1px solid rgba(255,255,255,.12); margin-bottom: 16px; }
.sb-icon { width: 76px; height: 76px; border-radius: 22px; box-shadow: 0 10px 24px rgba(0,0,0,.38); animation: floatY 4s ease-in-out infinite; }
.sb-name { color: #fff; font-weight: 800; font-size: 1.08rem; margin-top: 12px; }
.sb-th { color: rgba(255,255,255,.66); font-size: .72rem; line-height: 1.45; margin-top: 3px; }
.sb-label { color: rgba(255,255,255,.5); font-size: .7rem; letter-spacing: .1em; font-weight: 700; margin: 4px 6px 10px; }
.menu-active { display: flex; align-items: center; gap: 10px; padding: 12px 14px; border-radius: 14px; margin-bottom: 8px;
    background: linear-gradient(135deg, #2FA46A, #1E7F50); color: #fff; font-weight: 700; font-size: .93rem;
    box-shadow: 0 8px 18px rgba(0,0,0,.28); }
[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] { border-radius: 14px; padding: 12px 14px; margin-bottom: 8px;
    background: rgba(255,255,255,.06); color: rgba(255,255,255,.88) !important; transition: all .2s ease; }
[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]:hover { background: rgba(255,255,255,.16); transform: translateX(5px); }
[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] * { color: inherit !important; font-weight: 600; font-size: .93rem; }
.sb-foot { color: rgba(255,255,255,.42); font-size: .68rem; text-align: center; margin-top: 30px; line-height: 1.6; }
"""


def inject_shell_css():
    st.markdown(f"<style>{FONT_IMPORT}{KEYFRAMES}{SHELL_CSS}</style>", unsafe_allow_html=True)


def _menu_item(icon, label, page, is_active):
    if is_active:
        # หน้าปัจจุบันแสดงเป็นแถบเรืองสีเขียว (ไม่ต้องเป็นลิงก์)
        st.markdown(f"<div class='menu-active'><span>{icon}</span><span>{label}</span></div>", unsafe_allow_html=True)
    else:
        st.page_link(page, label=label, icon=icon)


def render_sidebar(current):
    """เมนูซ้าย 2 รายการ: หน้าหลัก (Dashboard) และ คณะผู้จัดทำโครงการ
    current = "dashboard" หรือ "team" """
    with st.sidebar:
        st.markdown(
            "<div class='sb-brand'>"
            f"{icon_html('sb-icon', small=True)}"
            "<div class='sb-name'>Smart Farm Alert</div>"
            f"<div class='sb-th'>{APP_NAME_TH}</div>"
            "</div>"
            "<div class='sb-label'>เมนู</div>",
            unsafe_allow_html=True,
        )
        _menu_item("🏠", "หน้าหลัก", PAGE_DASHBOARD, current == "dashboard")
        _menu_item("👥", "คณะผู้จัดทำโครงการ", PAGE_TEAM, current == "team")
        st.markdown(f"<div class='sb-foot'>{TAGLINE}</div>", unsafe_allow_html=True)
