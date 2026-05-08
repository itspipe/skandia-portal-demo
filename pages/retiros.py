"""Página de Retiros — flujo completo en 3 pasos basado en el portal de producción."""

import streamlit as st
from config.brand import GREEN, GRAY_DARK, RED_ALERT, YELLOW_WARN, header_html
from modules.session_manager import log_accion, activar_error
from data.base_conocimiento import ESCENARIOS_ERROR


def render_retiros():
    st.markdown(header_html("Portal Clientes"), unsafe_allow_html=True)
    st.markdown("← [Inicio](#)", unsafe_allow_html=True)

    cliente = st.session_state.get("cliente_activo", {})
    paso = st.session_state.get("retiro_paso", 1)

    # Layout: columna izquierda decorativa + columna derecha con formulario
    col_izq, col_der = st.columns([2, 3])

    with col_izq:
        st.markdown(f"""
        <div class="col-left-green">
          <div style="font-size:72px;margin-bottom:16px;">💼</div>
          <h3 style="color:{GRAY_DARK};">Retiros</h3>
          <p style="color:#555;text-align:center;font-size:14px;">
            Gestiona el desembolso de tu dinero de forma ágil, fácil y segura.
          </p>
          <br/>
          <a href="#" style="color:{GREEN};font-size:13px;text-decoration:none;">⓪ Ayuda</a>
        </div>
        """, unsafe_allow_html=True)

    with col_der:
        _barra_progreso(paso)

        if paso == 1:
            _paso1(cliente)
        elif paso == 2:
            _paso2(cliente)
        elif paso == 3:
            _paso3(cliente)
        elif paso == 4:
            _paso_otp(cliente)

    # Historial de retiros
    st.markdown("---")
    _historial_retiros(cliente)

    # Chatbot
    if st.session_state.get("chatbot_activo"):
        from modules.chatbot import render_chatbot
        render_chatbot()

    # Técnico
    if st.session_state.get("tecnico_conectado"):
        st.markdown("---")
        from modules.tecnico import render_tecnico
        render_tecnico()


def _barra_progreso(paso: int):
    total = 3
    progress = min((paso - 1) / total, 1.0)
    labels = ["Selección", "Monto", "Confirmación"]
    cols = st.columns(total)
    for i, (col, label) in enumerate(zip(cols, labels)):
        with col:
            color = GREEN if i < paso else "#ddd"
            st.markdown(
                f'<div style="height:6px;background:{color};border-radius:3px;"></div>'
                f'<div style="font-size:11px;color:{"#2D2926" if i<paso else "#999"};text-align:center;margin-top:4px;">{label}</div>',
                unsafe_allow_html=True
            )
    st.caption(f"Paso {min(paso, total)} de {total}")
    st.markdown("<br/>", unsafe_allow_html=True)


