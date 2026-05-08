"""Retiros — flujo 3 pasos. Error se dispara UNA sola vez por sesión."""

import streamlit as st
from config.brand import GREEN, GRAY_DARK, RED_ALERT, YELLOW_WARN
from modules.session_manager import log_accion, activar_error, limpiar_error
from modules.chatbot import render_chatbot_flotante
from modules.tecnico import render_tecnico

ERRORES_POR_ESCENARIO = {"A":"ERR001","B":"ERR002","C":"ERR003","libre":None}

def _header():
    nombre = st.session_state.get("cliente_activo",{}).get("nombre","")
    st.markdown(f"""
    <div style="background:#fff;border-top:4px solid #003087;padding:12px 28px;
        margin:-0.25rem -1rem 20px -1rem;
        box-shadow:0 2px 12px rgba(0,0,0,0.08);
        display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
      <span style="color:#00D261;font-size:24px;font-weight:900;">✦</span>
      <span style="font-size:20px;font-weight:700;color:#2D2926;">skandia</span>
      <span style="width:1px;height:24px;background:#e0e0e0;margin:0 8px;"></span>
      <span style="font-size:13px;color:#666;">Portal Clientes</span>
      <span style="margin-left:auto;display:flex;align-items:center;gap:10px;">
        <span style="font-size:13px;color:#666;">👤 {nombre}</span>
        <span style="background:#00D261;color:white;border-radius:20px;
               padding:4px 14px;font-size:13px;font-weight:600;">💰 Retiros</span>
      </span>
    </div>
    """, unsafe_allow_html=True)

