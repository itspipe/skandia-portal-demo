"""Páginas: Portafolio, Documentos, Mis Datos."""

import streamlit as st
import plotly.graph_objects as go
from config.brand import GREEN, GRAY_DARK, sk_header
from modules.session_manager import log_accion, activar_error
from modules.chatbot import render_chatbot_flotante
from modules.tecnico import render_tecnico



def render_portafolio():
    st.markdown(sk_header("Mi Portafolio", cliente.get("nombre","")), unsafe_allow_html=True)

    if st.session_state.get("chatbot_activo"):
        render_chatbot_flotante()
        st.markdown("---")
    if st.session_state.get("tecnico_conectado"):
        render_tecnico()
        return

    cliente = st.session_state.get("cliente_activo", {})
    saldo   = cliente.get("saldo_ahorro", 1414977.14)

    st.markdown(f"<h2 style='color:{GRAY_DARK};'>Mi Portafolio</h2>", unsafe_allow_html=True)

    c1, c2 = st.columns([1,1])
    with c1:
        fig = go.Figure(go.Pie(
            labels=["FPV Strategist Liquidez Col"],
            values=[100],
            hole=0.6,
            marker=dict(colors=[GREEN]),
            textinfo="label+percent",
        ))
        fig.update_layout(showlegend=False, margin=dict(t=10,b=10,l=10,r=10),
                          paper_bgcolor="rgba(0,0,0,0)", height=260)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div style="text-align:center;font-size:13px;color:#666;">100.00%</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="sk-card">
          <b>Distribución actual</b>
          <table style="width:100%;margin-top:10px;font-size:13px;">
            <tr style="background:#f5f5f5;">
              <th style="text-align:left;padding:6px;">Fondo</th>
              <th style="text-align:right;padding:6px;">Valor</th>
            </tr>
            <tr>
              <td style="padding:6px;">FPV Strategist Liquidez Col</td>
              <td style="text-align:right;padding:6px;">${saldo:,.2f}</td>
            </tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sk-card" style="text-align:center;">
          <div style="color:#666;font-size:13px;">Perfil de riesgo</div>
          <div style="font-size:22px;font-weight:700;">{cliente.get('perfil_riesgo','Moderado')}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("✏️ Cambiar perfil de inversión", use_container_width=True):
            escenario = st.session_state.get("escenario_demo","libre")
            if escenario == "C":
                log_accion("Intento cambio perfil → ERR011 (escenario C)")
                if not st.session_state.get("error_disparado_portafolio",False): activar_error("ERR011","Mi Portafolio")
                st.rerun()
            else:
                st.success("✅ Cuestionario de perfil abierto. Completa las preguntas.")


def render_documentos():
    st.markdown(sk_header("Documentos", (st.session_state.get("cliente_activo") or {}).get("nombre","")), unsafe_allow_html=True)

    if st.session_state.get("chatbot_activo"):
        render_chatbot_flotante()
        st.markdown("---")
    if st.session_state.get("tecnico_conectado"):
        render_tecnico()
        return

    st.markdown(f"<h2 style='color:{GRAY_DARK};'>Documentos y Certificados</h2>", unsafe_allow_html=True)

    docs = [
        {"nombre":"Certificado de aportes 2025","fecha":"Ene 2026","disponible":True},
        {"nombre":"Extracto Q1 2026","fecha":"Abr 2026","disponible":True},
        {"nombre":"Certificado de aportes 2026 (año en curso)","fecha":"Pendiente","disponible":False},
        {"nombre":"Constancia de afiliación","fecha":"May 2026","disponible":True},
    ]
    for doc in docs:
        c1, c2 = st.columns([4,1])
        with c1:
            badge = '<span class="badge-ok">Disponible</span>' if doc["disponible"] else '<span class="badge-warn">No disponible</span>'
            st.markdown(f"""
            <div class="sk-card" style="padding:12px 16px;">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div><b>📄 {doc['nombre']}</b><br/>
                     <span style="font-size:12px;color:#666;">{doc['fecha']}</span></div>
                <div>{badge}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            if doc["disponible"]:
                if st.button("⬇️", key=f"dl_{doc['nombre'][:10]}", use_container_width=True):
                    st.success(f"✅ {doc['nombre']} descargado.")
                    log_accion(f"Descargó: {doc['nombre']}")
            else:
                if st.button("ℹ️", key=f"inf_{doc['nombre'][:10]}", use_container_width=True):
                    activar_error("ERR012","Documentos")
                    st.rerun()


def render_mis_datos():
    st.markdown(sk_header("Mis Datos", cliente.get("nombre","")), unsafe_allow_html=True)

    if st.session_state.get("chatbot_activo"):
        render_chatbot_flotante()
        st.markdown("---")
    if st.session_state.get("tecnico_conectado"):
        render_tecnico()
        return

    cliente = st.session_state.get("cliente_activo",{})
    st.markdown(f"<h2 style='color:{GRAY_DARK};'>Mis Datos Personales</h2>", unsafe_allow_html=True)

    with st.form("form_datos"):
        c1, c2 = st.columns(2)
        with c1:
            nombre  = st.text_input("Nombre completo", value=cliente.get("nombre",""))
            email   = st.text_input("Correo electrónico", value=cliente.get("email",""))
        with c2:
            telefono = st.text_input("Teléfono celular", value=cliente.get("telefono",""))
            st.text_input("Número de documento", value=cliente.get("documento",""), disabled=True)

        st.caption("ℹ️ El número de documento no puede modificarse directamente.")
        guardar = st.form_submit_button("💾 Guardar cambios", use_container_width=True)

    if guardar:
        escenario = st.session_state.get("escenario_demo","libre")
        if escenario in ["B","C"]:
            log_accion("Intento actualización datos → ERR004")
            activar_error("ERR004","Mis Datos")
            st.rerun()
        else:
            st.session_state.cliente_activo["email"]    = email
            st.session_state.cliente_activo["telefono"] = telefono
            log_accion("Datos actualizados exitosamente")
            st.success("✅ Datos actualizados correctamente.")
