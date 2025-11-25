# backend.py
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np

app = FastAPI()

# 1. Load the trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# 2. Define the data we expect from the user
# This validates that the data sent is correct
class CarInput(BaseModel):
    company: str
    model_name: str
    year: int
    kms_driven: int
    fuel_type: str

@app.post("/predict")
def predict_price(car: CarInput):
    # A. Pre-process the inputs just like we did in Jupyter
    
    # Calculate Age
    current_year = 2024
    car_age = current_year - car.year
    
    # transform to Log (log1p)
    log_car_age = np.log1p(car_age)
    log_kms_driven = np.log1p(car.kms_driven)

    # B. Create a DataFrame matching the format your Pipeline expects
    # The column names MUST match exactly what you used in X_train
    input_data = pd.DataFrame([[
        car.company, 
        car.fuel_type, 
        car.model_name, 
        log_kms_driven, 
        log_car_age
    ]], columns=['company', 'fuel_type', 'model_name', 'kms_driven', 'car_age'])

    # C. Predict
    # The model returns a LOG price
    prediction_log = model.predict(input_data)
    
    # D. Convert Log price back to Real price (using expm1)
    predicted_price = np.expm1(prediction_log[0])

    return {"predicted_price": round(predicted_price, 2)}