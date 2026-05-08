"""Componente del Agente IA — chatbot contextual de soporte."""

import streamlit as st
import datetime
from data.base_conocimiento import KNOWLEDGE_BASE, AGENTES_DEMO
from modules.session_manager import log_accion
from config.brand import GREEN, RED_ALERT


def render_chatbot():
    """Renderiza el panel del chatbot si está activo."""
    if not st.session_state.get("chatbot_activo"):
        return

    error = st.session_state.get("error_activo", {})
    cliente = st.session_state.get("cliente_activo", {})
    if not error or not cliente:
        return

    datos = error.get("datos", {})
    pasos = datos.get("solucion_ia", [])
    completados = st.session_state.get("chatbot_pasos_completados", [])

    st.markdown("---")
    st.markdown(f"""
    <div style="background:#fff;border-radius:12px;padding:20px;
                border:2px solid {GREEN};box-shadow:0 2px 12px rgba(0,210,97,0.15);">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
        <span style="font-size:28px;">🤖</span>
        <div>
          <div style="font-weight:700;font-size:16px;color:#2D2926;">Agente IA Skandia</div>
          <div style="font-size:12px;color:{GREEN};">● En línea</div>
        </div>
      </div>
    """, unsafe_allow_html=True)

    # Mensaje inicial del agente
    nombre = cliente.get("nombre", "").split()[0]
    st.markdown(f"""
    <div class="bubble-agent">
      👋 Hola <strong>{nombre}</strong>, veo que estás teniendo un inconveniente en 
      <strong>{st.session_state.get('modulo_origen','el portal')}</strong>.<br/><br/>
      🔍 Detecté que podría ser: <strong>{datos.get('titulo','un error técnico')}</strong><br/><br/>
      Te guío paso a paso para resolverlo. ¿Empezamos?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Pasos para resolver tu inconveniente:**")

    all_done = True
    for i, paso in enumerate(pasos):
        done = i in completados
        if not done:
            all_done = False
        icono = "✅" if done else "⬜"
        color = "#1B5E20" if done else "#555"
        st.markdown(
            f'<div style="margin:6px 0;color:{color};">{icono} <b>Paso {i+1}:</b> {paso}</div>',
            unsafe_allow_html=True
        )
        if not done:
            if st.button(f"✓ Marcar paso {i+1} como realizado", key=f"paso_{i}"):
                completados.append(i)
                st.session_state.chatbot_pasos_completados = completados
                log_accion(f"Chatbot: Paso {i+1} completado — {paso[:50]}")
                st.rerun()
            break  # Mostrar solo el siguiente paso

    # Módulo destino
    modulo_destino = datos.get("modulo_destino", "")
    if modulo_destino and modulo_destino != st.session_state.get("modulo_origen", ""):
        st.markdown(f"""
        <div class="bubble-agent" style="margin-top:8px;">
          📍 Para completar este paso necesitas ir a: <strong>{modulo_destino}</strong>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"➡️ Ir a {modulo_destino}", key="nav_modulo"):
            log_accion(f"Navegación al módulo: {modulo_destino}")
            st.info(f"En la demo: navega al módulo '{modulo_destino}' en el menú lateral.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Pregunta final si todos los pasos están completos
    if all_done and len(completados) == len(pasos):
        st.markdown("---")
        st.markdown("""
        <div class="bubble-agent">
          ✅ ¡Completaste todos los pasos! ¿Lograste resolver el inconveniente?
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Sí, fue resuelto", key="resuelto_si", use_container_width=True):
                st.session_state.caso_resuelto = True
                st.session_state.chatbot_activo = False
                log_accion("Cliente confirmó resolución exitosa con Agente IA")
                st.success("🎉 ¡Excelente! Tu inconveniente fue resuelto. Puedes continuar con tu proceso.")
                st.rerun()
        with col2:
            if st.button("❌ No, sigue el problema", key="resuelto_no", use_container_width=True):
                log_accion("Agente IA no resolvió — se ofrece técnico")
                st.session_state["ofrecer_tecnico"] = True
                st.rerun()

    # Ofrecer técnico
    if st.session_state.get("ofrecer_tecnico"):
        _render_oferta_tecnico(cliente, error, datos)


def _render_oferta_tecnico(cliente, error, datos):
    """Ofrece conexión con técnico si el chatbot no resolvió."""
    st.markdown("---")
    st.markdown(f"""
    <div class="sk-card-warn">
      <b>🔧 Conectar con un Técnico Especializado</b><br/>
      El Agente IA ha agotado las opciones disponibles en la base de conocimiento.<br/><br/>
      ¿Deseas que un técnico te acompañe en tiempo real para validar tu inconveniente?<br/>
      Se compartirá el historial de validaciones ya realizadas para no repetir pasos.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Validaciones ya realizadas (checklist):**")
    for i, paso in enumerate(datos.get("solucion_ia", [])):
        done = i in st.session_state.chatbot_pasos_completados
        st.markdown(f"{'✅' if done else '❌'} {paso}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("👨‍💻 Sí, conectar con técnico", key="conectar_tecnico", use_container_width=True):
            st.session_state.tecnico_conectado = True
            st.session_state.ofrecer_tecnico = False
            st.session_state.chatbot_activo = False
            log_accion("Cliente solicitó conexión con técnico")
            st.rerun()
    with col2:
        if st.button("❌ No, prefiero salir", key="salir_sin_tecnico", use_container_width=True):
            st.session_state.chatbot_activo = False
            st.session_state.ofrecer_tecnico = False
            st.rerun()
