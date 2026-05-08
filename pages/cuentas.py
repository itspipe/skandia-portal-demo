"""Página de Cuentas Bancarias — inscripción con flujo biométrico."""

import streamlit as st
from config.brand import GREEN, GRAY_DARK, header_html
from modules.session_manager import log_accion, activar_error
from data.base_conocimiento import ESCENARIOS_ERROR

BANCOS = [
    "Bancolombia", "Banco Davivienda", "Banco de Bogotá", "BBVA Colombia",
    "Banco Popular", "Banco Agrario", "Nequi", "Daviplata", "Banco Caja Social",
    "Scotiabank Colpatria", "Banco Falabella", "Banco Finandina",
]


def render_cuentas():
    st.markdown(header_html("Portal Clientes"), unsafe_allow_html=True)
    st.markdown("← Inicio / Inscripción de cuentas", unsafe_allow_html=True)

    cliente = st.session_state.get("cliente_activo", {})
    paso = st.session_state.get("cuenta_paso", 1)

    col_izq, col_der = st.columns([2, 3])

    with col_izq:
        st.markdown(f"""
        <div class="col-left-green">
          <div style="font-size:72px;margin-bottom:16px;">🏦</div>
          <h3 style="color:{GRAY_DARK};">Cuentas bancarias</h3>
          <p style="color:#555;text-align:center;font-size:14px;">
            Administra tus cuentas bancarias o agrega tu cheque para realizar
            transacciones de forma rápida y segura.
          </p>
        </div>
        """, unsafe_allow_html=True)

    with col_der:
        _barra_cuentas(paso)

        if paso == 1:
            _paso_lista_cuentas(cliente)
        elif paso == 2:
            _paso_agregar_cuenta(cliente)
        elif paso == 3:
            _paso_biometria_info()
        elif paso == 4:
            _paso_verificacion_identidad()
        elif paso == 5:
            _paso_exito_registro(cliente)

    if st.session_state.get("chatbot_activo"):
        st.markdown("---")
        from modules.chatbot import render_chatbot
        render_chatbot()

    if st.session_state.get("tecnico_conectado"):
        st.markdown("---")
        from modules.tecnico import render_tecnico
        render_tecnico()


def _barra_cuentas(paso):
    total = 3
    labels = ["Mis cuentas", "Datos", "Verificación"]
    cols = st.columns(total)
    for i, (col, label) in enumerate(zip(cols, labels)):
        with col:
            color = GREEN if i < paso else "#ddd"
            st.markdown(
                f'<div style="height:6px;background:{color};border-radius:3px;"></div>'
                f'<div style="font-size:11px;color:{"#2D2926" if i<paso else "#999"};text-align:center;margin-top:4px;">{label}</div>',
                unsafe_allow_html=True
            )
    st.caption(f"{min(paso, total)} de {total}")
    st.markdown("<br/>", unsafe_allow_html=True)


def _paso_lista_cuentas(cliente):
    st.markdown("#### ¿A dónde quieres enviar tu dinero?")

    tab1, tab2 = st.tabs(["🏦 Cuenta bancaria", "📋 Cheque"])
    with tab1:
        cuentas = cliente.get("cuentas", [])
        if cuentas:
            for c in cuentas:
                num_mask = c["numero"][:2] + "*" * (len(c["numero"]) - 6) + c["numero"][-4:]
                st.markdown(f"""
                <div style="border:1px solid #ddd;border-radius:10px;padding:14px;
                            margin-bottom:8px;cursor:pointer;background:#fff;">
                  <div style="display:flex;align-items:center;gap:10px;">
                    <div style="width:12px;height:12px;background:{GREEN};border-radius:50%;"></div>
                    <div>
                      <b>{c['banco']}</b> <span style="color:#666;font-size:13px;">Personal</span><br/>
                      <span style="font-size:13px;color:#555;">Mi cuenta | # {num_mask} | {c['tipo']}</span>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="text-align:center;padding:40px 0;">
              <div style="font-size:48px;color:#bbb;margin-bottom:12px;">🏦</div>
              <b>Aún no has agregado ninguna cuenta</b><br/>
              <p style="color:#666;font-size:14px;">
                Recuerda que puedes agregar tus cuentas de forma fácil y segura para usarlas cuando las necesites.
              </p>
            </div>
            """, unsafe_allow_html=True)

        if st.button("+ Agregar cuenta", key="btn_agregar", use_container_width=True):
            st.session_state.cuenta_paso = 2
            log_accion("Inicio inscripción nueva cuenta bancaria")
            st.rerun()

    with tab2:
        st.info("La opción de cheque no está disponible en este momento.")

    st.markdown("<br/>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Regresar", key="cta_back1", use_container_width=True):
            st.session_state.pagina_activa = "retiros"
            st.rerun()
    with col2:
        disabled = len(cliente.get("cuentas", [])) == 0
        label = "Continuar →" if not disabled else "Agrega una cuenta primero"
        if st.button(label, key="cta_cont1", use_container_width=True, disabled=disabled):
            st.session_state.pagina_activa = "retiros"
            st.rerun()


