"""Skandia brand — paleta, CSS global, componentes visuales."""

GREEN        = "#00D261"
GREEN_DARK   = "#00A84F"
GREEN_LIGHT  = "#E8F5E9"
GRAY_DARK    = "#2D2926"
BLUE_HEADER  = "#003087"
RED_ALERT    = "#D32F2F"
RED_BG       = "#FFEBEE"
YELLOW_WARN  = "#FFF8E1"
YELLOW_BDR   = "#F9A825"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #F0EEE9 0%, #EDF7F1 100%) !important;
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
}
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e8e8e8 !important;
    box-shadow: 2px 0 12px rgba(0,0,0,0.06) !important;
}
[data-testid="stSidebar"] * { color: #2D2926 !important; }
.block-container { padding-top: 0.25rem !important; padding-bottom: 2rem !important; }
#MainMenu, footer, header { visibility: hidden; }

/* ── Cards ── */
.sk-card {
    background: #fff; border-radius: 16px; padding: 20px 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07); margin-bottom: 16px;
    border: 1px solid rgba(0,0,0,0.04);
}
.sk-card-alert {
    background: #FFF5F5; border-radius: 16px; padding: 18px 20px;
    border-left: 5px solid #D32F2F; margin-bottom: 16px;
    box-shadow: 0 2px 12px rgba(211,47,47,0.08);
}
.sk-card-success {
    background: linear-gradient(135deg,#E8F5E9,#F1FFF5); border-radius: 16px;
    padding: 18px 20px; border-left: 5px solid #00D261; margin-bottom: 16px;
    box-shadow: 0 2px 12px rgba(0,210,97,0.10);
}
.sk-card-warn {
    background: #FFFBF0; border-radius: 16px; padding: 16px 20px;
    border-left: 5px solid #F9A825; margin-bottom: 16px;
    box-shadow: 0 2px 8px rgba(249,168,37,0.10);
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #00D261, #00A84F) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 600 !important;
    padding: 11px 26px !important; font-size: 14px !important;
    transition: all 0.2s !important;
    box-shadow: 0 2px 8px rgba(0,210,97,0.30) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(0,210,97,0.40) !important;
}
.stButton > button[kind="secondary"] {
    background: transparent !important; color: #00D261 !important;
    border: 2px solid #00D261 !important; box-shadow: none !important;
}

/* ── Progress ── */
.stProgress > div > div > div { background: linear-gradient(90deg,#00D261,#00A84F) !important; border-radius: 4px !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { gap: 6px; border-bottom: 2px solid #eee; }
.stTabs [data-baseweb="tab"] { border-radius: 10px 10px 0 0 !important; font-weight: 500; }
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: #00D261 !important; color: white !important;
}

/* ── Badges ── */
.badge-ok   { background:#E8F5E9; color:#1B5E20; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:600; display:inline-block; }
.badge-warn { background:#FFF8E1; color:#E65100; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:600; display:inline-block; }
.badge-err  { background:#FFEBEE; color:#C62828; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:600; display:inline-block; }

/* ── Chat ── */
.bubble-user  { background: linear-gradient(135deg,#DCF8C6,#C8F5B0); border-radius:16px 16px 0 16px; padding:12px 16px; margin:8px 0; max-width:82%; margin-left:auto; font-size:14px; }
.bubble-agent { background:#f4f4f4; border-radius:16px 16px 16px 0; padding:12px 16px; margin:8px 0; max-width:82%; font-size:14px; }
.bubble-tech  { background:linear-gradient(135deg,#E3F2FD,#BBDEFB); border-radius:16px 16px 16px 0; padding:12px 16px; margin:8px 0; max-width:82%; border:1px solid #90CAF9; font-size:14px; }

/* ── Layout helpers ── */
.col-left-green {
    background: linear-gradient(160deg, #E8F5E9 0%, #F1FFF7 100%);
    border-radius: 16px; padding: 36px 24px; text-align: center;
    min-height: 360px; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    border: 1px solid rgba(0,210,97,0.15);
}

/* ── Metric cards ── */
.metric-card {
    background: #fff; border-radius: 16px; padding: 18px 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07); text-align: center;
    border-top: 4px solid #00D261;
}
.metric-card.red   { border-top-color: #D32F2F; }
.metric-card.amber { border-top-color: #F9A825; }
.metric-card.blue  { border-top-color: #1565C0; }

/* ── Chatbot floating pill ── */
.chat-pill-wrapper {
    position: fixed; bottom: 24px; right: 24px; z-index: 9999;
    display: flex; flex-direction: column; align-items: flex-end; gap: 10px;
}
.chat-pill-btn {
    background: linear-gradient(135deg,#00D261,#00A84F);
    color: white; border: none; border-radius: 50px;
    padding: 12px 22px; font-size: 15px; font-weight: 600;
    cursor: pointer; display: flex; align-items: center; gap: 8px;
    box-shadow: 0 4px 20px rgba(0,210,97,0.45);
    animation: float-btn 3s ease-in-out infinite;
    white-space: nowrap;
}
.chat-pill-badge {
    background: #D32F2F; color: white; border-radius: 50%;
    width: 20px; height: 20px; font-size: 11px; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    border: 2px solid white;
}
.chat-pill-tooltip {
    background: #2D2926; color: white; border-radius: 10px;
    padding: 10px 16px; font-size: 13px; max-width: 260px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.20); line-height: 1.5;
}
@keyframes float-btn {
    0%,100% { transform: translateY(0); box-shadow: 0 4px 20px rgba(0,210,97,0.45); }
    50%      { transform: translateY(-4px); box-shadow: 0 8px 28px rgba(0,210,97,0.60); }
}

/* ── Paso activo en chatbot ── */
.paso-activo {
    background: linear-gradient(135deg,#FFF8E1,#FFF3CD);
    border: 2px solid #F9A825; border-radius: 12px;
    padding: 14px 16px; margin: 8px 0;
}
.paso-done {
    background: linear-gradient(135deg,#E8F5E9,#F1FFF5);
    border-radius: 12px; padding: 12px 14px; margin: 6px 0;
}
.paso-pending {
    background: #f9f9f9; border-radius: 12px;
    padding: 12px 14px; margin: 6px 0; opacity: 0.55;
}

/* ── Animaciones ── */
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.5;} }
.blink { animation: blink 1.4s ease-in-out infinite; }
@keyframes slideIn { from{transform:translateY(20px);opacity:0;} to{transform:translateY(0);opacity:1;} }
.slide-in { animation: slideIn 0.4s ease-out; }

/* ── Sidebar nav btn activo ── */
div[data-testid="stSidebar"] .stButton > button.active-nav {
    background: linear-gradient(135deg,#00D261,#00A84F) !important;
    color: white !important; font-weight: 700 !important;
}

/* ── Welcome banner ── */
.welcome-banner {
    background: linear-gradient(135deg,#003087,#1565C0);
    border-radius: 16px; padding: 24px 28px; color: white;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(0,48,135,0.25);
}
</style>
"""
