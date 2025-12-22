# 🇦🇺 Streamlit Weather App  
A lightweight Streamlit application for forecasting weather in Australia ☀️🌧️  
Built using a trained **Random Forest** model and deployed on **Streamlit Cloud**.

👉 [Open the app on Streamlit Cloud](https://app-weather-app361.streamlit.app/)


## Features
- Input meteorological parameters (temperature, pressure, humidity, etc.)
- Predict the **probability of rain tomorrow** using a pre-trained ML model
- Dynamic background that changes based on predicted weather conditions
- Interactive map highlighting the selected city


## Run Locally

```bash
git clone https://github.com/Sofipet/streamlit-weather-app.git
cd streamlit-weather-app
pip install -r requirements.txt
streamlit run app.py
