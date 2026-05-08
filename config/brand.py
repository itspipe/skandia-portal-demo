"""Skandia brand — paleta oficial, logo SVG y CSS global."""

GREEN       = "#00D261"
GREEN_DARK  = "#00A84F"
GREEN_LIGHT = "#E8F5E9"
GRAY_DARK   = "#2D2926"
BLUE_H      = "#003087"
RED_ALERT   = "#D32F2F"
RED_BG      = "#FFEBEE"
YELLOW_W    = "#FFF8E1"
YELLOW_B    = "#F9A825"

# Logo SVG oficial Skandia (hoja verde + texto oscuro)
LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 36" height="36">
  <!-- Hoja verde Skandia -->
  <path d="M8 28 C8 28 2 20 6 12 C10 4 20 4 20 4 C20 4 14 12 16 20 C18 26 24 28 24 28 Z"
        fill="#00D261"/>
  <!-- Texto skandia -->
  <text x="30" y="25" font-family="Inter,Arial,sans-serif" font-size="20"
        font-weight="700" fill="#2D2926" letter-spacing="-0.5">skandia</text>
</svg>
"""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html,body,[data-testid="stAppViewContainer"]{
  background:#F4F6F9 !important;
  font-family:'Inter','Segoe UI',sans-serif !important;
}
[data-testid="stSidebar"]{
  background:#ffffff !important;
  border-right:1px solid #EAEAEA !important;
  box-shadow:3px 0 16px rgba(0,0,0,0.05) !important;
}
[data-testid="stSidebar"] *{color:#2D2926 !important;}
.block-container{padding-top:0 !important; padding-bottom:2rem !important;}
#MainMenu,footer,header{visibility:hidden;}

/* ── Top Header ── */
.sk-header{
  background:#fff;
  border-bottom:3px solid #00D261;
  padding:0 28px;
  height:60px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  box-shadow:0 2px 12px rgba(0,0,0,0.07);
  margin:-0.25rem -1rem 0 -1rem;
  gap:12px;
  flex-wrap:wrap;
}
.sk-header-left{display:flex;align-items:center;gap:14px;}
.sk-header-divider{width:1px;height:28px;background:#E0E0E0;}
.sk-header-section{font-size:13px;color:#888;font-weight:400;}
.sk-header-right{display:flex;align-items:center;gap:10px;}
.sk-header-user{font-size:13px;color:#555;display:flex;align-items:center;gap:6px;}
.sk-header-badge{
  background:#00D261;color:white;
  border-radius:20px;padding:5px 16px;
  font-size:13px;font-weight:600;
  display:flex;align-items:center;gap:5px;
}

/* ── Cards ── */
.sk-card{
  background:#fff;border-radius:14px;padding:20px 24px;
  box-shadow:0 1px 8px rgba(0,0,0,0.06);
  margin-bottom:16px;border:1px solid rgba(0,0,0,0.04);
}
.sk-card-alert{
  background:#FFF5F5;border-radius:14px;padding:16px 20px;
  border-left:4px solid #D32F2F;margin-bottom:16px;
  box-shadow:0 2px 10px rgba(211,47,47,0.08);
}
.sk-card-success{
  background:linear-gradient(135deg,#E8F5E9,#F0FFF6);
  border-radius:14px;padding:16px 20px;
  border-left:4px solid #00D261;margin-bottom:16px;
}
.sk-card-warn{
  background:#FFFBF0;border-radius:14px;padding:14px 18px;
  border-left:4px solid #F9A825;margin-bottom:16px;
}
.sk-card-blue{
  background:linear-gradient(135deg,#EBF3FF,#F5F9FF);
  border-radius:14px;padding:16px 20px;
  border-left:4px solid #1565C0;margin-bottom:16px;
}

/* ── Buttons ── */
.stButton>button{
  background:linear-gradient(135deg,#00D261,#00B856) !important;
  color:white !important;border:none !important;
  border-radius:10px !important;font-weight:600 !important;
  padding:10px 22px !important;font-size:14px !important;
  transition:all 0.2s ease !important;
  box-shadow:0 3px 10px rgba(0,210,97,0.28) !important;
  letter-spacing:0.1px !important;
}
.stButton>button:hover{
  transform:translateY(-2px) !important;
  box-shadow:0 6px 18px rgba(0,210,97,0.38) !important;
  background:linear-gradient(135deg,#00B856,#009B48) !important;
}
.stButton>button[kind="secondary"]{
  background:transparent !important;
  color:#00D261 !important;
  border:2px solid #00D261 !important;
  box-shadow:none !important;
}
.stButton>button[kind="secondary"]:hover{
  background:#F0FFF6 !important;
  transform:translateY(-1px) !important;
}

/* ── Chatbot POPUP flotante ── */
.chatbot-popup-overlay{
  position:fixed;bottom:90px;right:24px;
  width:380px;max-width:94vw;
  background:#fff;border-radius:18px;
  box-shadow:0 12px 40px rgba(0,0,0,0.18);
  border:2px solid #00D261;z-index:9998;
  overflow:hidden;
  animation:popupIn 0.3s cubic-bezier(0.34,1.56,0.64,1);
}
@keyframes popupIn{
  from{opacity:0;transform:translateY(20px) scale(0.95);}
  to{opacity:1;transform:translateY(0) scale(1);}
}
.chatbot-popup-header{
  background:linear-gradient(135deg,#003087,#1565C0);
  padding:14px 18px;
  display:flex;align-items:center;gap:10px;color:white;
}
.chatbot-popup-body{
  padding:16px;max-height:380px;overflow-y:auto;
}
.chatbot-fab{
  position:fixed;bottom:22px;right:24px;
  width:58px;height:58px;border-radius:50%;
  background:linear-gradient(135deg,#00D261,#00A84F);
  color:white;cursor:pointer;z-index:9999;
  display:flex;align-items:center;justify-content:center;
  font-size:26px;
  box-shadow:0 4px 18px rgba(0,210,97,0.50);
  animation:fabPulse 2.5s ease-in-out infinite;
  border:3px solid white;
}
.chatbot-fab-badge{
  position:absolute;top:-4px;right:-4px;
  background:#D32F2F;color:white;border-radius:50%;
  width:20px;height:20px;font-size:11px;font-weight:700;
  display:flex;align-items:center;justify-content:center;
  border:2px solid white;
}
@keyframes fabPulse{
  0%,100%{box-shadow:0 4px 18px rgba(0,210,97,0.50);}
  50%{box-shadow:0 4px 28px rgba(0,210,97,0.75),0 0 0 8px rgba(0,210,97,0.12);}
}
.chatbot-tooltip{
  position:fixed;bottom:88px;right:90px;
  background:#2D2926;color:white;border-radius:10px;
  padding:8px 14px;font-size:12px;font-weight:500;
  white-space:nowrap;z-index:9997;
  animation:fadeIn 0.3s ease;
  box-shadow:0 4px 12px rgba(0,0,0,0.2);
}
.chatbot-tooltip::after{
  content:'';position:absolute;right:-6px;top:50%;
  transform:translateY(-50%);
  border:6px solid transparent;border-left-color:#2D2926;
  border-right:none;
}
@keyframes fadeIn{from{opacity:0;}to{opacity:1;}}

/* ── Pasos del chatbot ── */
.paso-done{
  background:linear-gradient(135deg,#E8F5E9,#F0FFF6);
  border-radius:10px;padding:10px 14px;margin:5px 0;
  border-left:3px solid #00D261;
}
.paso-activo{
  background:linear-gradient(135deg,#FFF8E1,#FFFBF0);
  border-radius:10px;padding:12px 14px;margin:5px 0;
  border-left:3px solid #F9A825;
  box-shadow:0 2px 8px rgba(249,168,37,0.15);
}
.paso-pending{
  background:#FAFAFA;border-radius:10px;
  padding:10px 14px;margin:5px 0;opacity:0.5;
}

/* ── Dashboard cards ── */
.dash-metric{
  background:#fff;border-radius:14px;padding:20px;
  text-align:center;box-shadow:0 2px 10px rgba(0,0,0,0.06);
  transition:transform 0.2s,box-shadow 0.2s;cursor:default;
  border:1px solid rgba(0,0,0,0.04);
}
.dash-metric:hover{transform:translateY(-3px);box-shadow:0 6px 20px rgba(0,0,0,0.10);}
.dash-action-btn{
  background:linear-gradient(135deg,#fff,#F8F9FA);
  border:2px solid #E0E0E0;border-radius:14px;
  padding:18px 14px;text-align:center;cursor:pointer;
  transition:all 0.2s;
}
.dash-action-btn:hover{
  border-color:#00D261;background:linear-gradient(135deg,#F0FFF6,#E8F5E9);
  transform:translateY(-2px);box-shadow:0 4px 14px rgba(0,210,97,0.20);
}

/* ── Progress ── */
.stProgress>div>div>div{
  background:linear-gradient(90deg,#00D261,#00A84F) !important;
  border-radius:4px !important;
}

/* ── Badges ── */
.badge-ok{background:#E8F5E9;color:#1B5E20;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:600;display:inline-block;}
.badge-warn{background:#FFF8E1;color:#E65100;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:600;display:inline-block;}
.badge-err{background:#FFEBEE;color:#C62828;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:600;display:inline-block;}

/* ── Chat bubbles ── */
.bubble-user{background:linear-gradient(135deg,#DCF8C6,#C8F4B0);border-radius:16px 16px 0 16px;padding:10px 14px;margin:6px 0;max-width:82%;margin-left:auto;font-size:13px;}
.bubble-agent{background:#F4F4F4;border-radius:16px 16px 16px 0;padding:10px 14px;margin:6px 0;max-width:82%;font-size:13px;}
.bubble-tech{background:linear-gradient(135deg,#E3F2FD,#BBDEFB);border-radius:16px 16px 16px 0;padding:10px 14px;margin:6px 0;max-width:82%;font-size:13px;}

/* ── Col izquierda ── */
.col-left-green{
  background:linear-gradient(160deg,#E8F5E9,#F1FFF8);
  border-radius:14px;padding:32px 20px;text-align:center;
  min-height:340px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;
  border:1px solid rgba(0,210,97,0.12);
}

/* ── Welcome banner ── */
.welcome-banner{
  background:linear-gradient(135deg,#003087 0%,#1565C0 60%,#1976D2 100%);
  border-radius:16px;padding:22px 26px;color:white;
  margin-bottom:20px;box-shadow:0 4px 20px rgba(0,48,135,0.22);
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{gap:6px;}
.stTabs [data-baseweb="tab"]{border-radius:10px 10px 0 0 !important;font-weight:500;}
.stTabs [data-baseweb="tab"][aria-selected="true"]{
  background:linear-gradient(135deg,#00D261,#00A84F) !important;
  color:white !important;
}

/* ── Slider ── */
.stSlider>div>div>div>div{background:#00D261 !important;}

/* ── Animations ── */
@keyframes blink{0%,100%{opacity:1;}50%{opacity:0.45;}}
.blink{animation:blink 1.4s ease-in-out infinite;}
@keyframes slideUp{from{opacity:0;transform:translateY(16px);}to{opacity:1;transform:translateY(0);}}
.slide-up{animation:slideUp 0.4s ease-out;}
</style>
"""

def sk_header(seccion: str = "", cliente_nombre: str = "") -> str:
    """Header oficial con logo SVG Skandia."""
    badge = f'<div class="sk-header-badge">💰 {seccion}</div>' if seccion else ""
    usuario = f'<div class="sk-header-user">👤 {cliente_nombre}</div>' if cliente_nombre else ""
    return f"""
    <div class="sk-header">
      <div class="sk-header-left">
        {LOGO_SVG}
        <div class="sk-header-divider"></div>
        <span class="sk-header-section">Portal Clientes</span>
      </div>
      <div class="sk-header-right">
        {usuario}
        {badge}
      </div>
    </div>
    """
