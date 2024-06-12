import streamlit as st
import pandas as pd
import seaborn as sns
import os

st.header('Modelo imagen')
st.caption('Detección automática de vehículos mediante YOLO.')

# Obtener la ruta del directorio del script actual
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

# Construir las rutas completas a los archivos necesarios, subiendo un nivel desde 'pages'
base_dir = os.path.dirname(script_dir)  # Subir un nivel desde 'pages'

model_path = os.path.join(base_dir, "pickle_modelo", "xgboost_NO2.pkl")

st.video(os.path.join(base_dir, "data", "vehicles_detector.mp4"))
