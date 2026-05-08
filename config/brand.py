"""Skandia brand guidelines — colores, CSS global y helpers de estilo."""

# ── Paleta oficial ──────────────────────────────────────────────────────────
GREEN       = "#00D261"
GREEN_DARK  = "#00A84F"
GRAY_DARK   = "#2D2926"
CLOUD       = "#F0EEE9"
BLUE_HEADER = "#003087"
RED_ALERT   = "#D32F2F"
RED_BG      = "#FFEBEE"
YELLOW_WARN = "#FFF8E1"
YELLOW_BORDER = "#F9A825"

CSS = f"""
<style>
/* ── Reset & base ── */
html, body, [data-testid="stAppViewContainer"] {{
    background-color: {CLOUD} !important;
    font-family: 'Inter', 'Segoe UI', sans-serif;
    color: {GRAY_DARK};
}}
[data-testid="stSidebar"] {{
    background-color: #ffffff !important;
    border-right: 1px solid #e0e0e0;
}}
[data-testid="stSidebar"] * {{ color: {GRAY_DARK} !important; }}

/* ── Header bar ── */
.skandia-header {{
    background: #fff;
    border-top: 4px solid {BLUE_HEADER};
    padding: 12px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    margin-bottom: 0;
}}
.skandia-logo {{
    font-size: 26px;
    font-weight: 700;
    color: {GRAY_DARK};
    display: flex;
    align-items: center;
    gap: 8px;
}}
.skandia-logo span {{ color: {GREEN}; font-size: 30px; }}
.nav-divider {{
    width: 1px; height: 28px;
    background: #ddd; margin: 0 16px;
}}
.portal-tag {{
    font-size: 14px; color: #666; font-weight: 400;
}}

/* ── Cards ── */
.sk-card {{
    background: #fff;
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    margin-bottom: 16px;
}}
.sk-card-alert {{
    background: {RED_BG};
    border-radius: 12px;
    padding: 20px 24px;
    border-left: 4px solid {RED_ALERT};
    margin-bottom: 16px;
}}
.sk-card-success {{
    background: #E8F5E9;
    border-radius: 12px;
    padding: 20px 24px;
    border-left: 4px solid {GREEN};
    margin-bottom: 16px;
}}
.sk-card-warn {{
    background: {YELLOW_WARN};
    border-radius: 12px;
    padding: 16px 20px;
    border-left: 4px solid {YELLOW_BORDER};
    margin-bottom: 16px;
}}

/* ── Buttons ── */
.stButton > button {{
    background-color: {GREEN} !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    transition: background 0.2s !important;
}}
.stButton > button:hover {{
    background-color: {GREEN_DARK} !important;
}}
.btn-outline {{
    background: transparent !important;
    color: {GREEN} !important;
    border: 2px solid {GREEN} !important;
    border-radius: 8px !important;
}}

/* ── Progress bar ── */
.stProgress > div > div > div {{
    background-color: {GREEN} !important;
}}

/* ── Blink animation for detractor alert ── */
@keyframes blink {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.4; }}
}}
.blink {{ animation: blink 1.2s ease-in-out infinite; }}

/* ── Two-column layout helper ── */
.col-left-green {{
    background: #E8F5E9;
    border-radius: 12px;
    padding: 32px 24px;
    text-align: center;
    min-height: 400px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}

/* ── Status badges ── */
.badge-ok   {{ background:#E8F5E9; color:#1B5E20; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:600; }}
.badge-warn {{ background:#FFF8E1; color:#E65100; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:600; }}
.badge-err  {{ background:{RED_BG}; color:{RED_ALERT}; padding:3px 10px; border-radius:20px; font-size:12px; font-weight:600; }}

/* ── Chat bubbles ── */
.bubble-user    {{ background:#DCF8C6; border-radius:12px 12px 0 12px; padding:10px 14px; margin:6px 0; max-width:80%; margin-left:auto; }}
.bubble-agent   {{ background:#fff; border-radius:12px 12px 12px 0; padding:10px 14px; margin:6px 0; max-width:80%; border:1px solid #e0e0e0; }}
.bubble-tech    {{ background:#E3F2FD; border-radius:12px 12px 12px 0; padding:10px 14px; margin:6px 0; max-width:80%; border:1px solid #90CAF9; }}

/* ── Checklist items ── */
.check-item-done {{ color:#1B5E20; margin:4px 0; }}
.check-item-todo {{ color:#555; margin:4px 0; }}

/* ── Slider override ── */
.stSlider > div > div > div > div {{ background: {GREEN} !important; }}

/* ── Hide streamlit default menu ── */
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 1rem !important; }}
</style>
"""

def header_html(page_title: str = "Portal Clientes") -> str:
    return f"""
    <div class="skandia-header">
      <div style="display:flex;align-items:center;">
        <div class="skandia-logo">
          <span>✦</span> skandia
        </div>
        <div class="nav-divider"></div>
        <div class="portal-tag">{page_title}</div>
      </div>
      <div style="display:flex;gap:8px;">
        <div style="border:1px solid #ddd;border-radius:8px;padding:8px 16px;text-align:center;cursor:pointer;font-size:12px;">
          💰<br/>APORTES
        </div>
        <div style="border:1px solid #ddd;border-radius:8px;padding:8px 16px;text-align:center;cursor:pointer;font-size:12px;">
          ↔<br/>RETIROS
        </div>
        <div style="border:1px solid #ddd;border-radius:8px;padding:8px 16px;text-align:center;cursor:pointer;font-size:12px;">
          📄<br/>DOCUMENTOS
        </div>
      </div>
    </div>
    """
