"""Inicialización y helpers de st.session_state."""
import datetime
import streamlit as st


def init_session():
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
        "ofrecer_tecnico": False,
        "tecnico_conectado": False,
        "tecnico_chat": [],
        "tecnico_acciones": [],
        "caso_escalado": False,
        "caso_resuelto": False,
        "ticket_actual": None,
        "modulo_origen": "",
        "notificaciones_enviadas": [],
        "retiro_paso": 1,
        "retiro_producto": None,
        "retiro_monto": 5000,
        "cuenta_paso": 1,
        "nps_score": 8,
        "nps_comentario": "",
        "timestamp_inicio": datetime.datetime.now(),
        # Flags para evitar re-disparo de errores
        "error_disparado_retiros": False,
        "error_disparado_cuentas": False,
        "error_disparado_portafolio": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def log_accion(accion: str):
    entrada = {"hora": datetime.datetime.now().strftime("%H:%M:%S"), "accion": accion}
    if "chatbot_log" not in st.session_state:
        st.session_state.chatbot_log = []
    st.session_state.chatbot_log.append(entrada)


def activar_error(error_id: str, modulo: str):
    """Activa error y chatbot. No reactiva si ya fue resuelto."""
    from data.base_conocimiento import KNOWLEDGE_BASE
    if error_id not in KNOWLEDGE_BASE:
        return
    # No reactivar si el caso ya fue resuelto en este flujo
    flag_key = f"error_disparado_{modulo.lower().replace(' ','_')}"
    if st.session_state.get(flag_key, False):
        return
    st.session_state.error_activo              = {"error_id": error_id, "datos": KNOWLEDGE_BASE[error_id]}
    st.session_state.chatbot_activo            = True
    st.session_state.ofrecer_tecnico           = False
    st.session_state.modulo_origen             = modulo
    st.session_state.chatbot_pasos_completados = []
    st.session_state.chatbot_mensajes          = []
    st.session_state.timestamp_inicio          = datetime.datetime.now()
    log_accion(f"[ERROR] {error_id} en {modulo}")


def limpiar_error():
    """Limpia el error activo y marca como resuelto para no re-disparar."""
    modulo = st.session_state.get("modulo_origen", "")
    flag_key = f"error_disparado_{modulo.lower().replace(' ','_')}"
    st.session_state[flag_key]        = True
    st.session_state.error_activo     = None
    st.session_state.chatbot_activo   = False
    st.session_state.ofrecer_tecnico  = False
    st.session_state.caso_resuelto    = True


def reset_demo():
    keys = [
        "error_activo","chatbot_activo","chatbot_pasos_completados",
        "chatbot_log","chatbot_mensajes","ofrecer_tecnico",
        "tecnico_conectado","tecnico_chat","tecnico_acciones",
        "caso_escalado","caso_resuelto","ticket_actual","modulo_origen",
        "notificaciones_enviadas","retiro_paso","retiro_producto",
        "cuenta_paso","login_intentos",
        "error_disparado_retiros","error_disparado_cuentas","error_disparado_portafolio",
    ]
    for k in keys:
        if k in st.session_state:
            del st.session_state[k]
    init_session()
