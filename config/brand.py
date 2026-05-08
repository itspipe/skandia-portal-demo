import streamlit as st

# Colores Oficiales Skandia
GREEN = "#00D261"
GRAY_DARK = "#2D2926"
CLOUD_DANCER = "#F0EEE9"
RED_ALERT = "#FFEBEE"
RED_BORDER = "#D32F2F"
YELLOW_WARN = "#FFF8E1" # Fix para tecnico.py
YELLOW_BORDER = "#F9A825"

# Logo SVG para consistencia
LOGO_SVG = """
<svg width="150" height="40" viewBox="0 0 150 40" xmlns="http://www.w3.org/2000/svg">
    <path d="M15 10 L25 20 L15 30 L5 20 Z" fill="#00D261"/>
    <text x="35" y="25" font-family="Arial" font-weight="bold" font-size="20" fill="#2D2926">skandia</text>
</svg>
"""

CSS = f"""
<style>
    /* Fondo Global y Animación */
    .stApp {{
        background-color: {CLOUD_DANCER};
        animation: fadeIn 0.6s ease-in;
    }}
    @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}

    /* Tarjetas de Alerta Dinámicas */
    .sk-alert-card {{
        background-color: {RED_ALERT};
        border-left: 6px solid {RED_BORDER};
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}

    /* Botones Skandia Style */
    .stButton>button {{
        border-radius: 25px !important;
        background-color: {GREEN} !important;
        color: white !important;
        border: none !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        padding: 0.5rem 2rem !important;
    }}
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,210,97,0.3) !important;
    }}

    /* Estilo para los inputs */
    .stTextInput>div>div>input {{
        border-radius: 10px !important;
    }}
</style>
"""