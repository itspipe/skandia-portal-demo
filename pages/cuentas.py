"""Página Cuentas Bancarias — flujo con error por escenario B."""

import streamlit as st
from config.brand import GREEN, GRAY_DARK
from modules.session_manager import log_accion, activar_error
from modules.chatbot import render_chatbot_flotante
from modules.tecnico import render_tecnico

BANCOS = ["Bancolombia","Banco Davivienda","Banco de Bogotá","BBVA Colombia",
          "Banco Popular","Nequi","Daviplata","Banco Caja Social"]

ERRORES_POR_ESCENARIO = {
    "A":     None,       # En escenario A el error es en Retiros, aquí se inscribe OK
    "B":     "ERR009",   # SARLAFT
    "C":     None,
    "libre": None,
}


def render_cuentas():
    st.markdown(f"""
    <div style="background:#fff;border-top:4px solid #003087;padding:12px 24px;
                margin:-0.5rem -1rem 16px -1rem;box-shadow:0 2px 8px rgba(0,0,0,0.08);
                display:flex;align-items:center;gap:8px;">
      <span style="color:{GREEN};font-size:22px;font-weight:900;">✦</span>
      <span style="font-size:19px;font-weight:700;">skandia</span>
      <span style="width:1px;height:22px;background:#ddd;margin:0 10px;"></span>
      <span style="font-size:13px;color:#666;">Portal Clientes</span>
      <span style="margin-left:auto;font-size:13px;color:{GREEN};">🏦 Cuentas Bancarias</span>
    </div>
    <div style="font-size:13px;color:{GREEN};margin-bottom:12px;">
      ← Inicio / Inscripción de cuentas
    </div>
    """, unsafe_allow_html=True)

    # Chatbot si hay error
    if st.session_state.get("chatbot_activo"):
        render_chatbot_flotante()
        st.markdown("---")

    # Técnico si está conectado
    if st.session_state.get("tecnico_conectado"):
        render_tecnico()
        return

    cliente = st.session_state.get("cliente_activo", {})
    paso    = st.session_state.get("cuenta_paso", 1)

    col_izq, col_der = st.columns([2, 3])

    with col_izq:
        st.markdown(f"""
        <div class="col-left-green">
          <div style="font-size:64px;margin-bottom:12px;">🏦</div>
          <h3 style="color:{GRAY_DARK};">Cuentas bancarias</h3>
          <p style="color:#555;font-size:14px;text-align:center;">
            Administra tus cuentas bancarias para realizar transacciones de forma rápida y segura.
          </p>
        </div>
        """, unsafe_allow_html=True)

    with col_der:
        _barra(paso)
        if paso == 1:
            _lista_cuentas(cliente)
        elif paso == 2:
            _form_cuenta(cliente)
        elif paso == 3:
            _antes_biometria()
        elif paso == 4:
            _verificacion_identidad()
        elif paso == 5:
            _exito(cliente)


def _barra(paso):
    labels = ["Mis cuentas", "Datos", "Verificación"]
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
    st.caption(f"{min(paso,3)} de 3")
    st.markdown("<br/>", unsafe_allow_html=True)


