import streamlit as st
import numpy as np
import joblib
# import matplotlib.pyplot as plt
import time

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# ================= PDF FUNCTION =================
def create_pdf(prediction, inputs_dict):
    file_path = "house_price_report.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, "House Price Prediction Report")

    c.setFont("Helvetica", 14)
    c.drawString(50, 720, f"Estimated Price: ${prediction:,.2f}")

    c.setFont("Helvetica-Bold", 15)
    c.drawString(50, 690, "Input Details:")

    y = 660
    c.setFont("Helvetica", 12)

    for key, value in inputs_dict.items():
        c.drawString(50, y, f"{key}: {value}")
        y -= 20
        if y < 50:
            c.showPage()
            y = 750

    c.save()
    return file_path


# ================= ANIMATED COUNTER =================
def animated_counter(target_value, duration=1.5):
    placeholder = st.empty()
    steps = 50
    sleep_time = duration / steps

    for i in range(steps + 1):
        value = int((target_value / steps) * i)
        placeholder.markdown(
            f"<h2 style='text-align:center; color:#27ae60;'>💰 ${value:,.0f}</h2>",
            unsafe_allow_html=True
        )
        time.sleep(sleep_time)


# ================= PAGE CONFIG =================
st.set_page_config(
    # page_title="🏠 House Price Predictor",
    page_icon="🏡",
    layout="wide",
)


# ================= CSS + ANIMATION =================
st.markdown("""
<style>

@keyframes slideFade {
    0% {opacity: 0; transform: translateY(25px);}
    100% {opacity: 1; transform: translateY(0);}
}

@keyframes pulse {
    0% {box-shadow: 0 0 0 0 rgba(74,144,226,0.6);}
    70% {box-shadow: 0 0 0 15px rgba(74,144,226,0);}
    100% {box-shadow: 0 0 0 0 rgba(74,144,226,0);}
}

div[data-testid="stNumberInput"],
div[data-testid="stSelectbox"] {
    animation: slideFade 0.8s ease-in-out;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

div[data-testid="stNumberInput"]:hover,
div[data-testid="stSelectbox"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
}

input:focus {
    border: 2px solid #4a90e2 !important;
    box-shadow: 0 0 10px rgba(74,144,226,0.5) !important;
}

.stButton>button {
    background-color: #4a90e2;
    color: white;
    font-size: 18px;
    border-radius: 10px;
    padding: 12px 28px;
    animation: pulse 2s infinite;
    transition: transform 0.3s ease;
}

.stButton>button:hover {
    background-color: #357ABD;
    transform: scale(1.05);
}

.card {
    background: rgba(255,255,255,0.95);
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    animation: slideFade 1s ease-in-out;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #2C3E50;
}

.subtext {
    text-align: center;
    color: #7f8c8d;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)


# ================= TITLE =================
st.markdown("<div class='title'>🏠 House Price Prediction App</div>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Enter property details to estimate price</div><br>", unsafe_allow_html=True)


# ================= SIDEBAR =================
st.sidebar.header("🔧 App Settings")

model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

st.sidebar.success("Model Loaded Successfully ✔")


# ================= INPUT FORM =================
st.markdown("### 📝 Enter House Details")
col1, col2, col3 = st.columns(3)

with col1:
    bedrooms = st.number_input("🛏 Bedrooms", 1, 10, 3)
    bathrooms = st.number_input("🛁 Bathrooms", 1, 8, 2)
    sqft_living = st.number_input("📐 Living Area (sqft)", 200, 10000, 2000)
    floors = st.number_input("🏢 Floors", 1, 4, 1)
    waterfront = st.selectbox("🌊 Waterfront View", [0, 1])

with col2:
    view = st.number_input("👀 View Rating", 0, 4, 0)
    condition = st.number_input("🔧 Condition", 1, 5, 3)
    grade = st.number_input("📊 Grade", 1, 13, 7)
    sqft_above = st.number_input("⬆ Sqft Above", 100, 10000, 1500)
    sqft_basement = st.number_input("⬇ Sqft Basement", 0, 3000, 0)

with col3:
    yr_built = st.number_input("🏗 Year Built", 1900, 2022, 1990)
    zipcode = st.number_input("📮 Zipcode", 98000, 99000, 98103)
    lat = st.number_input("📍 Latitude", 47.0, 48.0, 47.50)
    long = st.number_input("📌 Longitude", -122.5, -121.0, -121.20)
    sqft_living15 = st.number_input("📏 Living Area (15)", 200, 5000, 1800)
    year = st.number_input("📆 Sale Year", 2010, 2025, 2015)
    month = st.number_input("🗓 Sale Month", 1, 12, 6)


# ================= PREPARE DATA =================
input_data = np.array([[
    bedrooms, bathrooms, sqft_living, floors, waterfront,
    view, condition, grade, sqft_above, sqft_basement,
    yr_built, zipcode, lat, long, sqft_living15, year, month
]])

scaled_data = scaler.transform(input_data)


# ================= PREDICTION =================
st.markdown("### 📈 Prediction Result")

if st.button("🪄 Predict House Price"):
    log_prediction = model.predict(scaled_data)[0]
    
    # Convert log(price) → actual price
    prediction = np.exp(log_prediction)

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.markdown("### 🏡 Estimated House Price")
    animated_counter(prediction)

    st.caption("📘 Price estimated using ML model")

    inputs_dict = {
        "Bedrooms": bedrooms,
        "Bathrooms": bathrooms,
        "Sqft Living": sqft_living,
        "Floors": floors,
        "Waterfront": waterfront,
        "View": view,
        "Condition": condition,
        "Grade": grade,
        "Sqft Above": sqft_above,
        "Sqft Basement": sqft_basement,
        "Year Built": yr_built,
        "Zipcode": zipcode,
        "Latitude": lat,
        "Longitude": long,
        "Sqft Living 15": sqft_living15,
        "Sale Year": year,
        "Sale Month": month
    }

    pdf_file = create_pdf(prediction, inputs_dict)

    with open(pdf_file, "rb") as f:
        st.download_button(
            "📄 Download Prediction Report (PDF)",
            f,
            file_name="House_Price_Report.pdf",
            mime="application/pdf"
        )

    st.markdown("</div>", unsafe_allow_html=True)
