"""
Chatbot IA Skandia — panel siempre visible cuando hay error activo.
Se muestra como sección prominente ANTES del contenido de la página,
no al final. Incluye notificación proactiva y botón flotante.
"""

import streamlit as st
import datetime
from data.base_conocimiento import KNOWLEDGE_BASE, AGENTES_DEMO
from modules.session_manager import log_accion
from config.brand import GREEN, RED_ALERT, YELLOW_BDR


def render_chatbot_flotante():
    """
    Renderiza el banner de notificación proactivo cuando hay un error activo.
    Se llama al INICIO de cada página, antes de cualquier otro contenido.
    """
    if not st.session_state.get("chatbot_activo"):
        return
    if st.session_state.get("tecnico_conectado"):
        return

    error  = st.session_state.get("error_activo", {})
    cliente = st.session_state.get("cliente_activo", {})
    if not error or not cliente:
        return

    datos  = error.get("datos", {})
    nombre = cliente.get("nombre", "").split()[0]

    # ── Banner de alerta prominente con llamada a acción ──────────────────
    st.markdown(f"""
    <div style="background:#fff;border:3px solid {GREEN};border-radius:14px;
                padding:18px 22px;margin-bottom:20px;
                box-shadow:0 4px 20px rgba(0,210,97,0.25);">
      <div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;">
        <div style="font-size:42px;animation:pulse 2s ease-in-out infinite;">🤖</div>
        <div style="flex:1;min-width:200px;">
          <div style="font-weight:700;font-size:16px;color:{GREEN};">
            Agente IA Skandia ● En línea
          </div>
          <div style="font-size:14px;color:#2D2926;margin-top:2px;">
            Hola <b>{nombre}</b>, detecté un inconveniente:
            <b style="color:{RED_ALERT};">{datos.get('titulo','')}</b>
          </div>
          <div style="font-size:13px;color:#666;margin-top:4px;">
            👇 Expande el asistente para recibir ayuda paso a paso
          </div>
        </div>
        <div style="font-size:24px;animation:blink 1.3s ease-in-out infinite;">⚠️</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Panel expandido del chatbot ────────────────────────────────────────
    with st.expander("🤖 Abrir Asistente IA — Solución paso a paso", expanded=True):
        _render_pasos(cliente, error, datos)


def render_chatbot():
    """Alias para compatibilidad — llama al flotante."""
    render_chatbot_flotante()


def _render_pasos(cliente, error, datos):
    """Renderiza el flujo guiado de pasos del chatbot."""
    pasos      = datos.get("solucion_ia", [])
    completados = st.session_state.get("chatbot_pasos_completados", [])
    nombre     = cliente.get("nombre", "").split()[0]

    # Mensaje de bienvenida
    st.markdown(f"""
    <div class="bubble-agent">
      👋 Hola <b>{nombre}</b>, estoy analizando tu situación en
      <b>{st.session_state.get('modulo_origen','el portal')}</b>.<br/><br/>
      🔍 <b>Problema detectado:</b> {datos.get('titulo','')}<br/>
      📋 <b>Categoría:</b> {datos.get('categoria','')}<br/><br/>
      Sigue los pasos a continuación para resolver el inconveniente:
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Pasos con progreso visual ──────────────────────────────────────────
    total_pasos = len(pasos)
    num_done    = len(completados)

    # Barra de progreso
    if total_pasos > 0:
        pct = num_done / total_pasos
        st.progress(pct, text=f"Progreso: {num_done}/{total_pasos} pasos completados")

    hay_pendiente = False
    for i, paso in enumerate(pasos):
        done = i in completados
        if done:
            st.markdown(f"""
            <div style="display:flex;align-items:flex-start;gap:10px;margin:8px 0;
                        padding:10px 14px;background:#E8F5E9;border-radius:8px;">
              <span style="font-size:18px;margin-top:1px;">✅</span>
              <div>
                <span style="font-size:12px;color:#666;">Paso {i+1}</span><br/>
                <span style="color:#1B5E20;">{paso}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)
        elif not hay_pendiente:
            # Paso activo actual
            hay_pendiente = True
            st.markdown(f"""
            <div style="display:flex;align-items:flex-start;gap:10px;margin:8px 0;
                        padding:12px 16px;background:#FFF8E1;border:2px solid {YELLOW_BDR};border-radius:8px;">
              <span style="font-size:18px;margin-top:1px;">▶️</span>
              <div style="flex:1;">
                <span style="font-size:12px;color:#666;">Paso {i+1} — ACCIÓN REQUERIDA</span><br/>
                <span style="font-weight:600;color:#2D2926;">{paso}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Botón de navegación si aplica
            modulo_destino = datos.get("modulo_destino", "")
            modulo_origen  = st.session_state.get("modulo_origen", "")
            nav_map = {
                "Cuentas Bancarias": "cuentas",
                "Mi Portafolio":     "portafolio",
                "Mis Datos":         "mis_datos",
                "Documentos":        "documentos",
                "Retiros":           "retiros",
                "Login":             "login",
            }
            if modulo_destino and modulo_destino != modulo_origen and modulo_destino in nav_map:
                st.markdown(f"""
                <div class="bubble-agent" style="margin:8px 0;">
                  📍 Para este paso necesitas ir a: <b>{modulo_destino}</b>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"➡️ Ir a {modulo_destino}", key=f"nav_dest_{i}", use_container_width=True):
                    st.session_state.pagina_activa = nav_map[modulo_destino]
                    log_accion(f"Navegó a {modulo_destino} por indicación del chatbot")
                    st.rerun()

            col1, col2 = st.columns([2, 1])
            with col1:
                if st.button(f"✅ Completé el paso {i+1}", key=f"paso_ok_{i}", use_container_width=True):
                    completados.append(i)
                    st.session_state.chatbot_pasos_completados = completados
                    log_accion(f"Chatbot paso {i+1} completado: {paso[:60]}")
                    st.rerun()
            with col2:
                if st.button(f"❓ No pude", key=f"paso_no_{i}", use_container_width=True):
                    log_accion(f"Chatbot paso {i+1} fallido: {paso[:60]}")
                    # Marcar todos los restantes como intentados y ofrecer técnico
                    st.session_state["ofrecer_tecnico"] = True
                    st.rerun()
        else:
            # Paso pendiente futuro
            st.markdown(f"""
            <div style="display:flex;align-items:flex-start;gap:10px;margin:8px 0;
                        padding:10px 14px;background:#f9f9f9;border-radius:8px;opacity:0.6;">
              <span style="font-size:18px;margin-top:1px;">⬜</span>
              <div>
                <span style="font-size:12px;color:#999;">Paso {i+1} — pendiente</span><br/>
                <span style="color:#888;">{paso}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Todos los pasos completados ────────────────────────────────────────
    if not hay_pendiente and num_done == total_pasos and total_pasos > 0:
        st.markdown("---")
        st.markdown(f"""
        <div class="bubble-agent">
          🎉 ¡Completaste todos los pasos! ¿Se resolvió tu inconveniente?
        </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Sí, ya quedó resuelto", key="chatbot_si", use_container_width=True):
                st.session_state.caso_resuelto   = True
                st.session_state.chatbot_activo  = False
                log_accion("Cliente confirmó resolución con Agente IA ✅")
                st.rerun()
        with col2:
            if st.button("❌ No, sigue el problema", key="chatbot_no", use_container_width=True):
                st.session_state["ofrecer_tecnico"] = True
                log_accion("Agente IA agotado — ofreciendo técnico")
                st.rerun()

    # ── Ofrecer técnico ────────────────────────────────────────────────────
    if st.session_state.get("ofrecer_tecnico"):
        _render_oferta_tecnico(datos)


def _render_oferta_tecnico(datos):
    st.markdown("---")
    st.markdown(f"""
    <div class="sk-card-warn">
      <div style="font-weight:700;font-size:15px;margin-bottom:8px;">
        🔧 El Agente IA no pudo resolver el inconveniente
      </div>
      ¿Deseas conectarte con un <b>Técnico Especializado en tiempo real</b>?<br/>
      El técnico recibirá todo el historial de lo que ya intentaste para no repetir pasos.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Resumen de lo que ya se intentó:**")
    pasos_ia = datos.get("solucion_ia", [])
    completados = st.session_state.get("chatbot_pasos_completados", [])
    for i, paso in enumerate(pasos_ia):
        icon = "✅" if i in completados else "❌"
        st.markdown(f"{icon} {paso}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("👨‍💻 Conectar con Técnico", key="btn_tecnico", use_container_width=True):
            st.session_state.tecnico_conectado  = True
            st.session_state.ofrecer_tecnico    = False
            st.session_state.chatbot_activo     = False
            log_accion("Cliente solicitó técnico en tiempo real")
            st.rerun()
    with col2:
        if st.button("✕ Salir sin soporte", key="btn_salir_chat", use_container_width=True):
            st.session_state.chatbot_activo  = False
            st.session_state.ofrecer_tecnico = False
            st.rerun()