def _lista_cuentas(cliente):
    st.markdown("#### ¿A dónde quieres enviar tu dinero?")
    tab1, tab2 = st.tabs(["🏦 Cuenta bancaria", "📋 Cheque"])

    with tab1:
        cuentas = cliente.get("cuentas", [])
        if cuentas:
            for c in cuentas:
                n  = c.get("numero", "")
                nm = (n[:2] + "*" * (len(n)-6) + n[-4:]) if len(n) >= 6 else n
                st.markdown(f"""
                <div style="border:1px solid #ddd;border-radius:10px;padding:14px;
                            margin-bottom:8px;background:#fff;">
                  <div style="display:flex;align-items:center;gap:10px;">
                    <div style="width:12px;height:12px;background:{GREEN};border-radius:50%;"></div>
                    <div>
                      <b>{c['banco']}</b>
                      <span style="color:#666;font-size:13px;"> Personal</span><br/>
                      <span style="font-size:13px;color:#555;">Mi cuenta | # {nm} | {c['tipo']}</span>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="text-align:center;padding:36px 0;">
              <div style="font-size:48px;color:#ccc;margin-bottom:10px;">🏦</div>
              <b>Aún no has agregado ninguna cuenta</b><br/>
              <p style="color:#888;font-size:14px;">
                Agrega una cuenta para poder hacer retiros.
              </p>
            </div>
            """, unsafe_allow_html=True)

        if st.button("+ Agregar cuenta", key="btn_agregar", use_container_width=True):
            st.session_state.cuenta_paso = 2
            log_accion("Inicio inscripción cuenta bancaria")
            st.rerun()

    with tab2:
        st.info("La opción de cheque no está disponible en este momento.")

    st.markdown("<br/>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Regresar", key="cta_back1", use_container_width=True):
            st.session_state.pagina_activa = "retiros"
            st.rerun()
    with c2:
        tiene_cuenta = len(cliente.get("cuentas", [])) > 0
        if st.button("Continuar →" if tiene_cuenta else "Agrega una cuenta primero",
                     key="cta_cont1", use_container_width=True, disabled=not tiene_cuenta):
            # Volver a retiros con la cuenta seleccionada
            st.session_state.pagina_activa = "retiros"
            st.session_state.retiro_paso   = 3
            st.rerun()


