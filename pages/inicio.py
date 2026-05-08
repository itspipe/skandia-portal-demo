"""Página de inicio — dashboard personal del cliente con visual mejorado."""
import streamlit as st
from config.brand import GREEN, GRAY_DARK
from modules.session_manager import log_accion
from modules.chatbot import render_chatbot_flotante
from modules.tecnico import render_tecnico


def _header(cliente):
    nombre = cliente.get("nombre","")
    st.markdown(f"""
    <div style="background:#fff;border-top:4px solid #003087;padding:12px 28px;
        margin:-0.25rem -1rem 20px -1rem;
        box-shadow:0 2px 12px rgba(0,0,0,0.08);
        display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
      <span style="color:#00D261;font-size:24px;font-weight:900;">✦</span>
      <span style="font-size:20px;font-weight:700;color:#2D2926;">skandia</span>
      <span style="width:1px;height:24px;background:#e0e0e0;margin:0 8px;"></span>
      <span style="font-size:13px;color:#666;">Portal Clientes</span>
      <span style="margin-left:auto;font-size:13px;color:#666;">👤 {nombre}</span>
    </div>
    """, unsafe_allow_html=True)


def render_inicio():
    cliente = st.session_state.get("cliente_activo", {})
    _header(cliente)

    if st.session_state.get("chatbot_activo"):
        render_chatbot_flotante()
        st.markdown("---")
    if st.session_state.get("tecnico_conectado"):
        render_tecnico()
        return

    nombre     = cliente.get("nombre","Cliente")
    primer_n   = nombre.split()[0]
    saldo_inv  = cliente.get("saldo_ahorro", 1414977.14)
    saldo_pen  = cliente.get("saldo_pension", 0)
    perfil     = cliente.get("perfil_riesgo","Moderado")

    # ── Banner de bienvenida personalizado ────────────────────────────────
    import datetime
    hora = datetime.datetime.now().hour
    saludo = "Buenos días" if hora < 12 else ("Buenas tardes" if hora < 18 else "Buenas noches")

    st.markdown(f"""
    <div class="welcome-banner slide-in">
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
        <div>
          <div style="font-size:22px;font-weight:700;margin-bottom:4px;">
            {saludo}, {primer_n}! 👋
          </div>
          <div style="opacity:0.85;font-size:14px;">
            Bienvenido a tu Portal Skandia. Aquí tienes el resumen de tu situación financiera.
          </div>
        </div>
        <div style="text-align:right;">
          <div style="font-size:11px;opacity:0.7;">Contrato</div>
          <div style="font-weight:600;font-size:14px;">{cliente.get('contrato','')}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Métricas rápidas ──────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    metricas = [
        ("💼","Ahorro e Inversión", f"${saldo_inv:,.0f}", None),
        ("🏛️","Pensión Obligatoria", f"${saldo_pen:,.0f}", None),
        ("📊","Perfil de riesgo", perfil, None),
        ("✅","Estado del contrato","Activo","green"),
    ]
    colores = [None, None, None, "green"]
    for col, (ico, tit, val, color) in zip([m1,m2,m3,m4], metricas):
        extra = f"border-top-color:{'#00D261' if color=='green' else '#003087'};"
        with col:
            st.markdown(f"""
            <div class="metric-card" style="{extra}">
              <div style="font-size:24px;margin-bottom:6px;">{ico}</div>
              <div style="font-size:11px;color:#888;font-weight:500;text-transform:uppercase;
                   letter-spacing:0.5px;">{tit}</div>
              <div style="font-size:16px;font-weight:700;color:#2D2926;margin-top:4px;">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["💼 Ahorro e Inversión","🏛️ Pensión Obligatoria","🛡️ Pólizas de Seguros"])

    with tab1:
        _tab_ahorro(cliente)
    with tab2:
        _tab_pension(cliente)
    with tab3:
        st.markdown("""
        <div class="sk-card" style="text-align:center;padding:40px;">
          <div style="font-size:48px;margin-bottom:12px;">🛡️</div>
          <b>Sin pólizas activas</b>
          <p style="color:#888;margin-top:8px;">No tienes pólizas de seguros vinculadas a este contrato.</p>
        </div>
        """, unsafe_allow_html=True)


def _tab_ahorro(cliente):
    saldo = cliente.get("saldo_ahorro", 1414977.14)
    cn    = cliente.get("contrato_num","100006674636")

    st.markdown(f"""
    <div class="sk-card">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
        <b style="font-size:15px;">Mis contratos</b>
        <span style="color:#999;font-size:12px;">
          🕐 Actualizado al 07 de mayo de 2026
        </span>
      </div>
      <table style="width:100%;border-collapse:collapse;">
        <thead>
          <tr style="border-bottom:2px solid #f0f0f0;">
            <th style="text-align:left;padding:8px 6px;font-size:12px;color:#999;font-weight:500;">CONTRATO</th>
            <th style="text-align:right;padding:8px 6px;font-size:12px;color:#00D261;font-weight:500;">SALDO TOTAL</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="padding:12px 6px;">
              <div style="font-size:11px;color:#aaa;">{cn} — Potencializar mi inversión</div>
              <div style="font-weight:600;font-size:14px;color:#2D2926;margin-top:3px;">Pensiones Voluntarias</div>
              <div style="font-size:12px;color:#888;">Skandia Inversión Plus</div>
            </td>
            <td style="padding:12px 6px;text-align:right;">
              <div style="font-weight:700;font-size:16px;color:#00D261;">${saldo:,.2f}</div>
            </td>
          </tr>
          <tr style="border-top:2px solid #f5f5f5;background:linear-gradient(135deg,#F1FFF7,#fff);">
            <td style="padding:10px 6px;font-weight:700;color:#00D261;">SALDO TOTAL</td>
            <td style="padding:10px 6px;text-align:right;font-weight:700;font-size:17px;color:#00D261;">${saldo:,.2f}</td>
          </tr>
        </tbody>
      </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ¿Qué quieres hacer hoy?")
    a1, a2, a3, a4 = st.columns(4)
    acciones = [
        ("a1","💰","Hacer Retiro","retiros"),
        ("a2","⬆️","Hacer Aporte",None),
        ("a3","📊","Mi Portafolio","portafolio"),
        ("a4","📄","Documentos","documentos"),
    ]
    for col, (key, ico, label, pagina) in zip([a1,a2,a3,a4], acciones):
        with col:
            if st.button(f"{ico}\n{label}", key=f"home_{key}", use_container_width=True):
                if pagina:
                    st.session_state.pagina_activa = pagina
                    log_accion(f"Navegó a {pagina} desde inicio")
                    st.rerun()
                else:
                    st.info("Módulo próximamente disponible.")


def _tab_pension(cliente):
    sp = cliente.get("saldo_pension",0)
    st.markdown(f"""
    <div class="sk-card" style="text-align:center;padding:32px;max-width:400px;margin:auto;">
      <div style="font-size:40px;margin-bottom:10px;">🏛️</div>
      <div style="color:#888;font-size:13px;">Pensión Obligatoria y Cesantías</div>
      <div style="color:#00D261;font-size:28px;font-weight:700;margin:8px 0;">${sp:,.2f}</div>
      <div style="color:#aaa;font-size:12px;">Saldo actualizado al 07/05/2026</div>
    </div>
    """, unsafe_allow_html=True)