def _paso_agregar_cuenta(cliente):
    st.markdown(f"""
    <div style="text-align:center;margin-bottom:16px;">
      <div style="font-size:36px;margin-bottom:8px;">🏦</div>
      <h4>Agrega tu cuenta bancaria</h4>
      <p style="color:#666;font-size:13px;">
        Registra tus cuentas bancarias, ya sean propias o de otras personas,
        para realizar el retiro de tu dinero de forma rápida y segura.
      </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_cuenta"):
        tipo_titular = st.selectbox("Titular de la cuenta", ["Cuenta personal", "Cuenta de tercero"])
        banco = st.selectbox("Banco", BANCOS)
        tipo_cuenta = st.radio("Tipo de cuenta", ["Ahorros", "Corriente"], horizontal=True)
        numero = st.text_input("Número de cuenta", placeholder="Ej: 12345678991")
        ciudad = st.selectbox("Ciudad", ["BOGOTA D.C., BOGOTA", "MEDELLÍN, ANTIOQUIA",
                                          "CALI, VALLE DEL CAUCA", "BARRANQUILLA, ATLÁNTICO",
                                          "BUCARAMANGA, SANTANDER"])
        col1, col2 = st.columns(2)
        with col1:
            back = st.form_submit_button("← Regresar", use_container_width=True)
        with col2:
            continuar = st.form_submit_button("Hacer validación biométrica →", use_container_width=True)

    if back:
        st.session_state.cuenta_paso = 1
        st.rerun()

    if continuar:
        if not numero.strip():
            st.error("Por favor ingresa el número de cuenta.")
        else:
            # Verificar error de cuenta por escenario
            escenario = st.session_state.get("escenario_demo", "libre")
            err_id = ESCENARIOS_ERROR.get(escenario, None)
            if err_id in ["ERR001", "ERR009"]:
                log_accion(f"Error en inscripción de cuenta: {err_id}")
                activar_error(err_id, "Cuentas Bancarias")
                st.rerun()
            else:
                st.session_state["nueva_cuenta"] = {
                    "banco": banco, "tipo": tipo_cuenta,
                    "numero": numero, "titular": tipo_titular, "ciudad": ciudad
                }
                st.session_state.cuenta_paso = 3
                log_accion(f"Cuenta ingresada: {banco} {tipo_cuenta} {numero[-4:]}")
                st.rerun()


def _paso_biometria_info():
    st.markdown("### Antes de Comenzar")
    st.markdown("*Ten en cuenta estas recomendaciones:*")

    col1, col2, col3 = st.columns(3)
    cards = [
        ("📋", "Documentos", "Ten a la mano tu **documento de identidad** (cédula de ciudadanía o cédula de extranjería)"),
        ("📱", "Cámara", "Asegúrate de que la cámara de tu dispositivo funcione correctamente y ubícate en un lugar con **buena iluminación.**"),
        ("🌐", "Navegador", "No cierres la ventana de tu navegador, ya que podrías **perder tu progreso en el proceso.**"),
    ]
    for col, (ico, tit, desc) in zip([col1, col2, col3], cards):
        with col:
            st.markdown(f"""
            <div class="sk-card" style="text-align:center;min-height:220px;">
              <div style="font-size:40px;margin-bottom:12px;">{ico}</div>
              <b>{tit}</b><br/>
              <p style="font-size:13px;color:#555;margin-top:8px;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.caption("Al hacer clic en Continuar, confirmas la Autorización para el tratamiento de tus datos personales, conforme a nuestra Política de Tratamiento de Información.")

    if st.button("Continuar →", key="bio_cont", use_container_width=True):
        st.session_state.cuenta_paso = 4
        log_accion("Aceptó términos biométricos")
        st.rerun()


def _paso_verificacion_identidad():
    st.markdown(f"""
    <div style="text-align:center;padding:10px 0 20px 0;">
      <h3>Verifica tu identidad desde tu celular</h3>
      <p style="color:#666;font-size:14px;">
        Te recomendamos completar la verificación desde tu celular
        para tomar fotos y videos con mejor calidad.
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Elige cómo quieres recibir el enlace:**")
    canal = st.radio("", ["WhatsApp", "Mensaje de texto SMS"], horizontal=True,
                     label_visibility="collapsed")

    col1, _, col2 = st.columns([1, 0.1, 3])
    with col1:
        st.selectbox("País", ["🇨🇴 +57"], label_visibility="collapsed")
    with col2:
        celular = st.text_input("Número de celular", placeholder="Número de celular",
                                label_visibility="collapsed")

    st.markdown(f'<div style="text-align:center;margin:8px 0;"><a href="#" style="color:{GREEN};">Usar código QR</a></div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Seguir aquí →", key="bio_aqui", use_container_width=True):
            log_accion("Validación biométrica: seguir en mismo dispositivo")
            st.session_state.cuenta_paso = 5
            st.rerun()
    with col2:
        if st.button("📲 Enviar enlace", key="bio_enviar", use_container_width=True):
            if celular.strip():
                st.success(f"✅ Enlace enviado por {canal} al número {celular}")
                log_accion(f"Enlace biométrico enviado por {canal}")
                st.info("Completa la validación desde tu celular y regresa aquí.")
            else:
                st.error("Por favor ingresa tu número de celular.")


def _paso_exito_registro(cliente):
    cuenta = st.session_state.get("nueva_cuenta", {})
    num = cuenta.get("numero", "12345678991")
    num_mask = num[:2] + "*" * (len(num) - 6) + num[-4:]

    # Modal de validación exitosa biométrica
    st.markdown(f"""
    <div style="text-align:center;padding:20px;background:#fff;
                border-radius:12px;box-shadow:0 4px 16px rgba(0,0,0,0.12);max-width:440px;margin:auto;">
      <div style="font-size:52px;margin-bottom:12px;">✅</div>
      <h3 style="color:#1B5E20;">Validación exitosa</h3>
      <p style="font-weight:600;">¡Tu identidad ha sido validada con éxito!</p>
      <p style="color:#666;font-size:14px;">Ahora puedes continuar con el proceso donde se solicitó la biometría.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Modal de registro exitoso
    st.markdown(f"""
    <div style="text-align:center;padding:20px;background:#fff;
                border-radius:12px;box-shadow:0 4px 16px rgba(0,0,0,0.12);max-width:440px;margin:auto;">
      <div style="width:48px;height:48px;background:{GREEN};border-radius:50%;
                  display:flex;align-items:center;justify-content:center;
                  font-size:24px;margin:0 auto 12px auto;">✓</div>
      <h3>Registro exitoso</h3>
      <p>Tu cuenta se registró correctamente.</p>
      <div style="background:#f5f5f5;border-radius:8px;padding:12px;margin-top:12px;">
        <b>{cuenta.get('banco','Banco Davivienda')}</b>
        <span style="float:right;color:#666;font-size:13px;">Personal</span><br/>
        <span style="font-size:13px;color:#555;">Mi cuenta | # {num_mask} | {cuenta.get('tipo','Ahorros')}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    if st.button("Continuar →", key="exito_cont", use_container_width=True):
        # Agregar cuenta al cliente
        if "nueva_cuenta" in st.session_state:
            nueva = st.session_state["nueva_cuenta"]
            cliente.setdefault("cuentas", []).append({
                "banco": nueva["banco"],
                "tipo": nueva["tipo"],
                "numero": nueva["numero"],
                "estado": "Activa"
            })
            st.session_state.cliente_activo = cliente
            log_accion(f"Cuenta {nueva['banco']} registrada exitosamente")

        st.session_state.cuenta_paso = 1
        st.session_state.pagina_activa = "retiros"
        st.rerun()
