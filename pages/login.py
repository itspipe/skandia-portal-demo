"""Página de Login — acceso al portal con simulación de errores de acceso."""

import streamlit as st
from data.base_conocimiento import CLIENTES_DEMO
from modules.session_manager import log_accion, activar_error
from config.brand import GREEN, GREEN_DARK, GRAY_DARK, BLUE_HEADER, RED_BG, RED_ALERT


def render_login():
    """Renderiza la pantalla de login del portal."""
    st.markdown(f"""
    <div style="border-top:4px solid {BLUE_HEADER};background:#fff;
                padding:14px 32px;margin:-1rem -1rem 0 -1rem;
                display:flex;align-items:center;gap:12px;
                box-shadow:0 2px 8px rgba(0,0,0,0.08);">
      <span style="font-size:26px;color:{GREEN};font-weight:900;">✦</span>
      <span style="font-size:22px;font-weight:700;color:{GRAY_DARK};">skandia</span>
      <span style="width:1px;height:26px;background:#ddd;margin:0 8px;"></span>
      <span style="font-size:14px;color:#666;">Portal Clientes</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Card centrada
    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        st.markdown(f"""
        <div style="background:#fff;border-radius:16px;padding:36px 32px;
                    box-shadow:0 4px 20px rgba(0,0,0,0.10);text-align:center;">
          <div style="font-size:30px;color:{GREEN};font-weight:900;margin-bottom:4px;">✦ skandia</div>
          <div style="font-size:15px;color:#666;margin-bottom:28px;">Ingresa a tu Portal Clientes</div>
        </div>
        """, unsafe_allow_html=True)

        intentos = st.session_state.get("login_intentos", 0)

        # Alerta de bloqueo
        if intentos >= 3:
            st.markdown(f"""
            <div class="sk-card-alert blink">
              🔒 <b>Portal bloqueado temporalmente</b><br/>
              Superaste el límite de intentos de acceso. Usa la opción de recuperar contraseña.
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔑 Recuperar contraseña", use_container_width=True):
                activar_error("ERR013", "Login")
                st.rerun()
            if st.button("🚨 Reportar actividad sospechosa", use_container_width=True):
                activar_error("ERR014", "Login")
                st.rerun()
            _render_chatbot_login()
            return

        with st.form("login_form"):
            st.markdown("**Número de documento**")
            documento = st.text_input("", placeholder="Ej: 1020456789", label_visibility="collapsed")
            st.markdown("**Contraseña**")
            password = st.text_input("", type="password", placeholder="••••••••", label_visibility="collapsed")
            recordar = st.checkbox("Recordar mi usuario")
            submitted = st.form_submit_button("Ingresar", use_container_width=True)

        st.markdown(
            f'<div style="text-align:center;margin-top:8px;">'
            f'<a href="#" style="color:{GREEN};text-decoration:none;font-size:14px;">¿Olvidaste tu contraseña?</a>'
            f'&nbsp;·&nbsp;'
            f'<a href="#" style="color:{GREEN};text-decoration:none;font-size:14px;">Regístrate aquí</a>'
            f'</div>',
            unsafe_allow_html=True
        )

        if submitted:
            _procesar_login(documento, password)

    # Errores de login activos
    if st.session_state.get("chatbot_activo"):
        _render_chatbot_login()


def _procesar_login(documento: str, password: str):
    """Valida credenciales demo y activa errores si corresponde."""
    # Usuario demo válidos: documento del cliente y password "skandia123"
    cliente_encontrado = None
    for c in CLIENTES_DEMO:
        if c["documento"] == documento.strip():
            cliente_encontrado = c
            break

    if not cliente_encontrado:
        st.session_state.login_intentos += 1
        log_accion(f"Intento fallido de login — documento: {documento}")
        st.error("⚠️ Usuario no encontrado. Verifica tu número de documento.")
        if st.session_state.login_intentos >= 2:
            st.warning("Recuerda: si no puedes acceder, usa '¿Olvidaste tu contraseña?'")
        return

    if password != "skandia123":
        st.session_state.login_intentos += 1
        restantes = 3 - st.session_state.login_intentos
        if restantes <= 0:
            activar_error("ERR013", "Login")
            st.rerun()
        st.error(f"⚠️ Contraseña incorrecta. Te quedan {max(restantes,0)} intento(s) antes del bloqueo.")
        log_accion(f"Contraseña incorrecta — {st.session_state.login_intentos} intento(s)")
        return

    # Login exitoso — mostrar OTP
    st.session_state.cliente_activo = cliente_encontrado
    st.session_state.escenario_demo = cliente_encontrado.get("escenario", "libre")
    st.session_state.login_intentos = 0
    st.session_state["mostrar_otp"] = True
    log_accion("Login exitoso — mostrando validación OTP")
    st.rerun()


def render_otp():
    """Renderiza el modal de validación OTP."""
    cliente = st.session_state.get("cliente_activo", {})

    st.markdown(f"""
    <div style="background:#fff;border-radius:16px;padding:36px 32px;
                box-shadow:0 4px 20px rgba(0,0,0,0.15);max-width:520px;margin:40px auto;
                text-align:center;">
      <div style="font-size:48px;margin-bottom:16px;">🔐</div>
      <h3 style="color:#2D2926;margin-bottom:8px;">Validación de seguridad</h3>
      <p style="color:#666;font-size:14px;">
        Ingresa el código enviado a tu celular y correo registrados.<br/>
        Si no lo recibes, solicítalo nuevamente al terminar el cronómetro.
      </p>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        with st.form("otp_form"):
            codigo = st.text_input("Escribe el código de verificación",
                                    placeholder="_ _ _ _ _ _",
                                    max_chars=6)
            st.caption("⏱️ Tiempo restante: 04:58 | Código demo: **123456**")
            col1, col2 = st.columns(2)
            with col1:
                reenviar = st.form_submit_button("Reenviar código", use_container_width=True)
            with col2:
                verificar = st.form_submit_button("Verificar ✓", use_container_width=True)

        st.markdown(
            f'<div style="text-align:center;"><a href="#" style="color:{GREEN};font-size:13px;">'
            f'¿No has recibido el código de seguridad?</a></div>',
            unsafe_allow_html=True
        )

        if reenviar:
            st.info("📱 Código reenviado a tu celular y correo registrado.")
            log_accion("OTP reenviado")

        if verificar:
            if codigo == "123456":
                st.session_state["mostrar_otp"] = False
                st.session_state.logged_in = True
                st.session_state.pagina_activa = "inicio"
                log_accion("OTP verificado — acceso concedido")
                st.rerun()
            else:
                st.error("❌ Código incorrecto. El código demo es 123456.")
                activar_error("ERR017", "Verificación OTP")
                st.rerun()


def _render_chatbot_login():
    """Chatbot embebido en la pantalla de login."""
    from modules.chatbot import render_chatbot
    st.markdown("---")
    render_chatbot()
