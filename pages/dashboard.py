"""Dashboard de Big Data — análisis masivo de NPS y quejas."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config.brand import GREEN, RED_ALERT, GRAY_DARK, header_html
from data.base_conocimiento import generar_nps_sintetico
from modules.session_manager import activar_error, log_accion


def render_dashboard():
    st.markdown(header_html("Analítica CX"), unsafe_allow_html=True)

    st.markdown(f"""
    <div style="padding:16px 0 8px 0;">
      <h2 style="color:{GRAY_DARK};">📈 Dashboard de Experiencia de Cliente</h2>
      <p style="color:#666;">Análisis masivo de NPS, quejas y comportamiento de clientes.</p>
    </div>
    """, unsafe_allow_html=True)

    # Cargar datos
    df = _cargar_datos()

    # ── KPIs ──────────────────────────────────────────────────────────────
    total = len(df)
    nps_prom = df["NPS"].mean()
    det_pct = round((df["Segmento_NPS"] == "Detractor").mean() * 100, 1)
    prom_pct = round((df["Segmento_NPS"] == "Promotor").mean() * 100, 1)
    nps_score = round(prom_pct - det_pct, 1)

    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("Total registros", total)
    with m2:
        st.metric("NPS Score", f"{nps_score}")
    with m3:
        st.metric("Promotores", f"{prom_pct}%", delta="+2.1%")
    with m4:
        st.metric("Detractores", f"{det_pct}%", delta=f"-{det_pct}%", delta_color="inverse")
    with m5:
        st.metric("Promedio NPS", f"{nps_prom:.1f}/10")

    st.markdown("---")

    # ── Gráficos ──────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Distribución NPS por segmento**")
        seg_count = df["Segmento_NPS"].value_counts().reset_index()
        seg_count.columns = ["Segmento", "Cantidad"]
        color_map = {"Detractor": RED_ALERT, "Pasivo": "#F57C00", "Promotor": GREEN}
        fig1 = px.bar(
            seg_count, x="Segmento", y="Cantidad",
            color="Segmento", color_discrete_map=color_map,
            text="Cantidad"
        )
        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False, margin=dict(t=10, b=10),
            font=dict(family="Inter, sans-serif")
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("**Top quejas por categoría de transacción**")
        det_df = df[df["Segmento_NPS"] == "Detractor"]
        cat_count = det_df["Transaccion"].value_counts().head(8).reset_index()
        cat_count.columns = ["Categoría", "Detractores"]
        fig2 = px.bar(
            cat_count, x="Detractores", y="Categoría",
            orientation="h", color_discrete_sequence=[RED_ALERT],
            text="Detractores"
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10, b=10), yaxis=dict(autorange="reversed"),
            font=dict(family="Inter, sans-serif")
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Serie de tiempo ───────────────────────────────────────────────────
    st.markdown("**Evolución del NPS Promedio (2026)**")
    if "Fecha" in df.columns:
        df["Fecha"] = pd.to_datetime(df["Fecha"])
        ts = df.groupby("Fecha")["NPS"].mean().reset_index()
        fig3 = px.line(ts, x="Fecha", y="NPS", color_discrete_sequence=[GREEN])
        fig3.add_hline(y=7, line_dash="dash", line_color=RED_ALERT, annotation_text="Mínimo promotor")
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10, b=10),
            font=dict(family="Inter, sans-serif")
        )
        st.plotly_chart(fig3, use_container_width=True)

    # ── Tabla de detractores activos ──────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🔴 Detractores Activos — Gestión en Tiempo Real")

    filtro_cat = st.selectbox(
        "Filtrar por categoría:",
        ["Todas"] + list(df["Transaccion"].unique()),
        key="filtro_dash"
    )

    det_tabla = df[df["Segmento_NPS"] == "Detractor"].copy()
    if filtro_cat != "Todas":
        det_tabla = det_tabla[det_tabla["Transaccion"] == filtro_cat]

    for i, row in det_tabla.head(10).iterrows():
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            st.markdown(f"""
            <div class="sk-card-alert" style="padding:10px 14px;">
              <span class="badge-err">NPS: {row['NPS']}</span>
              <b style="margin-left:8px;">Contrato anónimo #{i:04d}</b><br/>
              <span style="font-size:12px;color:#555;">{row['Transaccion']}</span><br/>
              <span style="font-size:12px;color:#777;">"{row['Comentario'][:80]}..."</span>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("💬 Chat", key=f"dash_chat_{i}", use_container_width=True):
                log_accion(f"Agente inició chat con detractor #{i:04d}")
                st.success("Chat iniciado. El cliente fue notificado.")
        with col3:
            if st.button("📞 Llamada", key=f"dash_call_{i}", use_container_width=True):
                log_accion(f"Llamada programada para detractor #{i:04d}")
                st.success("Llamada programada para los próximos 10 minutos.")


def _cargar_datos() -> pd.DataFrame:
    """Carga datos desde CSV o genera sintéticos."""
    import os
    csv_path = "Portal Clientes 2026.xlsx - Sheet0.csv"
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            # Detectar columna NPS
            nps_col = next((c for c in df.columns if "nps" in c.lower() or "calificaci" in c.lower() or "puntuaci" in c.lower()), None)
            if nps_col:
                df["NPS"] = pd.to_numeric(df[nps_col], errors="coerce")
                df = df.dropna(subset=["NPS"])
                df["NPS"] = df["NPS"].astype(int).clip(0, 10)
                df["Segmento_NPS"] = df["NPS"].apply(lambda x: "Detractor" if x <= 6 else ("Pasivo" if x <= 8 else "Promotor"))
            # Detectar columna transacción
            tx_col = next((c for c in df.columns if "transacci" in c.lower()), None)
            if tx_col:
                df["Transaccion"] = df[tx_col].fillna("Otras")
            else:
                df["Transaccion"] = "Otras"
            if "NPS" in df.columns and "Transaccion" in df.columns:
                return df
        except Exception:
            pass

    # Datos sintéticos
    registros = generar_nps_sintetico(120)
    return pd.DataFrame(registros)
