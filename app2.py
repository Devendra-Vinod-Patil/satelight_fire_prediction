from textwrap import dedent

code = dedent(r'''
# NOTE:
# This is a starter professional app.py template that keeps your existing
# backend (predict_live.py, live_predict.py, fetch_live_satellite.py, etc.)
# unchanged.

import requests
import streamlit as st
from PIL import Image
from live_predict import live_prediction

OPENWEATHER_API_KEY = "bc6666ea6cf36a2bc50815e582ed4372"

st.set_page_config(page_title="Forest Fire Prediction", page_icon="🌲", layout="wide")

st.markdown("""
<style>
.main {background:#f5f7fa;}
.metric-card{
background:white;padding:15px;border-radius:10px;
box-shadow:0 2px 8px rgba(0,0,0,.1);
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_weather(lat, lon):
    if OPENWEATHER_API_KEY == "PASTE_YOUR_OPENWEATHER_API_KEY":
        return None
    url=f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    r=requests.get(url,timeout=20)
    if r.status_code!=200:
        return None
    return r.json()

st.sidebar.title("🌲 Forest Fire Dashboard")
page=st.sidebar.radio("Navigation",["Home","Live Prediction"])

if page=="Home":
    st.title("🌍 Forest Fire Prediction System")
    st.info("CNN + NASA GIBS + NASA FIRMS + OpenWeather")
    st.write("Developed by Devendra Patil")

else:
    st.title("🛰 Live Prediction")

    c1,c2=st.columns(2)
    with c1:
        lat=st.number_input("Latitude",value=21.1702,format="%.6f")
    with c2:
        lon=st.number_input("Longitude",value=72.8311,format="%.6f")

    if st.button("Predict"):
        with st.spinner("Running prediction..."):
            result=live_prediction(lat,lon)

        weather=get_weather(lat,lon)

        m1,m2,m3,m4=st.columns(4)
        m1.metric("Prediction",result["predicted_label"])
        m2.metric("Confidence",f'{result["confidence"]*100:.2f}%')
        m3.metric("Hotspots",result["firms_active_fire_hotspots_nearby"])
        m4.metric("Location",f"{lat:.2f},{lon:.2f}")

        if weather:
            st.subheader("🌦 Current Weather")
            w1,w2,w3,w4=st.columns(4)
            w1.metric("Temperature",f'{weather["main"]["temp"]} °C')
            w2.metric("Humidity",f'{weather["main"]["humidity"]}%')
            w3.metric("Wind",f'{weather["wind"]["speed"]} m/s')
            w4.metric("Condition",weather["weather"][0]["main"])

            st.write("### Client Information")
            st.write({
                "City": weather.get("name"),
                "Country": weather["sys"].get("country"),
                "Timezone": weather.get("timezone")
            })

        st.progress(int(result["confidence"]*100))

        if result["firms_active_fire_hotspots_nearby"]>0:
            st.error("🔥 Active Fire Hotspots Detected")
        else:
            st.success("✅ No Active Fire Hotspots")

        st.image(result["image_path"],caption="Live Satellite Image",use_container_width=True)
''')

path="/mnt/data/app.py"
with open(path,"w",encoding="utf-8") as f:
    f.write(code)

print(path)
