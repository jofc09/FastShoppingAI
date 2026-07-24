
import streamlit as st
import os
import base64
import time
from supabase import create_client, Client

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="FastShopping AI", page_icon="🛒", layout="wide")


# --- INTEGRACIÓN EXTRA ---
# ==========================================
# PARTE 2: LÓGICA DE ROLES, AUDIO Y BÚSQUEDA
# ==========================================

# 1. MOTOR DE SONIDO DE VANGUARDIA (100% Gratis - Sintetizado en navegador por Web Audio API)
def reproducir_sonido_ui():
    """Genera un efecto de sonido futurista 'pop/clic' sin usar archivos externos."""
    js_sonido = """
    <script>
    try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        const ganancia = ctx.createGain();
        osc.connect(ganancia);
        ganancia.connect(ctx.destination);
        
        osc.type = "sine";
        osc.frequency.setValueAtTime(587.33, ctx.currentTime); // Nota D5
        osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.08); // Sube a A5 (efecto IA)
        ganancia.gain.setValueAtTime(0.08, ctx.currentTime);
        ganancia.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.08);
        
        osc.start();
        osc.stop(ctx.currentTime + 0.08);
    } catch(e) {}
    </script>
    """
    st.components.v1.html(js_sonido, height=0, width=0)

# 2. CONTROL DE ESTADO (Evita pérdida de datos al recargar la página)
if 'rol_actual' not in st.session_state:
    st.session_state.rol_actual = "Comprador 🛒"
if 'busqueda_ia' not in st.session_state:
    st.session_state.busqueda_ia = ""

# 3. MÓDULO DE ENCABEZADO Y SELECTOR DE ROL DINÁMICO
def renderizar_encabezado_y_rol():
    # Contenedor centralizado para el selector de rol
    col_vacia1, col_selector, col_vacia2 = st.columns([1, 2, 1])
    with col_selector:
        nuevo_rol = st.radio(
            "Selecciona tu perfil:",
            ["Comprador 🛒", "Repartidor 🛵"],
            index=0 if st.session_state.rol_actual == "Comprador 🛒" else 1,
            horizontal=True,
            label_visibility="collapsed"
        )
        # Si el usuario cambia de rol, actualizamos memoria y emitimos sonido
        if nuevo_rol != st.session_state.rol_actual:
            st.session_state.rol_actual = nuevo_rol
            reproducir_sonido_ui()
            st.rerun()

    # Configuración visual dinámica según el rol
    if st.session_state.rol_actual == "Comprador 🛒":
        subtitulo = "Compra inteligente, rápido y fácil con Inteligencia Artificial."
        color_acento = "#FF6A00" # Naranja FastShopping
    else:
        subtitulo = "⚡ Portal de Reparto y Gestión de Pedidos en Tiempo Real."
        color_acento = "#00E5FF" # Neón cian para repartidores

    # Renderizado del Logo y Banner con diseño adaptativo en HTML/CSS puro
    logo_html = f"""
    <div style="text-align: center; margin: 10px 0 25px 0;">
        <div style="display: inline-flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.03); padding: 8px 24px; border-radius: 50px; border: 1px solid rgba(255,255,255,0.08); box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
            <span style="font-size: 26px; margin-right: 10px;">⚡🛒</span>
            <span style="font-size: 24px; font-weight: 700; color: #FFFFFF; letter-spacing: -0.5px;">
                FastShopping<span style="color: {color_acento};">AI</span>
            </span>
        </div>
        <p style="color: #8A8F9E; font-size: 14px; margin-top: 8px; font-weight: 300;">{subtitulo}</p>
    </div>
    """
    st.markdown(logo_html, unsafe_allow_html=True)

