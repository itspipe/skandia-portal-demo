"""
Skandia Portal CX — Demo Hackathon
Aplicación principal de Streamlit con router de páginas y sidebar de demo.
"""

import streamlit as st
from config.brand import CSS, GREEN, GRAY_DARK
from modules.session_manager import init_session, reset_demo
from data.base_conocimiento import CLIENTES_DEMO, ESCENARIOS_ERROR

st.set_page_config(
    page_title="Skandia | Portal Clientes",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS Global ────────────────────────────────────────────────────────────────
st.markdown(CSS, unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
init_session()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:12px 0 20px 0;border-bottom:2px solid {GREEN};">
      <div style="font-size:22px;font-weight:700;color:{GRAY_DARK};">
        <span style="color:{GREEN};">✦</span> skandia
      </div>
      <div style="font-size:11px;color:#666;margin-top:4px;">Portal CX — Demo Hackathon</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("logged_in"):
        cliente = st.session_state.get("cliente_activo", {})
        st.markdown(f"""
        <div style="padding:12px 0 8px 0;">
          <div style="font-size:13px;color:#666;">Conectado como:</div>
          <div style="font-weight:700;">{cliente.get('nombre','')}</div>
          <div style="font-size:12px;color:#666;">{cliente.get('contrato','')}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Navegación**")
        paginas = {
            "inicio":       "🏠  Mi Portal",
            "retiros":      "💰  Retiros",
            "cuentas":      "🏦  Cuentas Bancarias",
            "portafolio":   "📊  Mi Portafolio",
            "documentos":   "📄  Documentos",
            "mis_datos":    "⚙️  Mis Datos",
            "nps":          "📝  Encuesta NPS",
            "dashboard":    "📈  Dashboard Analítico",
            "control_tower":"🎯  Control Tower CX",
        }
        for key, label in paginas.items():
            activa = st.session_state.pagina_activa == key
            if st.button(label, key=f"nav_{key}",
                         use_container_width=True,
                         type="primary" if activa else "secondary"):
                st.session_state.pagina_activa = key
                st.rerun()

        st.markdown("---")
        st.markdown("**🎬 Modo Demo**")
        escenario = st.selectbox(
            "Escenario activo:",
            {
                "A": "A — IA resuelve exitosamente",
                "B": "B — IA falla, técnico resuelve",
                "C": "C — Escalado a mesa de ayuda",
                "libre": "Libre — Error aleatorio",
            },
            format_func=lambda x: {
                "A": "🟢 A — IA resuelve",
                "B": "🟡 B — Técnico resuelve",
                "C": "🔴 C — Escalamiento",
                "libre": "⚪ Libre",
            }[x],
            key="sel_escenario"
        )
        if escenario != st.session_state.get("escenario_demo"):
            st.session_state.escenario_demo = escenario
            # Cambiar cliente según escenario
            for c in CLIENTES_DEMO:
                if c.get("escenario") == escenario:
                    st.session_state.cliente_activo = c
                    break
            st.rerun()

        # Indicadores de estado del caso
        if st.session_state.get("error_activo"):
            err = st.session_state.error_activo
            st.markdown(f"""
            <div style="background:#FFF8E1;border-left:3px solid #F9A825;
                        border-radius:6px;padding:8px 10px;font-size:12px;margin-top:8px;">
              ⚠️ <b>Error activo:</b><br/>{err.get('error_id','')} — {err.get('datos',{}).get('titulo','')[:40]}
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.get("tecnico_conectado"):
            st.markdown(f"""
            <div style="background:#E3F2FD;border-left:3px solid #1565C0;
                        border-radius:6px;padding:8px 10px;font-size:12px;margin-top:8px;">
              👨‍💻 Técnico conectado en tiempo real
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.get("caso_escalado"):
            ticket = st.session_state.get("ticket_actual", {})
            st.markdown(f"""
            <div style="background:#FFEBEE;border-left:3px solid #D32F2F;
                        border-radius:6px;padding:8px 10px;font-size:12px;margin-top:8px;">
              🚨 Caso escalado: <b>{ticket.get('numero','')}</b>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.get("caso_resuelto"):
            st.markdown(f"""
            <div style="background:#E8F5E9;border-left:3px solid {GREEN};
                        border-radius:6px;padding:8px 10px;font-size:12px;margin-top:8px;">
              ✅ Caso resuelto exitosamente
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reset", use_container_width=True):
                reset_demo()
                st.rerun()
        with col2:
            if st.button("🚪 Salir", use_container_width=True):
                reset_demo()
                st.session_state.logged_in = False
                st.session_state.pagina_activa = "login"
                st.rerun()

    else:
        # No logueado
        st.markdown("""
        <div style="padding:12px 0;font-size:13px;color:#666;">
          Ingresa al portal para acceder a todas las funcionalidades de la demo.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Credenciales demo:**")
        for c in CLIENTES_DEMO:
            with st.expander(f"🔐 {c['nombre']}", expanded=False):
                st.markdown(f"""
                - **Doc:** `{c['documento']}`
                - **Pass:** `skandia123`
                - **Escenario:** {c.get('escenario','libre').upper()}
                """)

# ── Router principal ──────────────────────────────────────────────────────────
pagina = st.session_state.get("pagina_activa", "login")

if not st.session_state.get("logged_in"):
    if st.session_state.get("mostrar_otp"):
        from pages.login import render_otp
        render_otp()
    else:
        from pages.login import render_login
        render_login()

else:
    # Técnico directo (desde control tower)
    if pagina == "tecnico_directo":
        if st.session_state.get("tecnico_conectado") or st.session_state.get("error_activo"):
            from modules.tecnico import render_tecnico
            st.markdown("## 🔧 Sesión de Soporte Técnico")
            render_tecnico()
        else:
            st.session_state.pagina_activa = "control_tower"
            st.rerun()

    elif pagina == "inicio":
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
