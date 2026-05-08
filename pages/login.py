"""Página de Login — portal Skandia con OTP y manejo de errores."""
import streamlit as st
from data.base_conocimiento import CLIENTES_DEMO
from modules.session_manager import log_accion, activar_error
from config.brand import GREEN, GRAY_DARK, RED_ALERT


def render_login():
    st.markdown(f"""
    <div style="background:#fff;border-top:4px solid #003087;padding:14px 32px;
        margin:-0.25rem -1rem 0 -1rem;
        box-shadow:0 2px 12px rgba(0,0,0,0.08);
        display:flex;align-items:center;gap:12px;">
      <span style="color:{GREEN};font-size:26px;font-weight:900;">✦</span>
      <span style="font-size:22px;font-weight:700;color:{GRAY_DARK};">skandia</span>
      <span style="width:1px;height:26px;background:#e0e0e0;margin:0 10px;"></span>
      <span style="font-size:14px;color:#666;">Portal Clientes</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown(f"""
        <div style="background:#fff;border-radius:20px;padding:36px 32px;
            box-shadow:0 8px 32px rgba(0,0,0,0.10);text-align:center;">
          <div style="font-size:32px;color:{GREEN};font-weight:900;margin-bottom:4px;">✦ skandia</div>
          <div style="font-size:14px;color:#888;margin-bottom:28px;">Ingresa a tu Portal Clientes</div>
        </div>
        """, unsafe_allow_html=True)

        intentos = st.session_state.get("login_intentos", 0)

        if intentos >= 3:
            st.markdown(f"""
            <div class="sk-card-alert blink">
              🔒 <b>Portal bloqueado temporalmente</b><br/>
              Superaste el número máximo de intentos. Restablece tu contraseña.
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔑 Recuperar contraseña", use_container_width=True):
                activar_error("ERR013","Login")
                st.rerun()
            if st.button("🚨 Reportar actividad sospechosa", use_container_width=True):
                activar_error("ERR014","Login")
                st.rerun()
            if st.session_state.get("chatbot_activo"):
                from modules.chatbot import render_chatbot_flotante
                render_chatbot_flotante()
            return

        with st.form("login_form"):
            st.markdown("**Número de documento**")
            documento = st.text_input("", placeholder="Ej: 1020456789",
                                      label_visibility="collapsed")
            st.markdown("**Contraseña**")
            password  = st.text_input("", type="password", placeholder="••••••••",
                                      label_visibility="collapsed")
            st.checkbox("Recordar mi usuario")
            submitted = st.form_submit_button("Ingresar", use_container_width=True)

        st.markdown(f"""
        <div style="text-align:center;margin-top:10px;">
          <a href="#" style="color:{GREEN};text-decoration:none;font-size:14px;">
            ¿Olvidaste tu contraseña?
          </a>
          &nbsp;·&nbsp;
          <a href="#" style="color:{GREEN};text-decoration:none;font-size:14px;">
            Regístrate aquí
          </a>
        </div>
        """, unsafe_allow_html=True)

        if submitted:
            _procesar_login(documento, password)


def _procesar_login(documento, password):
    cliente_encontrado = None
    for c in CLIENTES_DEMO:
        if c["documento"] == documento.strip():
            cliente_encontrado = c
            break

    if not cliente_encontrado:
        st.session_state.login_intentos += 1
        log_accion(f"Login fallido — doc: {documento}")
        st.error("⚠️ Usuario no encontrado. Verifica tu número de documento.")
        return

    if password != "skandia123":
        st.session_state.login_intentos += 1
        restantes = max(3 - st.session_state.login_intentos, 0)
        if restantes <= 0:
            activar_error("ERR013","Login")
            st.rerun()
        st.error(f"⚠️ Contraseña incorrecta. Intentos restantes: {restantes}")
        log_accion(f"Contraseña incorrecta — intento {st.session_state.login_intentos}")
        return

    # Éxito
    st.session_state.cliente_activo  = cliente_encontrado
    st.session_state.escenario_demo  = cliente_encontrado.get("escenario","libre")
    st.session_state.login_intentos  = 0
    st.session_state["mostrar_otp"]  = True
    log_accion(f"Login exitoso — {cliente_encontrado['nombre']}")
    st.rerun()


def render_otp():
    """Modal de validación OTP."""
    cliente = st.session_state.get("cliente_activo", {})
    nombre  = cliente.get("nombre","").split()[0]

    st.markdown(f"""
    <div style="background:#fff;border-top:4px solid #003087;padding:14px 32px;
        margin:-0.25rem -1rem 0 -1rem;
        box-shadow:0 2px 12px rgba(0,0,0,0.08);
        display:flex;align-items:center;gap:12px;">
      <span style="color:{GREEN};font-size:26px;font-weight:900;">✦</span>
      <span style="font-size:22px;font-weight:700;color:{GRAY_DARK};">skandia</span>
      <span style="width:1px;height:26px;background:#e0e0e0;margin:0 10px;"></span>
      <span style="font-size:14px;color:#666;">Portal Clientes</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])

    with col:
        st.markdown(f"""
        <div style="background:#fff;border-radius:20px;padding:36px 32px;
            box-shadow:0 8px 32px rgba(0,0,0,0.10);text-align:center;">
          <div style="font-size:56px;margin-bottom:12px;">🔐</div>
          <h3 style="color:{GRAY_DARK};margin-bottom:6px;">Hola, {nombre}!</h3>
          <h4 style="font-weight:400;color:#666;margin-bottom:16px;">Validación de seguridad</h4>
          <p style="color:#888;font-size:14px;">
            Ingresa el código enviado a tu celular y correo registrados.<br/>
            <b style="color:{GRAY_DARK};">Código demo: 123456</b>
          </p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("otp_login_form"):
            codigo = st.text_input("Código de verificación",
                                   placeholder="_ _ _ _ _ _", max_chars=6,
                                   label_visibility="collapsed")
            st.caption("⏱️ Tiempo restante: 04:58")
            c1, c2 = st.columns(2)
            with c1: rev = st.form_submit_button("Reenviar código", use_container_width=True)
            with c2: ver = st.form_submit_button("Verificar ✓", use_container_width=True)

        st.markdown(f'<div style="text-align:center;margin-top:8px;"><a href="#" style="color:{GREEN};font-size:13px;">¿No recibiste el código?</a></div>', unsafe_allow_html=True)

        if rev:
            st.info(f"📱 Código reenviado al celular de {nombre}.")
            log_accion("OTP reenviado")

        if ver:
            if codigo == "123456":
                st.session_state["mostrar_otp"] = False
                st.session_state.logged_in      = True
                st.session_state.pagina_activa  = "inicio"
                log_accion(f"✅ OTP verificado — {cliente.get('nombre','')} ingresó al portal")
                st.rerun()
            else:
                st.error("❌ Código incorrecto. El código demo es 123456.")
                activar_error("ERR017","Verificación OTP")
                st.rerun()