# 4. MÓDULO DE BÚSQUEDA INTELIGENTE (Estilo diseño Figma)
def renderizar_barra_busqueda_ia():
    if st.session_state.rol_actual == "Comprador 🛒":
        # Estilizamos el campo de texto para que tenga bordes redondos y brillo morado al escribir
        st.markdown("""
        <style>
        div[data-testid="stTextInput"] input {
            background-color: #181B26 !important;
            border: 1px solid rgba(123, 63, 242, 0.4) !important;
            border-radius: 30px !important;
            padding: 12px 20px !important;
            color: white !important;
            font-size: 15px;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #7B3FF2 !important;
            box-shadow: 0 0 15px rgba(123, 63, 242, 0.4) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Grid para la barra de búsqueda y el botón de IA
        col_input, col_boton = st.columns([5, 1])
        with col_input:
            query = st.text_input(
                "Búsqueda",
                placeholder="¿Qué producto buscas hoy? (ej. Audífonos por menos de RD$3,000)...",
                label_visibility="collapsed",
                key="input_ia"
            )
        with col_boton:
            buscar = st.button("🔍", key="btn_buscar", help="Buscar con IA", use_container_width=True)
            if buscar and query:
                st.session_state.busqueda_ia = query
                reproducir_sonido_ui()
                st.toast(f"🤖 IA filtrando el catálogo para: '{query}'...", icon="⚡")
    else:
        # Vista rápida para el Repartidor
        st.success("📦 **Radar de Pedidos Activo:** Conectado en tiempo real a la zona centro.")

# Ejecución de la Parte 2
renderizar_encabezado_y_rol()
renderizar_barra_busqueda_ia()

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


# =========================================================
# PARTE 3: CATÁLOGO, TIENDAS Y CHAT INTELIGENTE (RESULTADO FINAL)
# =========================================================

# 1. CATÁLOGO DE PRODUCTOS ("Recomendado para ti")
st.markdown("<h3 style='color: white; margin-top: 20px;'>Recomendado para ti <span style='font-size:14px; float:right; color:#7B3FF2; cursor:pointer;'>Ver todo</span></h3>", unsafe_allow_html=True)

# Creamos 3 columnas para la rejilla (grid) de productos
col1, col2, col3 = st.columns(3)

productos = [
    {"nombre": "Audífonos Inalámbricos", "precio": "RD$2,450", "rating": "★ 4.8", "img": "🎧", "col": col1},
    {"nombre": "Smartwatch Pro 4", "precio": "RD$4,950", "rating": "★ 4.7", "img": "⌚", "col": col2},
    {"nombre": "Mochila Urbana", "precio": "RD$1,850", "rating": "★ 4.6", "img": "🎒", "col": col3}
]

for prod in productos:
    with prod["col"]:
        # Renderizamos la tarjeta visual usando la clase CSS de la Parte 1
        st.markdown(f"""
        <div class="tarjeta-interactiva" style="text-align: center; margin-bottom: 10px;">
            <div style="font-size: 45px; background: rgba(255,255,255,0.05); border-radius: 12px; padding: 15px; margin-bottom: 10px;">{prod['img']}</div>
            <h4 style="margin: 5px 0; font-size: 15px; color: white;">{prod['nombre']}</h4>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                <span style="color: #FF6A00; font-weight: bold; font-size: 14px;">{prod['precio']}</span>
                <span style="color: #FFD700; font-size: 13px;">{prod['rating']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Botón funcional de Streamlit que activa el sonido
        if st.button(f"Comprar", key=f"btn_{prod['nombre']}", use_container_width=True):
            reproducir_sonido_ui()
            st.toast(f"¡{prod['nombre']} añadido al carrito!", icon="🛒")

# 2. BANNER PROMOCIONAL INTELIGENTE (IA)
st.markdown("""
<div class="banner-ia" style="margin: 30px 0; display: flex; align-items: center; justify-content: space-between; text-align: left;">
    <div>
        <h3 style="margin:0; color:white;">Ahorra tiempo. Ahorra dinero.</h3>
        <p style="margin:5px 0 0 0; color:#DDD; font-size: 14px;">Nosotros buscamos y comparamos por ti.</p>
    </div>
    <div style="font-size: 35px; background: #7B3FF2; padding: 10px 20px; border-radius: 15px; font-weight: bold; color: white; box-shadow: 0 0 20px rgba(123,63,242,0.6);">
        AI
    </div>
</div>
""", unsafe_allow_html=True)

# 3. TIENDAS DESTACADAS
st.markdown("<h3 style='color: white;'>Tiendas destacadas <span style='font-size:14px; float:right; color:#7B3FF2; cursor:pointer;'>Ver todo</span></h3>", unsafe_allow_html=True)

# 5 columnas para los íconos de las tiendas
t_cols = st.columns(5)
tiendas = [
    {"nombre": "Amazon", "icono": "🛒", "bg": "#FF9900"},
    {"nombre": "M. Libre", "icono": "🤝", "bg": "#FFE600"},
    {"nombre": "Walmart", "icono": "☀", "bg": "#0071CE"},
    {"nombre": "AliExpress", "icono": "🛍️", "bg": "#FF4747"},
    {"nombre": "Shein", "icono": "👗", "bg": "#000000"}
]

for i, tienda in enumerate(tiendas):
    with t_cols[i]:
        if st.button(f"{tienda['icono']} \n {tienda['nombre']}", key=f"tienda_{i}", use_container_width=True):
            reproducir_sonido_ui()
            st.session_state.busqueda_ia = f"Filtrando por {tienda['nombre']}..."
            st.rerun()

# 4. SIMULACIÓN DE RESPUESTA DE CHAT IA (Si el usuario usó la barra de búsqueda en la Parte 2)
if st.session_state.get("busqueda_ia"):
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background: rgba(123, 63, 242, 0.15); border-left: 4px solid #7B3FF2; padding: 15px; border-radius: 8px;">
        <span style="color: #7B3FF2; font-weight: bold;">🤖 Respuesta de FastShopping AI:</span><br>
        <span style="color: white;">He comparado más de 15 tiendas para tu búsqueda: <b>"{st.session_state.busqueda_ia}"</b>. La mejor opción actual está en Amazon con envío gratis a República Dominicana.</span>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# PARTE 3: CATÁLOGO, TIENDAS Y CHAT INTELIGENTE (RESULTADO FINAL)
# =========================================================

# 1. CATÁLOGO DE PRODUCTOS ("Recomendado para ti")
st.markdown("<h3 style='color: white; margin-top: 20px;'>Recomendado para ti <span style='font-size:14px; float:right; color:#7B3FF2; cursor:pointer;'>Ver todo</span></h3>", unsafe_allow_html=True)

# Creamos 3 columnas para la rejilla (grid) de productos
col1, col2, col3 = st.columns(3)

productos = [
    {"nombre": "Audífonos Inalámbricos", "precio": "RD$2,450", "rating": "★ 4.8", "img": "🎧", "col": col1},
    {"nombre": "Smartwatch Pro 4", "precio": "RD$4,950", "rating": "★ 4.7", "img": "⌚", "col": col2},
    {"nombre": "Mochila Urbana", "precio": "RD$1,850", "rating": "★ 4.6", "img": "🎒", "col": col3}
]

for prod in productos:
    with prod["col"]:
        # Renderizamos la tarjeta visual usando la clase CSS de la Parte 1
        st.markdown(f"""
        <div class="tarjeta-interactiva" style="text-align: center; margin-bottom: 10px;">
            <div style="font-size: 45px; background: rgba(255,255,255,0.05); border-radius: 12px; padding: 15px; margin-bottom: 10px;">{prod['img']}</div>
            <h4 style="margin: 5px 0; font-size: 15px; color: white;">{prod['nombre']}</h4>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                <span style="color: #FF6A00; font-weight: bold; font-size: 14px;">{prod['precio']}</span>
                <span style="color: #FFD700; font-size: 13px;">{prod['rating']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Botón funcional de Streamlit que activa el sonido
        if st.button(f"Comprar", key=f"btn_{prod['nombre']}", use_container_width=True):
            reproducir_sonido_ui()
            st.toast(f"¡{prod['nombre']} añadido al carrito!", icon="🛒")

# 2. BANNER PROMOCIONAL INTELIGENTE (IA)
st.markdown("""
<div class="banner-ia" style="margin: 30px 0; display: flex; align-items: center; justify-content: space-between; text-align: left;">
    <div>
        <h3 style="margin:0; color:white;">Ahorra tiempo. Ahorra dinero.</h3>
        <p style="margin:5px 0 0 0; color:#DDD; font-size: 14px;">Nosotros buscamos y comparamos por ti.</p>
    </div>
    <div style="font-size: 35px; background: #7B3FF2; padding: 10px 20px; border-radius: 15px; font-weight: bold; color: white; box-shadow: 0 0 20px rgba(123,63,242,0.6);">
        AI
    </div>
</div>
""", unsafe_allow_html=True)

# 3. TIENDAS DESTACADAS
st.markdown("<h3 style='color: white;'>Tiendas destacadas <span style='font-size:14px; float:right; color:#7B3FF2; cursor:pointer;'>Ver todo</span></h3>", unsafe_allow_html=True)

# 5 columnas para los íconos de las tiendas
t_cols = st.columns(5)
tiendas = [
    {"nombre": "Amazon", "icono": "🛒", "bg": "#FF9900"},
    {"nombre": "M. Libre", "icono": "🤝", "bg": "#FFE600"},
    {"nombre": "Walmart", "icono": "☀", "bg": "#0071CE"},
    {"nombre": "AliExpress", "icono": "🛍️", "bg": "#FF4747"},
    {"nombre": "Shein", "icono": "👗", "bg": "#000000"}
]

for i, tienda in enumerate(tiendas):
    with t_cols[i]:
        if st.button(f"{tienda['icono']} \n {tienda['nombre']}", key=f"tienda_{i}", use_container_width=True):
            reproducir_sonido_ui()
            st.session_state.busqueda_ia = f"Filtrando por {tienda['nombre']}..."
            st.rerun()

# 4. SIMULACIÓN DE RESPUESTA DE CHAT IA (Si el usuario usó la barra de búsqueda en la Parte 2)
if st.session_state.get("busqueda_ia"):
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background: rgba(123, 63, 242, 0.15); border-left: 4px solid #7B3FF2; padding: 15px; border-radius: 8px;">
        <span style="color: #7B3FF2; font-weight: bold;">🤖 Respuesta de FastShopping AI:</span><br>
        <span style="color: white;">He comparado más de 15 tiendas para tu búsqueda: <b>"{st.session_state.busqueda_ia}"</b>. La mejor opción actual está en Amazon con envío gratis a República Dominicana.</span>
    </div>
    """, unsafe_allow_html=True)