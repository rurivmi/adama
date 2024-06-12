import streamlit as st
import pandas as pd
import seaborn as sns
import os
import base64

st.header('Modelo imagen')
st.caption('Detección automática de vehículos mediante YOLO.')

# Obtener la ruta del directorio del script actual
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

# Construir las rutas completas a los archivos necesarios, subiendo un nivel desde 'pages'
base_dir = os.path.dirname(script_dir)  # Subir un nivel desde 'pages'

model_path = os.path.join(base_dir, "pickle_modelo", "xgboost_NO2.pkl")
video_path = os.path.join(base_dir, "data", "vehicles_detector.mp4")

# Incrustar el video en HTML para reproducir automáticamente y en bucle
video_html = f"""
    <video width="700" autoplay loop>
        <source src="data:video/mp4;base64,{base64.b64encode(open(video_path, 'rb').read()).decode()}" type="video/mp4">
    </video>
    """

st.markdown(video_html, unsafe_allow_html=True)