def render_retiros():
    _header()

    # ── Técnico tiene prioridad total ─────────────────────────────────────
    if st.session_state.get("tecnico_conectado"):
        render_tecnico()
        return

    # ── Chatbot flotante (solo si hay error activo) ───────────────────────
    if st.session_state.get("chatbot_activo"):
        render_chatbot_flotante()
        st.markdown("---")

    # ── Caso resuelto: banner + continuar sin re-disparar error ───────────
    if st.session_state.get("caso_resuelto"):
        cliente_n = st.session_state.get("cliente_activo",{}).get("nombre","").split()[0]
        st.markdown(f"""
        <div class="sk-card-success slide-in" style="text-align:center;padding:28px 24px;">
          <div style="font-size:52px;margin-bottom:12px;">🎉</div>
          <div style="font-size:20px;font-weight:700;color:#1B5E20;margin-bottom:8px;">
            ¡Inconveniente resuelto, {cliente_n}!
          </div>
          <p style="color:#2E7D32;margin:0;">
            Ya puedes continuar con tu retiro de forma exitosa.
          </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💰 Continuar con mi retiro →", use_container_width=True, key="cont_resuelto"):
            st.session_state.caso_resuelto  = False
            st.session_state.retiro_paso    = 2
            st.rerun()
        return

    cliente = st.session_state.get("cliente_activo", {})
    paso    = st.session_state.get("retiro_paso", 1)

    col_izq, col_der = st.columns([2, 3])
    with col_izq:
        _panel_izq()
    with col_der:
        _barra(paso)
        if   paso == 1: _paso1(cliente)
        elif paso == 2: _paso2(cliente)
        elif paso == 3: _paso3(cliente)
        elif paso == 4: _paso_otp()

    st.markdown("---")
    _historial(cliente)


def _panel_izq():
    st.markdown(f"""
    <div class="col-left-green">
      <div style="font-size:72px;margin-bottom:16px;filter:drop-shadow(0 4px 8px rgba(0,0,0,0.1));">💼</div>
      <h3 style="color:#2D2926;margin-bottom:8px;">Retiros</h3>
      <p style="color:#555;font-size:14px;text-align:center;line-height:1.6;">
        Gestiona el desembolso de tu dinero de forma ágil, fácil y segura.
      </p>
      <div style="margin-top:20px;padding:12px 16px;background:rgba(0,210,97,0.1);
           border-radius:10px;font-size:13px;color:#1B5E20;">
        🔒 Tus fondos están protegidos con verificación biométrica
      </div>
      <br/>
      <a href="#" style="color:#00D261;font-size:13px;text-decoration:none;">⓪ Centro de ayuda</a>
    </div>
    """, unsafe_allow_html=True)


def _barra(paso):
    labels = ["Selección","Monto y tipo","Confirmación"]
    cols   = st.columns(3)
    for i,(c,lbl) in enumerate(zip(cols,labels)):
        with c:
            done   = i < paso
            active = i == paso - 1
            bg     = "#00D261" if done else "#f0f0f0"
            tc     = "#2D2926" if done else "#aaa"
            fw     = "700" if active else "500"
            st.markdown(
                f'<div style="height:7px;background:{bg};border-radius:4px;'
                f'box-shadow:{"0 2px 6px rgba(0,210,97,0.4)" if done else "none"};"></div>'
                f'<div style="font-size:11px;color:{tc};font-weight:{fw};text-align:center;margin-top:4px;">{lbl}</div>',
                unsafe_allow_html=True)
    st.caption(f"Paso {min(paso,3)} de 3")
    st.markdown("<br/>", unsafe_allow_html=True)


def _paso1(cliente):
    saldo = cliente.get("saldo_ahorro", 1414977.14)
    cn    = cliente.get("contrato_num","100006674636")
    nombre_c = cliente.get("nombre","Cliente")

    st.markdown(f"""
    <div style="margin-bottom:6px;">
      <h3 style="color:#2D2926;">¿De dónde vas a retirar?</h3>
      <p style="color:#888;font-size:13px;">Selecciona el producto del cual deseas retirar</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="border:2px solid #00D261;border-radius:14px;padding:18px 20px;
        margin:12px 0;background:linear-gradient(135deg,#fff,#F1FFF7);cursor:pointer;
        box-shadow:0 2px 12px rgba(0,210,97,0.15);">
      <div style="display:flex;align-items:center;gap:14px;">
        <div style="width:16px;height:16px;background:#00D261;border-radius:50%;
             box-shadow:0 2px 6px rgba(0,210,97,0.4);flex-shrink:0;"></div>
        <div>
          <div style="font-weight:700;font-size:15px;color:#2D2926;">Potencializar mi inversión</div>
          <div style="color:#777;font-size:13px;margin-top:2px;">
            P. Voluntaria &nbsp;|&nbsp; Ahorro e inversión &nbsp;|&nbsp; #{cn[-6:]}
          </div>
          <div style="font-size:14px;margin-top:6px;">
            Saldo total: <b style="color:#00D261;">${saldo:,.2f}</b>
          </div>
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
        if st.button("← Cancelar", key="r1_can", use_container_width=True):
            st.session_state.pagina_activa = "inicio"
            st.rerun()
    with c2:
        if st.button("Empezar →", key="r1_start", use_container_width=True):
            st.session_state.retiro_producto = "Potencializar mi inversión"
            st.session_state.retiro_paso     = 2
            log_accion("Retiro: producto seleccionado")
            st.rerun()


def _paso2(cliente):
    saldo     = cliente.get("saldo_ahorro", 1414977.14)
    disp      = saldo - 4048.40

    st.markdown(f"""
    <div style="text-align:center;padding:18px 0 10px;">
      <div style="color:#888;font-size:13px;margin-bottom:4px;">Saldo total en pensión voluntaria</div>
      <div style="font-size:36px;font-weight:700;color:#2D2926;">${saldo:,.2f}</div>
      <a href="#" style="color:#00D261;font-size:13px;">Ver detalle completo ↗</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**¿Qué tipo de retiro harás?**")
    tipo = st.radio("",["Retirar un monto específico","Retiro total"],
                    key="r2_tipo", label_visibility="collapsed")

    if tipo == "Retirar un monto específico":
        monto = st.number_input("Monto a retirar (COP)",
                                min_value=5000, max_value=int(disp),
                                value=st.session_state.get("retiro_monto",5000),
                                step=1000, format="%d")
        st.session_state.retiro_monto = monto
        st.caption(f"💡 Disponible para retirar: ${disp:,.2f}")
    else:
        st.session_state.retiro_monto = disp
        st.success(f"Se retirará el total disponible: ${disp:,.2f}")

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#EDE7F6,#F3E5F5);border-radius:10px;
        padding:12px 16px;margin:12px 0;font-size:13px;border-left:4px solid #7B1FA2;">
      📅 Tu retiro estará disponible el <b>08/05/2026</b> después de las <b>3:00 p.m.</b>
      &nbsp;<a href="#" style="color:#7B1FA2;">Ver más</a>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Regresar", key="r2_back", use_container_width=True):
            st.session_state.retiro_paso = 1
            st.rerun()
    with c2:
        if st.button("Continuar →", key="r2_cont", use_container_width=True):
            log_accion(f"Retiro: monto ${st.session_state.retiro_monto:,.0f}")
            _disparar_error()


def _disparar_error():
    """Dispara el error SOLO si no se ha disparado antes en esta sesión."""
    escenario = st.session_state.get("escenario_demo","libre")
    err_id    = ERRORES_POR_ESCENARIO.get(escenario)

    # Si ya fue resuelto o no hay error para este escenario → paso 3
    if not err_id or st.session_state.get("error_disparado_retiros", False):
        st.session_state.retiro_paso = 3
        st.rerun()
        return

    log_accion(f"Error disparado en Retiros: {err_id}")
    activar_error(err_id,"Retiros")
    st.rerun()


def _paso3(cliente):
    monto   = st.session_state.get("retiro_monto", 5000)
    cuentas = cliente.get("cuentas", [])

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#FFF8E1,#FFF3CD);border-radius:10px;
        padding:12px 18px;margin-bottom:16px;font-size:13px;border-left:4px solid #F9A825;
        display:flex;align-items:center;gap:8px;">
      ⚠️ <span>Una vez tramitado <b>no se podrá modificar ni cancelar</b></span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Resumen de tu retiro")

    cuenta = cuentas[0] if cuentas else {"banco":"Sin cuenta inscrita","tipo":"—","numero":"——"}
    n      = cuenta.get("numero","")
    nm     = ("a****"+n[-4:]) if len(n)>=4 else "—"
    cargo  = monto * 0.004
    neto   = monto - cargo

    st.markdown(f"""
    <div class="sk-card">
      <table style="width:100%;font-size:14px;border-collapse:collapse;">
        <tr><td style="color:#888;padding:8px 0;">Especie</td>
            <td style="text-align:right;font-weight:600;">FPV Strategist Liquidez Col</td></tr>
        <tr><td style="color:#888;padding:8px 0;">Fecha esperada</td>
            <td style="text-align:right;font-weight:600;">08/05/2026</td></tr>
        <tr><td style="color:#888;padding:8px 0;">Valor del retiro</td>
            <td style="text-align:right;font-weight:600;">${monto:,.2f}</td></tr>
        <tr><td style="color:#888;padding:8px 0;">Cargos e impuestos</td>
            <td style="text-align:right;color:#D32F2F;">−${cargo:,.2f}</td></tr>
        <tr style="border-top:2px solid #eee;">
          <td style="font-weight:700;padding:10px 0;">Valor neto a recibir</td>
          <td style="text-align:right;font-weight:700;color:#00D261;font-size:18px;">${neto:,.2f}</td>
        </tr>
        <tr><td colspan="2" style="padding-top:14px;font-size:13px;color:#666;">
          🏦 <b>Destinatario:</b> {cuenta['banco']} | {nm} | {cuenta['tipo']}
        </td></tr>
        <tr><td colspan="2" style="font-size:13px;color:#666;">
          👤 <b>Titular:</b> {cliente.get('nombre','')}
        </td></tr>
      </table>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📊 Ver portafolios afectados"):
        st.markdown(f"""
        <table style="width:100%;font-size:13px;border-collapse:collapse;">
          <tr style="background:#f5f5f5;">
            <th style="text-align:left;padding:8px;border-radius:8px 0 0 0;">Portafolio</th>
            <th style="text-align:right;padding:8px;">Porcentaje</th>
          </tr>
          <tr>
            <td style="padding:8px;">FPV Strategist Liquidez Col</td>
            <td style="text-align:right;padding:8px;font-weight:600;">100,00%</td>
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


def _paso_otp():
    st.markdown(f"""
    <div class="sk-card" style="text-align:center;padding:28px;">
      <div style="font-size:56px;margin-bottom:12px;">🔐</div>
      <h3 style="color:#2D2926;">Validación de seguridad</h3>
      <p style="color:#777;font-size:14px;margin:0;">
        Ingresa el código enviado a tu celular y correo registrados.<br/>
        <b>Código demo: 123456</b>
      </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("otp_form_ret"):
        codigo = st.text_input("Código de verificación",
                               placeholder="_ _ _ _ _ _", max_chars=6,
                               label_visibility="collapsed")
        st.caption("⏱ 04:58 restantes")
        c1, c2 = st.columns(2)
        with c1: rev = st.form_submit_button("Reenviar código", use_container_width=True)
        with c2: ver = st.form_submit_button("Verificar ✓", use_container_width=True)

    st.markdown(f'<div style="text-align:center;margin-top:6px;"><a href="#" style="color:#00D261;font-size:13px;">¿No recibiste el código?</a></div>', unsafe_allow_html=True)

    if rev:
        st.info("📱 Código reenviado.")
        log_accion("OTP reenviado")

    if ver:
        if codigo == "123456":
            monto = st.session_state.get("retiro_monto",0)
            log_accion(f"✅ Retiro exitoso ${monto:,.0f}")
            st.session_state.retiro_paso = 1
            nombre_c = st.session_state.get("cliente_activo",{}).get("nombre","").split()[0]
            st.success(f"🎉 ¡Listo, {nombre_c}! Tu retiro de ${monto:,.2f} fue procesado. Lo recibirás el 08/05/2026.")
            st.balloons()
        else:
            st.error("❌ Código incorrecto. El código demo es 123456.")


def _historial(cliente):
    with st.expander("📋 Historial de retiros", expanded=False):
        h_list = cliente.get("historial",[])
        if not h_list:
            st.info("No tienes retiros registrados.")
            return
        for h in h_list:
            est = h.get("estado","")
            bc  = "badge-ok" if est=="Procesado" else ("badge-warn" if est=="En trámite" else "badge-err")
            mt  = f"${h.get('monto',0):,.0f}" if h.get("monto",0)>0 else "—"
            st.markdown(f"""
            <div class="sk-card" style="padding:12px 16px;margin-bottom:6px;">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div><b>{h.get('tipo','')}</b>
                  <div style="font-size:12px;color:#888;">{h.get('fecha','')}</div>
                </div>
                <div style="text-align:right;"><b>{mt}</b><br/><span class="{bc}">{est}</span></div>
              </div>
            </div>
            """, unsafe_allow_html=True)
