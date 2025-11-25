# frontend.py
import streamlit as st
import requests
import json

st.title("🚗 Used Car Price Predictor")

# 1. Load options for dropdowns
with open('options.json', 'r') as f:
    options = json.load(f)

# 2. Create the User Interface
col1, col2 = st.columns(2)

with col1:
    company = st.selectbox("Select Car Brand", options['companies'])
    # Filter models based on selected company could be done here, 
    # but for simplicity, we show all models or you can implement logic to filter
    model_name = st.selectbox("Select Model", options['models'])
    fuel_type = st.selectbox("Select Fuel Type", options['fuel_types'])

with col2:
    year = st.number_input("Manufacturing Year", min_value=1990, max_value=2024, value=2018)
    kms_driven = st.number_input("Kilometers Driven", min_value=0, value=50000)

# 3. The Predict Button
if st.button("Predict Price"):
    # Prepare the data to send to FastAPI
    payload = {
        "company": company,
        "model_name": model_name,
        "year": year,
        "kms_driven": kms_driven,
        "fuel_type": fuel_type
    }

    # Send request to our FastAPI backend
    # Note: We assume backend is running on port 8000
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            price = result['predicted_price']
            st.success(f"Estimated Price: ₹ {price:,.2f}")
        else:
            st.error("Error getting prediction from backend.")
            
    except requests.exceptions.ConnectionError:
        st.error("Backend is not running! Please start FastAPI.")