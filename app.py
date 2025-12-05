import streamlit as st
import pandas as pd
import joblib
import pydeck as pdk



# 1. Page settings

st.set_page_config(
    page_title="Australian Weather Forecast",
    page_icon="☀️",
    layout="centered"
)


# 2. Load model

@st.cache_resource
def load_model():
    data = joblib.load("models/aussie_rain_rf.joblib")
    return data

data = load_model()
model = data["model"]
imputer = data["imputer"]
scaler = data["scaler"]
encoder = data["encoder"]
numeric_cols = data["numeric_cols"]
categorical_cols = data["categorical_cols"]


# 3. Dynamic background function

def set_dynamic_background(state="default"):

    if state == "sunny":
        bg_url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"
    elif state == "rainy":
        bg_url = "https://images.unsplash.com/photo-1635848499642-ae0fa19d6c3e?fm=jpg&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8cmFpbiUyMG9uJTIwd2luZG93fGVufDB8fDB8fHww&ixlib=rb-4.1.0&q=80&w=2000"
    else:
        bg_url = "https://images.unsplash.com/photo-1672211989567-ffedea9cc234?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=2574"

    st.markdown(f"""
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stToolbar"] {{
        background: transparent !important;
    }}

    .stApp {{
        background:
            linear-gradient(rgba(255,255,255,0.35), rgba(255,255,255,0.35)),
            url('{bg_url}') no-repeat center center fixed !important;
        background-size: cover !important;
    }}

    .block-container {{
        background: #ffffff;
        border-radius: 20px;
        padding: 2rem 3.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        max-width: 1100px;
        margin: 2rem auto;
    }}

    h1 {{
        text-align: center;
        color: #0d47a1;
        font-weight: 700;
    }}

    p.subtitle {{
        text-align: center;
        color: #1a237e;
        font-size: 16px;
        margin-top: -10px;
    }}

    .stButton > button {{
        background: linear-gradient(90deg, #2196f3, #64b5f6);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6em 1.3em;
        font-size: 16px;
        transition: all 0.2s ease-in-out;
    }}
    .stButton > button:hover {{
        background: linear-gradient(90deg, #42a5f5, #90caf9);
        transform: scale(1.03);
    }}
    </style>
    """, unsafe_allow_html=True)


# Initialize background state
if "weather_state" not in st.session_state:
    st.session_state["weather_state"] = "default"

# Apply background
set_dynamic_background(st.session_state["weather_state"])


# 4. Title

st.markdown("<h1>🇦🇺 Australian Weather Forecast</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Check what the weather will be tomorrow — sunny or rainy</p>", unsafe_allow_html=True)
st.divider()


# 5. User input

st.markdown("### 📍 Main indicators")

col1, col2 = st.columns(2)
with col1:
    Location = st.selectbox("City", [
        "Adelaide", "Albany", "Albury", "AliceSprings",
        "Brisbane", "Canberra", "Darwin", "Hobart", "Melbourne", "Sydney"
    ])
with col2:
    Rainfall = st.slider("Rainfall today (mm)", 0.0, 100.0, 0.0)

col1, col2 = st.columns(2)
with col1:
    MinTemp = st.slider("Minimum temperature (°C)", -5.0, 35.0, 10.0)
with col2:
    MaxTemp = st.slider("Maximum temperature (°C)", 0.0, 45.0, 25.0)

col1, col2 = st.columns(2)
with col1:
    Sunshine = st.slider("Sunshine hours", 0.0, 14.0, 7.0)
with col2:
    Evaporation = st.slider("Evaporation (mm)", 0.0, 20.0, 5.0)

st.markdown("---")
st.markdown("### 💨 Wind and pressure")

col1, col2, col3 = st.columns(3)
with col1:
    WindGustDir = st.selectbox("Wind gust direction", ["N","NE","E","SE","S","SW","W","NW"])
with col2:
    WindGustSpeed = st.slider("Gust speed (km/h)", 0, 150, 35)
with col3:
    RainToday = st.selectbox("Was there rain today?", ["No", "Yes"])

col1, col2, col3 = st.columns(3)
with col1:
    Pressure9am = st.slider("Pressure at 9am (hPa)", 980.0, 1040.0, 1015.0)
with col2:
    Pressure3pm = st.slider("Pressure at 3pm (hPa)", 980.0, 1040.0, 1012.0)
