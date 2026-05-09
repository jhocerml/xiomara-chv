import streamlit as st
from google import genai

# --- CONFIGURACIÓN DE FONDO Y ESTILO ---
st.set_page_config(page_title="Xiomara AI", page_icon="✨")

# Estilo de fondo oscuro elegante
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0e1117;
    background-image: radial-gradient(#2c3e50 0.5px, #0e1117 0.5px);
    background-size: 20px 20px;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# --- CONEXIÓN INTERNA ---
@st.cache_resource
def configurar_ia():
    # Tu llave sigue segura en st.secrets
    return genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

cliente = configurar_ia()

# --- INTERFAZ PERSONALIZADA ---
st.title("✨ Xiomara AI: Tu Asistente Personal")
st.write("Bienvenido. Escribe tu mensaje y te responderé de inmediato.")

# Formulario de Chat
with st.form("chat_ia", clear_on_submit=True):
    pregunta = st.text_input("¿En qué puedo ayudarte?", placeholder="Escribe aquí...")
    enviar = st.form_submit_button("Enviar mensaje")

    if enviar and pregunta:
        try:
            # Personalizamos la respuesta para que se identifique como Xiomara AI
            prompt_personalizado = f"Eres Xiomara AI, una asistente inteligente, amable y eficiente. Responde a lo siguiente: {pregunta}"
            
            res_ia = cliente.models.generate_content(
                model="gemini-1.5-flash", 
                contents=prompt_personalizado
            )
            
            st.markdown("---")
            st.subheader("Xiomara AI dice:")
            st.info(res_ia.text)
            
        except Exception as e:
            st.warning("Estoy procesando mucha información ahora mismo. Por favor, intenta de nuevo en un momento.")

# Pie de página opcional
st.markdown("<br><br><p style='text-align: center; color: gray;'>Desarrollado por Xiomara ChV</p>", unsafe_allow_html=True)