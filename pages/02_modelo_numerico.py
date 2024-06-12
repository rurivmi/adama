import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

# Cargar los modelos y scalers
model = pickle.load(open((os.path.join("\\".join(script_path.split("\\")[:-1]), "pickle_modelo/xgboost_NO2.pkl")), 'rb'))
scaler_X = pickle.load(open((os.path.join("\\".join(script_path.split("\\")[:-1]), "pickle_modelo/scaler_x.pkl")), 'rb'))
encoder = pickle.load(open((os.path.join("\\".join(script_path.split("\\")[:-1]), "pickle_modelo/encoder.pkl")), 'rb'))
scaler_y = pickle.load(open((os.path.join("\\".join(script_path.split("\\")[:-1]), "pickle_modelo/scaler_y.pkl")), 'rb'))
festivos_df = pd.read_excel('data/calendario.xls', parse_dates=['Dia'])
festivos_dict = festivos_df.set_index('Dia')['laborable / festivo / domingo festivo'].to_dict()

# Definir las funciones de preprocesamiento
def get_franja_horaria(hour):
    if 0 <= hour < 7:
        return 'madrugada'
    elif 7 <= hour < 12:
        return 'mañana'
    elif 12 <= hour < 16:
        return 'medio_dia'
    elif 16 <= hour < 21:
        return 'tarde'
    elif 21 <= hour < 24:
        return 'noche'

def get_confinamiento_status(date):
    start_confinamiento_general = pd.Timestamp('2020-03-14')
    end_confinamiento_general = pd.Timestamp('2020-06-21')
    if start_confinamiento_general <= date <= end_confinamiento_general:
        return 'si'
    else:
        return 'no'

def get_estacion(month, day):
    if (month == 12 and day >= 21) or (month in [1, 2]) or (month == 3 and day < 21):
        return 'invierno'
    elif (month == 3 and day >= 21) or (month in [4, 5]) or (month == 6 and day < 21):
        return 'primavera'
    elif (month == 6 and day >= 21) or (month in [7, 8]) or (month == 9 and day < 21):
        return 'verano'
    elif (month == 9 and day >= 21) or (month in [10, 11]) or (month == 12 and day < 21):
        return 'otoño'

def preprocess_input_data(json_data, scaler_X, encoder, festivos_dict):
    df = pd.DataFrame([json_data])
    df['datetime'] = pd.to_datetime(df['datetime'])

    df['franja_horaria'] = df['datetime'].dt.hour.apply(get_franja_horaria)
    df['confinamiento'] = df['datetime'].apply(get_confinamiento_status)
    df['estacion'] = df['datetime'].apply(lambda x: get_estacion(x.month, x.day))
    df['hora_del_dia'] = df['datetime'].dt.hour

    df['festivo'] = df['datetime'].apply(lambda x: 'si' if festivos_dict.get(x.date()) in ['festivo', 'domingo festivo'] else 'no')
    df['fin_de_semana'] = df['datetime'].apply(lambda x: 'si' if x.weekday() >= 5 else 'no')

    df = df.drop(columns=['datetime'])

    numerical_cols = ['vel_viento', 'dir_viento', 'temperatura', 'humedad_relativa', 'presion_barometrica', 'precipitacion', 'intensidad', 'hora_del_dia']
    categorical_cols = ['franja_horaria', 'estacion', 'confinamiento', 'festivo', 'fin_de_semana']

    df[numerical_cols] = scaler_X.transform(df[numerical_cols])
    encoded_cols = encoder.transform(df[categorical_cols])
    encoded_df = pd.DataFrame(encoded_cols, columns=encoder.get_feature_names_out(categorical_cols), index=df.index)
    df_processed = pd.concat([df.drop(columns=categorical_cols), encoded_df], axis=1)

    return df_processed

def predict_no2(json_data, model, scaler_X, encoder, scaler_y, festivos_dict):
    df_processed = preprocess_input_data(json_data, scaler_X, encoder, festivos_dict)
    y_pred_scaled = model.predict(df_processed)
    y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1))
    return y_pred[0, 0]

# Interfaz de usuario en Streamlit
st.header('Modelo numérico')
st.caption('En esta sección se muestra el modelo numérico que se ha desarrollado para predecir la concentración de NO2')

date = st.date_input('Selecciona la fecha')
time = st.time_input('Selecciona la hora')
datetime = pd.Timestamp.combine(date, time)

vel_viento = st.slider('Velocidad del viento (m/s)', 0.0, 8.0, 0.68)
dir_viento = st.slider('Dirección del viento', 0.0, 360.0, 48.0)
temperatura = st.slider('Temperatura (C°)', -10.0, 50.0, 2.6)
humedad_relativa = st.slider('Humedad relativa (%)', 0.0, 100.0, 71.0)
presion_barometrica = st.slider('Presión barométrica (mb)', 920.0, 1040.0, 959.0)
precipitacion = st.slider('Precipitación (l/m²)', 0.0, 10.0, 0.0)
intensidad = st.slider('Intensidad (vehículos/hora)', 0, 860, 135)

json_data = {
    "datetime": datetime,
    "vel_viento": vel_viento,
    "dir_viento": dir_viento,
    "temperatura": temperatura,
    "humedad_relativa": humedad_relativa,
    "presion_barometrica": presion_barometrica,
    "precipitacion": precipitacion,
    "intensidad": intensidad
}

# Realizar la predicción cuando el usuario haga clic en el botón
if st.button('Predecir'):
    predicted_no2 = predict_no2(json_data, model, scaler_X, encoder, scaler_y, festivos_dict)
    st.write(f"Predicción de NO2: {predicted_no2:.2f} µg/m³")
    
    # Visualización del semáforo
    if predicted_no2 < 50:
        st.success('Muy bueno: Es seguro hacer deporte al aire libre.')
    elif 50 <= predicted_no2 < 80:
        st.info('Bueno: Es seguro hacer deporte al aire libre.')
    elif 80 <= predicted_no2 < 120:
        st.warning('Regular: Considera limitar la actividad al aire libre.')
    else:
        st.error('Peligroso: No es seguro hacer deporte al aire libre.')
