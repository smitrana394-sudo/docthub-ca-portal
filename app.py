import streamlit as st
import plotly.graph_objects as go
import base64, pathlib

# ── LOGO (base64 so it works in HTML img tags) ────────────────────────────────
_logo_path = pathlib.Path(__file__).parent / "logo.png"
_LOGO_B64  = base64.b64encode(_logo_path.read_bytes()).decode() if _logo_path.exists() else ""
LOGO_IMG   = f'<img src="data:image/png;base64,{_LOGO_B64}" style="height:28px;width:auto;display:block;">' if _LOGO_B64 else "🩺"
LOGO_LOGIN = f'<img src="data:image/png;base64,{_LOGO_B64}" style="height:44px;width:auto;">' if _LOGO_B64 else "🩺"

st.set_page_config(
    page_title="DOCTHUB CA Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── DOCTHUB BRAND COLORS ──────────────────────────────────────────────────────
# Primary  #1565C0  |  Accent  #00ACC1  |  BG  #F5F9FF  |  Card  #FFFFFF
# Text     #0D1B2A  |  Muted   #546E7A  |  Border  #CFE2F3  |  Success #43A047

DOCTHUB_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

*, html, body, [class*="css"] { font-family:'Inter',sans-serif; }
#MainMenu, footer, header { visibility:hidden; }

/* ── APP BG ── */
.stApp { background:#F5F9FF !important; }

/* ── SIDEBAR — hidden, no colour bleed ── */
[data-testid="stSidebar"] { display:none !important; }
[data-testid="stSidebarCollapsedControl"] { display:none !important; }

/* ── CARD ── */
.dt-card {
    background:#fff;
    border:1.5px solid #CFE2F3;
    border-radius:16px;
    padding:24px;
    box-shadow:0 2px 16px rgba(21,101,192,0.07);
    margin-bottom:16px;
    transition:transform .2s, box-shadow .2s;
}
.dt-card:hover { transform:translateY(-2px); box-shadow:0 8px 28px rgba(21,101,192,0.12); }

/* ── STAT CARD ── */
.stat-card {
    background:#fff;
    border:1.5px solid #CFE2F3;
    border-radius:16px;
    padding:22px 20px;
    text-align:center;
    box-shadow:0 2px 16px rgba(21,101,192,0.07);
    transition:transform .2s, box-shadow .2s;
}
.stat-card:hover { transform:translateY(-3px); box-shadow:0 10px 30px rgba(21,101,192,0.13); }
.stat-num {
    font-size:36px; font-weight:800;
    background:linear-gradient(135deg,#1565C0,#00ACC1);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    line-height:1.1;
}
.stat-label { color:#546E7A; font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:.8px; margin-top:5px; }
.stat-delta { color:#43A047; font-size:12px; font-weight:600; margin-top:4px; }

/* ── PAGE HEADER ── */
.page-hdr { color:#0D1B2A; font-size:26px; font-weight:800; margin-bottom:2px; }
.page-sub { color:#546E7A; font-size:13.5px; margin-bottom:24px; }
.section-hdr { color:#0D1B2A; font-size:17px; font-weight:700; margin-bottom:14px; margin-top:4px; }

/* ── BADGE ── */
.badge { display:inline-block; padding:4px 12px; border-radius:100px; font-size:12px; font-weight:600; }
.badge-blue   { background:#DBEAFE; color:#1D4ED8; }
.badge-teal   { background:#E0F7FA; color:#00838F; }
.badge-green  { background:#DCFCE7; color:#166534; }
.badge-orange { background:#FEF3C7; color:#92400E; }
.badge-red    { background:#FEE2E2; color:#991B1B; }
.badge-purple { background:#EDE9FE; color:#5B21B6; }
.badge-gold   { background:#FEF9C3; color:#854D0E; }

/* ── LB ROW ── */
.lb-row {
    display:flex; align-items:center; gap:14px;
    padding:12px 18px; border-radius:12px; margin-bottom:8px;
    background:#fff; border:1.5px solid #CFE2F3;
    transition:all .2s;
}
.lb-row:hover { background:#F0F7FF; border-color:#1565C0; }
.lb-row.me { background:#EFF6FF; border-color:#1565C0; }
.lb-av {
    width:40px; height:40px; border-radius:50%;
    background:linear-gradient(135deg,#1565C0,#00ACC1);
    color:#fff; display:flex; align-items:center; justify-content:center;
    font-weight:700; font-size:14px; flex-shrink:0;
}

/* ── TASK CARD ── */
.task-card {
    background:#fff; border:1.5px solid #CFE2F3; border-radius:14px;
    padding:18px 20px; margin-bottom:10px; transition:all .2s;
}
.task-card:hover { border-color:#00ACC1; box-shadow:0 4px 16px rgba(0,172,193,0.12); }
.task-title { color:#0D1B2A; font-weight:700; font-size:14.5px; margin-bottom:4px; }
.task-desc  { color:#546E7A; font-size:13px; margin-bottom:12px; }
.pts-chip {
    background:linear-gradient(135deg,#1565C0,#00ACC1);
    color:#fff; padding:3px 10px; border-radius:100px; font-size:12px; font-weight:700;
}

/* ── REWARD CARD ── */
.reward-card {
    background:#fff; border:1.5px solid #CFE2F3; border-radius:16px;
    padding:22px; text-align:center; transition:all .3s; margin-bottom:12px;
}
.reward-card:hover { transform:translateY(-4px); box-shadow:0 12px 32px rgba(21,101,192,0.14); border-color:#1565C0; }
.reward-card.locked { opacity:.55; filter:grayscale(.4); }
.reward-icon { font-size:42px; margin-bottom:10px; }
.reward-name { color:#0D1B2A; font-weight:700; font-size:15px; margin-bottom:4px; }
.reward-pts  { font-size:20px; font-weight:800; color:#1565C0; }

/* ── COUPON CARD ── */
.coupon-card {
    background:#fff; border:2px dashed #00ACC1; border-radius:16px;
    padding:20px 22px; margin-bottom:12px; position:relative; transition:all .2s;
}
.coupon-card:hover { background:#F0FBFC; box-shadow:0 6px 20px rgba(0,172,193,0.12); }
.coupon-code {
    font-family:monospace; font-size:20px; font-weight:800;
    color:#1565C0; background:#EFF6FF; border:1.5px solid #CFE2F3;
    border-radius:8px; padding:8px 16px; display:inline-block; letter-spacing:2px;
    margin:10px 0;
}

/* ── EVENT CARD ── */
.event-card {
    background:#fff; border:1.5px solid #CFE2F3; border-radius:14px;
    padding:18px 20px; margin-bottom:10px;
    border-left:4px solid #1565C0; transition:all .2s;
}
.event-card:hover { box-shadow:0 6px 20px rgba(21,101,192,0.1); border-left-color:#00ACC1; }

/* ── RESOURCE CARD ── */
.resource-card {
    background:#fff; border:1.5px solid #CFE2F3; border-radius:14px;
    padding:18px; text-align:center; margin-bottom:10px; transition:all .2s;
}
.resource-card:hover { border-color:#1565C0; box-shadow:0 6px 20px rgba(21,101,192,0.1); }

/* ── REFERRAL CARD ── */
.ref-card {
    background:#fff; border:1.5px solid #CFE2F3; border-radius:14px;
    padding:14px 18px; margin-bottom:8px; display:flex; align-items:center; gap:14px;
    transition:all .2s;
}
.ref-card:hover { background:#F0F7FF; }

/* ── PROGRESS BAR ── */
.prog-wrap { background:#E3F2FD; border-radius:8px; height:8px; overflow:hidden; margin-top:8px; }
.prog-fill { height:100%; border-radius:8px; background:linear-gradient(90deg,#1565C0,#00ACC1); }

/* ── LOGIN ── */
.login-wrap {
    max-width:420px; margin:0 auto;
    background:#fff; border:1.5px solid #CFE2F3; border-radius:20px;
    padding:44px 40px; box-shadow:0 8px 40px rgba(21,101,192,0.12);
}
.login-logo {
    text-align:center; margin-bottom:28px;
}
.login-logo h1 { color:#1565C0; font-size:28px; font-weight:800; margin:10px 0 4px; }
.login-logo p  { color:#546E7A; font-size:13.5px; }

/* ── INPUTS ── */
.stTextInput input, .stNumberInput input, .stSelectbox select, .stTextArea textarea {
    border:1.5px solid #CFE2F3 !important;
    border-radius:10px !important;
    background:#F5F9FF !important;
    color:#0D1B2A !important;
    font-size:14.5px !important;
}
.stTextInput input:focus, .stSelectbox select:focus {
    border-color:#1565C0 !important;
    box-shadow:0 0 0 3px rgba(21,101,192,0.1) !important;
    background:#fff !important;
}
.stTextInput label, .stSelectbox label, .stNumberInput label, .stTextArea label {
    color:#0D1B2A !important; font-weight:600 !important; font-size:13.5px !important;
}

/* ── BUTTONS ── */
.stButton button {
    background:linear-gradient(135deg,#1565C0,#1976D2) !important;
    color:#fff !important; border:none !important;
    border-radius:10px !important; font-weight:600 !important;
    transition:all .2s !important;
    -webkit-text-fill-color:#fff !important;
}
.stButton button:hover {
    background:linear-gradient(135deg,#0D47A1,#1565C0) !important;
    transform:translateY(-1px) !important;
    box-shadow:0 6px 20px rgba(21,101,192,0.3) !important;
}
.stButton button p, .stButton button span {
    color:#fff !important;
    -webkit-text-fill-color:#fff !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] { background:#EFF6FF !important; border-radius:10px !important; padding:4px !important; }
.stTabs [data-baseweb="tab"] { border-radius:8px !important; font-weight:600 !important; color:#546E7A !important; }
.stTabs [data-baseweb="tab"][aria-selected="true"] { background:#1565C0 !important; color:#fff !important; }

/* ── ALERTS ── */
.stSuccess { background:#F0FDF4 !important; border:1px solid #BBF7D0 !important; color:#166534 !important; border-radius:10px !important; }
.stWarning { background:#FFFBEB !important; border:1px solid #FDE68A !important; color:#92400E !important; border-radius:10px !important; }

/* ── DIVIDER ── */
.dt-divider { border:none; border-top:1.5px solid #CFE2F3; margin:20px 0; }

/* ── SIDEBAR — hide entirely ── */
[data-testid="stSidebar"] { display:none !important; }
[data-testid="stSidebarCollapsedControl"] { display:none !important; }

/* ── HORIZONTAL NAV RADIO ── */
[data-testid="stAppViewContainer"] > section.main > div:first-child { padding-top:70px !important; }
div[data-testid="stRadio"] > div[role="radiogroup"] {
    display:flex !important;
    flex-wrap:nowrap !important;
    gap:4px !important;
    background:#fff !important;
    border-bottom:1.5px solid #CFE2F3 !important;
    padding:8px 12px !important;
    overflow-x:auto !important;
    margin:0 -1rem !important;
}
div[data-testid="stRadio"] > div[role="radiogroup"] label {
    flex-shrink:0 !important;
    padding:7px 14px !important;
    border-radius:9px !important;
    font-size:13px !important;
    font-weight:600 !important;
    color:#546E7A !important;
    background:transparent !important;
    border:1.5px solid transparent !important;
    cursor:pointer !important;
    transition:all .15s !important;
    white-space:nowrap !important;
}
div[data-testid="stRadio"] > div[role="radiogroup"] label:hover {
    background:#EFF6FF !important;
    color:#1565C0 !important;
    border-color:#CFE2F3 !important;
}
div[data-testid="stRadio"] > div[role="radiogroup"] label[data-baseweb="radio"] span:first-child { display:none !important; }
div[data-testid="stRadio"] > div[role="radiogroup"] label[aria-checked="true"] {
    background:#1565C0 !important;
    color:#fff !important;
    border-color:#1565C0 !important;
}
/* ensure emoji in active nav label stay visible */
div[data-testid="stRadio"] > div[role="radiogroup"] label[aria-checked="true"] p,
div[data-testid="stRadio"] > div[role="radiogroup"] label[aria-checked="true"] span {
    color:#fff !important;
    -webkit-text-fill-color:#fff !important;
}
/* inactive labels: dark text so emoji + text are readable */
div[data-testid="stRadio"] > div[role="radiogroup"] label p,
div[data-testid="stRadio"] > div[role="radiogroup"] label span {
    color:#546E7A !important;
    -webkit-text-fill-color:#546E7A !important;
}
/* override gradient text-fill for anything inside nav */
div[data-testid="stRadio"] .stat-num,
div[data-testid="stRadio"] [style*="text-fill"] { -webkit-text-fill-color:unset !important; }

/* ── ACTIVITY ── */
.act-item {
    display:flex; align-items:flex-start; gap:12px;
    padding:12px 0; border-bottom:1px solid #F0F7FF;
}
.act-dot { width:9px; height:9px; border-radius:50%; flex-shrink:0; margin-top:5px; }
.act-text { color:#0D1B2A; font-size:13.5px; flex:1; }
.act-time { color:#546E7A; font-size:12px; white-space:nowrap; }

/* ── TOP NAV BAR ── */
#dt-topbar {
    position:fixed;
    top:0; left:0; right:0;
    height:54px;
    background:#ffffff;
    border-bottom:1.5px solid #CFE2F3;
    box-shadow:0 2px 12px rgba(21,101,192,0.08);
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:0 18px 0 20px;
    z-index:9999;
}
#dt-topbar .tb-logo {
    display:flex; align-items:center; gap:9px;
    font-size:17px; font-weight:800; color:#1565C0;
    text-decoration:none;
}
#dt-topbar .tb-logo-icon {
    width:34px; height:34px;
    background:linear-gradient(135deg,#1565C0,#00ACC1);
    border-radius:9px;
    display:flex; align-items:center; justify-content:center;
    font-size:17px;
}
/* Sign-out button — small ghost style */
button[kind="secondary"] { font-size:12px !important; }
</style>
"""
st.markdown(DOCTHUB_CSS, unsafe_allow_html=True)

# ── DEMO CREDENTIALS ──────────────────────────────────────────────────────────
DEMO_USERS = {
    "smit@docthub.com":   {"password": "docthub123", "name": "Smit Rana",         "college": "AIIMS Kalyani",  "rank": 12, "points": 2450},
    "aarav@docthub.com":  {"password": "docthub123", "name": "Aarav Shah",      "college": "AIIMS Delhi",    "rank": 1,  "points": 5800},
    "riya@docthub.com":   {"password": "docthub123", "name": "Riya Mehta",      "college": "CMC Vellore",    "rank": 2,  "points": 5200},
}

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "page" not in st.session_state:
    st.session_state.page = "🏠  Dashboard"

# ── DATA ──────────────────────────────────────────────────────────────────────
from backend import (
    LEADERBOARD, TASKS, REWARDS, ACTIVITIES,
    POINTS_HISTORY, PERFORMANCE_STATS, BADGES, TIMELINE,
    get_task_summary, get_pending_tasks, can_redeem, progress_pct
)

COUPONS = [
    {"code": "DOCTHUB20", "disc": "20% Off",   "desc": "20% off on DOCTHUB Premium subscription",       "uses": 47,  "limit": 100, "exp": "Jun 30, 2026", "cat": "Premium"},
    {"code": "MEDICA50",  "disc": "₹50 Off",   "desc": "₹50 cashback on first course purchase",          "uses": 82,  "limit": 150, "exp": "May 31, 2026", "cat": "Course"},
    {"code": "CAEXTRA15", "disc": "15% Off",   "desc": "15% off on live webinars for your referrals",    "uses": 28,  "limit": 80,  "exp": "Jul 15, 2026", "cat": "Webinar"},
    {"code": "AIIMS2026", "disc": "Free Trial","desc": "7-day free premium trial for new sign-ups",      "uses": 120, "limit": 200, "exp": "Jun 5, 2026",  "cat": "Trial"},
    {"code": "MEDREF100", "disc": "₹100 Off",  "desc": "₹100 off on annual plan via your referral link", "uses": 15,  "limit": 50,  "exp": "Aug 1, 2026",  "cat": "Annual"},
]

EVENTS = [
    {"title": "National Medical Career Summit",    "date": "Jun 5, 2026",  "time": "10:00 AM", "type": "Webinar",   "pts": 150, "reg": True,  "seats": 500, "speaker": "Dr. Ravi Sharma"},
    {"title": "DOCTHUB Ambassador Orientation",   "date": "May 28, 2026", "time": "4:00 PM",  "type": "Online",    "pts": 100, "reg": True,  "seats": 300, "speaker": "DOCTHUB Team"},
    {"title": "Radiology Career Workshop",         "date": "Jun 12, 2026", "time": "11:00 AM", "type": "Workshop",  "pts": 200, "reg": False, "seats": 150, "speaker": "Dr. Priya Nair"},
    {"title": "AIIMS Kalyani Medical Fest",        "date": "Jun 20, 2026", "time": "9:00 AM",  "type": "Fest",      "pts": 300, "reg": False, "seats": 1000,"speaker": "Multiple Speakers"},
    {"title": "PG Entrance Strategy Masterclass",  "date": "Jul 2, 2026",  "time": "6:00 PM",  "type": "Webinar",   "pts": 120, "reg": False, "seats": 400, "speaker": "Dr. K. Iyer"},
]

RESOURCES = [
    {"name": "CA Starter Kit",          "type": "ZIP",  "size": "8.4 MB", "icon": "📦", "desc": "Banners, posters & scripts to kickstart promotion",   "cat": "Kit",     "downloads": 234},
    {"name": "Instagram Story Pack",    "type": "ZIP",  "size": "5.2 MB", "icon": "📸", "desc": "Ready-made story templates for DOCTHUB campaigns",     "cat": "Social",  "downloads": 412},
    {"name": "LinkedIn Post Templates", "type": "DOCX", "size": "1.1 MB", "icon": "📝", "desc": "Professional post templates for LinkedIn promotion",    "cat": "Social",  "downloads": 189},
    {"name": "CA Handbook 2026",        "type": "PDF",  "size": "3.7 MB", "icon": "📖", "desc": "Full guide to policies, rewards & task guidelines",     "cat": "Guide",   "downloads": 578},
    {"name": "Pitch Script – Batch",    "type": "PDF",  "size": "0.9 MB", "icon": "🎙️", "desc": "Word-for-word pitch to use in class/college groups",    "cat": "Script",  "downloads": 321},
    {"name": "Referral Tracking Sheet", "type": "XLSX", "size": "0.4 MB", "icon": "📊", "desc": "Excel sheet to track referrals, status & earnings",     "cat": "Tool",    "downloads": 267},
]

REFERRALS = [
    {"name": "Rohit Sharma",   "email": "rohit@aiims.ac.in",   "date": "May 18", "status": "Verified",  "pts": 50},
    {"name": "Priti Gupta",    "email": "priti@aiims.ac.in",   "date": "May 16", "status": "Verified",  "pts": 50},
    {"name": "Manish Yadav",   "email": "manish@kmc.ac.in",    "date": "May 15", "status": "Pending",   "pts": 0},
    {"name": "Simran Kaur",    "email": "simran@pg.ac.in",     "date": "May 13", "status": "Verified",  "pts": 50},
    {"name": "Aditya Roy",     "email": "aditya@jipmer.ac.in", "date": "May 11", "status": "Verified",  "pts": 50},
    {"name": "Kavya Reddy",    "email": "kavya@nims.ac.in",    "date": "May 9",  "status": "Pending",   "pts": 0},
    {"name": "Deepak Mishra",  "email": "deepak@bhu.ac.in",    "date": "May 6",  "status": "Rejected",  "pts": 0},
    {"name": "Ankita Das",     "email": "ankita@ms.ac.in",     "date": "May 3",  "status": "Verified",  "pts": 50},
]

# ── LOGIN PAGE ────────────────────────────────────────────────────────────────
def login_page():
    col_l, col_c, col_r = st.columns([1, 1.2, 1])
    with col_c:
        st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='text-align:center;margin-bottom:32px;'>
            <div style='margin:0 auto 18px;'>{LOGO_LOGIN}</div>
            <p style='color:#546E7A;font-size:14px;margin:6px 0 0;font-weight:600;'>Campus Ambassador Portal</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='dt-card'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#0D1B2A;font-weight:700;font-size:18px;margin-bottom:20px;'>Sign In to Your Account</p>", unsafe_allow_html=True)

        email = st.text_input("Email Address", placeholder="your@email.com")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        col_btn, col_forgot = st.columns([1, 1])
        with col_btn:
            login_btn = st.button("Sign In →", width="stretch")
        with col_forgot:
            st.markdown("<p style='color:#1565C0;font-size:13px;text-align:right;margin-top:10px;cursor:pointer;'>Forgot password?</p>", unsafe_allow_html=True)

        if login_btn:
            if email in DEMO_USERS and DEMO_USERS[email]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.rerun()
            else:
                st.error("❌ Invalid email or password. Try the demo credentials below.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style='background:#EFF6FF;border:1.5px solid #CFE2F3;border-radius:12px;padding:14px 16px;margin-top:16px;'>
            <p style='color:#1565C0;font-weight:700;font-size:13px;margin-bottom:8px;'>🔑 Demo Credentials</p>
            <p style='color:#546E7A;font-size:12.5px;margin:3px 0;'>👤 Smit Rana &nbsp;·&nbsp; 📧 smit@docthub.com &nbsp;|&nbsp; 🔒 docthub123</p>
            <p style='color:#546E7A;font-size:12.5px;margin:3px 0;'>👤 Aarav Shah &nbsp;·&nbsp; 📧 aarav@docthub.com &nbsp;|&nbsp; 🔒 docthub123</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <p style='text-align:center;color:#546E7A;font-size:12.5px;margin-top:20px;'>
            Not a Campus Ambassador yet?
            <span style='color:#1565C0;font-weight:600;cursor:pointer;'> Apply Now →</span>
        </p>
        """, unsafe_allow_html=True)

# ── MAIN APP ─────────────────────────────────────────────────────────────────
def main_app():
    u = DEMO_USERS[st.session_state.user_email]
    name     = u["name"]
    college  = u["college"]
    points   = u["points"]
    rank     = u["rank"]
    initials = "".join(w[0] for w in name.split()[:2])

    # ── TOP BAR ──────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div id="dt-topbar">
        <div class="tb-logo">
            {LOGO_IMG}
        </div>
        <div style='display:flex;align-items:center;gap:14px;margin-left:auto;'>
            <div style='text-align:right;'>
                <div style='color:#0D1B2A;font-size:13px;font-weight:700;'>{name}</div>
                <div style='color:#546E7A;font-size:11px;'>{college} &nbsp;·&nbsp; ⭐ {points:,} pts</div>
            </div>
            <div style='width:36px;height:36px;background:linear-gradient(135deg,#1565C0,#00ACC1);
                 border-radius:50%;display:flex;align-items:center;justify-content:center;
                 color:#fff;font-weight:800;font-size:14px;flex-shrink:0;'>{initials}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KEEP-ALIVE (prevents session timeout during presentations) ───────────
    st.markdown("""
    <script>
    (function(){
        if(window._dtKeepalive) return;
        window._dtKeepalive = setInterval(function(){
            // Simulate user presence to keep Streamlit WebSocket alive
            document.dispatchEvent(new MouseEvent('mousemove',{bubbles:true,clientX:1,clientY:1}));
            document.dispatchEvent(new Event('focus',{bubbles:true}));
        }, 25000);
    })();
    </script>
    """, unsafe_allow_html=True)

    # ── NAVIGATION (native horizontal radio — always works) ───────────────────
    NAV_PAGES = [
        "🏠 Dashboard", "🏆 Leaderboard", "✅ Tasks",
        "🎟️ Coupons",  "📅 Events",      "📚 Resources",
        "👥 Referrals", "🎁 Redeem",      "👤 Profile",
    ]
    PAGE_MAP = {
        "🏠 Dashboard":   "🏠  Dashboard",
        "🏆 Leaderboard": "🏆  Leaderboard",
        "✅ Tasks":       "✅  My Tasks",
        "🎟️ Coupons":   "🎟️  Coupons",
        "📅 Events":      "📅  Events",
        "📚 Resources":   "📚  Resources",
        "👥 Referrals":   "👥  Referrals",
        "🎁 Redeem":      "🎁  Redeem",
        "👤 Profile":     "👤  Profile",
    }
    PAGE_MAP_REV = {v: k for k, v in PAGE_MAP.items()}
    current_nav = PAGE_MAP_REV.get(st.session_state.page, "🏠 Dashboard")

    selected = st.radio(
        "nav",
        NAV_PAGES,
        index=NAV_PAGES.index(current_nav),
        horizontal=True,
        label_visibility="hidden",
        key="main_nav",
    )
    if PAGE_MAP[selected] != st.session_state.page:
        st.session_state.page = PAGE_MAP[selected]
        st.rerun()

    page = st.session_state.page

    # Sign out
    so_col1, so_col2 = st.columns([9, 1])
    with so_col2:
        if st.button("🚪 Sign Out", key="signout_btn"):
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            st.session_state.page = "🏠  Dashboard"
            st.rerun()

    # ── DASHBOARD ────────────────────────────────────────────────────────────
    if page == "🏠  Dashboard":
        first = name.split()[0]
        st.markdown(f"<div class='page-hdr'>👋 Welcome back, {first}!</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='page-sub'>Here's your performance overview · {college}</div>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        cards = [
            ("⭐", f"{points:,}", "Total Points", "▲ +350 this week"),
            ("🏅", f"#{rank}", "National Rank", "▲ Improved from #14"),
            ("✅", "28/35", "Tasks Done", "4 pending"),
            ("👥", "40", "Referrals", "▲ +8 this month"),
        ]
        for col, (icon, num, label, delta) in zip([c1, c2, c3, c4], cards):
            with col:
                st.markdown(f"""
                <div class='stat-card'>
                    <div style='font-size:26px;margin-bottom:8px;'>{icon}</div>
                    <div class='stat-num'>{num}</div>
                    <div class='stat-label'>{label}</div>
                    <div class='stat-delta'>{delta}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
        col_l, col_r = st.columns([3, 2])

        with col_l:
            st.markdown("<div class='section-hdr'>📈 Points Growth</div>", unsafe_allow_html=True)
            fig = go.Figure()
            months = POINTS_HISTORY["months"]
            pts_data = POINTS_HISTORY["points"]
            fig.add_trace(go.Scatter(
                x=months, y=pts_data, fill='tozeroy',
                fillcolor='rgba(21,101,192,0.08)',
                line=dict(color='#1565C0', width=3),
                mode='lines+markers',
                marker=dict(size=9, color='#00ACC1', line=dict(color='white', width=2)),
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=10, b=0), height=210,
                xaxis=dict(showgrid=False, color='#546E7A', tickfont=dict(size=12)),
                yaxis=dict(showgrid=True, gridcolor='#EDF2F7', color='#546E7A', tickfont=dict(size=11)),
                showlegend=False,
            )
            st.plotly_chart(fig, width="stretch", config={'displayModeBar': False})

            st.markdown("<div class='section-hdr'>⚡ Recent Activity</div>", unsafe_allow_html=True)
            st.markdown("<div class='dt-card' style='padding:16px 20px;'>", unsafe_allow_html=True)
            for a in ACTIVITIES:
                st.markdown(f"""
                <div class='act-item'>
                    <div class='act-dot' style='background:{a["color"]};'></div>
                    <div class='act-text'>{a["text"]}</div>
                    <div class='act-time'>{a["time"]}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_r:
            st.markdown("<div class='section-hdr'>📊 Task Breakdown</div>", unsafe_allow_html=True)
            ts = get_task_summary(TASKS)
            fig2 = go.Figure(go.Pie(
                labels=["Completed", "Pending", "New"],
                values=[ts["completed"], ts["pending"], ts["new"]],
                hole=0.62,
                marker=dict(colors=["#1565C0", "#00ACC1", "#90CAF9"],
                            line=dict(color='white', width=2)),
                textfont=dict(color='#0D1B2A', size=12),
            ))
            fig2.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=10, b=0), height=210,
                legend=dict(font=dict(color='#546E7A', size=12), bgcolor='rgba(0,0,0,0)',
                            orientation='h', x=0.5, xanchor='center', y=-0.05),
                annotations=[dict(text=f'<b>{ts["completed"]}</b><br><span style="font-size:11px">done</span>',
                                  x=0.5, y=0.5, font_size=18, showarrow=False, font_color='#1565C0')]
            )
            st.plotly_chart(fig2, width="stretch", config={'displayModeBar': False})

            st.markdown("<div class='section-hdr'>🏆 Top 3 This Week</div>", unsafe_allow_html=True)
            medals = ["🥇","🥈","🥉"]
            for i, entry in enumerate(LEADERBOARD[:3]):
                st.markdown(f"""
                <div class='lb-row' style='padding:10px 14px;'>
                    <div style='font-size:20px;width:32px;text-align:center;'>{medals[i]}</div>
                    <div style='flex:1;'>
                        <div style='color:#0D1B2A;font-weight:600;font-size:13.5px;'>{entry["name"]}</div>
                        <div style='color:#546E7A;font-size:11.5px;'>{entry["college"]}</div>
                    </div>
                    <div style='color:#1565C0;font-weight:700;font-size:13.5px;'>{entry["points"]:,}</div>
                </div>""", unsafe_allow_html=True)

    # ── LEADERBOARD ──────────────────────────────────────────────────────────
    elif page == "🏆  Leaderboard":
        st.markdown("<div class='page-hdr'>🏆 National Leaderboard</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-sub'>Top campus ambassadors across India</div>", unsafe_allow_html=True)

        p1, p2, p3 = st.columns(3)
        podium = [(LEADERBOARD[1], "2nd", "#C0C0C0", "🥈"),
                  (LEADERBOARD[0], "1st", "#FFD700", "🥇"),
                  (LEADERBOARD[2], "3rd", "#CD7F32", "🥉")]
        for col, (e, pos, clr, medal) in zip([p1, p2, p3], podium):
            with col:
                st.markdown(f"""
                <div class='dt-card' style='text-align:center;border-top:4px solid {clr};'>
                    <div style='font-size:38px;margin-bottom:8px;'>{medal}</div>
                    <div style='color:#0D1B2A;font-weight:700;font-size:15px;'>{e["name"]}</div>
                    <div style='color:#546E7A;font-size:12px;margin:3px 0 8px;'>{e["college"]}</div>
                    <div style='color:#1565C0;font-size:20px;font-weight:800;'>{e["points"]:,}</div>
                    <div style='color:#546E7A;font-size:12px;'>{pos} Place</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

        # search bar
        search = st.text_input("🔍 Search ambassador", placeholder="Type a name or college...")
        filtered = [e for e in LEADERBOARD if not search or search.lower() in e["name"].lower() or search.lower() in e["college"].lower()]

        for entry in filtered:
            is_me = entry["name"] == name
            row_class = "lb-row me" if is_me else "lb-row"
            rank_disp = {"1":"🥇","2":"🥈","3":"🥉"}.get(str(entry["rank"]), f"#{entry['rank']}")
            you_tag = "<span class='badge badge-teal' style='margin-left:8px;font-size:11px;'>You</span>" if is_me else ""
            st.markdown(f"""
            <div class='{row_class}'>
                <div style='width:38px;text-align:center;font-size:{"20" if entry["rank"]<=3 else "15"}px;
                     font-weight:800;color:#1565C0;'>{rank_disp}</div>
                <div class='lb-av'>{entry["name"][0]}</div>
                <div style='flex:1;'>
                    <div style='color:#0D1B2A;font-weight:600;font-size:14px;'>
                        {entry["name"]}{you_tag}
                    </div>
                    <div style='color:#546E7A;font-size:12px;'>{entry["college"]}</div>
                </div>
                <div style='color:#1565C0;font-weight:700;font-size:15px;'>{entry["points"]:,} pts</div>
            </div>""", unsafe_allow_html=True)

    # ── TASKS ────────────────────────────────────────────────────────────────
    elif page == "✅  My Tasks":
        st.markdown("<div class='page-hdr'>✅ My Tasks</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-sub'>Complete tasks to earn points and climb the leaderboard</div>", unsafe_allow_html=True)

        tab_all, tab_pen, tab_add = st.tabs(["📋 All Tasks", "⏳ Pending", "➕ Submit Task"])

        with tab_all:
            for t in TASKS:
                status_badge = {
                    "Completed": "<span class='badge badge-green'>✓ Completed</span>",
                    "Pending":   "<span class='badge badge-orange'>⏳ Pending</span>",
                    "New":       "<span class='badge badge-blue'>🆕 New</span>",
                }[t["status"]]
                dl = t["deadline"]
                dl_html = "" if dl == "Done" else f"📅 {dl}"
                st.markdown(f"""
                <div class='task-card'>
                    <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                        <div class='task-title'>{t["task"]}</div>
                        <span class='pts-chip'>+{t["pts"]} pts</span>
                    </div>
                    <div class='task-desc'>{t["desc"]}</div>
                    <div style='display:flex;align-items:center;justify-content:space-between;'>
                        {status_badge}
                        <span style='color:#546E7A;font-size:12px;'>{dl_html}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

        with tab_pen:
            pending = get_pending_tasks(TASKS)
            for t in pending:
                badge = "<span class='badge badge-orange'>⏳ Pending</span>" if t["status"]=="Pending" else "<span class='badge badge-blue'>🆕 New</span>"
                st.markdown(f"""
                <div class='task-card' style='border-left:4px solid #00ACC1;'>
                    <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                        <div class='task-title'>{t["task"]}</div>
                        <span class='pts-chip'>+{t["pts"]} pts</span>
                    </div>
                    <div class='task-desc'>{t["desc"]}</div>
                    <div style='display:flex;align-items:center;justify-content:space-between;'>
                        {badge}
                        <span style='color:#546E7A;font-size:12px;'>📅 Due: {t["deadline"]}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

        with tab_add:
            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
            t_name = st.text_input("Task Name", placeholder="e.g. Facebook Story Campaign")
            t_desc = st.text_area("Description", placeholder="Describe what you did or plan to do...", height=90)
            ca, cb = st.columns(2)
            with ca:
                t_pts = st.number_input("Points (estimated)", min_value=0, value=50, step=25)
            with cb:
                t_dl = st.text_input("Deadline / Date Done", placeholder="e.g. Jun 15")
            proof = st.text_input("Proof Link (optional)", placeholder="Screenshot, post URL, etc.")
            if st.button("📤 Submit for Review", width="stretch"):
                if t_name:
                    st.success(f"✅ '{t_name}' submitted! Our team will verify within 48 hours.")
                else:
                    st.warning("Please enter a task name.")

    # ── COUPONS ──────────────────────────────────────────────────────────────
    elif page == "🎟️  Coupons":
        st.markdown("<div class='page-hdr'>🎟️ Ambassador Coupons</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-sub'>Share these exclusive codes with students to earn bonus points</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style='background:linear-gradient(135deg,#1565C0,#00ACC1);border-radius:16px;
             padding:20px 24px;margin-bottom:24px;color:#fff;display:flex;
             align-items:center;gap:16px;'>
            <div style='font-size:36px;'>💡</div>
            <div>
                <div style='font-weight:700;font-size:16px;margin-bottom:4px;'>How it works</div>
                <div style='opacity:.85;font-size:13.5px;'>Share these codes with your college peers.
                For every successful use, you earn <strong>+25 bonus points</strong> on top of your referral points!</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        cat_filter = st.selectbox("Filter by Category", ["All", "Premium", "Course", "Webinar", "Trial", "Annual"])
        filtered = COUPONS if cat_filter == "All" else [c for c in COUPONS if c["cat"] == cat_filter]

        for cp in filtered:
            used_pct = int(cp["uses"] / cp["limit"] * 100)
            cat_colors = {"Premium":"badge-blue","Course":"badge-teal","Webinar":"badge-purple","Trial":"badge-green","Annual":"badge-orange"}
            cp_cat = cp["cat"]
            cp_badge_cls = cat_colors.get(cp_cat, "badge-blue")
            badge = f"<span class='badge {cp_badge_cls}'>{cp_cat}</span>"
            st.markdown(f"""
            <div class='coupon-card'>
                <div style='display:flex;align-items:flex-start;justify-content:space-between;'>
                    <div>
                        <div style='color:#0D1B2A;font-weight:700;font-size:15px;margin-bottom:4px;'>{cp["disc"]}</div>
                        <div style='color:#546E7A;font-size:13px;margin-bottom:10px;'>{cp["desc"]}</div>
                        <div class='coupon-code'>{cp["code"]}</div>
                    </div>
                    <div style='text-align:right;flex-shrink:0;margin-left:16px;'>
                        {badge}
                        <div style='color:#546E7A;font-size:12px;margin-top:8px;'>Expires</div>
                        <div style='color:#0D1B2A;font-weight:600;font-size:12.5px;'>{cp["exp"]}</div>
                    </div>
                </div>
                <div style='margin-top:12px;'>
                    <div style='display:flex;justify-content:space-between;margin-bottom:5px;'>
                        <span style='color:#546E7A;font-size:12px;'>{cp["uses"]}/{cp["limit"]} uses</span>
                        <span style='color:#1565C0;font-size:12px;font-weight:600;'>{used_pct}%</span>
                    </div>
                    <div class='prog-wrap' style='height:6px;'>
                        <div class='prog-fill' style='width:{used_pct}%;'></div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"📋 Copy {cp['code']}", key=f"copy_{cp['code']}"):
                st.success(f"✅ Code **{cp['code']}** copied! Share it with your peers.")

    # ── EVENTS ───────────────────────────────────────────────────────────────
    elif page == "📅  Events":
        st.markdown("<div class='page-hdr'>📅 Events & Webinars</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-sub'>Attend events to earn points and grow your network</div>", unsafe_allow_html=True)

        type_filter = st.selectbox("Filter by Type", ["All", "Webinar", "Online", "Workshop", "Fest"])
        filtered_ev = EVENTS if type_filter == "All" else [e for e in EVENTS if e["type"] == type_filter]

        for ev in filtered_ev:
            type_color = {"Webinar":"badge-blue","Online":"badge-teal","Workshop":"badge-purple","Fest":"badge-orange"}
            ev_type = ev["type"]
            ev_badge_cls = type_color.get(ev_type, "badge-blue")
            badge = f"<span class='badge {ev_badge_cls}'>{ev_type}</span>"
            reg_label = "✅ Registered" if ev["reg"] else "Register Now"
            reg_style = "background:#DCFCE7;color:#166534;border:1.5px solid #BBF7D0;" if ev["reg"] else "background:linear-gradient(135deg,#1565C0,#1976D2);color:#fff;"
            st.markdown(f"""
            <div class='event-card'>
                <div style='display:flex;align-items:flex-start;justify-content:space-between;gap:16px;'>
                    <div style='flex:1;'>
                        <div style='display:flex;align-items:center;gap:8px;margin-bottom:6px;'>
                            {badge}
                            <span style='color:#546E7A;font-size:12px;'>+{ev["pts"]} pts on attendance</span>
                        </div>
                        <div style='color:#0D1B2A;font-weight:700;font-size:15px;margin-bottom:4px;'>{ev["title"]}</div>
                        <div style='color:#546E7A;font-size:13px;'>🎙️ {ev["speaker"]}</div>
                        <div style='color:#546E7A;font-size:12.5px;margin-top:6px;'>
                            📅 {ev["date"]} &nbsp;·&nbsp; 🕐 {ev["time"]} &nbsp;·&nbsp; 💺 {ev["seats"]:,} seats
                        </div>
                    </div>
                    <div style='flex-shrink:0;'>
                        <div style='padding:8px 18px;border-radius:8px;font-weight:600;font-size:13px;
                             text-align:center;{reg_style}'>{reg_label}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        if st.button("📢 Suggest an Event", width="content"):
            st.info("📧 Email your event suggestion to ca@docthub.com with subject 'Event Suggestion'.")

    # ── RESOURCES ────────────────────────────────────────────────────────────
    elif page == "📚  Resources":
        st.markdown("<div class='page-hdr'>📚 Resource Library</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-sub'>Download official assets to supercharge your promotion</div>", unsafe_allow_html=True)

        cat_r = st.selectbox("Filter by Category", ["All", "Kit", "Social", "Guide", "Script", "Tool"])
        filtered_r = RESOURCES if cat_r == "All" else [r for r in RESOURCES if r["cat"] == cat_r]

        r_cols = st.columns(3)
        for i, r in enumerate(filtered_r):
            with r_cols[i % 3]:
                type_color = {"ZIP":"badge-orange","PDF":"badge-red","DOCX":"badge-blue","XLSX":"badge-green"}
                r_type = r["type"]
                r_badge_cls = type_color.get(r_type, "badge-blue")
                type_badge = f"<span class='badge {r_badge_cls}'>{r_type}</span>"
                st.markdown(f"""
                <div class='resource-card'>
                    <div style='font-size:40px;margin-bottom:10px;'>{r["icon"]}</div>
                    {type_badge}
                    <div style='color:#0D1B2A;font-weight:700;font-size:14.5px;margin:10px 0 4px;'>{r["name"]}</div>
                    <div style='color:#546E7A;font-size:12.5px;margin-bottom:10px;line-height:1.5;'>{r["desc"]}</div>
                    <div style='color:#546E7A;font-size:11.5px;margin-bottom:14px;'>
                        📦 {r["size"]} &nbsp;·&nbsp; ⬇️ {r["downloads"]} downloads
                    </div>
                </div>""", unsafe_allow_html=True)
                if st.button(f"⬇️ Download", key=f"dl_{i}", width="stretch"):
                    st.success(f"✅ '{r['name']}' download started!")

    # ── REFERRALS ────────────────────────────────────────────────────────────
    elif page == "👥  Referrals":
        st.markdown("<div class='page-hdr'>👥 Referral Tracker</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-sub'>Track every referral and earn points for verified sign-ups</div>", unsafe_allow_html=True)

        verified = sum(1 for r in REFERRALS if r["status"] == "Verified")
        pending  = sum(1 for r in REFERRALS if r["status"] == "Pending")
        total_pts = sum(r["pts"] for r in REFERRALS)

        ca, cb, cc = st.columns(3)
        for col, (icon, num, label) in zip([ca, cb, cc], [
            ("✅", verified, "Verified"),
            ("⏳", pending,  "Pending Review"),
            ("⭐", f"{total_pts}", "Points Earned"),
        ]):
            with col:
                st.markdown(f"""
                <div class='stat-card'>
                    <div style='font-size:24px;margin-bottom:6px;'>{icon}</div>
                    <div class='stat-num'>{num}</div>
                    <div class='stat-label'>{label}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

        tab_list, tab_add = st.tabs(["📋 Referral List", "➕ Add Referral"])

        with tab_list:
            status_filter = st.selectbox("Filter by Status", ["All", "Verified", "Pending", "Rejected"])
            filtered_refs = REFERRALS if status_filter == "All" else [r for r in REFERRALS if r["status"] == status_filter]

            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
            for r in filtered_refs:
                s_badge = {
                    "Verified": "<span class='badge badge-green'>✓ Verified</span>",
                    "Pending":  "<span class='badge badge-orange'>⏳ Pending</span>",
                    "Rejected": "<span class='badge badge-red'>✗ Rejected</span>",
                }[r["status"]]
                pts_disp = f"+{r['pts']} pts" if r["pts"] > 0 else "—"
                st.markdown(f"""
                <div class='ref-card'>
                    <div style='width:38px;height:38px;background:#EFF6FF;border-radius:50%;
                         display:flex;align-items:center;justify-content:center;
                         font-weight:700;color:#1565C0;font-size:14px;flex-shrink:0;'>
                        {r["name"][0]}
                    </div>
                    <div style='flex:1;'>
                        <div style='color:#0D1B2A;font-weight:600;font-size:14px;'>{r["name"]}</div>
                        <div style='color:#546E7A;font-size:12px;'>{r["email"]}</div>
                    </div>
                    <div style='text-align:right;'>
                        {s_badge}
                        <div style='color:#546E7A;font-size:11.5px;margin-top:4px;'>📅 {r["date"]}</div>
                    </div>
                    <div style='color:#1565C0;font-weight:700;font-size:14px;min-width:60px;text-align:right;'>
                        {pts_disp}
                    </div>
                </div>""", unsafe_allow_html=True)

        with tab_add:
            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
            ref_name  = st.text_input("Referral Name", placeholder="Full name of the person you referred")
            ref_email = st.text_input("Referral Email", placeholder="their@email.com")
            ref_col   = st.text_input("Their College", placeholder="College/Institution name")
            ref_note  = st.text_area("Note (optional)", placeholder="How did you refer them?", height=80)
            if st.button("📤 Submit Referral", width="stretch"):
                if ref_name and ref_email:
                    st.success(f"✅ Referral for **{ref_name}** submitted! You'll earn 50 pts once they sign up and verify.")
                else:
                    st.warning("Please enter name and email.")

    # ── REDEEM ───────────────────────────────────────────────────────────────
    elif page == "🎁  Redeem":
        st.markdown("<div class='page-hdr'>🎁 Redeem Rewards</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='page-sub'>Your balance: <strong style='color:#1565C0;'>{points:,} pts</strong> · Redeem for exclusive perks</div>", unsafe_allow_html=True)

        r_cols = st.columns(3)
        for i, r in enumerate(REWARDS):
            with r_cols[i % 3]:
                can = can_redeem(points, r["pts"])
                pct = progress_pct(points, r["pts"])
                st.markdown(f"""
                <div class='reward-card {"" if can else "locked"}'>
                    <div class='reward-icon'>{r["icon"]}</div>
                    <div class='reward-name'>{r["name"]}</div>
                    <div class='reward-pts'>{r["pts"]:,} pts</div>
                    <div style='color:#546E7A;font-size:12.5px;margin:6px 0 14px;'>{r["desc"]}</div>
                    <div class='prog-wrap' style='margin-bottom:8px;'>
                        <div class='prog-fill' style='width:{pct}%;
                             background:{"linear-gradient(90deg,#1565C0,#00ACC1)" if can else "linear-gradient(90deg,#90CAF9,#4DD0E1)"};'></div>
                    </div>
                    <div style='color:#546E7A;font-size:11px;margin-bottom:14px;'>{pct}% of goal</div>
                </div>""", unsafe_allow_html=True)
                if can:
                    if st.button(f"✅ Redeem", key=f"rd_{i}", width="stretch"):
                        st.success(f"🎉 Redemption request for **{r['name']}** sent! Expect delivery in 3–5 business days.")
                else:
                    st.markdown(f"""
                    <div style='text-align:center;color:#546E7A;font-size:12px;
                         background:#F5F9FF;border-radius:8px;padding:7px;'>
                        🔒 Need {r["pts"]-points:,} more pts
                    </div>""", unsafe_allow_html=True)

    # ── PROFILE ──────────────────────────────────────────────────────────────
    elif page == "👤  Profile":
        st.markdown("<div class='page-hdr'>👤 My Profile</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-sub'>Your ambassador identity and achievements</div>", unsafe_allow_html=True)

        col_p, col_s = st.columns([2, 3])

        with col_p:
            st.markdown(f"""
            <div class='dt-card' style='text-align:center;'>
                <div style='width:80px;height:80px;background:linear-gradient(135deg,#1565C0,#00ACC1);
                     border-radius:50%;display:flex;align-items:center;justify-content:center;
                     font-size:28px;font-weight:800;color:#fff;margin:0 auto 14px;
                     box-shadow:0 8px 24px rgba(21,101,192,0.3);'>{initials}</div>
                <div style='color:#0D1B2A;font-size:20px;font-weight:800;margin-bottom:3px;'>{name}</div>
                <div style='color:#546E7A;font-size:13px;margin-bottom:4px;'>Campus Ambassador · DOCTHUB</div>
                <div style='color:#546E7A;font-size:13px;margin-bottom:14px;'>🏫 {college}</div>
                <span style='background:#FEF9C3;color:#854D0E;padding:5px 16px;
                      border-radius:100px;font-size:12.5px;font-weight:700;'>⭐ Gold Ambassador</span>
                <div style='margin-top:18px;padding-top:18px;border-top:1.5px solid #CFE2F3;'>
                    <div style='display:flex;justify-content:space-around;'>
                        <div style='text-align:center;'>
                            <div style='color:#1565C0;font-weight:800;font-size:18px;'>{points:,}</div>
                            <div style='color:#546E7A;font-size:11px;'>Points</div>
                        </div>
                        <div style='text-align:center;'>
                            <div style='color:#1565C0;font-weight:800;font-size:18px;'>#{rank}</div>
                            <div style='color:#546E7A;font-size:11px;'>Rank</div>
                        </div>
                        <div style='color:#CFE2F3;font-size:20px;'>|</div>
                        <div style='text-align:center;'>
                            <div style='color:#1565C0;font-weight:800;font-size:18px;'>40</div>
                            <div style='color:#546E7A;font-size:11px;'>Referrals</div>
                        </div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

            st.markdown("<div class='section-hdr' style='margin-top:8px;'>🎖️ Badges</div>", unsafe_allow_html=True)
            badges_html = "<div class='dt-card' style='display:flex;flex-wrap:wrap;gap:7px;'>"
            for b in BADGES:
                b_bg = b["bg"]; b_clr = b["color"]; b_brd = b["border"]; b_lbl = b["label"]
                badges_html += f"<span class='badge' style='background:{b_bg};color:{b_clr};border:1px solid {b_brd};padding:5px 13px;'>{b_lbl}</span>"
            badges_html += "</div>"
            st.markdown(badges_html, unsafe_allow_html=True)

        with col_s:
            st.markdown("<div class='section-hdr'>📊 Performance Radar</div>", unsafe_allow_html=True)
            cats = PERFORMANCE_STATS["categories"]
            vals = PERFORMANCE_STATS["values"]
            fig = go.Figure(go.Scatterpolar(
                r=vals + [vals[0]], theta=cats + [cats[0]],
                fill='toself',
                fillcolor='rgba(21,101,192,0.1)',
                line=dict(color='#1565C0', width=2),
                marker=dict(color='#00ACC1', size=8),
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                polar=dict(
                    bgcolor='rgba(0,0,0,0)',
                    radialaxis=dict(visible=True, range=[0,100], gridcolor='#E3F2FD', color='#546E7A'),
                    angularaxis=dict(gridcolor='#E3F2FD', color='#0D1B2A')
                ),
                margin=dict(l=40, r=40, t=20, b=20), height=250, showlegend=False,
            )
            st.plotly_chart(fig, width="stretch", config={'displayModeBar': False})

            st.markdown("<div class='section-hdr' style='margin-top:4px;'>📅 Activity Timeline</div>", unsafe_allow_html=True)
            for month, event, color in TIMELINE:
                st.markdown(f"""
                <div style='display:flex;gap:12px;margin-bottom:12px;align-items:flex-start;'>
                    <div style='width:10px;height:10px;border-radius:50%;background:{color};
                         margin-top:4px;flex-shrink:0;'></div>
                    <div>
                        <div style='color:#0D1B2A;font-size:13.5px;font-weight:500;'>{event}</div>
                        <div style='color:#546E7A;font-size:12px;'>{month}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

# ── ROUTER ────────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
