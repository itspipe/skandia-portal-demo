"""Página de inicio — dashboard personal del cliente."""

import streamlit as st
from config.brand import GREEN, GRAY_DARK
from modules.session_manager import log_accion
from modules.chatbot import render_chatbot_flotante
from modules.tecnico import render_tecnico


def render_inicio():
    st.markdown(f"""
    <div style="background:#fff;border-top:4px solid #003087;padding:12px 24px;
                margin:-0.5rem -1rem 16px -1rem;box-shadow:0 2px 8px rgba(0,0,0,0.08);
                display:flex;align-items:center;gap:8px;">
      <span style="color:{GREEN};font-size:22px;font-weight:900;">✦</span>
      <span style="font-size:19px;font-weight:700;">skandia</span>
      <span style="width:1px;height:22px;background:#ddd;margin:0 10px;"></span>
      <span style="font-size:13px;color:#666;">Portal Clientes</span>
    </div>
    """, unsafe_allow_html=True)

    # Chatbot si hay error activo (volvió de otro módulo)
    if st.session_state.get("chatbot_activo"):
        render_chatbot_flotante()
        st.markdown("---")
    if st.session_state.get("tecnico_conectado"):
        render_tecnico()
        return

    cliente = st.session_state.get("cliente_activo", {})
    nombre  = cliente.get("nombre", "Cliente")

    st.markdown(f"""
    <div style="padding:8px 0 16px 0;">
      <h2 style="color:{GRAY_DARK};margin-bottom:4px;">¡Hola, {nombre.split()[0]}! 👋</h2>
      <p style="color:#666;">Bienvenido a tu Portal Skandia. Aquí tienes el resumen de tu situación financiera.</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["💼 Ahorro e Inversión","🏛️ Pensión Obligatoria","🛡️ Pólizas de Seguros"])

    with tab1:
        _tab_ahorro(cliente)
    with tab2:
        _tab_pension(cliente)
    with tab3:
        st.info("No tienes pólizas de seguros activas en este momento.")


def _tab_ahorro(cliente):
    saldo = cliente.get("saldo_ahorro", 1414977.14)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="sk-card" style="text-align:center;">
          <div style="color:#666;font-size:13px;">Ahorro e Inversión</div>
          <div style="color:{GREEN};font-size:22px;font-weight:700;">${saldo:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="sk-card" style="text-align:center;">
          <div style="color:#666;font-size:13px;">Último aporte</div>
          <div style="font-size:20px;font-weight:700;color:{GREEN};">$2.000.000</div>
          <div style="color:#999;font-size:12px;">02 Mar 2026</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="sk-card" style="text-align:center;">
          <div style="color:#666;font-size:13px;">Perfil de riesgo</div>
          <div style="font-size:20px;font-weight:700;color:{GRAY_DARK};">{cliente.get('perfil_riesgo','Moderado')}</div>
        </div>
        """, unsafe_allow_html=True)

    contrato_n = cliente.get("contrato_num","100006674636")
    st.markdown(f"""
    <div class="sk-card">
      <div style="display:flex;justify-content:space-between;margin-bottom:10px;">
        <b>Mis contratos</b>
        <span style="color:#999;font-size:12px;">Saldos actualizados al 07 de mayo de 2026</span>
      </div>
      <table style="width:100%;border-collapse:collapse;">
        <thead><tr style="border-bottom:1px solid #eee;">
          <th style="text-align:left;padding:8px;font-size:12px;color:#666;">CONTRATO</th>
          <th style="text-align:right;padding:8px;font-size:12px;color:{GREEN};">SALDO TOTAL</th>
        </tr></thead>
        <tbody>
          <tr>
            <td style="padding:10px 8px;">
              <div style="font-size:12px;color:#999;">{contrato_n} — Potencializar mi inversión</div>
              <div style="font-weight:600;">Pensiones Voluntarias</div>
              <div style="font-size:12px;color:#666;">Skandia Inversión Plus</div>
            </td>
            <td style="padding:10px 8px;text-align:right;font-weight:600;">${saldo:,.2f}</td>
          </tr>
          <tr style="border-top:1px solid #eee;">
            <td style="padding:10px 8px;color:{GREEN};font-weight:700;">SALDO TOTAL</td>
            <td style="padding:10px 8px;text-align:right;color:{GREEN};font-weight:700;">${saldo:,.2f}</td>
          </tr>
        </tbody>
      </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Acciones rápidas:**")
    a1, a2, a3, a4 = st.columns(4)
    with a1:
        if st.button("💰 Hacer Retiro", use_container_width=True, key="inicio_retiro"):
            st.session_state.pagina_activa = "retiros"
            log_accion("Navegó a Retiros desde inicio")
            st.rerun()
    with a2:
        if st.button("⬆️ Hacer Aporte", use_container_width=True, key="inicio_aporte"):
            st.info("Módulo de Aportes próximamente.")
    with a3:
        if st.button("📊 Portafolio", use_container_width=True, key="inicio_port"):
            st.session_state.pagina_activa = "portafolio"
            log_accion("Navegó a Portafolio desde inicio")
            st.rerun()
    with a4:
        if st.button("📄 Documentos", use_container_width=True, key="inicio_docs"):
            st.session_state.pagina_activa = "documentos"
            log_accion("Navegó a Documentos desde inicio")
            st.rerun()


def _tab_pension(cliente):
    saldo_p = cliente.get("saldo_pension", 0)
    st.markdown(f"""
    <div class="sk-card" style="text-align:center;max-width:380px;margin:auto;">
      <div style="color:#666;font-size:13px;">Pensión Obligatoria y Cesantías</div>
      <div style="color:{GREEN};font-size:26px;font-weight:700;">${saldo_p:,.2f}</div>
      <div style="color:#999;font-size:12px;margin-top:6px;">Saldo actualizado al 07/05/2026</div>
    </div>
    """, unsafe_allow_html=True)