def _form_cuenta(cliente):
    st.markdown(f"""
    <div style="text-align:center;margin-bottom:16px;">
      <div style="font-size:36px;margin-bottom:8px;">🏦</div>
      <h4>Agrega tu cuenta bancaria</h4>
      <p style="color:#666;font-size:13px;">
        Registra tu cuenta bancaria para usarla en retiros de forma rápida y segura.
      </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_cuenta_nueva"):
        titular  = st.selectbox("Titular", ["Cuenta personal", "Cuenta de tercero"])
        banco    = st.selectbox("Banco", BANCOS)
        tipo_cta = st.radio("Tipo de cuenta", ["Ahorros", "Corriente"], horizontal=True)
        numero   = st.text_input("Número de cuenta", placeholder="Ej: 12345678991")
        ciudad   = st.selectbox("Ciudad", ["BOGOTA D.C., BOGOTA","MEDELLÍN, ANTIOQUIA",
                                            "CALI, VALLE DEL CAUCA","BARRANQUILLA, ATLÁNTICO"])
        c1, c2 = st.columns(2)
        with c1:
            back = st.form_submit_button("← Regresar", use_container_width=True)
        with c2:
            cont = st.form_submit_button("Hacer validación biométrica →", use_container_width=True)

    if back:
        st.session_state.cuenta_paso = 1
        st.rerun()

    if cont:
        if not numero.strip():
            st.error("Por favor ingresa el número de cuenta.")
            return

        # Verificar error según escenario
        escenario = st.session_state.get("escenario_demo", "libre")
        err_id    = ERRORES_POR_ESCENARIO.get(escenario)

        if err_id:
            log_accion(f"Error en inscripción de cuenta: {err_id} (escenario {escenario})")
            activar_error(err_id, "Cuentas Bancarias")
            st.rerun()
        else:
            st.session_state["nueva_cuenta"] = {
                "banco": banco, "tipo": tipo_cta,
                "numero": numero, "titular": titular, "ciudad": ciudad,
            }
            st.session_state.cuenta_paso = 3
            log_accion(f"Cuenta ingresada: {banco} {tipo_cta} ...{numero[-4:]}")
            st.rerun()


def _antes_biometria():
    st.markdown("### Antes de Comenzar")
    st.markdown("Ten en cuenta estas recomendaciones:")

    cards = [
        ("📋","Documentos","Ten a la mano tu **documento de identidad** (cédula de ciudadanía o cédula de extranjería)"),
        ("📱","Cámara","Asegúrate de que la cámara de tu dispositivo funcione y ubícate en un lugar con **buena iluminación.**"),
        ("🌐","Navegador","No cierres la ventana del navegador, podrías **perder tu progreso.**"),
    ]
    c1, c2, c3 = st.columns(3)
    for col, (ico, tit, desc) in zip([c1,c2,c3], cards):
        with col:
            st.markdown(f"""
            <div class="sk-card" style="text-align:center;min-height:200px;padding:20px 14px;">
              <div style="font-size:36px;margin-bottom:10px;">{ico}</div>
              <b>{tit}</b>
              <p style="font-size:13px;color:#555;margin-top:8px;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.caption("Al continuar, confirmas la Autorización para el tratamiento de tus datos personales.")
    if st.button("Continuar →", key="bio_cont", use_container_width=True):
        st.session_state.cuenta_paso = 4
        log_accion("Aceptó términos biométricos")
        st.rerun()


def _verificacion_identidad():
    st.markdown(f"""
    <div style="text-align:center;padding:10px 0 18px;">
      <h3>Verifica tu identidad desde tu celular</h3>
      <p style="color:#666;font-size:14px;">
        Completa la verificación para tomar fotos y videos con mejor calidad.
      </p>
    </div>
    """, unsafe_allow_html=True)

    canal  = st.radio("Elige cómo quieres recibir el enlace:",
                      ["WhatsApp","Mensaje de texto SMS"], horizontal=True)
    celular = st.text_input("Número de celular", placeholder="+57 300 000 0000")
    st.markdown(f'<div style="text-align:center;margin:6px 0;"><a href="#" style="color:{GREEN};font-size:13px;">Usar código QR</a></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Seguir aquí →", key="bio_aqui", use_container_width=True):
            log_accion("Biometría: continuar en mismo dispositivo")
            st.session_state.cuenta_paso = 5
            st.rerun()
    with c2:
        if st.button("📲 Enviar enlace", key="bio_env", use_container_width=True):
            if celular.strip():
                st.success(f"✅ Enlace enviado por {canal} al {celular}")
                log_accion(f"Enlace biométrico enviado por {canal}")
            else:
                st.error("Ingresa tu número de celular.")


def _exito(cliente):
    cuenta = st.session_state.get("nueva_cuenta", {})
    num    = cuenta.get("numero","12345678991")
    nm     = (num[:2]+"*"*(len(num)-6)+num[-4:]) if len(num)>=6 else num

    st.markdown(f"""
    <div style="text-align:center;padding:16px;background:#E8F5E9;
                border-radius:12px;border:2px solid {GREEN};max-width:420px;margin:auto;">
      <div style="font-size:52px;margin-bottom:10px;">✅</div>
      <h3 style="color:#1B5E20;">Validación exitosa</h3>
      <p style="font-weight:600;">¡Tu identidad fue validada con éxito!</p>
      <p style="color:#666;font-size:14px;">Ya puedes continuar con el proceso.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center;padding:16px;background:#fff;border-radius:12px;
                box-shadow:0 4px 16px rgba(0,0,0,0.10);max-width:420px;margin:auto;">
      <div style="width:44px;height:44px;background:{GREEN};border-radius:50%;
                  display:flex;align-items:center;justify-content:center;
                  font-size:22px;margin:0 auto 10px;">✓</div>
      <h3>Registro exitoso</h3>
      <p>Tu cuenta se registró correctamente.</p>
      <div style="background:#f5f5f5;border-radius:8px;padding:10px;margin-top:10px;text-align:left;">
        <b>{cuenta.get('banco','Banco Davivienda')}</b>
        <span style="float:right;color:#666;font-size:13px;">Personal</span><br/>
        <span style="font-size:13px;color:#555;">Mi cuenta | # {nm} | {cuenta.get('tipo','Ahorros')}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    if st.button("Continuar →", key="cta_exito", use_container_width=True):
        # Agregar la cuenta al cliente
        nueva = st.session_state.get("nueva_cuenta", {})
        if nueva:
            cliente.setdefault("cuentas", []).append({
                "banco":  nueva["banco"],
                "tipo":   nueva["tipo"],
                "numero": nueva["numero"],
                "estado": "Activa",
            })
            st.session_state.cliente_activo = cliente
            log_accion(f"Cuenta {nueva['banco']} registrada exitosamente")

        st.session_state.cuenta_paso = 1
        # Si venimos de retiros (escenario A), volver a retiros paso 2
        if st.session_state.get("escenario_demo") == "A":
            st.session_state.error_activo  = None
            st.session_state.chatbot_activo = False
            st.session_state.caso_resuelto  = True
            st.session_state.pagina_activa  = "retiros"
            st.session_state.retiro_paso    = 2
        else:
            st.session_state.pagina_activa = "retiros"
        st.rerun()
