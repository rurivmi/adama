import streamlit as st
import pandas as pd
import os


st.header('Datos históricos')
st.caption('Visualización de distintas variables por mes y año')


# Sidebar for accepting input parameters
with st.sidebar:

    variable = st.select_slider('Selecciona una variable', options=["vel_viento", "dir_viento", "temperatura", "humedad_relativa", "presion_barometrica", "precipitacion",
                                                                     "CO", "NO", "NO2", "PPM2_5", "PPM10", "NOX",
                                                                     "intensidad", "ocupacion", "carga"])
    
    year = st.select_slider('Selecciona un año', options=["2019", "2020", "2021", "2022", "2023"])
    
    month = st.select_slider('Selecciona un mes', options=["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"])

    script_path = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join("\\".join(script_path.split("\\")[:-1]), "data/df_final.csv"))


year_df = df[df['datetime'].str.split("-").str[0] == year]
print(year_df.shape)
month_mapping = {'Enero': '01', 'Febrero': '02', 'Marzo': '03', 'Abril': '04', 'Mayo': '05', 'Junio': '06', 'Julio': '07', 'Agosto': '08', 'Septiembre': '09', 'Octubre': '10', 'Noviembre': '11', 'Diciembre': '12'}
month_number = month_mapping.get(month, None)
print(month_number)
if month_number is not None:
    month_df = year_df[year_df['datetime'].str.split("-").str[1] == str(month_number)]
    print(month_df.shape)
else:
    st.error('Invalid month name')

barchart = st.bar_chart(data=month_df, x='datetime', y=variable, width=0, height=0, use_container_width=True, color='#FFCC22')
linechart = st.line_chart(data=month_df, x='datetime', y=variable, width=0, height=0, use_container_width=True, color='#22CCCC')