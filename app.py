"""
Skandia Portal CX — Entrypoint Principal
Hackathon 2026 - Proyecto de Recuperación Proactiva NPS
"""
import streamlit as st
import os
import sys

# FIX DE RUTAS: Asegura que Streamlit encuentre las carpetas 'config', 'modules', 'pages', etc.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Intentar importar la configuración de marca
try:
    from config.brand import CSS, GREEN, GRAY_DARK, LOGO_SVG
except ImportError:
    st.error("Error crítico: No se encontró la carpeta 'config' o el archivo 'brand.py'. Verifica la estructura en GitHub.")
    st.stop()

from modules.session_manager import init_session, reset_demo
from data.base_conocimiento import CLIENTES_DEMO

# 1. Configuración de la Página
st.set_page_config(
    page_title="Skandia | Portal Clientes",
    page_icon="✦", 
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inyectar CSS global (Cloud Dancer background y estilos de componentes)
st.markdown(CSS, unsafe_allow_html=True)

# Inicializar estado de la sesión (Logs, errores, datos del cliente)
init_session()

# ═══════════════════════════════════════════════
# SIDEBAR - CONTROL DEL DEMO
# ═══════════════════════════════════════════════
with st.sidebar:
    # Header con Logo Skandia
    st.markdown(f"""
    <div style="padding:14px 4px 16px;border-bottom:3px solid {GREEN};margin-bottom:12px;">
      {LOGO_SVG}
      <div style="font-size:10px;color:#aaa;margin-top:4px;text-align:center;">
        Portal CX · Demo Hackathon 2026
      </div>
    </div>
    """, unsafe_allow_html=True)

    logged = st.session_state.get("logged_in", False)

    if logged:
        cliente = st.session_state.get("cliente_activo", {})
        st.write(f"👤 **Usuario:** {cliente.get('nombre', 'Andrés Osorio')}")
        st.write(f"💼 **FP Asignado:** {cliente.get('agente', 'Simón Lobo')}")
        
        st.divider()
        
        # Selector de Escenarios para el Jurado
        st.subheader("🛠️ Modos del Demo")
        escenario = st.selectbox(
            "Selecciona un escenario de prueba:",
            ["Libre (Sin errores)", "Falla: IA Resuelve", "Falla: Técnico Resuelve", "Falla: Escalamiento Final"],
            key="escenario_demo"
        )
        
        if st.button("Resetear Demo"):
            reset_demo()
            st.rerun()
            
        st.divider()
        if st.button("Cerrar Sesión"):
            st.session_state.pagina_activa = "nps_logout"
            st.rerun()

# ═══════════════════════════════════════════════
# ROUTER DE NAVEGACIÓN
# ═══════════════════════════════════════════════
pagina = st.session_state.get("pagina_activa", "login")

# Flujo de Login y Seguridad
if not st.session_state.get("logged_in"):
    if st.session_state.get("mostrar_otp"):
        from pages.login import render_otp
        render_otp()
    else:
        from pages.login import render_login
        render_login()

# Flujo Post-Login
else:
    # Si el usuario cerró sesión, lo enviamos a la encuesta final
    if pagina == "nps_logout":
        from pages.nps import render_nps
        render_nps(desde_logout=True)
    
    # Navegación Principal
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
        
    # Paneles Administrativos (Solo visibles si se activa en el demo)
    elif pagina == "dashboard":
        from pages.dashboard import render_dashboard
        render_dashboard()
        
    elif pagina == "control_tower":
        from pages.control_tower import render_control_tower
        render_control_tower()

# Footer sutil
st.markdown("""
    <div style='text-align: center; color: #aaa; font-size: 0.8rem; margin-top: 50px;'>
        © 2026 Skandia Colombia | Innovación y Big Data
    </div>
""", unsafe_allow_html=True)