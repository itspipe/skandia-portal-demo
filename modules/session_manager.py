"""Inicialización y helpers de st.session_state."""

import datetime
import streamlit as st


def init_session():
    """Inicializa todas las claves de session_state necesarias."""
    defaults = {
        "logged_in": False,
        "login_intentos": 0,
        "cliente_activo": None,
        "escenario_demo": "libre",
        "pagina_activa": "login",
        "error_activo": None,
        "chatbot_activo": False,
        "chatbot_pasos_completados": [],
        "chatbot_log": [],
        "chatbot_mensajes": [],
        "tecnico_conectado": False,
        "tecnico_chat": [],
        "tecnico_acciones": [],
        "caso_escalado": False,
        "caso_resuelto": False,
        "ticket_actual": None,
        "modulo_origen": "",
        "notificaciones_enviadas": [],
        "df_nps": None,
        "retiro_paso": 1,
        "retiro_producto": None,
        "retiro_monto": 5000,
        "retiro_tipo": "parcial",
        "cuenta_paso": 1,
        "nps_score": 8,
        "nps_comentario": "",
        "timestamp_inicio": datetime.datetime.now(),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def log_accion(accion: str):
    """Agrega una entrada al log de la sesión."""
    entrada = {
        "hora": datetime.datetime.now().strftime("%H:%M:%S"),
        "accion": accion,
    }
    st.session_state.chatbot_log.append(entrada)


def activar_error(error_id: str, modulo: str):
    """Activa un error y el chatbot."""
    from data.base_conocimiento import KNOWLEDGE_BASE
    if error_id not in KNOWLEDGE_BASE:
        return
    st.session_state.error_activo = {
        "error_id": error_id,
        "datos": KNOWLEDGE_BASE[error_id],
    }
    st.session_state.chatbot_activo = True
    st.session_state.modulo_origen = modulo
    st.session_state.chatbot_pasos_completados = []
    st.session_state.chatbot_mensajes = []
    st.session_state.timestamp_inicio = datetime.datetime.now()
    log_accion(f"Error {error_id} detectado en módulo {modulo}")


def reset_demo():
    """Resetea el estado de la demo manteniendo el cliente seleccionado."""
    keys_to_reset = [
        "error_activo", "chatbot_activo", "chatbot_pasos_completados",
        "chatbot_log", "chatbot_mensajes", "tecnico_conectado",
        "tecnico_chat", "tecnico_acciones", "caso_escalado", "caso_resuelto",
        "ticket_actual", "modulo_origen", "notificaciones_enviadas",
        "retiro_paso", "retiro_producto", "cuenta_paso",
        "login_intentos",
    ]
    for k in keys_to_reset:
        if k in st.session_state:
            del st.session_state[k]
    init_session()
