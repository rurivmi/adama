import streamlit as st
import pandas as pd
import seaborn as sns
import os

st.header('Modelo imagen')
st.caption('Detección automática de vehículos mediante YOLO.')

# Obtener la ruta del directorio del script actual
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

video_url = "/data/vehicles_detector.mp4"
 
st.video(video_url)
