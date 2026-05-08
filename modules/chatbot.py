"""
Chatbot IA Skandia — widget flotante en esquina inferior derecha.
No invasivo: muestra un botón pill que el usuario puede expandir.
Solo se expande automáticamente si el error es crítico.
"""

import streamlit as st
import datetime
from data.base_conocimiento import KNOWLEDGE_BASE
from modules.session_manager import log_accion
from config.brand import GREEN, RED_ALERT, YELLOW_BDR


def render_chatbot_flotante():
    """
    Botón flotante pill en esquina inferior derecha.
    Se expande en un panel cuando el usuario hace clic o hay error crítico.
    """
    if not st.session_state.get("chatbot_activo"):
        return
    if st.session_state.get("tecnico_conectado"):
        return

    error   = st.session_state.get("error_activo", {})
    cliente = st.session_state.get("cliente_activo", {})
    if not error or not cliente:
        return

    datos   = error.get("datos", {})
    # ── Nombre correcto del cliente activo ──────────────────────────────
    nombre  = cliente.get("nombre", "Cliente").split()[0]
    es_critico = datos.get("es_critico", False)

    # ── Banner no invasivo en la parte superior ─────────────────────────
    # Solo un banner pequeño, NO un panel expandido automáticamente
    st.markdown(f"""
    <div class="slide-in" style="background:linear-gradient(135deg,#E8F5E9,#F1FFF7);
        border:2px solid {GREEN};border-radius:14px;padding:14px 20px;
        margin-bottom:18px;display:flex;align-items:center;gap:14px;flex-wrap:wrap;">
      <div style="width:44px;height:44px;background:{GREEN};border-radius:50%;
           display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0;">
        🤖
      </div>
      <div style="flex:1;min-width:180px;">
        <div style="font-weight:700;font-size:14px;color:#1B5E20;">
          Agente IA Skandia • En línea
        </div>
        <div style="font-size:13px;color:#2D2926;margin-top:2px;">
          Hola <b>{nombre}</b> — detecté: <b style="color:{RED_ALERT};">{datos.get('titulo','')}</b>
        </div>
      </div>
      <div style="font-size:11px;color:#666;text-align:right;white-space:nowrap;">
        👇 Ver solución abajo
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Panel del chatbot — colapsado por defecto, expandible ─────────────
    panel_key = f"panel_chatbot_{error.get('error_id','')}"
    if panel_key not in st.session_state:
        # Auto-expandir solo si es crítico
        st.session_state[panel_key] = es_critico

    with st.expander(
        f"🤖 Asistente IA — Solución para: {datos.get('titulo','')}",
        expanded=st.session_state.get(panel_key, False)
    ):
        _render_pasos_chatbot(cliente, error, datos, nombre)


def render_chatbot():
    """Alias de compatibilidad."""
    render_chatbot_flotante()


def _render_pasos_chatbot(cliente, error, datos, nombre):
    """Pasos guiados del chatbot con visual mejorado."""
    pasos       = datos.get("solucion_ia", [])
    completados = st.session_state.get("chatbot_pasos_completados", [])

    # Mensaje de bienvenida del agente
    st.markdown(f"""
    <div class="bubble-agent">
      👋 Hola <b>{nombre}</b>, estoy analizando lo que ocurrió en
      <b>{st.session_state.get('modulo_origen','el portal')}</b>.<br/><br/>
      🔍 <b>Problema:</b> {datos.get('titulo','')}<br/>
      📋 <b>Categoría:</b> {datos.get('categoria','')}<br/><br/>
      Sigue los pasos para resolverlo:
    </div>
    """, unsafe_allow_html=True)

    # Barra de progreso
    total  = len(pasos)
    ndone  = len(completados)
    if total > 0:
        st.progress(ndone / total, text=f"Progreso: {ndone}/{total} pasos completados")

    hay_pendiente = False
    for i, paso in enumerate(pasos):
        done = i in completados
        if done:
            st.markdown(f"""
            <div class="paso-done">
              ✅ <span style="color:#1B5E20;font-size:13px;"><b>Paso {i+1}</b> completado</span><br/>
              <span style="color:#2E7D32;font-size:13px;">{paso}</span>
            </div>
            """, unsafe_allow_html=True)
        elif not hay_pendiente:
            hay_pendiente = True
            st.markdown(f"""
            <div class="paso-activo">
              ▶️ <span style="font-size:12px;color:#795548;font-weight:600;">PASO {i+1} — ACCIÓN REQUERIDA</span><br/>
              <span style="font-weight:600;color:#2D2926;font-size:14px;">{paso}</span>
            </div>
            """, unsafe_allow_html=True)

            # Botón de navegación si aplica
            _boton_navegacion(datos, i)

            col_si, col_no = st.columns([3, 2])
            with col_si:
                if st.button(f"✅ Completé el paso {i+1}", key=f"paso_ok_{i}_{error.get('error_id','')}",
                             use_container_width=True):
                    completados.append(i)
                    st.session_state.chatbot_pasos_completados = completados
                    log_accion(f"Paso {i+1} completado: {paso[:50]}")
                    st.rerun()
            with col_no:
                if st.button(f"❓ No pude hacerlo", key=f"paso_no_{i}_{error.get('error_id','')}",
                             use_container_width=True):
                    log_accion(f"Paso {i+1} no resuelto — ofreciendo técnico")
                    st.session_state["ofrecer_tecnico"] = True
                    st.rerun()
        else:
            st.markdown(f"""
            <div class="paso-pending">
              ⬜ <span style="font-size:12px;color:#999;">Paso {i+1} — pendiente</span><br/>
              <span style="color:#aaa;font-size:13px;">{paso}</span>
            </div>
            """, unsafe_allow_html=True)

    # ── Todos completados ─────────────────────────────────────────────────
    if not hay_pendiente and ndone == total and total > 0:
        st.markdown(f"""
        <div class="sk-card-success" style="text-align:center;padding:20px;">
          <div style="font-size:36px;margin-bottom:8px;">🎉</div>
          <b style="font-size:15px;">¡Completaste todos los pasos!</b><br/>
          <span style="color:#555;font-size:13px;">¿Se resolvió tu inconveniente?</span>
        </div>
        """, unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Sí, resuelto", key=f"si_{error.get('error_id','')}", use_container_width=True):
                _marcar_resuelto()
        with c2:
            if st.button("❌ No, persiste", key=f"no_{error.get('error_id','')}", use_container_width=True):
                st.session_state["ofrecer_tecnico"] = True
                log_accion("Cliente indicó que el problema persiste — ofreciendo técnico")
                st.rerun()

    # ── Ofrecer técnico ───────────────────────────────────────────────────
    if st.session_state.get("ofrecer_tecnico"):
        _render_oferta_tecnico(datos)


def _boton_navegacion(datos, paso_idx):
    """Muestra botón de navegación al módulo destino si aplica."""
    nav_map = {
        "Cuentas Bancarias": "cuentas",
        "Mi Portafolio":     "portafolio",
        "Mis Datos":         "mis_datos",
        "Documentos":        "documentos",
        "Retiros":           "retiros",
        "Login":             "login",
    }
    modulo_destino = datos.get("modulo_destino", "")
    modulo_origen  = st.session_state.get("modulo_origen", "")
    if modulo_destino and modulo_destino != modulo_origen and modulo_destino in nav_map:
        st.markdown(f"""
        <div style="background:#E3F2FD;border-radius:10px;padding:10px 14px;
                    margin:6px 0;font-size:13px;">
          📍 Para completar este paso debes ir a: <b>{modulo_destino}</b>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"➡️ Ir a {modulo_destino}", key=f"nav_{modulo_destino}_{paso_idx}",
                     use_container_width=True):
            # Guardar página de origen para regresar
            st.session_state["pagina_origen_chatbot"] = st.session_state.get("pagina_activa","")
            st.session_state.pagina_activa = nav_map[modulo_destino]
            log_accion(f"Chatbot: navegó a {modulo_destino}")
            st.rerun()