def _paso1(cliente):
    st.markdown("### ¿De dónde vas a retirar?")

    saldo = cliente.get("saldo_ahorro", 1414977.14)
    contrato_num = cliente.get("contrato_num", "100006674636")

    st.markdown(f"""
    <div style="border:2px solid {GREEN};border-radius:10px;padding:16px;margin:12px 0;cursor:pointer;">
      <div style="display:flex;align-items:center;gap:10px;">
        <div style="width:16px;height:16px;background:{GREEN};border-radius:50%;"></div>
        <div>
          <b>Potencializar mi inversión</b><br/>
          <span style="color:#666;font-size:13px;">P. Voluntaria | Ahorro e inversión | #{contrato_num[-6:]}</span><br/>
          <span style="font-size:13px;">Saldo total: <b>${saldo:,.2f}</b></span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    vivienda = st.toggle("¿Quieres hacer un retiro para vivienda con beneficio tributario?", value=False)
    if vivienda:
        st.info("ℹ️ Para retiros con beneficio tributario de vivienda, se requiere documentación adicional.")

    st.markdown("<br/>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancelar", key="ret_cancelar", use_container_width=True):
            st.session_state.pagina_activa = "inicio"
            st.rerun()
    with col2:
        if st.button("Empezar →", key="ret_empezar", use_container_width=True):
            st.session_state.retiro_producto = "Potencializar mi inversión"
            st.session_state.retiro_paso = 2
            log_accion("Retiro: producto seleccionado")
            st.rerun()


def _paso2(cliente):
    saldo = cliente.get("saldo_ahorro", 1414977.14)
    disponible = saldo - 4048.40

    st.markdown(f"""
    <div style="text-align:center;padding:20px 0;">
      <div style="color:#666;font-size:13px;">Saldo total en pensión voluntaria</div>
      <div style="font-size:36px;font-weight:700;color:{GRAY_DARK};">${saldo:,.2f}</div>
      <a href="#" style="color:{GREEN};font-size:13px;">Ver detalle</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**¿Qué tipo de retiro harás?**")

    tipo = st.radio(
        "",
        ["Retirar un monto específico", "Retiro total"],
        key="retiro_tipo_sel",
        label_visibility="collapsed"
    )

    if tipo == "Retirar un monto específico":
        monto = st.number_input(
            "Monto a retirar (COP)",
            min_value=5000,
            max_value=int(disponible),
            value=st.session_state.get("retiro_monto", 5000),
            step=1000,
            format="%d"
        )
        st.session_state.retiro_monto = monto
        st.caption(f"Disponible para retirar: ${disponible:,.2f}")
    else:
        st.session_state.retiro_monto = disponible
        st.info(f"Se retirará el total disponible: ${disponible:,.2f}")

    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:8px;background:#f5f5f5;
                border-radius:8px;padding:10px 14px;margin:12px 0;">
      <span>📅</span>
      <span style="font-size:13px;">Tu retiro estará disponible el <b>08/05/2026</b> después de las <b>3:00 p.m.</b>
      <a href="#" style="color:{GREEN};">Ver más</a></span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Regresar", key="ret2_back", use_container_width=True):
            st.session_state.retiro_paso = 1
            st.rerun()
    with col2:
        if st.button("Continuar →", key="ret2_cont", use_container_width=True):
            log_accion(f"Retiro: monto ingresado ${st.session_state.retiro_monto:,.0f}")
            _verificar_error_retiro(cliente)


def _verificar_error_retiro(cliente):
    """Verifica si debe disparar un error según el escenario activo."""
    escenario = st.session_state.get("escenario_demo", "libre")
    err_id = ESCENARIOS_ERROR.get(escenario, "ERR002")

    # Solo disparar errores relacionados con retiros
    errores_retiro = ["ERR001", "ERR002", "ERR003", "ERR010"]
    if err_id in errores_retiro:
        log_accion(f"Error detectado en Retiros: {err_id}")
        activar_error(err_id, "Retiros")
        st.rerun()
    else:
        # Sin error — continuar al paso 3
        st.session_state.retiro_paso = 3
        st.rerun()


def _paso3(cliente):
    saldo = cliente.get("saldo_ahorro", 1414977.14)
    monto = st.session_state.get("retiro_monto", 5000)
    cuentas = cliente.get("cuentas", [])

    # Banner de advertencia
    st.markdown(f"""
    <div style="background:{YELLOW_WARN};border:1px solid #F9A825;border-radius:8px;
                padding:10px 16px;display:flex;align-items:center;gap:8px;margin-bottom:16px;">
      ⚠️ <span style="font-size:13px;">Una vez en proceso de tramitado, <b>no se podrá modificar ni cancelar</b></span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Resumen de tu retiro")

    cuenta = cuentas[0] if cuentas else {"banco": "Banco Davivienda", "tipo": "Ahorros", "numero": "12345678991"}
    num_enmascarado = "a****" + cuenta.get("numero", "")[-4:]
    cargo = monto * 0.004
    neto = monto - cargo

    st.markdown(f"""
    <div class="sk-card">
      <table style="width:100%;font-size:14px;">
        <tr><td style="color:#666;padding:6px 0;">Especie</td>
            <td style="text-align:right;font-weight:600;">FPV Strategist Liquidez Col</td></tr>
        <tr><td style="color:#666;padding:6px 0;">Fecha esperada</td>
            <td style="text-align:right;font-weight:600;">08/05/2026</td></tr>
        <tr><td style="color:#666;padding:6px 0;">Valor del retiro</td>
            <td style="text-align:right;font-weight:600;">${monto:,.2f}</td></tr>
        <tr><td style="color:#666;padding:6px 0;">Cargos e impuestos</td>
            <td style="text-align:right;color:{RED_ALERT};">-${cargo:,.2f}</td></tr>
        <tr style="border-top:1px solid #eee;">
          <td style="font-weight:700;padding:8px 0;">Valor neto a recibir</td>
          <td style="text-align:right;font-weight:700;color:{GREEN};">${neto:,.2f}</td>
        </tr>
        <tr><td colspan="2" style="padding-top:12px;color:#666;font-size:13px;">
          <b>Destinatario:</b> {cuenta.get('banco','')} | {num_enmascarado} | {cuenta.get('tipo','')}
        </td></tr>
        <tr><td colspan="2" style="color:#666;font-size:13px;">
          <b>Titular:</b> {st.session_state.get('cliente_activo',{}).get('nombre','')}
        </td></tr>
      </table>
    </div>
    """, unsafe_allow_html=True)

    if st.button("📊 Ver impacto en portafolios", key="ver_portafolios"):
        st.markdown(f"""
        <div style="background:#fff;border:1px solid #ddd;border-radius:10px;padding:20px;margin:12px 0;">
          <b>Portafolios afectados por tu retiro</b>
          <table style="width:100%;margin-top:12px;font-size:13px;">
            <tr style="background:#f5f5f5;">
              <th style="text-align:left;padding:8px;">Portafolio</th>
              <th style="text-align:right;padding:8px;">Porcentaje</th>
            </tr>
            <tr>
              <td style="padding:8px;">FPV Strategist Liquidez Col</td>
              <td style="text-align:right;padding:8px;">100,00%</td>
            </tr>
          </table>
          <p style="font-size:12px;color:#666;margin-top:12px;">
            Los recursos se distribuirán proporcionalmente entre los Portafolios Strategist e Individuales.
          </p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Regresar", key="ret3_back", use_container_width=True):
            st.session_state.retiro_paso = 2
            st.rerun()
    with col2:
        if st.button("🔐 Solicitar código de verificación", key="ret3_otp", use_container_width=True):
            st.session_state.retiro_paso = 4
            log_accion("Solicitud de código OTP para retiro")
            st.rerun()


def _paso_otp(cliente):
    st.markdown(f"""
    <div style="text-align:center;padding:20px 0;">
      <div style="font-size:56px;margin-bottom:12px;">🔐</div>
      <h3>Validación de seguridad</h3>
      <p style="color:#666;font-size:14px;">
        Ingresa el código enviado a tu celular y correo registrados.<br/>
        Código demo: <b>123456</b>
      </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("otp_retiro"):
        codigo = st.text_input("Código de verificación", placeholder="_ _ _ _ _ _", max_chars=6)
        st.caption("⏱ 04:58 restantes")
        col1, col2 = st.columns(2)
        with col1:
            reenviar = st.form_submit_button("Reenviar código (00:28)", use_container_width=True)
        with col2:
            verificar = st.form_submit_button("Verificar ✓", use_container_width=True)

    st.markdown(f'<div style="text-align:center;"><a href="#" style="color:{GREEN};font-size:13px;">¿No has recibido el código de seguridad?</a></div>', unsafe_allow_html=True)

    if reenviar:
        st.info("Código reenviado a tu celular y correo.")
        log_accion("OTP de retiro reenviado")

    if verificar:
        if codigo == "123456":
            monto = st.session_state.get("retiro_monto", 0)
            log_accion(f"Retiro exitoso por ${monto:,.0f}")
            st.session_state.retiro_paso = 1
            st.success(f"✅ ¡Retiro procesado exitosamente! Recibirás ${monto:,.2f} el 08/05/2026 después de las 3:00 p.m.")
            st.balloons()
        else:
            st.error("Código incorrecto. Por favor intenta de nuevo.")
            activar_error("ERR017", "Validación OTP retiro")
            st.rerun()


def _historial_retiros(cliente):
    historial = cliente.get("historial", [])

    with st.expander("📋 Historial de retiros", expanded=False):
        st.caption("Aquí encontrarás el historial completo de retiros realizados.")

        if not historial:
            st.info("No tienes retiros registrados.")
            return

        for h in historial:
            estado = h.get("estado", "")
            badge_class = "badge-ok" if estado == "Procesado" else ("badge-warn" if estado == "En trámite" else "badge-err")
            monto_txt = f"${h.get('monto', 0):,.0f}" if h.get("monto", 0) > 0 else "—"
            st.markdown(f"""
            <div class="sk-card" style="padding:12px 16px;margin-bottom:8px;">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                  <b>{h.get('tipo','')}</b>
                  <div style="font-size:12px;color:#666;">{h.get('fecha','')}</div>
                </div>
                <div style="text-align:right;">
                  <div style="font-weight:600;">{monto_txt}</div>
                  <span class="{badge_class}">{estado}</span>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)
