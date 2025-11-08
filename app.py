import streamlit as st
import pandas as pd
import numpy as np
import joblib


# 1. Завантаження моделі

@st.cache_resource
def load_model():
    model = joblib.load("models/aussie_rain.joblib")
    return model

model = load_model()

st.title("🌦️ Прогноз дощу в Австралії")
st.write("Введи дані нижче, щоб дізнатися, чи буде дощ завтра.")


# 2. Інтерфейс користувача

col1, col2 = st.columns(2)

with col1:
    MinTemp = st.number_input("Мінімальна температура (°C)", value=10.0)
    MaxTemp = st.number_input("Максимальна температура (°C)", value=25.0)
    Rainfall = st.number_input("Опади сьогодні (мм)", value=0.0)
    Evaporation = st.number_input("Випаровування (мм)", value=5.0)
    Sunshine = st.number_input("Сонячні години", value=7.0)

with col2:
    WindGustDir = st.selectbox("Напрям вітру (порив)", 
                               ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW'])
    WindGustSpeed = st.number_input("Швидкість пориву (км/год)", value=35.0)
    Humidity3pm = st.slider("Вологість о 15:00 (%)", 0, 100, 60)
    Pressure3pm = st.number_input("Тиск о 15:00 (hPa)", value=1015.0)
    RainToday = st.selectbox("Чи був дощ сьогодні?", ['No', 'Yes'])


# 3. Формування DataFrame

input_dict = {
    'MinTemp': [MinTemp],
    'MaxTemp': [MaxTemp],
    'Rainfall': [Rainfall],
    'Evaporation': [Evaporation],
    'Sunshine': [Sunshine],
    'WindGustDir': [WindGustDir],
    'WindGustSpeed': [WindGustSpeed],
    'Humidity3pm': [Humidity3pm],
    'Pressure3pm': [Pressure3pm],
    'RainToday': [RainToday]
}

input_df = pd.DataFrame(input_dict)


# 4. Прогноз

if st.button("🔮 Прогнозувати"):
    prediction = model.predict(input_df)
    prob = model.predict_proba(input_df)[0][1]

    if prediction[0] == "Yes":
        st.error(f"☔ Ймовірність дощу завтра: **{prob:.2%}**")
    else:
        st.success(f"🌤️ Ймовірність дощу завтра: **{prob:.2%}**")