with col3:
    WindSpeed3pm = st.slider("Average wind speed (km/h)", 0, 80, 15)

st.markdown("---")
st.markdown("### 🌦️ Humidity and cloudiness")

col1, col2, col3 = st.columns(3)
with col1:
    Humidity9am = st.slider("Humidity at 9am (%)", 0, 100, 60)
with col2:
    Humidity3pm = st.slider("Humidity at 3pm (%)", 0, 100, 55)
with col3:
    Cloud3pm = st.slider("Cloudiness (0–9)", 0, 9, 4)


# 6. City coordinates for the map

cities = pd.DataFrame({
    "city": ["Adelaide","Albany","Albury","AliceSprings","Brisbane","Canberra","Darwin","Hobart","Melbourne","Sydney"],
    "lat": [-34.9285,-35.02,-36.0737,-23.698,-27.4698,-35.2809,-12.4634,-42.8821,-37.8136,-33.8688],
    "lon": [138.6007,117.88,146.9135,133.8807,153.0251,149.13,130.8456,147.3272,144.9631,151.2093]
})


# 7. Build input dataframe

input_data = pd.DataFrame({
    "Location": [Location],
    "MinTemp": [MinTemp],
    "MaxTemp": [MaxTemp],
    "Rainfall": [Rainfall],
    "Evaporation": [Evaporation],
    "Sunshine": [Sunshine],
    "WindGustDir": [WindGustDir],
    "WindGustSpeed": [WindGustSpeed],
    "WindDir9am": ["N"],
    "WindDir3pm": ["N"],
    "WindSpeed9am": [10.0],
    "WindSpeed3pm": [WindSpeed3pm],
    "Humidity9am": [Humidity9am],
    "Humidity3pm": [Humidity3pm],
    "Pressure9am": [Pressure9am],
    "Pressure3pm": [Pressure3pm],
    "Cloud9am": [4],
    "Cloud3pm": [Cloud3pm],
    "Temp9am": [15.0],
    "Temp3pm": [MaxTemp - 3],
    "RainToday": ["Yes" if RainToday == "Yes" else "No"]
})

input_data[numeric_cols] = imputer.transform(input_data[numeric_cols])
scaled = scaler.transform(input_data[numeric_cols])
scaled_df = pd.DataFrame(scaled, columns=numeric_cols)
encoded = encoder.transform(input_data[categorical_cols])
encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(categorical_cols))
X_ready = pd.concat([scaled_df, encoded_df], axis=1)


# 8. Prediction

st.markdown("---")
if st.button("Show forecast for tomorrow", use_container_width=True):
    prob = model.predict_proba(X_ready)[0][1]
    prediction = int(prob > 0.5)

    # Dynamic background
    if prediction == 1:
        st.session_state["weather_state"] = "rainy"
    else:
        st.session_state["weather_state"] = "sunny"

    set_dynamic_background(st.session_state["weather_state"])

    st.markdown("## Tomorrow's forecast:")
    if prediction == 1:
        st.error(f"Chance of rain tomorrow: **{prob:.1%}**")
        st.markdown("Rain is likely tomorrow — better take an umbrella.")
        st.image("https://cdn-icons-png.flaticon.com/512/4150/4150897.png", width=100)
    else:
        st.success(f"Chance of rain tomorrow: **{prob:.1%}**")
        st.markdown("Dry, pleasant weather is expected. A great day to enjoy the outdoors!")
        st.image("https://cdn-icons-png.flaticon.com/512/869/869869.png", width=100)


    # 9. Australia map

    selected_city = cities[cities["city"] == Location]

    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(latitude=-25, longitude=135, zoom=3.0),
        layers=[
            pdk.Layer("ScatterplotLayer",
                      data=cities,
                      get_position=["lon", "lat"],
                      get_color=[180, 180, 180],
                      get_radius=30000),
            pdk.Layer("ScatterplotLayer",
                      data=selected_city,
                      get_position=["lon", "lat"],
                      get_color=[0, 100, 255],
                      get_radius=40500),
            pdk.Layer("TextLayer",
                      data=selected_city,
                      get_position=["lon", "lat"],
                      get_text="city",
                      get_color=[0, 0, 0],
                      get_size=18,
                      get_alignment_baseline="'top'")
        ]
    ))

st.caption("© 2025 Australian Weather App | Sofiia Petrova💛")
