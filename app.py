#!/usr/bin/env python
# coding: utf-8

# In[5]:


from flask import Flask, request, jsonify
import datetime
import joblib
import numpy as np
import pandas as pd


# In[6]:


# Initialize Flask app
app = Flask(__name__)

# Load the trained model and scaler
model = joblib.load('carmodel.pkl')
scaler = joblib.load('scaler.pkl')

# Load the column names used during training
original_columns = ['year', 'km_driven', 'fuel_Diesel', 'fuel_LPG', 'fuel_Petrol',
       'seller_type_Individual', 'seller_type_Trustmark Dealer',
       'transmission_Manual', 'owner_Fourth & Above Owner',
       'owner_Second Owner', 'owner_Test Drive Car', 'owner_Third Owner',
       'Manufacturer_Audi', 'Manufacturer_BMW', 'Manufacturer_Chevrolet',
       'Manufacturer_Daewoo', 'Manufacturer_Datsun', 'Manufacturer_Fiat',
       'Manufacturer_Force', 'Manufacturer_Ford', 'Manufacturer_Honda',
       'Manufacturer_Hyundai', 'Manufacturer_Isuzu', 'Manufacturer_Jaguar',
       'Manufacturer_Jeep', 'Manufacturer_Kia', 'Manufacturer_Land',
       'Manufacturer_MG', 'Manufacturer_Mahindra', 'Manufacturer_Maruti',
       'Manufacturer_Mercedes-Benz', 'Manufacturer_Mitsubishi',
       'Manufacturer_Nissan', 'Manufacturer_OpelCorsa', 'Manufacturer_Renault',
       'Manufacturer_Skoda', 'Manufacturer_Tata', 'Manufacturer_Toyota',
       'Manufacturer_Volkswagen', 'Manufacturer_Volvo']

@app.route('/')
def home():
    return "Car Price Prediction API is running. Use /predict endpoint to get predictions."

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_data = pd.DataFrame([data])
        make = input_data["name"].str.split(" ", expand=True)
        input_data["Manufacturer"] = make[0]
        curr_time = datetime.datetime.now()
        input_data['year'] = input_data['year'].apply(lambda x: curr_time.year - x)
        input_data_encoded = pd.get_dummies(input_data, columns=['fuel', 'seller_type', 'transmission', 'owner', 'Manufacturer'], drop_first=True)

        # Ensure the input data has the same columns as the training data
        input_data_encoded = input_data_encoded.reindex(columns=original_columns, fill_value=0)
        scaled_features = scaler.transform(input_data_encoded)
        prediction = model.predict(scaled_features)
        return jsonify({'predicted_price': prediction[0]})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)


# In[ ]:





# In[ ]:




