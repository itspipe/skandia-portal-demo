"""Página de Retiros — flujo completo 3 pasos con errores por escenario."""

import streamlit as st
from config.brand import GREEN, GRAY_DARK, RED_ALERT, YELLOW_WARN
from modules.session_manager import log_accion, activar_error
from modules.chatbot import render_chatbot_flotante
from modules.tecnico import render_tecnico

ERRORES_POR_ESCENARIO = {
    "A":     "ERR001",   # cuenta bancaria no inscrita
    "B":     "ERR002",   # fondos insuficientes
    "C":     "ERR003",   # perfil vencido
    "libre": "ERR002",
}


def render_retiros():
    # ── Header ──────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="background:#fff;border-top:4px solid #003087;padding:12px 24px;
                margin:-0.5rem -1rem 16px -1rem;box-shadow:0 2px 8px rgba(0,0,0,0.08);
                display:flex;align-items:center;gap:8px;">
      <span style="color:{GREEN};font-size:22px;font-weight:900;">✦</span>
      <span style="font-size:19px;font-weight:700;">skandia</span>
      <span style="width:1px;height:22px;background:#ddd;margin:0 10px;"></span>
      <span style="font-size:13px;color:#666;">Portal Clientes</span>
      <span style="margin-left:auto;font-size:13px;color:{GREEN};">💰 Retiros</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Chatbot PRIMERO si hay error ─────────────────────────────────────
    if st.session_state.get("chatbot_activo"):
        render_chatbot_flotante()
        st.markdown("---")

    # ── Técnico si está conectado ─────────────────────────────────────────
    if st.session_state.get("tecnico_conectado"):
        render_tecnico()
        return

    # ── Caso resuelto ─────────────────────────────────────────────────────
    if st.session_state.get("caso_resuelto") and not st.session_state.get("error_activo"):
        st.markdown(f"""
        <div class="sk-card-success">
          <div style="font-size:18px;font-weight:700;color:{GREEN};">✅ ¡Inconveniente resuelto!</div>
          <p>Ya puedes continuar con tu retiro. El proceso está habilitado.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💰 Continuar con mi retiro", use_container_width=True):
            st.session_state.caso_resuelto = False
            st.session_state.retiro_paso   = 2
            st.rerun()
        return

    cliente = st.session_state.get("cliente_activo", {})
    paso    = st.session_state.get("retiro_paso", 1)

    col_izq, col_der = st.columns([2, 3])

    with col_izq:
        st.markdown(f"""
        <div class="col-left-green">
          <div style="font-size:64px;margin-bottom:12px;">💼</div>
          <h3 style="color:{GRAY_DARK};">Retiros</h3>
          <p style="color:#555;font-size:14px;text-align:center;">
            Gestiona el desembolso de tu dinero de forma ágil, fácil y segura.
          </p>
          <br/>
          <a href="#" style="color:{GREEN};font-size:13px;">⓪ Ayuda</a>
        </div>
        """, unsafe_allow_html=True)

    with col_der:
        _barra(paso)
        if paso == 1:
            _paso1(cliente)
        elif paso == 2:
            _paso2(cliente)
        elif paso == 3:
            _paso3(cliente)
        elif paso == 4:
            _paso_otp(cliente)

    # ── Historial ─────────────────────────────────────────────────────────
    st.markdown("---")
    with st.expander("📋 Historial de retiros", expanded=False):
        historial = cliente.get("historial", [])
        if not historial:
            st.info("No tienes retiros registrados.")
        else:
            for h in historial:
                est = h.get("estado", "")
                bc  = "badge-ok" if est == "Procesado" else ("badge-warn" if est == "En trámite" else "badge-err")
                monto_txt = f"${h.get('monto',0):,.0f}" if h.get("monto", 0) > 0 else "—"
                st.markdown(f"""
                <div class="sk-card" style="padding:10px 16px;margin-bottom:6px;">
                  <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div><b>{h.get('tipo','')}</b>
                      <div style="font-size:12px;color:#666;">{h.get('fecha','')}</div>
                    </div>
                    <div style="text-align:right;">
                      <b>{monto_txt}</b><br/><span class="{bc}">{est}</span>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)


def _barra(paso):
    labels = ["Selección", "Monto y tipo", "Confirmación"]
    cols   = st.columns(3)
    for i, (c, lbl) in enumerate(zip(cols, labels)):
        with c:
            color = GREEN if i < paso else "#ddd"
            txt_c = "#2D2926" if i < paso else "#aaa"
            st.markdown(
                f'<div style="height:6px;background:{color};border-radius:3px;"></div>'
                f'<div style="font-size:11px;color:{txt_c};text-align:center;margin-top:3px;">{lbl}</div>',
                unsafe_allow_html=True,
            )
    st.caption(f"Paso {min(paso,3)} de 3")
    st.markdown("<br/>", unsafe_allow_html=True)


