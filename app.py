"""
Skandia Portal CX — Demo Hackathon
Router principal con sidebar de navegación siempre visible
y menú lateral fijo con todos los módulos.
"""

import streamlit as st
from config.brand import CSS, GREEN, GRAY_DARK, RED_ALERT
from modules.session_manager import init_session, reset_demo
from data.base_conocimiento import CLIENTES_DEMO

st.set_page_config(
    page_title="Skandia | Portal Clientes",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CSS, unsafe_allow_html=True)
init_session()

# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR — siempre visible, con todos los módulos accesibles
# ═══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo
    st.markdown(f"""
    <div style="text-align:center;padding:14px 0 16px 0;
                border-bottom:3px solid {GREEN};margin-bottom:12px;">
      <div style="font-size:24px;font-weight:700;color:{GRAY_DARK};">
        <span style="color:{GREEN};font-size:28px;">✦</span> skandia
      </div>
      <div style="font-size:11px;color:#999;margin-top:2px;">Portal CX · Demo Hackathon</div>
    </div>
    """, unsafe_allow_html=True)

    logged = st.session_state.get("logged_in", False)

    if logged:
        cliente = st.session_state.get("cliente_activo", {})
        pagina  = st.session_state.get("pagina_activa", "inicio")

        # Info del cliente
        escenario = st.session_state.get("escenario_demo", "libre")
        esc_color = {"A": "#00D261", "B": "#F57C00", "C": "#D32F2F", "libre": "#888"}.get(escenario, "#888")
        st.markdown(f"""
        <div style="background:#f9f9f9;border-radius:10px;padding:10px 12px;margin-bottom:12px;">
          <div style="font-size:12px;color:#999;">Sesión activa</div>
          <div style="font-weight:700;font-size:15px;">{cliente.get('nombre','')}</div>
          <div style="font-size:11px;color:#666;">{cliente.get('contrato','')}</div>
          <div style="margin-top:6px;">
            <span style="background:{esc_color};color:white;padding:2px 8px;
                          border-radius:10px;font-size:11px;font-weight:600;">
              Escenario {escenario.upper()}
            </span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Estado del caso actual ──────────────────────────────────────
        if st.session_state.get("error_activo"):
            err = st.session_state.error_activo
            st.markdown(f"""
            <div style="background:#FFF8E1;border:1px solid #F9A825;border-radius:8px;
                        padding:8px 10px;font-size:12px;margin-bottom:8px;">
              ⚠️ <b>Error activo</b><br/>
              <span style="color:#D32F2F;">{err.get('error_id','')} — {err.get('datos',{}).get('titulo','')[:45]}</span>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.get("tecnico_conectado"):
            st.markdown("""
            <div style="background:#E3F2FD;border:1px solid #1565C0;border-radius:8px;
                        padding:8px 10px;font-size:12px;margin-bottom:8px;">
              👨‍💻 <b>Técnico conectado</b> — Soporte en vivo
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.get("caso_escalado"):
            ticket = st.session_state.get("ticket_actual", {})
            st.markdown(f"""
            <div style="background:#FFEBEE;border:1px solid #D32F2F;border-radius:8px;
                        padding:8px 10px;font-size:12px;margin-bottom:8px;">
              🚨 <b>Escalado</b>: {ticket.get('numero','')}
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.get("caso_resuelto"):
            st.markdown(f"""
            <div style="background:#E8F5E9;border:1px solid {GREEN};border-radius:8px;
                        padding:8px 10px;font-size:12px;margin-bottom:8px;">
              ✅ <b>Caso resuelto</b>
            </div>
            """, unsafe_allow_html=True)

        # ── Menú de navegación completo ─────────────────────────────────
        st.markdown("<div style='font-size:11px;color:#999;font-weight:600;margin:8px 0 4px;text-transform:uppercase;letter-spacing:0.5px;'>Navegación</div>", unsafe_allow_html=True)

        PAGINAS = [
            ("inicio",        "🏠", "Mi Portal"),
            ("retiros",       "💰", "Retiros"),
            ("cuentas",       "🏦", "Cuentas Bancarias"),
            ("portafolio",    "📊", "Mi Portafolio"),
            ("documentos",    "📄", "Documentos"),
            ("mis_datos",     "⚙️", "Mis Datos"),
            ("nps",           "📝", "Encuesta NPS"),
            ("dashboard",     "📈", "Dashboard Analítico"),
            ("control_tower", "🎯", "Control Tower CX"),
        ]

        for key, icon, label in PAGINAS:
            is_active = (pagina == key)
            # Indicar si la página tiene error activo
            has_error = (
                st.session_state.get("error_activo") and
                st.session_state.get("modulo_origen", "").lower() in label.lower()
            )
            suffix = " 🔴" if has_error else ""
            btn_label = f"{icon} {label}{suffix}"

            if is_active:
                st.markdown(f"""
                <div style="background:{GREEN};color:white;border-radius:8px;
                            padding:9px 14px;margin:2px 0;font-size:14px;font-weight:600;">
                  {btn_label}
                </div>
                """, unsafe_allow_html=True)
                # Botón invisible para capturar clics en la misma página
                if st.button(btn_label, key=f"nav_{key}", use_container_width=True,
                             help=f"Estás en {label}"):
                    st.rerun()
            else:
                if st.button(btn_label, key=f"nav_{key}", use_container_width=True):
                    st.session_state.pagina_activa = key
                    st.rerun()

        # ── Modo Demo ───────────────────────────────────────────────────
        st.markdown("<hr style='margin:12px 0;border:none;border-top:1px solid #eee;'/>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:11px;color:#999;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;'>🎬 Modo Demo</div>", unsafe_allow_html=True)

        opciones_esc = {
            "A":     "🟢 A — IA resuelve",
            "B":     "🟡 B — Técnico resuelve",
            "C":     "🔴 C — Escalamiento",
            "libre": "⚪ Libre",
        }
        esc_sel = st.selectbox(
            "Escenario:",
            list(opciones_esc.keys()),
            format_func=lambda x: opciones_esc[x],
            index=list(opciones_esc.keys()).index(st.session_state.get("escenario_demo", "libre")),
            key="sel_esc",
            label_visibility="collapsed",
        )
        if esc_sel != st.session_state.get("escenario_demo"):
            st.session_state.escenario_demo = esc_sel
            for c in CLIENTES_DEMO:
                if c.get("escenario") == esc_sel:
                    st.session_state.cliente_activo = c
                    break
            reset_demo()
            st.session_state.logged_in = True
            st.session_state.escenario_demo = esc_sel
            for c in CLIENTES_DEMO:
                if c.get("escenario") == esc_sel:
                    st.session_state.cliente_activo = c
                    break
            st.session_state.pagina_activa = "inicio"
            st.rerun()

        st.markdown("<div style='font-size:11px;color:#666;margin:4px 0 8px 0;'>Guía del escenario activo:</div>", unsafe_allow_html=True)
        guias = {
            "A":     "1️⃣ Ir a **Retiros** → Procesar → Error de cuenta → IA resuelve",
            "B":     "1️⃣ Ir a **Cuentas** → Agregar → Error SARLAFT → IA falla → Técnico",
            "C":     "1️⃣ Ir a **Portafolio** → Cambiar perfil → Error firma → Escalar",
            "libre": "Explora libremente. Sin errores predefinidos.",
        }
        st.markdown(f"<div style='font-size:12px;color:#444;background:#f5f5f5;border-radius:6px;padding:8px 10px;'>{guias.get(esc_sel,'')}</div>", unsafe_allow_html=True)

        st.markdown("<hr style='margin:10px 0;border:none;border-top:1px solid #eee;'/>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reset", use_container_width=True, key="btn_reset"):
                esc_actual = st.session_state.get("escenario_demo", "libre")
                cliente_actual = st.session_state.get("cliente_activo")
                reset_demo()
                st.session_state.logged_in = True
                st.session_state.escenario_demo = esc_actual
                if cliente_actual:
                    st.session_state.cliente_activo = cliente_actual
                st.session_state.pagina_activa = "inicio"
                st.rerun()
        with col2:
            if st.button("🚪 Salir", use_container_width=True, key="btn_salir"):
                reset_demo()
                st.session_state.logged_in  = False
                st.session_state.pagina_activa = "login"
                st.rerun()

    else:
        # ── Sin sesión: credenciales demo ──────────────────────────────
        st.markdown("""
        <div style="font-size:13px;color:#666;margin-bottom:12px;">
          Ingresa al portal para ver la demo completa.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**👤 Credenciales demo:**")
        escenarios_info = {"A": "🟢 IA resuelve", "B": "🟡 Técnico", "C": "🔴 Escalamiento", "libre": "⚪ Libre"}
        for c in CLIENTES_DEMO:
            esc = c.get("escenario", "libre")
            with st.expander(f"{escenarios_info.get(esc,'')} {c['nombre']}"):
                st.code(f"Doc: {c['documento']}\nPass: skandia123\nOTP: 123456")
                st.caption(f"Escenario: {esc.upper()}")


# ═══════════════════════════════════════════════════════════════════════════
# ROUTER PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════
pagina = st.session_state.get("pagina_activa", "login")

if not st.session_state.get("logged_in"):
    if st.session_state.get("mostrar_otp"):
        from pages.login import render_otp
        render_otp()
    else:
        from pages.login import render_login
        render_login()
else:
    if pagina == "inicio":
        from pages.inicio import render_inicio
        render_inicio()
    elif pagina == "retiros":
        from pages.retiros import render_retiros
        render_retiros()
    elif pagina == "cuentas":
        from pages.cuentas import render_cuentas
        render_cuentas()
    elif pagina == "portafolio":
        from pages.otras_paginas import render_portafolio
        render_portafolio()
    elif pagina == "documentos":
        from pages.otras_paginas import render_documentos
        render_documentos()
    elif pagina == "mis_datos":
        from pages.otras_paginas import render_mis_datos
        render_mis_datos()
    elif pagina == "nps":
        from pages.nps import render_nps
        render_nps()
    elif pagina == "dashboard":
        from pages.dashboard import render_dashboard
        render_dashboard()
    elif pagina == "control_tower":
        from pages.control_tower import render_control_tower
        render_control_tower()
    else:
        st.session_state.pagina_activa = "inicio"
        st.rerun()
