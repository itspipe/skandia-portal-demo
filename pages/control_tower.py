"""Control Tower CX — panel de servicio al cliente en tiempo real."""

import streamlit as st
import datetime
from config.brand import GREEN, GRAY_DARK, RED_ALERT, sk_header
from data.base_conocimiento import CLIENTES_DEMO, AGENTES_DEMO
from modules.session_manager import log_accion, activar_error
from modules.report_generator import generar_informe_tecnico


def render_control_tower():
    st.markdown(sk_header("Control Tower CX"), unsafe_allow_html=True)

    st.markdown(f"""
    <div style="padding:16px 0 8px 0;">
      <h2>🎯 Centro de Control — Experiencia de Cliente</h2>
      <p style="color:#666;">Monitoreo en tiempo real de detractores y gestión de casos activos.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Métricas en tiempo real ───────────────────────────────────────────
    casos_abiertos = 3
    casos_proceso = 1
    casos_resueltos = 7
    tiempo_respuesta = "8 min"

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="sk-card-alert" style="text-align:center;padding:16px;">
          <div style="font-size:32px;font-weight:700;color:{RED_ALERT};">{casos_abiertos}</div>
          <div style="font-size:13px;">Casos abiertos</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="sk-card-warn" style="text-align:center;padding:16px;">
          <div style="font-size:32px;font-weight:700;color:#E65100;">{casos_proceso}</div>
          <div style="font-size:13px;">En proceso</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="sk-card-success" style="text-align:center;padding:16px;">
          <div style="font-size:32px;font-weight:700;color:#1B5E20;">{casos_resueltos}</div>
          <div style="font-size:13px;">Resueltos hoy</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="sk-card" style="text-align:center;padding:16px;">
          <div style="font-size:32px;font-weight:700;color:#2D2926;">{tiempo_respuesta}</div>
          <div style="font-size:13px;">Tiempo prom. respuesta</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div class="blink" style="background:{RED_BG};border-left:4px solid {RED_ALERT};
                border-radius:8px;padding:12px 16px;margin-bottom:16px;">
      🔴 <b>ALERTA:</b> {casos_abiertos} detractores activos sin gestionar en tiempo real.
    </div>
    """, unsafe_allow_html=True)

    # ── Lista de detractores simulados ────────────────────────────────────
    st.markdown("### 👥 Detractores Activos")

    casos_demo = [
        {
            "cliente": CLIENTES_DEMO[0],
            "score": 3,
            "comentario": "No pude inscribir mi cuenta bancaria, llevo 2 días intentando",
            "categoria": "Registros de cuentas bancarias",
            "error_id": "ERR001",
            "hora": "14:32",
            "estado": "Sin gestionar"
        },
        {
            "cliente": CLIENTES_DEMO[1],
            "score": 2,
            "comentario": "El retiro me fue rechazado sin explicación y perdí tiempo",
            "categoria": "Solicité un retiro",
            "error_id": "ERR009",
            "hora": "14:45",
            "estado": "Sin gestionar"
        },
        {
            "cliente": CLIENTES_DEMO[2],
            "score": 5,
            "comentario": "No puedo actualizar mi perfil de inversión, la firma no funciona",
            "categoria": "Gestioné mi portafolio",
            "error_id": "ERR011",
            "hora": "15:01",
            "estado": "Sin gestionar"
        },
    ]

    for idx, caso in enumerate(casos_demo):
        c = caso["cliente"]
        fp = AGENTES_DEMO.get(c.get("fp_id", "FP001"), {})

        col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
        with col1:
            st.markdown(f"""
            <div class="sk-card-alert" style="padding:12px 16px;margin-bottom:0;">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                <span class="badge-err">NPS: {caso['score']}</span>
                <b>{c['nombre']}</b>
                <span style="color:#666;font-size:12px;">· {caso['hora']} · {caso['estado']}</span>
              </div>
              <div style="font-size:13px;color:#555;">
                📌 {caso['categoria']}<br/>
                💬 "{caso['comentario']}"
              </div>
              <div style="font-size:12px;color:#888;margin-top:4px;">
                FP: {fp.get('nombre','')} ({fp.get('email','')})
              </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("💬 Chat", key=f"ct_chat_{idx}", use_container_width=True):
                _iniciar_gestion(caso, "chat")
        with col3:
            if st.button("📞 Llamada", key=f"ct_call_{idx}", use_container_width=True):
                _iniciar_gestion(caso, "llamada")
        with col4:
            if st.button("👤 Ver caso", key=f"ct_ver_{idx}", use_container_width=True):
                st.session_state.cliente_activo = c
                activar_error(caso["error_id"], caso["categoria"])
                st.session_state.pagina_activa = "tecnico_directo"
                st.rerun()

        st.markdown("<br/>", unsafe_allow_html=True)

    # ── Sugerencia de respuesta proactiva ──────────────────────────────────
    st.markdown("---")
    st.markdown("### 🤖 Respuesta Proactiva Sugerida por IA")

    cliente_sel = st.selectbox(
        "Generar respuesta para:",
        [c["cliente"]["nombre"] for c in casos_demo],
        key="ct_sel_cliente"
    )
    caso_sel = next(c for c in casos_demo if c["cliente"]["nombre"] == cliente_sel)

    respuesta = _generar_respuesta_proactiva(caso_sel)
    st.text_area("Respuesta sugerida (personalizada por IA):", respuesta, height=180)
    if st.button("📤 Enviar esta respuesta al cliente", key="ct_enviar_resp", use_container_width=True):
        st.success(f"✅ Respuesta enviada a {caso_sel['cliente']['email']}.")
        log_accion(f"Respuesta proactiva enviada a {caso_sel['cliente']['nombre']}")


def _iniciar_gestion(caso, tipo):
    """Registra el inicio de gestión de un caso."""
    cliente = caso["cliente"]
    log_accion(f"Agente inició {tipo} con {cliente['nombre']}")

    st.success(f"✅ {'Chat iniciado' if tipo=='chat' else 'Llamada programada'} con {cliente['nombre']}.")
    with st.expander("📋 Informe automático enviado al agente", expanded=False):
        st.session_state.cliente_activo = cliente
        activar_error(caso["error_id"], caso["categoria"])
        from modules.report_generator import generar_informe_tecnico
        informe = generar_informe_tecnico(st.session_state)
        st.text_area("", informe, height=250, disabled=True, key=f"inf_{cliente['id']}_{tipo}")


def _generar_respuesta_proactiva(caso) -> str:
    from data.base_conocimiento import KNOWLEDGE_BASE
    cliente = caso["cliente"]
    err = KNOWLEDGE_BASE.get(caso["error_id"], {})
    nombre = cliente["nombre"].split()[0]
    return f"""Estimado/a {nombre},

Hemos notado que tuviste una experiencia difícil durante tu visita al portal hoy, específicamente al intentar "{caso['categoria'].lower()}".

Queremos que sepas que tu inconveniente relacionado con "{err.get('titulo', 'el proceso solicitado')}" es nuestra prioridad.

Ya hemos identificado la causa y nuestro equipo está listo para ayudarte a resolverlo en los próximos minutos.

¿Tienes disponibilidad para conectarte ahora mismo por chat o prefieres que te llamemos?

Con gusto, 
{caso['cliente'].get('fp_id','FP001')} — Equipo Skandia"""
