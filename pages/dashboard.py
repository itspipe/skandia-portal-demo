"""Dashboard analítico — métricas modernas e interactivas."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config.brand import GREEN, RED_ALERT, GRAY_DARK, sk_header
from data.base_conocimiento import generar_nps_sintetico
from modules.session_manager import activar_error, log_accion


def render_dashboard():
    cliente = st.session_state.get("cliente_activo",{})
    st.markdown(sk_header("Dashboard Analítico", cliente.get("nombre","")), unsafe_allow_html=True)

    st.markdown(f"""
    <div class="welcome-banner slide-up">
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;">
        <div>
          <div style="font-size:20px;font-weight:700;">📊 Dashboard de Experiencia de Cliente</div>
          <div style="opacity:0.85;font-size:13px;margin-top:3px;">Análisis NPS en tiempo real · Skandia 2026</div>
        </div>
        <div style="font-size:28px;">📈</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    df = _cargar_datos()
    total  = len(df)
    nps_p  = df["NPS"].mean()
    det_p  = round((df["Segmento_NPS"]=="Detractor").mean()*100,1)
    pas_p  = round((df["Segmento_NPS"]=="Pasivo").mean()*100,1)
    pro_p  = round((df["Segmento_NPS"]=="Promotor").mean()*100,1)
    nps_sc = round(pro_p - det_p, 1)

    # ── Métricas ──────────────────────────────────────────────────────────
    m1,m2,m3,m4,m5 = st.columns(5)
    mets = [
        (m1,"📋","Registros",str(total),"#003087"),
        (m2,"🎯","NPS Score",f"{nps_sc:+.0f}","#00D261" if nps_sc>=0 else RED_ALERT),
        (m3,"😊","Promotores",f"{pro_p}%","#00D261"),
        (m4,"😐","Pasivos",f"{pas_p}%","#F57C00"),
        (m5,"😞","Detractores",f"{det_p}%",RED_ALERT),
    ]
    for col,(c,ico,tit,val,clr) in enumerate(mets):
        with c:
            st.markdown(f"""
            <div class="dash-metric" style="border-top:4px solid {clr};">
              <div style="font-size:28px;margin-bottom:6px;">{ico}</div>
              <div style="font-size:11px;color:#999;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;">{tit}</div>
              <div style="font-size:22px;font-weight:700;color:{clr};margin-top:4px;">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Gráficos ──────────────────────────────────────────────────────────
    g1, g2 = st.columns(2)

    with g1:
        st.markdown("**Distribución por segmento**")
        seg = df["Segmento_NPS"].value_counts().reset_index()
        seg.columns = ["Segmento","Cantidad"]
        fig = px.bar(seg,x="Segmento",y="Cantidad",
                     color="Segmento",
                     color_discrete_map={"Detractor":RED_ALERT,"Pasivo":"#F57C00","Promotor":GREEN},
                     text="Cantidad")
        fig.update_traces(textposition="outside",marker_line_width=0)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                          showlegend=False,margin=dict(t=10,b=10,l=0,r=0),
                          font=dict(family="Inter,sans-serif"),height=260)
        st.plotly_chart(fig,use_container_width=True)

    with g2:
        st.markdown("**Top quejas — detractores**")
        det = df[df["Segmento_NPS"]=="Detractor"]["Transaccion"].value_counts().head(6).reset_index()
        det.columns = ["Categoría","Qty"]
        fig2 = px.bar(det,x="Qty",y="Categoría",orientation="h",
                      color_discrete_sequence=[RED_ALERT],text="Qty")
        fig2.update_traces(textposition="outside",marker_line_width=0)
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                           showlegend=False,yaxis=dict(autorange="reversed"),
                           margin=dict(t=10,b=10,l=0,r=0),height=260,
                           font=dict(family="Inter,sans-serif"))
        st.plotly_chart(fig2,use_container_width=True)

    # Serie de tiempo
    if "Fecha" in df.columns:
        st.markdown("**Evolución del NPS promedio — 2026**")
        df["Fecha"] = pd.to_datetime(df["Fecha"])
        ts = df.groupby("Fecha")["NPS"].mean().reset_index()
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=ts["Fecha"],y=ts["NPS"],
                                   mode="lines+markers",line=dict(color=GREEN,width=2.5),
                                   fill="tozeroy",fillcolor="rgba(0,210,97,0.08)"))
        fig3.add_hline(y=7,line_dash="dash",line_color=RED_ALERT,annotation_text="Umbral promotor")
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                           margin=dict(t=10,b=10),height=200,
                           font=dict(family="Inter,sans-serif"))
        st.plotly_chart(fig3,use_container_width=True)

    # ── Tabla detractores ─────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🔴 Detractores — Gestión en tiempo real")
    filtro = st.selectbox("Filtrar por categoría:",["Todas"]+sorted(df["Transaccion"].unique().tolist()))
    det_t = df[df["Segmento_NPS"]=="Detractor"]
    if filtro!="Todas":
        det_t = det_t[det_t["Transaccion"]==filtro]

    for i, row in det_t.head(8).iterrows():
        c1,c2,c3 = st.columns([5,1,1])
        with c1:
            st.markdown(f"""
            <div class="sk-card-alert" style="padding:10px 14px;margin-bottom:4px;">
              <span class="badge-err">NPS {row['NPS']}</span>
              <b style="margin-left:8px;">Cliente #{i:04d}</b>
              <div style="font-size:12px;color:#666;margin-top:4px;">
                📌 {row['Transaccion']}<br/>
                💬 "{row['Comentario'][:72]}..."
              </div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            if st.button("💬",key=f"dc_{i}",use_container_width=True,help="Iniciar chat"):
                st.success(f"Chat iniciado con cliente #{i:04d}")
                log_accion(f"Chat iniciado dashboard cliente #{i:04d}")
        with c3:
            if st.button("📞",key=f"dl_{i}",use_container_width=True,help="Llamar"):
                st.success(f"Llamada programada para cliente #{i:04d}")


def _cargar_datos():
    import os
    path = "Portal Clientes 2026.xlsx - Sheet0.csv"
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            nc = next((c for c in df.columns if "nps" in c.lower() or "calificaci" in c.lower()),None)
            if nc:
                df["NPS"] = pd.to_numeric(df[nc],errors="coerce")
                df = df.dropna(subset=["NPS"])
                df["NPS"] = df["NPS"].astype(int).clip(0,10)
                df["Segmento_NPS"] = df["NPS"].apply(lambda x:"Detractor" if x<=6 else("Pasivo" if x<=8 else"Promotor"))
            tc = next((c for c in df.columns if "transacci" in c.lower()),None)
            df["Transaccion"] = df[tc].fillna("Otras") if tc else "Otras"
            if "NPS" in df.columns: return df
        except: pass
    return pd.DataFrame(generar_nps_sintetico(120))
