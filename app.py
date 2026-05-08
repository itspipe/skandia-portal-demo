"""Skandia Portal CX — entrypoint principal."""
import streamlit as st
from config.brand import CSS, GREEN, GRAY_DARK, LOGO_SVG
from modules.session_manager import init_session, reset_demo
from data.base_conocimiento import CLIENTES_DEMO

st.set_page_config(
    page_title="Skandia | Portal Clientes",
    page_icon="✦", layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(CSS, unsafe_allow_html=True)
init_session()

# ═══════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="padding:14px 4px 16px;border-bottom:3px solid {GREEN};margin-bottom:12px;">
      {LOGO_SVG}
      <div style="font-size:10px;color:#aaa;margin-top:4px;text-align:center;">
        Portal CX · Demo Hackathon 2026
      </div>
    </div>
    """, unsafe_allow_html=True)

    logged = st.session_state.get("logged_in",False)

    if logged:
        cliente  = st.session_state.get("cliente_activo",{})
        pagina   = st.session_state.get("pagina_activa","inicio")
        escenario= st.session_state.get("escenario_demo","libre")

        esc_cfg = {
            "A":    ("#00D261","IA resuelve"),
            "B":    ("#F57C00","Técnico"),
            "C":    ("#D32F2F","Escalamiento"),
            "libre":("#888","  Libre"),
        }
        clr,lbl = esc_cfg.get(escenario,("#888","Libre"))

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#F8F9FA,#fff);border-radius:12px;
             padding:12px 14px;margin-bottom:12px;border:1px solid #EAEAEA;">
          <div style="font-size:11px;color:#aaa;font-weight:600;text-transform:uppercase;">Sesión activa</div>
          <div style="font-weight:700;font-size:15px;margin-top:2px;">{cliente.get('nombre','')}</div>
          <div style="font-size:11px;color:#888;">{cliente.get('contrato','')}</div>
          <div style="margin-top:6px;">
            <span style="background:{clr};color:white;padding:2px 10px;
                  border-radius:10px;font-size:11px;font-weight:600;">
              Escenario {escenario.upper()} — {lbl}
            </span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Estado del caso — evaluación segura sin AttributeError
        _err    = st.session_state.get("error_activo") or {}
        _ticket = st.session_state.get("ticket_actual") or {}
        if _err:
            st.markdown(f'<div style="background:#FFF8E1;border-left:3px solid #F9A825;border-radius:8px;padding:7px 10px;font-size:12px;margin-bottom:6px;">⚠️ {_err.get("error_id","Error")} activo</div>', unsafe_allow_html=True)
        if st.session_state.get("tecnico_conectado"):
            st.markdown('<div style="background:#EBF3FF;border-left:3px solid #1565C0;border-radius:8px;padding:7px 10px;font-size:12px;margin-bottom:6px;">👨‍💻 Técnico conectado</div>', unsafe_allow_html=True)
        if st.session_state.get("caso_escalado"):
            st.markdown(f'<div style="background:#FFEBEE;border-left:3px solid #D32F2F;border-radius:8px;padding:7px 10px;font-size:12px;margin-bottom:6px;">🚨 {_ticket.get("numero","Escalado")}</div>', unsafe_allow_html=True)
        if st.session_state.get("caso_resuelto"):
            st.markdown('<div style="background:#E8F5E9;border-left:3px solid #00D261;border-radius:8px;padding:7px 10px;font-size:12px;margin-bottom:6px;">✅ Caso resuelto</div>', unsafe_allow_html=True)

        # Menú navegación
        st.markdown("<div style='font-size:10px;color:#aaa;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;margin:10px 0 6px;'>Navegación</div>", unsafe_allow_html=True)

        PAGINAS = [
            ("inicio","🏠","Mi Portal"),
            ("retiros","💰","Retiros"),
            ("cuentas","🏦","Cuentas Bancarias"),
            ("portafolio","📊","Mi Portafolio"),
            ("documentos","📄","Documentos"),
            ("mis_datos","⚙️","Mis Datos"),
            ("nps","📝","Encuesta NPS"),
            ("dashboard","📈","Dashboard Analítico"),
            ("control_tower","🎯","Control Tower CX"),
        ]
        for key,ico,label in PAGINAS:
            active = pagina==key
            has_err = (st.session_state.get("modulo_origen","").lower() in label.lower()
                       and st.session_state.get("chatbot_activo"))
            suf = " 🔴" if has_err else ""
            if active:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#00D261,#00A84F);color:white;
                     border-radius:9px;padding:9px 14px;margin:2px 0;font-size:13px;
                     font-weight:700;display:flex;align-items:center;gap:6px;">
                  {ico} {label}{suf}
                </div>
                """, unsafe_allow_html=True)
                st.button(label, key=f"nav_{key}", use_container_width=True,
                          label_visibility="collapsed")
            else:
                if st.button(f"{ico} {label}{suf}", key=f"nav_{key}", use_container_width=True):
                    st.session_state.pagina_activa = key
                    st.rerun()

        # Modo Demo
        st.markdown("<hr style='margin:10px 0;border:none;border-top:1px solid #eee;'/>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:10px;color:#aaa;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:6px;'>🎬 Modo Demo</div>", unsafe_allow_html=True)

        opts = {"A":"🟢 A — IA resuelve","B":"🟡 B — Técnico","C":"🔴 C — Escalamiento","libre":"⚪ Libre"}
        esc_sel = st.selectbox("",list(opts.keys()),format_func=lambda x:opts[x],
                               index=list(opts.keys()).index(st.session_state.get("escenario_demo","libre")),
                               key="sel_esc",label_visibility="collapsed")
        if esc_sel != st.session_state.get("escenario_demo"):
            esc_actual = esc_sel
            reset_demo()
            st.session_state.logged_in      = True
            st.session_state.escenario_demo = esc_actual
            for c in CLIENTES_DEMO:
                if c.get("escenario")==esc_actual:
                    st.session_state.cliente_activo = c; break
            st.session_state.pagina_activa = "inicio"
            st.rerun()

        guias = {
            "A":"1️⃣ Retiros → Continuar → ERR001 → IA guía a Cuentas → Regresa → ✅",
            "B":"1️⃣ Retiros → Continuar → ERR002 → IA → No resuelto → 👨‍💻 Técnico → ✅",
            "C":"1️⃣ Portafolio → Cambiar perfil → ERR011 → IA → Técnico → 🚨 Escala",
            "libre":"Explora libremente el portal.",
        }
        st.markdown(f"<div style='font-size:11px;color:#666;background:#F8F8F8;border-radius:8px;padding:8px 10px;margin-top:4px;line-height:1.5;'>{guias.get(esc_sel,'')}</div>",unsafe_allow_html=True)

        st.markdown("<hr style='margin:10px 0;border:none;border-top:1px solid #eee;'/>",unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        with c1:
            if st.button("🔄 Reset",use_container_width=True,key="btn_reset"):
                esc=st.session_state.get("escenario_demo","libre")
                cli=st.session_state.get("cliente_activo")
                reset_demo()
                st.session_state.logged_in=True
                st.session_state.escenario_demo=esc
                if cli: st.session_state.cliente_activo=cli
                st.session_state.pagina_activa="inicio"
                st.rerun()
        with c2:
            if st.button("🚪 Cerrar sesión",use_container_width=True,key="btn_salir"):
                # ── Redirigir al NPS antes de cerrar sesión ──────────────
                st.session_state["nps_desde_logout"] = True
                st.session_state.pagina_activa       = "nps_logout"
                st.rerun()

    else:
        st.markdown("<div style='font-size:13px;color:#888;margin-bottom:12px;'>Accede al portal para ver la demo completa.</div>",unsafe_allow_html=True)
        st.markdown("**Credenciales demo:**")
        ei = {"A":"🟢","B":"🟡","C":"🔴","libre":"⚪"}
        for c in CLIENTES_DEMO:
            e = c.get("escenario","libre")
            with st.expander(f"{ei.get(e,'')} {c['nombre']}"):
                st.code(f"Doc:  {c['documento']}\nPass: skandia123\nOTP:  123456")
                st.caption(f"Escenario {e.upper()}")

# ═══════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════
pagina = st.session_state.get("pagina_activa","login")

if not st.session_state.get("logged_in"):
    if st.session_state.get("mostrar_otp"):
        from pages.login import render_otp; render_otp()
    else:
        from pages.login import render_login; render_login()
else:
    # NPS de logout
    if pagina == "nps_logout":
        from pages.nps import render_nps
        render_nps(desde_logout=True)
    elif pagina=="inicio":
        from pages.inicio import render_inicio; render_inicio()
    elif pagina=="retiros":
        from pages.retiros import render_retiros; render_retiros()
    elif pagina=="cuentas":
        from pages.cuentas import render_cuentas; render_cuentas()
    elif pagina=="portafolio":
        from pages.otras_paginas import render_portafolio; render_portafolio()
    elif pagina=="documentos":
        from pages.otras_paginas import render_documentos; render_documentos()
    elif pagina=="mis_datos":
        from pages.otras_paginas import render_mis_datos; render_mis_datos()
    elif pagina=="nps":
        from pages.nps import render_nps; render_nps()
    elif pagina=="dashboard":
        from pages.dashboard import render_dashboard; render_dashboard()
    elif pagina=="control_tower":
        from pages.control_tower import render_control_tower; render_control_tower()
    else:
        st.session_state.pagina_activa="inicio"; st.rerun()
