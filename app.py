
import streamlit as st
import os
import base64
import time
from supabase import create_client, Client

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="FastShopping AI", page_icon="🛒", layout="wide")

# --- 2. SISTEMA DE AUDIO (JS/HTML5) ---
def play_sfx(audio_url):
    """Inyecta JS para reproducir sonidos de interacción"""
    audio_html = f"""
        <audio autoplay>
            <source src='{audio_url}' type='audio/mpeg'>
        </audio>
    """
    st.components.v1.html(audio_html, height=0)

# --- 3. DISEÑO Y ESTILOS CSS3 ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    /* Fondo y Base */
    .stApp {
        background-color: #0F1117;
        color: #FFFFFF;
        font-family: 'Poppins', sans-serif;
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Tarjetas Personalizadas */
    .card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(123, 63, 242, 0.3);
        border-radius: 15px;
        padding: 20px;
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }
    .card:hover {
        border-color: #FF6A00;
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(255, 106, 0, 0.2);
    }

    /* Botones Estilo Cyber */
    .stButton>button {
        background: linear-gradient(90deg, #7B3FF2, #FF6A00) !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px #7B3FF2;
        transform: scale(1.02);
    }

    /* Headers y Logos */
    .logo-container {
        text-align: center;
        padding: 20px;
    }
    .gradient-text {
        background: -webkit-linear-gradient(#7B3FF2, #FF6A00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. CABECERA DINÁMICA ---
st.markdown('<div class="logo-container"><h1 class="gradient-text">FASTSHOPPING AI</h1></div>', unsafe_allow_html=True)

# --- 5. LÓGICA DE ROLES EN SIDEBAR ---
with st.sidebar:
    st.markdown("### 👤 Perfil de Acceso")
    rol = st.radio("Selecciona tu modo:", ["Comprador 🛒", "Repartidor 🛵"])
    st.divider()
    st.info(f"Modo activo: {rol}")

# --- 6. FLUJO DE TRABAJO (COMPRADOR) ---
if "Comprador" in rol:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card"><h3>🍎 Alimentos</h3><p>Busca productos frescos con IA.</p></div>', unsafe_allow_html=True)
        if st.button("Explorar Comida"):
            play_sfx("https://www.soundjay.com/buttons/sounds/button-3.mp3")

    with col2:
        st.markdown('<div class="card"><h3>💊 Farmacia</h3><p>Medicamentos de entrega rápida.</p></div>', unsafe_allow_html=True)
        if st.button("Ver Medicinas"):
            play_sfx("https://www.soundjay.com/buttons/sounds/button-3.mp3")

    with col3:
        st.markdown('<div class="card"><h3>📦 Otros</h3><p>Cualquier cosa que necesites.</p></div>', unsafe_allow_html=True)
        if st.button("Otros Pedidos"):
            play_sfx("https://www.soundjay.com/buttons/sounds/button-3.mp3")

# --- 7. FLUJO DE TRABAJO (REPARTIDOR) ---
else:
    st.markdown("## 🛵 Panel de Logística")
    st.markdown('<div class="card"><h3>📍 Pedidos Disponibles</h3><p>No hay entregas pendientes en tu zona.</p></div>', unsafe_allow_html=True)
    if st.button("Refrescar Mapa"):
        play_sfx("https://www.soundjay.com/buttons/sounds/button-10.mp3")
        with st.spinner("Localizando pedidos..."):
            time.sleep(1)
        st.toast("Mapa actualizado")

# Pie de página modular
st.markdown("--- ")
st.caption("© 2024 FastShopping AI - Powered by Super Intelligence")
