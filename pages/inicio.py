"""Página de inicio — dashboard personal del cliente."""

import streamlit as st
from config.brand import GREEN, GRAY_DARK, header_html
from modules.session_manager import log_accion


def render_inicio():
    st.markdown(header_html("Portal Clientes"), unsafe_allow_html=True)

    cliente = st.session_state.get("cliente_activo", {})
    nombre = cliente.get("nombre", "Cliente")

    # Saludo
    st.markdown(f"""
    <div style="padding:20px 0 8px 0;">
      <h2 style="color:{GRAY_DARK};margin-bottom:4px;">¡Hola, {nombre.split()[0]}! 👋</h2>
      <p style="color:#666;">Bienvenido a tu Portal Skandia. Aquí tienes un resumen de tu situación financiera.</p>
    </div>
    """, unsafe_allow_html=True)

    # Tabs de productos
    tab1, tab2, tab3 = st.tabs(["💼 Ahorro e Inversión", "🏛️ Pensión Obligatoria y Cesantías", "🛡️ Pólizas de Seguros"])

    with tab1:
        _render_tab_ahorro(cliente)
    with tab2:
        _render_tab_pension(cliente)
    with tab3:
        st.info("No tienes pólizas de seguros activas en este momento.")


def _render_tab_ahorro(cliente):
    saldo = cliente.get("saldo_ahorro", 0)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="sk-card" style="text-align:center;">
          <div style="color:#666;font-size:13px;">Ahorro e Inversión</div>
          <div style="color:{GREEN};font-size:24px;font-weight:700;">${saldo:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="sk-card" style="text-align:center;">
          <div style="color:#666;font-size:13px;">Último aporte</div>
          <div style="color:{GREEN};font-size:22px;font-weight:700;">$2.000.000</div>
          <div style="color:#999;font-size:12px;">02 Mar 2026</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="sk-card" style="text-align:center;">
          <div style="color:#666;font-size:13px;">Perfil de riesgo</div>
          <div style="font-size:22px;font-weight:700;color:{GRAY_DARK};">{cliente.get('perfil_riesgo','N/A')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Tabla de contratos
    st.markdown(f"""
    <div class="sk-card">
      <div style="display:flex;justify-content:space-between;margin-bottom:12px;">
        <b>Mis contratos</b>
        <span style="color:#999;font-size:12px;">Saldos actualizados al 07 de mayo de 2026</span>
      </div>
      <table style="width:100%;border-collapse:collapse;">
        <thead>
          <tr style="border-bottom:1px solid #eee;">
            <th style="text-align:left;padding:8px;font-size:13px;color:#666;">CONTRATO</th>
            <th style="text-align:right;padding:8px;font-size:13px;color:{GREEN};">SALDO TOTAL</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="padding:10px 8px;">
              <div style="font-size:12px;color:#999;">{cliente.get('contrato_num','100006674636')} — Potencializar mi inversión</div>
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

    # Accesos rápidos
    st.markdown("**Acciones rápidas:**")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("💰 Hacer Retiro", use_container_width=True):
            st.session_state.pagina_activa = "retiros"
            log_accion("Navegó a Retiros desde inicio")
            st.rerun()
    with c2:
        if st.button("⬆️ Hacer Aporte", use_container_width=True):
            st.session_state.pagina_activa = "aportes"
            log_accion("Navegó a Aportes desde inicio")
            st.rerun()
    with c3:
        if st.button("📊 Mi Portafolio", use_container_width=True):
            st.session_state.pagina_activa = "portafolio"
            log_accion("Navegó a Portafolio desde inicio")
            st.rerun()
    with c4:
        if st.button("📄 Documentos", use_container_width=True):
            st.session_state.pagina_activa = "documentos"
            log_accion("Navegó a Documentos desde inicio")
            st.rerun()


def _render_tab_pension(cliente):
    saldo_pension = cliente.get("saldo_pension", 0)
    st.markdown(f"""
    <div class="sk-card" style="text-align:center;max-width:400px;margin:auto;">
      <div style="color:#666;font-size:13px;">Pensión Obligatoria y Cesantías</div>
      <div style="color:{GREEN};font-size:28px;font-weight:700;">${saldo_pension:,.2f}</div>
      <div style="color:#999;font-size:12px;margin-top:8px;">Saldo actualizado al 07/05/2026</div>
    </div>
    """, unsafe_allow_html=True)
