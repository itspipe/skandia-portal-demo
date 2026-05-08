"""Skandia brand guidelines — colores, CSS global y helpers de estilo."""

GREEN        = "#00D261"
GREEN_DARK   = "#00A84F"
GREEN_LIGHT  = "#E8F5E9"
GRAY_DARK    = "#2D2926"
BLUE_HEADER  = "#003087"
RED_ALERT    = "#D32F2F"
RED_BG       = "#FFEBEE"
YELLOW_WARN  = "#FFF8E1"
YELLOW_BDR   = "#F9A825"

CSS = f"""
<style>
html, body, [data-testid="stAppViewContainer"] {{
    background-color: #F0EEE9 !important;
    font-family: 'Inter','Segoe UI',sans-serif;
    color: #2D2926;
}}
[data-testid="stSidebar"] {{
    background-color: #ffffff !important;
    border-right: 1px solid #e0e0e0;
    min-width: 240px !important;
}}
[data-testid="stSidebar"] * {{ color: #2D2926 !important; }}
.block-container {{ padding-top: 0.5rem !important; max-width: 1200px; }}
#MainMenu, footer {{ visibility: hidden; }}

.sk-card {{
    background: #fff; border-radius: 12px; padding: 20px 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 16px;
}}
.sk-card-alert {{
    background: #FFEBEE; border-radius: 12px; padding: 18px 20px;
    border-left: 4px solid #D32F2F; margin-bottom: 16px;
}}
.sk-card-success {{
    background: #E8F5E9; border-radius: 12px; padding: 18px 20px;
    border-left: 4px solid #00D261; margin-bottom: 16px;
}}
.sk-card-warn {{
    background: #FFF8E1; border-radius: 12px; padding: 16px 20px;
    border-left: 4px solid #F9A825; margin-bottom: 16px;
}}
.stButton > button {{
    background-color: #00D261 !important; color: white !important;
    border: none !important; border-radius: 8px !important;
    font-weight: 600 !important; padding: 10px 24px !important;
    transition: background 0.2s !important;
}}
.stButton > button:hover {{ background-color: #00A84F !important; }}
.stButton > button[kind="secondary"] {{
    background-color: transparent !important; color: #00D261 !important;
    border: 2px solid #00D261 !important;
}}
.stProgress > div > div > div {{ background-color: #00D261 !important; }}
.stTabs [data-baseweb="tab"][aria-selected="true"] {{
    background: #00D261 !important; color: white !important;
    border-radius: 8px 8px 0 0;
}}
.badge-ok   {{ background:#E8F5E9;color:#1B5E20;padding:3px 10px;border-radius:20px;font-size:12px;font-weight:600; }}
.badge-warn {{ background:#FFF8E1;color:#E65100;padding:3px 10px;border-radius:20px;font-size:12px;font-weight:600; }}
.badge-err  {{ background:#FFEBEE;color:#D32F2F;padding:3px 10px;border-radius:20px;font-size:12px;font-weight:600; }}
.bubble-user  {{ background:#DCF8C6;border-radius:12px 12px 0 12px;padding:10px 14px;margin:6px 0;max-width:82%;margin-left:auto; }}
.bubble-agent {{ background:#f0f0f0;border-radius:12px 12px 12px 0;padding:10px 14px;margin:6px 0;max-width:82%; }}
.bubble-tech  {{ background:#E3F2FD;border-radius:12px 12px 12px 0;padding:10px 14px;margin:6px 0;max-width:82%;border:1px solid #90CAF9; }}
.col-left-green {{
    background: #E8F5E9; border-radius: 12px; padding: 32px 24px;
    text-align: center; min-height: 360px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
}}
@keyframes blink {{ 0%,100%{{opacity:1;}} 50%{{opacity:0.55;}} }}
.blink {{ animation: blink 1.3s ease-in-out infinite; }}
@keyframes pulse {{ 0%,100%{{transform:scale(1);box-shadow:0 4px 20px rgba(0,210,97,0.5);}} 50%{{transform:scale(1.07);box-shadow:0 4px 32px rgba(0,210,97,0.8);}} }}
</style>
"""

