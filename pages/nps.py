"""Página de Encuesta NPS — post-experiencia con clasificación IA."""

import streamlit as st
from config.brand import GREEN, RED_ALERT, RED_BG, header_html
from modules.nlp_categorizer import clasificar_transaccion, detectar_error_probable, analizar_sentimiento_tono
from modules.session_manager import log_accion, activar_error


def render_nps():
    st.markdown(header_html("Portal Clientes"), unsafe_allow_html=True)

    st.markdown(f"""
    <div style="padding:16px 0 8px 0;">
      <h2>📝 Cuéntanos sobre tu experiencia</h2>
      <p style="color:#666;">Tu opinión nos ayuda a mejorar el servicio. Esta encuesta es completamente voluntaria.</p>
    </div>
    """, unsafe_allow_html=True)

    cliente = st.session_state.get("cliente_activo", {})

    col1, col2 = st.columns([2, 1])

    with col1:
        score = st.slider(
            "¿Qué tan probable es que recomiendes Skandia a un familiar o amigo?",
            min_value=0, max_value=10,
            value=st.session_state.get("nps_score", 8),
            help="0 = Nada probable · 10 = Extremadamente probable"
        )
        st.session_state.nps_score = score

        col_labels = st.columns(3)
        with col_labels[0]:
            st.caption("0 — Nada probable")
        with col_labels[1]:
            st.caption("5 — Neutral")
        with col_labels[2]:
            st.caption("10 — Muy probable")

        if score <= 6:
            segmento = "Detractor"
            color = RED_ALERT
            emoji = "😞"
        elif score <= 8:
            segmento = "Pasivo"
            color = "#F57C00"
            emoji = "😐"
        else:
            segmento = "Promotor"
            color = "#2E7D32"
            emoji = "😊"

        st.markdown(f"""
        <div style="background:{color}22;border-left:4px solid {color};border-radius:8px;
                    padding:12px 16px;margin:12px 0;">
          {emoji} <b style="color:{color};">Segmento: {segmento}</b>
          <span style="float:right;font-size:28px;font-weight:700;color:{color};">{score}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**¿Qué transacción realizaste durante tu visita al portal?**")
        comentario = st.text_area(
            "Cuéntanos qué hiciste y cómo fue tu experiencia:",
            value=st.session_state.get("nps_comentario", ""),
            height=120,
            placeholder="Ej: Intenté hacer un retiro pero no pude inscribir mi cuenta bancaria..."
        )
        st.session_state.nps_comentario = comentario

        if st.button("📤 Enviar evaluación", use_container_width=True):
            _procesar_nps(score, segmento, comentario, cliente)

    with col2:
        if comentario:
            _panel_analisis_ia(comentario, score, segmento)


def _procesar_nps(score, segmento, comentario, cliente):
    if not comentario.strip():
        st.error("Por favor escribe un comentario antes de enviar.")
        return

    log_accion(f"NPS enviado: {score} — {segmento}")
    categoria = clasificar_transaccion(comentario)
    error_det = detectar_error_probable(comentario, categoria)
    tono = analizar_sentimiento_tono(comentario)

    st.success("✅ ¡Gracias por tu evaluación! Tu opinión es muy importante para nosotros.")

    if segmento == "Detractor":
        _alerta_detractor(score, categoria, error_det, tono, cliente)
    else:
        st.markdown(f"""
        <div class="sk-card-success">
          <b>Clasificación automática:</b><br/>
          📌 Transacción: <b>{categoria}</b><br/>
          🎯 Segmento: <b style="color:#2E7D32;">{segmento}</b>
        </div>
        """, unsafe_allow_html=True)


def _alerta_detractor(score, categoria, error_det, tono, cliente):
    st.markdown(f"""
    <div class="sk-card-alert blink">
      <div style="font-size:16px;font-weight:700;color:{RED_ALERT};">
        🚨 CLIENTE DETRACTOR DETECTADO — Puntuación: {score}/10
      </div>
      <br/>
      <b>Transacción identificada:</b> {categoria}<br/>
      <b>Tono detectado:</b> {tono['tono']}<br/>
      {'<b>Error probable:</b> ' + error_det['datos'].get('titulo','') if error_det['error_id'] else ''}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**¿Cómo podemos ayudarte ahora mismo?**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💬 CHAT EN LÍNEA", key="nps_chat", use_container_width=True):
            log_accion("Detractor eligió: Chat en línea")
            if error_det["error_id"]:
                activar_error(error_det["error_id"], "Portal (vía NPS)")
            st.success("✅ Chat iniciado. Un agente está revisando tu caso ahora mismo.")
            st.info("📋 El historial completo de tu experiencia fue compartido con el agente.")
    with col2:
        if st.button("📞 RECIBIR LLAMADA", key="nps_llamada", use_container_width=True):
            log_accion("Detractor eligió: Recibir llamada")
            st.success(f"✅ Te llamaremos en los próximos 10 minutos al {cliente.get('telefono','tu celular registrado')}.")
            st.info("📋 Tu asesor ya tiene el detalle completo de tu inconveniente.")
    with col3:
        if st.button("✕ Salir", key="nps_salir", use_container_width=True):
            log_accion("Detractor eligió: Salir sin contacto")
            st.session_state.pagina_activa = "inicio"
            st.rerun()

    # Informe automático para el agente
    if st.session_state.get("chatbot_activo") or st.session_state.get("error_activo"):
        with st.expander("📋 Informe técnico generado para el agente"):
            from modules.report_generator import generar_informe_tecnico
            informe = generar_informe_tecnico(st.session_state)
            st.text_area("", informe, height=200, disabled=True)


def _panel_analisis_ia(comentario, score, segmento):
    categoria = clasificar_transaccion(comentario)
    error_det = detectar_error_probable(comentario, categoria)
    tono = analizar_sentimiento_tono(comentario)

    st.markdown(f"""
    <div class="sk-card">
      <b style="font-size:13px;">🤖 Análisis IA en tiempo real</b>
      <hr style="margin:8px 0;border:none;border-top:1px solid #eee;"/>
      <div style="font-size:13px;">
        <b>Categoría detectada:</b><br/>
        <span style="color:{GREEN};">{categoria}</span>
      </div>
      <div style="font-size:13px;margin-top:8px;">
        <b>Tono / Sentimiento:</b><br/>
        {tono['tono']}
      </div>
    """, unsafe_allow_html=True)

    if error_det["error_id"]:
        st.markdown(f"""
      <div style="font-size:13px;margin-top:8px;">
        <b>Posible problema:</b><br/>
        <span style="color:{RED_ALERT};">{error_det['datos'].get('titulo','')}</span><br/>
        <span style="color:#666;">Confianza: {int(error_det['confianza']*100)}%</span>
      </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if score <= 6 and error_det["error_id"]:
        if st.button("🔍 Activar soporte IA", key="nps_activar_ia", use_container_width=True):
            activar_error(error_det["error_id"], "Portal (vía NPS)")
            st.rerun()
