"""
Chatbot IA Skandia — popup flotante en esquina inferior derecha.
Se abre/cierra con un botón FAB. No bloquea la interfaz principal.
Guía al usuario directamente al módulo correcto y retorna automáticamente.
"""
import streamlit as st
import datetime
from modules.session_manager import log_accion
from config.brand import GREEN, RED_ALERT, YELLOW_B


NAV_MAP = {
    "Cuentas Bancarias": "cuentas",
    "Mi Portafolio":     "portafolio",
    "Mis Datos":         "mis_datos",
    "Documentos":        "documentos",
    "Retiros":           "retiros",
    "Login":             "login",
}


def render_chatbot_flotante():
    """
    Muestra el botón FAB flotante y el popup del chatbot.
    Debe llamarse al FINAL de cada página para no interrumpir el layout.
    """
    if not st.session_state.get("chatbot_activo"):
        return
    if st.session_state.get("tecnico_conectado"):
        return

    error   = st.session_state.get("error_activo", {})
    cliente = st.session_state.get("cliente_activo", {})
    if not error or not cliente:
        return

    datos  = error.get("datos", {})
    nombre = cliente.get("nombre", "Cliente").split()[0]

    # ── Inicializar estado del popup ──────────────────────────────────────
    if "chatbot_popup_abierto" not in st.session_state:
        st.session_state.chatbot_popup_abierto = True  # Abre automáticamente al detectar error

    # ── Botón FAB + tooltip ───────────────────────────────────────────────
    error_count = len(datos.get("solucion_ia", [])) - len(st.session_state.get("chatbot_pasos_completados", []))

    st.markdown(f"""
    <div style="position:fixed;bottom:22px;right:24px;z-index:9999;">
      <div class="chatbot-fab" title="Agente IA Skandia">
        🤖
        <div class="chatbot-fab-badge">{max(error_count,1)}</div>
      </div>
    </div>
    {'<div class="chatbot-tooltip">💬 Tengo la solución para ti</div>' if not st.session_state.chatbot_popup_abierto else ''}
    """, unsafe_allow_html=True)

    # ── Control de apertura/cierre ────────────────────────────────────────
    col_fab, _ = st.columns([1, 8])
    with col_fab:
        btn_label = "🤖 Cerrar" if st.session_state.chatbot_popup_abierto else "🤖 Ayuda"
        if st.button(btn_label, key="fab_toggle", help="Agente IA Skandia"):
            st.session_state.chatbot_popup_abierto = not st.session_state.chatbot_popup_abierto
            st.rerun()

    if not st.session_state.chatbot_popup_abierto:
        return

    # ── Popup del chatbot ─────────────────────────────────────────────────
    st.markdown(f"""
    <div class="chatbot-popup-overlay slide-up">
      <div class="chatbot-popup-header">
        <div style="width:36px;height:36px;background:rgba(255,255,255,0.25);
             border-radius:50%;display:flex;align-items:center;
             justify-content:center;font-size:18px;">🤖</div>
        <div>
          <div style="font-weight:700;font-size:14px;">Agente IA Skandia</div>
          <div style="font-size:11px;opacity:0.8;">● En línea — listo para ayudarte</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Contenido del chat usando expander ────────────────────────────────
    with st.expander("💬 Ver conversación con el Agente IA", expanded=True):
        _render_chat_body(cliente, error, datos, nombre)


def render_chatbot():
    """Alias para compatibilidad."""
    render_chatbot_flotante()


def _render_chat_body(cliente, error, datos, nombre):
    """Cuerpo del chat con pasos guiados."""
    pasos       = datos.get("solucion_ia", [])
    completados = st.session_state.get("chatbot_pasos_completados", [])
    total       = len(pasos)
    ndone       = len(completados)

    # Bienvenida del agente
    st.markdown(f"""
    <div class="bubble-agent">
      👋 Hola <b>{nombre}</b>, vi que tuviste un inconveniente en
      <b>{st.session_state.get('modulo_origen','el portal')}</b>.<br/>
      🔍 <b>{datos.get('titulo','')}</b><br/>
      <span style="color:#888;font-size:12px;">Te guío paso a paso:</span>
    </div>
    """, unsafe_allow_html=True)

    # Progreso
    if total > 0:
        st.progress(ndone / total, text=f"{ndone}/{total} pasos")

    hay_pendiente = False
    paso_pendiente_idx = -1

    for i, paso in enumerate(pasos):
        done = i in completados
        if done:
            st.markdown(f"""
            <div class="paso-done">
              ✅ <b style="color:#1B5E20;font-size:12px;">Paso {i+1}</b>
              <span style="color:#2E7D32;font-size:13px;"> {paso}</span>
            </div>
            """, unsafe_allow_html=True)
        elif not hay_pendiente:
            hay_pendiente = True
            paso_pendiente_idx = i
            st.markdown(f"""
            <div class="paso-activo">
              <div style="font-size:11px;color:#795548;font-weight:700;
                   text-transform:uppercase;letter-spacing:0.5px;">
                ▶ Paso {i+1} — Acción requerida
              </div>
              <div style="font-size:13px;font-weight:600;color:#2D2926;margin-top:4px;">
                {paso}
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Botón de navegación directo al módulo
            modulo_dest = datos.get("modulo_destino","")
            modulo_orig = st.session_state.get("modulo_origen","")
            if modulo_dest and modulo_dest != modulo_orig and modulo_dest in NAV_MAP:
                st.markdown(f"""
                <div style="background:#EBF3FF;border-radius:8px;padding:8px 12px;
                     margin:6px 0;font-size:12px;color:#1565C0;">
                  📍 Debes ir a: <b>{modulo_dest}</b> para completar este paso
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"➡️ Ir ahora a {modulo_dest}", key=f"nav_{i}_{modulo_dest}",
                             use_container_width=True):
                    # Guardar página de retorno
                    st.session_state["retorno_chatbot"] = st.session_state.get("pagina_activa","inicio")
                    st.session_state.pagina_activa = NAV_MAP[modulo_dest]
                    log_accion(f"Chatbot: navegó a {modulo_dest}, retorna a {st.session_state['retorno_chatbot']}")
                    st.rerun()

            c1, c2 = st.columns([3, 2])
            with c1:
                if st.button(f"✅ Listo, lo hice", key=f"ok_{i}_{error.get('error_id','')}",
                             use_container_width=True):
                    completados.append(i)
                    st.session_state.chatbot_pasos_completados = completados
                    log_accion(f"Paso {i+1} completado")
                    # Si hay retorno pendiente, navegar de vuelta
                    if st.session_state.get("retorno_chatbot"):
                        retorno = st.session_state.pop("retorno_chatbot")
                        st.session_state.pagina_activa = retorno
                        log_accion(f"Retornando a {retorno} tras completar paso")
                    st.rerun()
            with c2:
                if st.button("❓ No pude", key=f"no_{i}_{error.get('error_id','')}",
                             use_container_width=True):
                    st.session_state["ofrecer_tecnico"] = True
                    log_accion(f"Paso {i+1} fallido — ofreciendo técnico")
                    st.rerun()
        else:
            st.markdown(f"""
            <div class="paso-pending">
              ⬜ <span style="font-size:12px;color:#999;">Paso {i+1}:</span>
              <span style="color:#bbb;font-size:13px;"> {paso}</span>
            </div>
            """, unsafe_allow_html=True)

    # Todos completados
    if not hay_pendiente and ndone == total and total > 0:
        st.markdown(f"""
        <div class="bubble-agent" style="background:linear-gradient(135deg,#E8F5E9,#F0FFF6);">
          🎉 ¡Completaste todos los pasos!<br/>
          <b>¿Se resolvió tu inconveniente?</b>
        </div>
        """, unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Sí, resuelto", key=f"si_{error.get('error_id','')}", use_container_width=True):
                _cerrar_resuelto()
        with c2:
            if st.button("❌ No, persiste", key=f"no_final_{error.get('error_id','')}", use_container_width=True):
                st.session_state["ofrecer_tecnico"] = True
                log_accion("Problema persiste — ofreciendo técnico")
                st.rerun()

    # Ofrecer técnico
    if st.session_state.get("ofrecer_tecnico"):
        _render_oferta_tecnico(datos)


def _cerrar_resuelto():
    log_accion("✅ Caso resuelto por Agente IA")
    st.session_state.caso_resuelto           = True
    st.session_state.chatbot_activo          = False
    st.session_state.error_activo            = None
    st.session_state.ofrecer_tecnico         = False
    st.session_state.chatbot_popup_abierto   = False
    st.session_state["error_disparado_retiros"]    = True
    st.session_state["error_disparado_cuentas"]    = True
    st.session_state["error_disparado_portafolio"] = True
    st.rerun()


def _render_oferta_tecnico(datos):
    st.markdown("---")
    st.markdown("""
    <div class="sk-card-warn">
      <b>🔧 El Agente IA no pudo resolver esto</b><br/>
      <span style="font-size:13px;">Un técnico puede ayudarte en tiempo real con todo el contexto ya cargado.</span>
    </div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("👨‍💻 Conectar Técnico", key="btn_tec", use_container_width=True):
            st.session_state.tecnico_conectado        = True
            st.session_state.ofrecer_tecnico          = False
            st.session_state.chatbot_activo           = False
            st.session_state.chatbot_popup_abierto    = False
            log_accion("Técnico solicitado")
            st.rerun()
    with c2:
        if st.button("✕ Salir", key="btn_salir_chat", use_container_width=True):
            st.session_state.chatbot_activo           = False
            st.session_state.ofrecer_tecnico          = False
            st.session_state.chatbot_popup_abierto    = False
            st.rerun()
