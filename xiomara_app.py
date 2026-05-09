python

import streamlit as st
from google import genai
from google.generativeai import types as gen_types  # ajustar import según versión

st.set_page_config(page_title="Xiomara AI", page_icon="✨")

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

@st.cache_resource
def configurar_ia():
    return genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

cliente = configurar_ia()

st.title("✨ Xiomara AI: Tu Asistente Personal")
st.write("Bienvenido. Escribe tu mensaje y te responderé de inmediato.")

with st.form("chat_ia", clear_on_submit=True):
    pregunta = st.text_input("¿En qué puedo ayudarte?", placeholder="Escribe aquí...")
    enviar = st.form_submit_button("Enviar mensaje")

    if enviar and pregunta:
        try:
            prompt_personalizado = f"Eres Xiomara AI, una asistente inteligente, amable y eficiente. Responde a lo siguiente: {pregunta}"

            # --- Forma robusta: construir Content/Part si la SDK lo requiere ---
            try:
                # Si la versión soporta genai.types.Content/Part
                content_obj = gen_types.Content(
                    role="user",
                    parts=[gen_types.Part(text=prompt_personalizado)]
                )
                resp = cliente.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=content_obj
                )
            except Exception:
                # Fallback simple: pasar un string en caso de que la SDK acepte directamente
                resp = cliente.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt_personalizado
                )

            # --- Extracción segura del texto de la respuesta ---
            respuesta_texto = None
            if hasattr(resp, "text") and resp.text:
                respuesta_texto = resp.text
            else:
                # Navegar la estructura candidates -> content -> parts -> text
                try:
                    respuesta_texto = resp.candidates[0].content.parts[0].text
                except Exception:
                    # Intentar otras variantes por compatibilidad
                    try:
                        respuesta_texto = resp.candidates[0].text
                    except Exception:
                        respuesta_texto = None

            st.markdown("---")
            st.subheader("Xiomara AI dice:")
            if respuesta_texto:
                st.info(respuesta_texto)
            else:
                st.warning("No se pudo extraer el texto de la respuesta. Revisa la versión de la SDK o imprime `resp` para inspeccionar su estructura.")
        except Exception as e:
            # Log más detallado para depuración (no mostrar secrets)
            st.warning("Estoy procesando mucha información ahora mismo. Por favor, intenta de nuevo en un momento.")
            st.error(f"Error interno: {e}")

st.markdown("<br><br><p style='text-align: center; color: gray;'>Desarrollado por Xiomara ChV</p>", unsafe_allow_html=True)