def _paso1(cliente):
    st.markdown("### ¿De dónde vas a retirar?")
    saldo       = cliente.get("saldo_ahorro", 1414977.14)
    contrato_n  = cliente.get("contrato_num", "100006674636")

    st.markdown(f"""
    <div style="border:2px solid {GREEN};border-radius:10px;padding:16px;
                margin:10px 0;background:#fff;cursor:pointer;">
      <div style="display:flex;align-items:center;gap:10px;">
        <div style="width:14px;height:14px;background:{GREEN};border-radius:50%;flex-shrink:0;"></div>
        <div>
          <b>Potencializar mi inversión</b><br/>
          <span style="color:#666;font-size:13px;">P. Voluntaria | Ahorro e inversión | #{contrato_n[-6:]}</span><br/>
          <span style="font-size:13px;">Saldo total: <b>${saldo:,.2f}</b></span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    vivienda = st.toggle("¿Retiro para vivienda con beneficio tributario?", value=False)
    if vivienda:
        st.info("ℹ️ Para retiros con beneficio tributario se requiere documentación adicional.")

    st.markdown("<br/>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Cancelar", key="r1_cancel", use_container_width=True):
            st.session_state.pagina_activa = "inicio"
            st.rerun()
    with c2:
        if st.button("Empezar →", key="r1_start", use_container_width=True):
            st.session_state.retiro_producto = "Potencializar mi inversión"
            st.session_state.retiro_paso     = 2
            log_accion("Retiro: producto seleccionado")
            st.rerun()


def _paso2(cliente):
    saldo      = cliente.get("saldo_ahorro", 1414977.14)
    disponible = saldo - 4048.40

    st.markdown(f"""
    <div style="text-align:center;padding:16px 0 8px;">
      <div style="color:#666;font-size:13px;">Saldo total en pensión voluntaria</div>
      <div style="font-size:34px;font-weight:700;color:{GRAY_DARK};">${saldo:,.2f}</div>
      <a href="#" style="color:{GREEN};font-size:13px;">Ver detalle</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**¿Qué tipo de retiro harás?**")
    tipo = st.radio(
        "", ["Retirar un monto específico", "Retiro total"],
        key="r2_tipo", label_visibility="collapsed",
    )
    if tipo == "Retirar un monto específico":
        monto = st.number_input(
            "Monto a retirar (COP)",
            min_value=5000, max_value=int(disponible),
            value=st.session_state.get("retiro_monto", 5000),
            step=1000, format="%d",
        )
        st.session_state.retiro_monto = monto
        st.caption(f"Disponible para retirar: ${disponible:,.2f}")
    else:
        st.session_state.retiro_monto = disponible
        st.info(f"Se retirará el total disponible: ${disponible:,.2f}")

    st.markdown(f"""
    <div style="background:#f5f5f5;border-radius:8px;padding:10px 14px;margin:10px 0;font-size:13px;">
      📅 Tu retiro estará disponible el <b>08/05/2026</b> después de las <b>3:00 p.m.</b>
      <a href="#" style="color:{GREEN};">Ver más</a>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Regresar", key="r2_back", use_container_width=True):
            st.session_state.retiro_paso = 1
            st.rerun()
    with c2:
        if st.button("Continuar →", key="r2_cont", use_container_width=True):
            log_accion(f"Retiro: monto ingresado ${st.session_state.retiro_monto:,.0f}")
            _disparar_error_o_continuar()


def _disparar_error_o_continuar():
    """Dispara el error del escenario activo o avanza al paso 3."""
    escenario = st.session_state.get("escenario_demo", "libre")
    err_id    = ERRORES_POR_ESCENARIO.get(escenario, "ERR002")

    # Escenario libre sin error definido → pasar al paso 3
    if escenario == "libre" and not st.session_state.get("forzar_error"):
        st.session_state.retiro_paso = 3
        st.rerun()
        return

    log_accion(f"Error disparado en Retiros: {err_id} (escenario {escenario})")
    activar_error(err_id, "Retiros")
    st.rerun()


def _paso3(cliente):
    saldo  = cliente.get("saldo_ahorro", 1414977.14)
    monto  = st.session_state.get("retiro_monto", 5000)
    cuentas = cliente.get("cuentas", [])

    # Advertencia
    st.markdown(f"""
    <div style="background:#FFF8E1;border:1px solid #F9A825;border-radius:8px;
                padding:10px 16px;margin-bottom:14px;font-size:13px;">
      ⚠️ Una vez en proceso de tramitado <b>no se podrá modificar ni cancelar</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Resumen de tu retiro")

    if cuentas:
        cuenta = cuentas[0]
    else:
        cuenta = {"banco": "Sin cuenta inscrita", "tipo": "—", "numero": "——"}

    num_e  = cuenta.get("numero", "")
    num_m  = ("a****" + num_e[-4:]) if len(num_e) >= 4 else "—"
    cargo  = monto * 0.004
    neto   = monto - cargo

    st.markdown(f"""
    <div class="sk-card">
      <table style="width:100%;font-size:14px;border-collapse:collapse;">
        <tr><td style="color:#666;padding:6px 0;">Especie</td>
            <td style="text-align:right;font-weight:600;">FPV Strategist Liquidez Col</td></tr>
        <tr><td style="color:#666;padding:6px 0;">Fecha esperada</td>
            <td style="text-align:right;font-weight:600;">08/05/2026</td></tr>
        <tr><td style="color:#666;padding:6px 0;">Valor del retiro</td>
            <td style="text-align:right;font-weight:600;">${monto:,.2f}</td></tr>
        <tr><td style="color:#666;padding:6px 0;">Cargos e impuestos</td>
            <td style="text-align:right;color:{RED_ALERT};">−${cargo:,.2f}</td></tr>
        <tr style="border-top:2px solid #eee;">
          <td style="font-weight:700;padding:8px 0;">Valor neto</td>
          <td style="text-align:right;font-weight:700;color:{GREEN};">${neto:,.2f}</td>
        </tr>
        <tr><td colspan="2" style="padding-top:12px;font-size:13px;color:#666;">
          <b>Destinatario:</b> {cuenta['banco']} | {num_m} | {cuenta['tipo']}
        </td></tr>
        <tr><td colspan="2" style="font-size:13px;color:#666;">
          <b>Titular:</b> {cliente.get('nombre','')}
        </td></tr>
      </table>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📊 Ver portafolios afectados"):
        st.markdown(f"""
        <table style="width:100%;font-size:13px;">
          <tr style="background:#f5f5f5;">
            <th style="text-align:left;padding:8px;">Portafolio</th>
            <th style="text-align:right;padding:8px;">Porcentaje</th>
          </tr>
          <tr>
            <td style="padding:8px;">FPV Strategist Liquidez Col</td>
            <td style="text-align:right;padding:8px;">100,00%</td>
          </tr>
        </table>
        """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Regresar", key="r3_back", use_container_width=True):
            st.session_state.retiro_paso = 2
            st.rerun()
    with c2:
        if st.button("🔐 Solicitar código de verificación", key="r3_otp", use_container_width=True):
            st.session_state.retiro_paso = 4
            log_accion("OTP de retiro solicitado")
            st.rerun()


def _paso_otp(cliente):
    st.markdown(f"""
    <div style="text-align:center;padding:16px 0;">
      <div style="font-size:52px;margin-bottom:10px;">🔐</div>
      <h3>Validación de seguridad</h3>
      <p style="color:#666;font-size:14px;">
        Ingresa el código enviado a tu celular y correo.<br/>
        <b>Código demo: 123456</b>
      </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("otp_retiro_form"):
        codigo = st.text_input("Código de verificación", placeholder="_ _ _ _ _ _",
                                max_chars=6, label_visibility="collapsed")
        st.caption("⏱ 04:58 restantes")
        c1, c2 = st.columns(2)
        with c1:
            reenv = st.form_submit_button("Reenviar código", use_container_width=True)
        with c2:
            verif = st.form_submit_button("Verificar ✓", use_container_width=True)

    st.markdown(f'<div style="text-align:center;"><a href="#" style="color:{GREEN};font-size:13px;">¿No recibiste el código?</a></div>', unsafe_allow_html=True)

    if reenv:
        st.info("📱 Código reenviado a tu celular y correo.")
        log_accion("OTP retiro reenviado")

    if verif:
        if codigo == "123456":
            monto = st.session_state.get("retiro_monto", 0)
            log_accion(f"Retiro exitoso ${monto:,.0f}")
            st.session_state.retiro_paso = 1
            st.success(f"✅ ¡Retiro procesado! Recibirás ${monto:,.2f} el 08/05/2026 después de las 3:00 p.m.")
            st.balloons()
        else:
            st.error("❌ Código incorrecto. El código demo es 123456.")
            log_accion("OTP incorrecto en retiro")
