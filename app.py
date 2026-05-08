import streamlit as st
import os
import sys

# Asegurar rutas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from config.brand import CSS, GREEN, LOGO_SVG
    from modules.session_manager import init_session, reset_demo
except ImportError as e:
    st.error(f"Error de importación: {e}")
    st.stop()

st.set_page_config(page_title="Skandia | Portal CX", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)
init_session()

# --- SIDEBAR DINÁMICO ---
with st.sidebar:
    st.markdown(f"<div style='text-align:center;'>{LOGO_SVG}</div>", unsafe_allow_html=True)
    st.divider()
    
    if st.session_state.get("logged_in"):
        cliente = st.session_state.cliente_activo
        st.success(f"✅ Conectado: **{cliente['nombre']}**")
        
        st.subheader("🛠️ Panel de Control Demo")
        escenario = st.selectbox(
            "Escenario del Pitch:",
            ["Libre", "IA Resuelve", "Técnico Resuelve", "Escalamiento Final"],
            key="escenario_demo"
        )
        
        st.divider()
        st.subheader("📊 Vista de Negocio")
        if st.button("📈 Dashboard NPS", use_container_width=True):
            st.session_state.pagina_activa = "dashboard"
            st.rerun()
        if st.button("🚨 Torre de Control CX", use_container_width=True):
            st.session_state.pagina_activa = "control_tower"
            st.rerun()
            
        if st.button("🔄 Resetear Todo", type="secondary"):
            reset_demo()
            st.rerun()

# --- ROUTER ---
pagina = st.session_state.get("pagina_activa", "login")

if not st.session_state.get("logged_in"):
    from pages.login import render_login
    render_login()
else:
    if pagina == "inicio":
        from pages.inicio import render_inicio
        render_inicio()
    elif pagina == "retiros":
        from pages.retiros import render_retiros
        render_retiros()
    elif pagina == "nps":
        from pages.nps import render_nps
        render_nps()
    elif pagina == "dashboard":
        from pages.dashboard import render_dashboard
        render_dashboard()
    elif pagina == "control_tower":
        from pages.control_tower import render_control_tower
        render_control_tower()