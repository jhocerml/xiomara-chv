import streamlit as st
from google import genai
from sklearn import tree

# 1. Conexión segura y cacheada
@st.cache_resource
def configurar_ia():
    return genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

cliente = configurar_ia()

# 2. Modelo de Machine Learning (Cacheado para que no entrene cada vez)
@st.cache_resource
def entrenar_modelo():
    caracteristicas = [[140, 0], [130, 0], [150, 1], [170, 1]]
    etiquetas = [0, 0, 1, 1]
    modelo = tree.DecisionTreeClassifier()
    return modelo.fit(caracteristicas, etiquetas)

xiomara_chv = entrenar_modelo()

# 3. Interfaz
st.title("🍎 Xiomara ChV: Versión Pro")

# Clasificador (Funciona instantáneo porque no usa internet)
peso = st.number_input("Peso:", value=150)
textura = st.selectbox("Textura:", [0, 1], format_func=lambda x: "Lisa" if x==0 else "Rugosa")

if st.button("Predecir"):
    res = xiomara_chv.predict([[peso, textura]])
    st.success(f"Es una {'Manzana' if res[0]==0 else 'Naranja'}")

st.divider()

# Chat (Protegido por formulario para no gastar API)
with st.form("chat_ia"):
    pregunta = st.text_input("Pregunta a Gemini:")
    enviar = st.form_submit_button("Consultar")
    
    if enviar and pregunta:
        try:
            res_ia = cliente.models.generate_content(model="gemini-1.5-flash", contents=pregunta)
            st.info(res_ia.text)
        except Exception as e:
            st.warning("Cuota temporalmente agotada. Espera 60 segundos.")