def _marcar_resuelto():
    """Marca el caso como resuelto y limpia el estado del error."""
    log_accion("Caso resuelto por Agente IA ✅")
    st.session_state.caso_resuelto   = True
    st.session_state.chatbot_activo  = False
    st.session_state.error_activo    = None   # ← limpiar error para no repetir
    st.session_state.ofrecer_tecnico = False
    # Limpiar flag de error ya disparado para que no vuelva a activarse
    st.session_state["error_disparado_retiros"] = True
    st.session_state["error_disparado_cuentas"] = True
    st.session_state["error_disparado_portafolio"] = True
    st.rerun()


def _render_oferta_tecnico(datos):
    st.markdown("---")
    st.markdown(f"""
    <div class="sk-card-warn slide-in">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
        <span style="font-size:24px;">🔧</span>
        <b style="font-size:15px;">El Agente IA no pudo resolver el inconveniente</b>
      </div>
      <p style="color:#555;font-size:13px;margin:0;">
        ¿Deseas conectarte con un <b>Técnico Especializado en tiempo real</b>?<br/>
        El técnico recibirá todo el historial sin que tengas que repetir nada.
      </p>
    </div>
    """, unsafe_allow_html=True)

    pasos_ia   = datos.get("solucion_ia", [])
    completados = st.session_state.get("chatbot_pasos_completados", [])
    with st.expander("📋 Ver resumen de lo intentado", expanded=False):
        for i, p in enumerate(pasos_ia):
            st.markdown(f"{'✅' if i in completados else '❌'} {p}")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("👨‍💻 Conectar con Técnico", key="btn_tec_offer", use_container_width=True):
            st.session_state.tecnico_conectado  = True
            st.session_state.ofrecer_tecnico    = False
            st.session_state.chatbot_activo     = False
            log_accion("Técnico solicitado por el cliente")
            st.rerun()
    with c2:
        if st.button("✕ Salir sin soporte", key="btn_salir_chat", use_container_width=True):
            st.session_state.chatbot_activo  = False
            st.session_state.ofrecer_tecnico = False
            st.rerun()
