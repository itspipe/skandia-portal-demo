"""Páginas: Portafolio, Documentos y Mis Datos."""

import streamlit as st
import plotly.graph_objects as go
from config.brand import GREEN, GRAY_DARK, header_html
from modules.session_manager import log_accion, activar_error
from data.base_conocimiento import ESCENARIOS_ERROR


# ── PORTAFOLIO ───────────────────────────────────────────────────────────────

def render_portafolio():
    st.markdown(header_html("Portal Clientes"), unsafe_allow_html=True)
    cliente = st.session_state.get("cliente_activo", {})
    saldo = cliente.get("saldo_ahorro", 1414977.14)

    st.markdown(f"""
    <div style="padding:16px 0 8px 0;">
      <h2 style="color:{GRAY_DARK};">Mi Portafolio</h2>
      <p style="color:#666;">Visualiza y gestiona la distribución de tus inversiones.</p>
    </div>
    """, unsafe_allow_html=True)

    fondos = [
        {"nombre": "FPV Strategist Liquidez Col", "pct": 100.0, "valor": saldo},
    ]

    col1, col2 = st.columns([1, 1])
    with col1:
        labels = [f["nombre"] for f in fondos]
        values = [f["pct"] for f in fondos]
        fig = go.Figure(go.Pie(
            labels=labels, values=values,
            hole=0.6,
            marker=dict(colors=[GREEN, "#2D2926", "#F0EEE9", "#00A84F"]),
            textinfo="label+percent",
        ))
        fig.update_layout(
            showlegend=False, margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=280
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'<div style="text-align:center;font-size:13px;color:#666;">100.00%</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="sk-card">
          <b>Distribución actual</b>
          <table style="width:100%;margin-top:10px;font-size:13px;">
            <tr style="background:#f5f5f5;"><th style="text-align:left;padding:6px;">Fondo</th>
            <th style="text-align:right;padding:6px;">% / Valor</th></tr>
        """, unsafe_allow_html=True)
        for f in fondos:
            st.markdown(f"""
            <tr>
              <td style="padding:6px;">{f['nombre']}</td>
              <td style="text-align:right;padding:6px;">{f['pct']:.2f}% / ${f['valor']:,.2f}</td>
            </tr>
            """, unsafe_allow_html=True)
        st.markdown("</table></div>", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="sk-card" style="text-align:center;">
          <div style="color:#666;font-size:13px;">Perfil de riesgo</div>
          <div style="font-size:22px;font-weight:700;">{cliente.get('perfil_riesgo','Moderado')}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("✏️ Cambiar perfil de inversión", use_container_width=True):
            escenario = st.session_state.get("escenario_demo", "libre")
            if escenario == "C":
                log_accion("Intento de cambio de perfil — ERR011 activado")
                activar_error("ERR011", "Mi Portafolio")
                st.rerun()
            else:
                st.success("✅ Cuestionario de perfil abierto. Completa las preguntas para actualizar tu perfil.")

    if st.session_state.get("chatbot_activo"):
        st.markdown("---")
        from modules.chatbot import render_chatbot
        render_chatbot()

    if st.session_state.get("tecnico_conectado"):
        st.markdown("---")
        from modules.tecnico import render_tecnico
        render_tecnico()


# ── DOCUMENTOS ───────────────────────────────────────────────────────────────

def render_documentos():
    st.markdown(header_html("Portal Clientes"), unsafe_allow_html=True)

    st.markdown(f"""
    <div style="padding:16px 0 8px 0;">
      <h2 style="color:{GRAY_DARK};">Documentos y Certificados</h2>
      <p style="color:#666;">Descarga tus extractos, certificados y demás documentos.</p>
    </div>
    """, unsafe_allow_html=True)

    docs = [
        {"nombre": "Certificado de aportes 2025", "tipo": "PDF", "fecha": "Ene 2026", "disponible": True},
        {"nombre": "Extracto Q1 2026", "tipo": "PDF", "fecha": "Abr 2026", "disponible": True},
        {"nombre": "Certificado de aportes 2026 (año en curso)", "tipo": "PDF", "fecha": "Pendiente", "disponible": False},
        {"nombre": "Constancia de afiliación", "tipo": "PDF", "fecha": "May 2026", "disponible": True},
    ]

    for doc in docs:
        col1, col2 = st.columns([4, 1])
        with col1:
            badge = '<span class="badge-ok">Disponible</span>' if doc["disponible"] else '<span class="badge-warn">No disponible</span>'
            st.markdown(f"""
            <div class="sk-card" style="padding:12px 16px;">
              <div style="display:flex;justify-content:space-between;">
                <div><b>📄 {doc['nombre']}</b><br/>
                     <span style="font-size:12px;color:#666;">{doc['tipo']} · {doc['fecha']}</span></div>
                <div>{badge}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if doc["disponible"]:
                if st.button("⬇️ Descargar", key=f"dl_{doc['nombre']}", use_container_width=True):
                    log_accion(f"Descarga solicitada: {doc['nombre']}")
                    st.success(f"✅ {doc['nombre']} descargado correctamente.")
            else:
                if st.button("⬇️ Descargar", key=f"dl_{doc['nombre']}", disabled=True, use_container_width=True):
                    pass
                if st.button("ℹ️ ¿Por qué no está?", key=f"info_{doc['nombre']}", use_container_width=True):
                    activar_error("ERR012", "Documentos")
                    st.rerun()

    if st.session_state.get("chatbot_activo"):
        st.markdown("---")
        from modules.chatbot import render_chatbot
        render_chatbot()

    if st.session_state.get("tecnico_conectado"):
        st.markdown("---")
        from modules.tecnico import render_tecnico
        render_tecnico()


# ── MIS DATOS ────────────────────────────────────────────────────────────────

def render_mis_datos():
    st.markdown(header_html("Portal Clientes"), unsafe_allow_html=True)
    cliente = st.session_state.get("cliente_activo", {})

    st.markdown(f"""
    <div style="padding:16px 0 8px 0;">
      <h2 style="color:{GRAY_DARK};">Mis Datos Personales</h2>
      <p style="color:#666;">Actualiza tu información de contacto y datos personales.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_datos"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre completo", value=cliente.get("nombre", ""))
            email = st.text_input("Correo electrónico", value=cliente.get("email", ""))
        with col2:
            telefono = st.text_input("Teléfono celular", value=cliente.get("telefono", ""))
            doc = st.text_input("Número de documento", value=cliente.get("documento", ""), disabled=True)

        st.caption("ℹ️ El número de documento no puede modificarse directamente. Contacta a tu FP para cambios.")
        guardar = st.form_submit_button("💾 Guardar cambios", use_container_width=True)

    if guardar:
        escenario = st.session_state.get("escenario_demo", "libre")
        if escenario in ["B", "C"]:
            log_accion("Intento de actualización de datos — ERR004 activado")
            activar_error("ERR004", "Mis Datos")
            st.rerun()
        else:
            st.session_state.cliente_activo["email"] = email
            st.session_state.cliente_activo["telefono"] = telefono
            log_accion("Datos personales actualizados exitosamente")
            st.success("✅ Tus datos fueron actualizados correctamente.")

    if st.session_state.get("chatbot_activo"):
        st.markdown("---")
        from modules.chatbot import render_chatbot
        render_chatbot()
