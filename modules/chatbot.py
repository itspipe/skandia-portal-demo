import streamlit as st

def render_chatbot_flotante():
    if not st.session_state.get("error_activo"):
        return

    error = st.session_state.error_activo
    
    with st.expander("🤖 Asistente Virtual Skandia", expanded=True):
        st.markdown(f"**Hola Andrés,** detecté un inconveniente al intentar **{error['modulo_origen']}**.")
        
        # Lógica de pasos dinámicos
        pasos = ["Validar fondos", "Verificar token", "Confirmar cuenta destino"]
        completados = st.session_state.get("pasos_ia_completados", 0)
        
        progreso = completados / len(pasos)
        st.progress(progreso)
        st.caption(f"Progreso de solución IA: {int(progreso*100)}%")

        if completados < len(pasos):
            if st.button(f"Siguiente paso: {pasos[completados]}"):
                st.session_state.pasos_ia_completados += 1
                st.rerun()
        else:
            st.success("IA: No logré solucionar el error con los protocolos base.")
            if st.button("📞 Hablar con un Técnico en línea"):
                st.session_state.chat_tecnico_activo = True
                st.rerun()