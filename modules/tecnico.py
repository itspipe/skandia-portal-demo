"""Interfaz del técnico en tiempo real — vista de soporte especializado."""

import streamlit as st
import datetime
from data.base_conocimiento import AGENTES_DEMO
from modules.report_generator import generar_informe_tecnico, generar_ticket_escalamiento, simular_correos
from modules.session_manager import log_accion
from config.brand import GREEN, RED_ALERT, YELLOW_WARN


def render_tecnico():
    """Renderiza la interfaz completa del técnico."""
    cliente = st.session_state.get("cliente_activo", {})
    error = st.session_state.get("error_activo", {})
    if not cliente or not error:
        st.warning("No hay caso activo para gestionar.")
        return

    datos = error.get("datos", {})
    fp = AGENTES_DEMO.get(cliente.get("fp_id", "FP001"), {})
    agente = AGENTES_DEMO.get("AGT001", {})

    st.markdown(f"""
    <div style="background:{RED_ALERT};color:white;padding:12px 20px;border-radius:8px;
                display:flex;align-items:center;gap:10px;margin-bottom:16px;">
      <span style="font-size:20px;">🔴</span>
      <b>CASO ACTIVO — Técnico conectado</b>
      <span style="margin-left:auto;font-size:12px;">
        Ticket iniciado: {st.session_state.get('timestamp_inicio',datetime.datetime.now()).strftime('%H:%M:%S')}
      </span>
    </div>
    """, unsafe_allow_html=True)

    col_cliente, col_tecnico = st.columns([1, 1])

    # ── Panel cliente (izquierda) ─────────────────────────────────────────
    with col_cliente:
        st.markdown("### 👤 Vista del Cliente")
        st.markdown(f"""
        <div class="sk-card">
          <b>{cliente.get('nombre','')}</b><br/>
          📋 Contrato: {cliente.get('contrato','')}<br/>
          📧 {cliente.get('email','')}<br/>
          📱 {cliente.get('telefono','')}<br/>
          <span class="badge-err">Error: {error.get('error_id','')}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sk-card-alert">
          <b>🔴 {datos.get('titulo','')}</b><br/>
          {datos.get('descripcion','')}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Pasos ya intentados con Agente IA:**")
        for i, paso in enumerate(datos.get("solucion_ia", [])):
            done = i in st.session_state.get("chatbot_pasos_completados", [])
            st.markdown(f"{'✅' if done else '❌'} {paso}")

        # Chat del cliente
        st.markdown("**💬 Chat con el Técnico:**")
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.get("tecnico_chat", []):
                css_class = "bubble-user" if msg["rol"] == "cliente" else "bubble-tech"
                st.markdown(
                    f'<div class="{css_class}"><b>{"Tú" if msg["rol"]=="cliente" else "🔧 "+agente.get("nombre","")}:</b> {msg["texto"]}</div>',
                    unsafe_allow_html=True
                )

        msg_cliente = st.text_input("Escribe tu mensaje:", key="msg_cliente_input", placeholder="Cuéntale al técnico tu situación...")
        if st.button("Enviar →", key="enviar_cliente"):
            if msg_cliente.strip():
                st.session_state.tecnico_chat.append({
                    "rol": "cliente",
                    "texto": msg_cliente,
                    "hora": datetime.datetime.now().strftime("%H:%M:%S")
                })
                log_accion(f"Cliente: {msg_cliente[:60]}")
                st.rerun()

    # ── Panel técnico (derecha) ───────────────────────────────────────────
    with col_tecnico:
        st.markdown(f"### {agente.get('avatar','🔧')} Vista del Técnico — {agente.get('nombre','')}")

        st.markdown(f"""
        <div class="sk-card">
          <b>📋 Resumen del caso</b><br/>
          🕐 Inicio: {st.session_state.get('timestamp_inicio',datetime.datetime.now()).strftime('%H:%M:%S')}<br/>
          📍 Módulo: {st.session_state.get('modulo_origen','')}<br/>
          🔴 Error: <b>{error.get('error_id','')} — {datos.get('titulo','')}</b><br/>
          👤 FP Asignado: {fp.get('nombre','')} ({fp.get('email','')})
        </div>
        """, unsafe_allow_html=True)

        # Log de acciones
        with st.expander("📋 Ver log completo de la experiencia", expanded=False):
            for entrada in st.session_state.get("chatbot_log", []):
                st.markdown(f"`[{entrada['hora']}]` {entrada['accion']}")

        # Acciones del técnico
        st.markdown("**🛠️ Acciones del Técnico:**")
        accion_tecnico = st.text_input("Registrar acción:", key="accion_tecnico_input",
                                       placeholder="Ej: Validé la cuenta en el sistema back-office...")
        if st.button("➕ Registrar acción", key="reg_accion"):
            if accion_tecnico.strip():
                entrada = {
                    "hora": datetime.datetime.now().strftime("%H:%M:%S"),
                    "accion": accion_tecnico
                }
                st.session_state.tecnico_acciones.append(entrada)
                log_accion(f"Técnico: {accion_tecnico[:60]}")
                # Respuesta automática al chat
                st.session_state.tecnico_chat.append({
                    "rol": "tecnico",
                    "texto": accion_tecnico,
                    "hora": datetime.datetime.now().strftime("%H:%M:%S")
                })
                st.rerun()

        for a in st.session_state.get("tecnico_acciones", []):
            st.markdown(f"🔧 `[{a['hora']}]` {a['accion']}")

        st.markdown("---")

        col_ok, col_esc = st.columns(2)
        with col_ok:
            if st.button("✅ Marcar como RESUELTO", key="tecnico_resuelto", use_container_width=True):
                _resolver_caso_tecnico(cliente, error, datos, fp, agente)
        with col_esc:
            if st.button("🚨 ESCALAR a Mesa de Ayuda", key="tecnico_escalar", use_container_width=True):
                _escalar_caso(cliente, error, datos, fp, agente)


def _resolver_caso_tecnico(cliente, error, datos, fp, agente):
    """Cierra el caso como resuelto por el técnico."""
    st.session_state.caso_resuelto = True
    st.session_state.tecnico_conectado = False
    log_accion(f"Técnico {agente.get('nombre','')} marcó el caso como RESUELTO")

    correos_ok = [
        {
            "destinatario": cliente.get("email", ""),
            "asunto": "Tu caso fue resuelto — Skandia",
            "cuerpo": f"Estimado/a {cliente.get('nombre','')},\n\nTu inconveniente con '{datos.get('titulo','')}' fue resuelto exitosamente por nuestro equipo técnico.\n\nNuestro agente {agente.get('nombre','')} realizó las validaciones necesarias y el proceso está disponible para que lo completes.\n\n¡Gracias por tu paciencia!\nEquipo Skandia",
        },
        {
            "destinatario": fp.get("email", ""),
            "asunto": f"[FP] Caso resuelto — {cliente.get('nombre','')}",
            "cuerpo": f"Hola {fp.get('nombre','')},\n\nEl caso de tu cliente {cliente.get('nombre','')} fue resuelto por {agente.get('nombre','')}.\n\nError: {datos.get('titulo','')}\nSolución: Validación y corrección manual por parte del equipo técnico.\n\nSistema Skandia",
        }
    ]
    st.session_state.notificaciones_enviadas = correos_ok

    st.success("✅ Caso resuelto exitosamente. Notificaciones enviadas al cliente y FP.")
    with st.expander("📧 Ver correos enviados"):
        for c in correos_ok:
            st.markdown(f"**Para:** {c['destinatario']}")
            st.markdown(f"**Asunto:** {c['asunto']}")
            st.text_area("", c["cuerpo"], height=150, disabled=True, key=f"correo_{c['destinatario']}")
    st.rerun()


def _escalar_caso(cliente, error, datos, fp, agente):
    """Escala el caso a la mesa de ayuda."""
    ticket = generar_ticket_escalamiento(st.session_state, st.session_state.get("tecnico_acciones", []))
    st.session_state.ticket_actual = ticket
    st.session_state.caso_escalado = True
    st.session_state.tecnico_conectado = False
    log_accion(f"Caso escalado a mesa de ayuda — Ticket: {ticket['numero']}")

    correos = simular_correos(ticket, fp, agente)
    st.session_state.notificaciones_enviadas = correos

    st.markdown(f"""
    <div class="sk-card-alert">
      <div class="blink" style="font-size:18px;font-weight:700;color:{RED_ALERT};">
        🚨 CASO ESCALADO A MESA DE AYUDA
      </div>
      <br/>
      <b>Ticket:</b> {ticket['numero']}<br/>
      <b>SLA:</b> {ticket['sla']}<br/>
      <b>Estado:</b> {ticket['estado']}
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📋 Ver informe completo del ticket"):
        st.text_area("Informe técnico", ticket["informe_completo"], height=300, disabled=True)

    with st.expander("📧 Ver correos enviados"):
        for c in correos:
            st.markdown(f"**Para:** `{c['destinatario']}`")
            st.markdown(f"**Asunto:** {c['asunto']}")
            st.text_area("", c["cuerpo"], height=120, disabled=True, key=f"esc_{c['destinatario']}")
    st.rerun()
