"""Retiros — flujo 3 pasos. Chatbot flotante al final. No muestra saldo si no hay fondos."""
import streamlit as st
from config.brand import GREEN, GRAY_DARK, RED_ALERT, sk_header
from modules.session_manager import log_accion, activar_error
from modules.chatbot import render_chatbot_flotante
from modules.tecnico import render_tecnico

ERRORES = {"A":"ERR001","B":"ERR002","C":"ERR003","libre":None}


def render_retiros():
    cliente = st.session_state.get("cliente_activo",{})
    nombre  = cliente.get("nombre","")
    st.markdown(sk_header("Retiros", nombre), unsafe_allow_html=True)

    if st.session_state.get("tecnico_conectado"):
        render_tecnico()
        return

    # Banner caso resuelto
    if st.session_state.get("caso_resuelto"):
        primer_n = nombre.split()[0]
        st.markdown(f"""
        <div class="sk-card-success slide-up" style="text-align:center;padding:32px;">
          <div style="font-size:52px;margin-bottom:10px;">🎉</div>
          <div style="font-size:20px;font-weight:700;color:#1B5E20;">¡Listo, {primer_n}!</div>
          <p style="color:#2E7D32;">Tu inconveniente fue resuelto. Ahora puedes continuar con tu retiro.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💰 Continuar con mi retiro →", use_container_width=True):
            st.session_state.caso_resuelto = False
            st.session_state.retiro_paso   = 2
            st.rerun()
        # Chatbot flotante al final
        render_chatbot_flotante()
        return

    paso = st.session_state.get("retiro_paso",1)
    col_l, col_r = st.columns([2,3])
    with col_l:
        _panel_izq()
    with col_r:
        _barra(paso)
        if   paso==1: _paso1(cliente)
        elif paso==2: _paso2(cliente)
        elif paso==3: _paso3(cliente)
        elif paso==4: _paso_otp()

    st.markdown("---")
    _historial(cliente)

    # Chatbot SIEMPRE al final (no interrumpe la página)
    render_chatbot_flotante()


def _panel_izq():
    st.markdown(f"""
    <div class="col-left-green">
      <div style="font-size:68px;margin-bottom:14px;">💼</div>
      <h3 style="color:{GRAY_DARK};margin-bottom:8px;">Retiros</h3>
      <p style="color:#666;font-size:14px;line-height:1.6;text-align:center;">
        Gestiona el desembolso de tu dinero de forma ágil, fácil y segura.
      </p>
      <div style="margin-top:18px;background:rgba(0,210,97,0.1);border-radius:10px;
           padding:10px 14px;font-size:12px;color:#1B5E20;">
        🔒 Verificación biométrica activa
      </div>
      <br/><a href="#" style="color:#00D261;font-size:13px;text-decoration:none;">⓪ Centro de ayuda</a>
    </div>
    """, unsafe_allow_html=True)


def _barra(paso):
    labels = ["Selección","Monto y tipo","Confirmación"]
    cols = st.columns(3)
    for i,(c,lbl) in enumerate(zip(cols,labels)):
        with c:
            done = i<paso
            st.markdown(
                f'<div style="height:6px;background:{"linear-gradient(90deg,#00D261,#00A84F)" if done else "#E8E8E8"};'
                f'border-radius:3px;box-shadow:{"0 2px 6px rgba(0,210,97,0.35)" if done else "none"};"></div>'
                f'<div style="font-size:11px;color:{"#2D2926" if done else "#bbb"};'
                f'font-weight:{"600" if i==paso-1 else "400"};text-align:center;margin-top:3px;">{lbl}</div>',
                unsafe_allow_html=True)
    st.caption(f"Paso {min(paso,3)} de 3")
    st.markdown("<br/>", unsafe_allow_html=True)


def _paso1(cliente):
    saldo = cliente.get("saldo_ahorro",1414977.14)
    cn    = cliente.get("contrato_num","100006674636")
    st.markdown(f"""
    <div style="margin-bottom:10px;">
      <h3 style="color:{GRAY_DARK};">¿De dónde vas a retirar?</h3>
      <p style="color:#999;font-size:13px;">Selecciona el producto del cual deseas hacer el retiro</p>
    </div>
    <div style="border:2px solid #00D261;border-radius:14px;padding:18px 20px;
         background:linear-gradient(135deg,#fff,#F5FFF9);
         box-shadow:0 3px 12px rgba(0,210,97,0.12);margin:12px 0;">
      <div style="display:flex;align-items:center;gap:14px;">
        <div style="width:14px;height:14px;background:#00D261;border-radius:50%;
             box-shadow:0 2px 6px rgba(0,210,97,0.4);flex-shrink:0;"></div>
        <div>
          <div style="font-weight:700;font-size:15px;color:{GRAY_DARK};">Potencializar mi inversión</div>
          <div style="color:#888;font-size:13px;margin-top:2px;">
            P. Voluntaria | Ahorro e inversión | #{cn[-6:]}
          </div>
          <div style="font-size:15px;margin-top:6px;font-weight:600;color:#00D261;">
            Saldo: ${saldo:,.2f}
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    vivienda = st.toggle("¿Retiro para vivienda con beneficio tributario?")
    if vivienda:
        st.info("ℹ️ Requiere documentación adicional. Contacta a tu Financial Planner.")

    st.markdown("<br/>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        if st.button("← Cancelar",key="r1c",use_container_width=True):
            st.session_state.pagina_activa="inicio"; st.rerun()
    with c2:
        if st.button("Empezar →",key="r1s",use_container_width=True):
            st.session_state.retiro_paso=2; log_accion("Producto seleccionado"); st.rerun()


def _paso2(cliente):
    saldo = cliente.get("saldo_ahorro",1414977.14)
    disp  = saldo - 4048.40
    escen = st.session_state.get("escenario_demo","libre")

    # Si el escenario B (fondos insuficientes) NO mostrar saldo alto
    if escen == "B":
        saldo_mostrar = 3500.00
        disp_mostrar  = 3500.00
    else:
        saldo_mostrar = saldo
        disp_mostrar  = disp

    st.markdown(f"""
    <div style="text-align:center;padding:16px 0 10px;">
      <div style="color:#999;font-size:13px;">Saldo disponible para retiro</div>
      <div style="font-size:34px;font-weight:700;color:{GRAY_DARK};">${saldo_mostrar:,.2f}</div>
      <a href="#" style="color:#00D261;font-size:13px;">Ver detalle ↗</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**¿Qué tipo de retiro harás?**")
    tipo = st.radio("",["Retirar un monto específico","Retiro total"],
                    key="r2t",label_visibility="collapsed")

    if tipo=="Retirar un monto específico":
        monto = st.number_input("Monto a retirar (COP)",
                                min_value=5000,max_value=int(disp_mostrar)+1,
                                value=min(st.session_state.get("retiro_monto",5000),int(disp_mostrar)),
                                step=1000,format="%d")
        st.session_state.retiro_monto = monto
        st.caption(f"💡 Disponible: ${disp_mostrar:,.2f}")
    else:
        st.session_state.retiro_monto = disp_mostrar
        st.success(f"Se retirará todo el disponible: ${disp_mostrar:,.2f}")

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#EDE7F6,#F3E5F5);border-radius:10px;
         padding:10px 14px;margin:10px 0;font-size:13px;border-left:3px solid #7B1FA2;">
      📅 Tu retiro estará disponible el <b>08/05/2026</b> después de las <b>3:00 p.m.</b>
    </div>
    """, unsafe_allow_html=True)

    c1,c2=st.columns(2)
    with c1:
        if st.button("← Regresar",key="r2b",use_container_width=True):
            st.session_state.retiro_paso=1; st.rerun()
    with c2:
        if st.button("Continuar →",key="r2c",use_container_width=True):
            log_accion(f"Monto seleccionado: ${st.session_state.retiro_monto:,.0f}")
            _disparar_error()


def _disparar_error():
    escen  = st.session_state.get("escenario_demo","libre")
    err_id = ERRORES.get(escen)
    if not err_id or st.session_state.get("error_disparado_retiros",False):
        st.session_state.retiro_paso=3; st.rerun(); return
    log_accion(f"Error disparado: {err_id} (escenario {escen})")
    activar_error(err_id,"Retiros")
    st.rerun()


def _paso3(cliente):
    monto   = st.session_state.get("retiro_monto",5000)
    cuentas = cliente.get("cuentas",[])
    cuenta  = cuentas[0] if cuentas else {"banco":"Sin cuenta","tipo":"—","numero":"——"}
    n       = cuenta.get("numero","")
    nm      = ("a****"+n[-4:]) if len(n)>=4 else "—"
    cargo   = monto*0.004
    neto    = monto-cargo

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#FFF8E1,#FFF3CD);border-radius:10px;
         padding:10px 16px;margin-bottom:14px;font-size:13px;border-left:3px solid #F9A825;
         display:flex;align-items:center;gap:8px;">
      ⚠️ <span>Una vez tramitado <b>no se podrá modificar ni cancelar</b></span>
    </div>
    <h3 style="color:{GRAY_DARK};">Resumen de tu retiro</h3>
    """, unsafe_allow_html=True)

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
            <td style="text-align:right;color:{RED_ALERT};">−${cargo:,.2f}</td></tr>
        <tr style="border-top:2px solid #f0f0f0;">
          <td style="font-weight:700;padding:10px 0;">Valor neto a recibir</td>
          <td style="text-align:right;font-weight:700;color:#00D261;font-size:18px;">${neto:,.2f}</td>
        </tr>
        <tr><td colspan="2" style="padding-top:12px;font-size:13px;color:#666;">
          🏦 <b>Destinatario:</b> {cuenta['banco']} | {nm} | {cuenta['tipo']}<br/>
          👤 <b>Titular:</b> {cliente.get('nombre','')}
        </td></tr>
      </table>
    </div>
    """, unsafe_allow_html=True)

    c1,c2=st.columns(2)
    with c1:
        if st.button("← Regresar",key="r3b",use_container_width=True):
            st.session_state.retiro_paso=2; st.rerun()
    with c2:
        if st.button("🔐 Solicitar código de verificación",key="r3o",use_container_width=True):
            st.session_state.retiro_paso=4; log_accion("OTP solicitado"); st.rerun()


def _paso_otp():
    st.markdown(f"""
    <div class="sk-card" style="text-align:center;padding:28px;">
      <div style="font-size:52px;margin-bottom:10px;">🔐</div>
      <h3 style="color:{GRAY_DARK};">Validación de seguridad</h3>
      <p style="color:#888;font-size:14px;">
        Ingresa el código enviado a tu celular y correo.<br/>
        <b style="color:{GRAY_DARK};">Código demo: 123456</b>
      </p>
    </div>
    """, unsafe_allow_html=True)
    with st.form("otp_ret"):
        codigo = st.text_input("",placeholder="_ _ _ _ _ _",max_chars=6,label_visibility="collapsed")
        st.caption("⏱ 04:58 restantes")
        c1,c2=st.columns(2)
        with c1: rev=st.form_submit_button("Reenviar código",use_container_width=True)
        with c2: ver=st.form_submit_button("Verificar ✓",use_container_width=True)
    st.markdown(f'<div style="text-align:center;"><a href="#" style="color:#00D261;font-size:13px;">¿No recibiste el código?</a></div>',unsafe_allow_html=True)
    if rev: st.info("📱 Código reenviado.")
    if ver:
        if codigo=="123456":
            m = st.session_state.get("retiro_monto",0)
            _cli_otp = st.session_state.get("cliente_activo") or {}
            n = (_cli_otp.get("nombre","Cliente") or "Cliente").split()[0]
            st.session_state.retiro_paso=1
            st.success(f"🎉 ¡Listo, {n}! Retiro de ${m:,.2f} procesado. Disponible el 08/05/2026.")
            st.balloons()
            log_accion(f"✅ Retiro exitoso ${m:,.0f}")
        else:
            st.error("❌ Código incorrecto. Usa 123456.")


def _historial(cliente):
    with st.expander("📋 Historial de retiros"):
        for h in cliente.get("historial",[]):
            est=h.get("estado","")
            bc="badge-ok" if est=="Procesado" else ("badge-warn" if est=="En trámite" else "badge-err")
            mt=f"${h.get('monto',0):,.0f}" if h.get("monto",0)>0 else "—"
            st.markdown(f"""
            <div class="sk-card" style="padding:10px 16px;margin-bottom:6px;">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div><b>{h.get('tipo','')}</b>
                  <div style="font-size:12px;color:#888;">{h.get('fecha','')}</div></div>
                <div style="text-align:right;"><b>{mt}</b><br/><span class="{bc}">{est}</span></div>
              </div>
            </div>""", unsafe_allow_html=True)
