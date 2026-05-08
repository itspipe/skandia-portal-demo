"""
Encuesta NPS — se muestra automáticamente al cerrar sesión
y también accesible desde el menú. Notifica al FP si es detractor.
"""
import streamlit as st
from config.brand import GREEN, RED_ALERT, GRAY_DARK, sk_header
from modules.nlp_categorizer import clasificar_transaccion, detectar_error_probable, analizar_sentimiento_tono
from modules.session_manager import log_accion, activar_error
from data.base_conocimiento import AGENTES_DEMO


def render_nps(desde_logout: bool = False):
    cliente = st.session_state.get("cliente_activo",{})
    nombre  = cliente.get("nombre","")
    primer_n = nombre.split()[0] if nombre else "Cliente"
    st.markdown(sk_header("Encuesta NPS", nombre), unsafe_allow_html=True)

    # Banner si viene del logout
    if desde_logout or st.session_state.get("nps_desde_logout"):
        st.markdown(f"""
        <div class="sk-card-blue slide-up" style="text-align:center;padding:22px 24px;">
          <div style="font-size:36px;margin-bottom:8px;">👋</div>
          <div style="font-size:18px;font-weight:700;color:#1565C0;">
            ¡Hasta pronto, {primer_n}!
          </div>
          <p style="color:#555;margin:6px 0 0 0;font-size:14px;">
            Antes de salir, cuéntanos cómo fue tu experiencia hoy.
            Tu opinión nos ayuda a mejorar el servicio.
          </p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns([3,1])

    with col1:
        primer_n_display = primer_n if primer_n else "Cliente"
        st.markdown(f"""
        <div style="padding:8px 0 16px 0;">
          <h2 style="color:{GRAY_DARK};">¿Cómo estuvo tu experiencia, {primer_n_display}?</h2>
          <p style="color:#888;">Tu opinión es completamente voluntaria y nos ayuda a mejorar.</p>
        </div>
        """, unsafe_allow_html=True)

        score = st.slider(
            "¿Qué tan probable es que recomiendes Skandia a un familiar o amigo?",
            min_value=0, max_value=10,
            value=st.session_state.get("nps_score",8)
        )
        st.session_state.nps_score = score

        # Etiquetas visuales
        cl, cm, cr = st.columns(3)
        with cl: st.caption("😞 0 — Nada probable")
        with cm: st.caption("😐 5 — Neutral")
        with cr: st.caption("😊 10 — Muy probable")

        # Segmento en tiempo real
        if score <= 6:
            seg, clr, ico = "Detractor",  RED_ALERT, "😞"
        elif score <= 8:
            seg, clr, ico = "Pasivo",    "#F57C00", "😐"
        else:
            seg, clr, ico = "Promotor",  "#2E7D32", "😊"

        st.markdown(f"""
        <div style="background:{clr}18;border-left:4px solid {clr};border-radius:10px;
             padding:12px 18px;margin:12px 0;display:flex;align-items:center;
             justify-content:space-between;">
          <div>{ico} <b style="color:{clr};">Segmento: {seg}</b></div>
          <div style="font-size:32px;font-weight:700;color:{clr};">{score}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**¿Qué transacción realizaste durante tu visita?**")
        comentario = st.text_area(
            "",
            value=st.session_state.get("nps_comentario",""),
            height=110,
            placeholder="Ej: Intenté hacer un retiro pero encontré un error al inscribir mi cuenta bancaria...",
            label_visibility="collapsed"
        )
        st.session_state.nps_comentario = comentario

        col_btn1, col_btn2 = st.columns([3,1])
        with col_btn1:
            if st.button("📤 Enviar evaluación", use_container_width=True, key="nps_enviar"):
                if not comentario.strip():
                    st.error("Por favor escribe un comentario.")
                else:
                    _procesar_nps(score, seg, comentario, cliente)
        with col_btn2:
            if st.button("Saltar →", use_container_width=True, key="nps_skip"):
                _finalizar_sesion()

    with col2:
        if comentario:
            _panel_analisis(comentario, score, seg)


def _procesar_nps(score, segmento, comentario, cliente):
    log_accion(f"NPS enviado: {score} — {segmento}")
    categoria  = clasificar_transaccion(comentario)
    error_det  = detectar_error_probable(comentario, categoria)
    tono       = analizar_sentimiento_tono(comentario)
    fp         = AGENTES_DEMO.get(cliente.get("fp_id","FP001"),{})
    primer_n   = cliente.get("nombre","Cliente").split()[0]

    if segmento == "Detractor":
        _flujo_detractor(score, categoria, error_det, tono, cliente, fp, primer_n)
    else:
        st.markdown(f"""
        <div class="sk-card-success slide-up">
          <div style="font-size:32px;margin-bottom:6px;">🙏</div>
          <b style="font-size:16px;">¡Gracias, {primer_n}!</b><br/>
          <p style="color:#555;margin:6px 0 0 0;">
            Tu evaluación fue registrada exitosamente.<br/>
            📌 Transacción: <b>{categoria}</b> | 🎯 Segmento: <b style="color:#2E7D32;">{segmento}</b>
          </p>
        </div>
        """, unsafe_allow_html=True)

        # Notificar al FP si es promotor
        if segmento == "Promotor":
            _simular_correo_fp(fp, cliente, score, comentario, "Promotor")
            with st.expander("📧 Notificación enviada a tu Financial Planner"):
                st.success(f"✅ {fp.get('nombre','FP')} fue notificado de tu excelente experiencia.")

        if st.button("✅ Finalizar sesión", use_container_width=True, key="nps_fin_ok"):
            _finalizar_sesion()


def _flujo_detractor(score, categoria, error_det, tono, cliente, fp, primer_n):
    st.markdown(f"""
    <div class="sk-card-alert blink">
      <div style="font-size:16px;font-weight:700;color:{RED_ALERT};margin-bottom:8px;">
        🚨 Lamentamos mucho tu experiencia, {primer_n}
      </div>
      <div style="font-size:13px;">
        📌 <b>Transacción:</b> {categoria}<br/>
        🎭 <b>Tono detectado:</b> {tono['tono']}<br/>
        {'🔴 <b>Problema probable:</b> ' + error_det['datos'].get('titulo','') if error_det.get('error_id') else ''}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Notificar automáticamente al FP
    _simular_correo_fp(fp, cliente, score, "", "Detractor")

    st.markdown(f"""
    <div class="sk-card-warn">
      <b>Tu Financial Planner fue notificado automáticamente</b><br/>
      <span style="font-size:13px;color:#666;">
        {fp.get('nombre','')} ({fp.get('email','')}) recibirá tu caso para hacer seguimiento.
      </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**¿Cómo te podemos ayudar ahora mismo?**")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("💬 Chat en línea", key="nps_chat", use_container_width=True):
            log_accion("Detractor: eligió chat en línea")
            if error_det.get("error_id"):
                activar_error(error_det["error_id"],"Portal NPS")
            st.success(f"✅ Chat iniciado, {primer_n}. Un agente tiene todo el contexto de tu caso.")
    with c2:
        if st.button("📞 Recibir llamada", key="nps_llamada", use_container_width=True):
            log_accion("Detractor: eligió llamada")
            st.success(f"✅ Te llamamos en 10 minutos al {cliente.get('telefono','tu celular')}.")
    with c3:
        if st.button("✕ Salir ahora", key="nps_salir_d", use_container_width=True):
            _finalizar_sesion()

    # Informe técnico
    with st.expander("📋 Informe generado para el agente"):
        from modules.report_generator import generar_informe_tecnico
        st.text_area("",generar_informe_tecnico(st.session_state),height=180,disabled=True)


def _panel_analisis(comentario, score, segmento):
    categoria  = clasificar_transaccion(comentario)
    error_det  = detectar_error_probable(comentario, categoria)
    tono       = analizar_sentimiento_tono(comentario)

    st.markdown(f"""
    <div class="sk-card">
      <div style="font-size:13px;font-weight:700;margin-bottom:10px;">🤖 Análisis IA en tiempo real</div>
      <div style="font-size:13px;margin-bottom:8px;">
        <span style="color:#888;">Categoría:</span><br/>
        <b style="color:#00D261;">{categoria}</b>
      </div>
      <div style="font-size:13px;margin-bottom:8px;">
        <span style="color:#888;">Tono:</span><br/>
        <b>{tono['tono']}</b>
      </div>
    """, unsafe_allow_html=True)
    if error_det.get("error_id"):
        st.markdown(f"""
      <div style="font-size:13px;">
        <span style="color:#888;">Problema probable:</span><br/>
        <b style="color:{RED_ALERT};">{error_det['datos'].get('titulo','')}</b><br/>
        <span style="color:#aaa;font-size:11px;">Confianza: {int(error_det['confianza']*100)}%</span>
      </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if score <= 6 and error_det.get("error_id"):
        if st.button("🔍 Activar soporte IA", key="nps_ia", use_container_width=True):
            activar_error(error_det["error_id"],"Portal NPS")
            st.rerun()


def _simular_correo_fp(fp, cliente, score, comentario, segmento):
    log_accion(f"Notificación NPS enviada a FP: {fp.get('nombre','')}")


def _finalizar_sesion():
    """Cierra sesión completamente después del NPS."""
    from modules.session_manager import reset_demo
    reset_demo()
    st.session_state.logged_in        = False
    st.session_state.pagina_activa    = "login"
    st.session_state.nps_desde_logout = False
    st.success("✅ Sesión cerrada. ¡Hasta pronto!")
    st.rerun()
