import numpy as np
import requests
from flask import Flask, request, jsonify
import pickle
import logging
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from your React frontend

# Load the trained models
model1 = pickle.load(open('RespiratoryCases.pkl', 'rb'))
model2 = pickle.load(open('CardiovascularCases.pkl', 'rb'))
model3 = pickle.load(open('himpact.pkl', 'rb'))

# Define the weather_disease_mapping
weather_disease_mapping = {
    "hot_weather": [
        "Fungal_infection", "Allergy", "Diabetes", "Bronchial_Asthma", 
        "Hypertension", "Migraine", "Chicken_pox", "Malaria", "Jaundice"
    ],
    "cold_weather": [
        "Common_Cold", "Pneumonia", "Hypothyroidism", "Arthritis", "Osteoarthritis"
    ],
    "rainy": [
        "Typhoid", "Dengue", "Gastroenteritis", "Tuberculosis", "Malaria"
    ],
    "high_humidity": [
        "Acne", "Psoriasis", "Fungal_infections", "Allergy"
    ]
}

# Use environment variable for the API key (set in your system)
API_KEY = os.getenv('WEATHER_API_KEY', 'ef76c046cf45aaf0f94784dbf8f826fc')

# Set up logging
logging.basicConfig(level=logging.INFO)

# Get weather data
def get_weather_data(city_name):
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    logging.info(f"Requesting weather data for {city_name} from {weather_url}")

    try:
        response = requests.get(weather_url)
        response.raise_for_status()
        data = response.json()

        if data.get('cod') != 200:
            logging.error(f"City not found or API error: {data.get('message')}")
            return None, "City not found or weather data unavailable."

        return data, None

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        return None, "City not found or weather data unavailable."
    except Exception as err:
        logging.error(f"Other error occurred: {err}")
        return None, "City not found or weather data unavailable."

# Get air pollution data
def get_air_pollution_data(lat, lon):
    air_pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    logging.info(f"Requesting air pollution data for coordinates ({lat}, {lon})")

    try:
        response = requests.get(air_pollution_url)
        response.raise_for_status()
        data = response.json()

        if 'list' not in data or not data['list']:
            logging.error("Air pollution data not found.")
            return None, "Air pollution data unavailable."

        return data, None

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        return None, "Air pollution data unavailable."
    except Exception as err:
        logging.error(f"Other error occurred: {err}")
        return None, "Air pollution data unavailable."

# Generate health advice based on predictions
def generate_health_advice(resp_cases, card_cases, health_score):
    advice = {}

    # Respiratory cases advice
    if resp_cases < 100:
        advice['respiratory_advice'] = "Air quality is fair, respiratory risks are low."
    elif 100 <= resp_cases < 200:
        advice['respiratory_advice'] = "Moderate risk. People with pre-existing respiratory issues should stay indoors."
    else:
        advice['respiratory_advice'] = "High risk! Avoid outdoor activities, especially for those with respiratory conditions."

    # Cardiovascular cases advice
    if card_cases < 50:
        advice['cardiovascular_advice'] = "Cardiovascular risk is minimal, no major precautions required."
    elif 50 <= card_cases < 150:
        advice['cardiovascular_advice'] = "Moderate cardiovascular risk. Elderly people should avoid strenuous activities."
    else:
        advice['cardiovascular_advice'] = "High cardiovascular risk! Avoid outdoor activities and strenuous exercises."

    # Health impact score advice
    if health_score < 80:
        advice['health_impact_advice'] = "Overall health impact is low, no special precautions needed."
    elif 80 <= health_score < 120:
        advice['health_impact_advice'] = "Moderate health impact. Keep a watch on air quality and limit exposure."
    else:
        advice['health_impact_advice'] = "High health impact! It’s advised to stay indoors and use air purifiers."

    return advice

def generate_health_advice1(resp_cases, card_cases, health_score):
    precautions = {}

    # Respiratory cases precautions for hospital administration
    if resp_cases < 100:
        precautions['respiratory_precautions'] = "No immediate action required. Ensure standard respiratory care facilities are available."
    elif 100 <= resp_cases < 200:
        precautions['respiratory_precautions'] = "Prepare for a moderate increase in respiratory cases. Consider allocating additional respiratory care units and monitoring bed availability."
    else:
        precautions['respiratory_precautions'] = "High influx of respiratory cases expected. Mobilize resources, allocate additional beds, ensure respiratory care units are fully staffed, and stock up on necessary medical supplies."

    # Cardiovascular cases precautions for hospital administration
    if card_cases < 50:
        precautions['cardiovascular_precautions'] = "No immediate action required. Maintain regular cardiovascular care resources."
    elif 50 <= card_cases < 150:
        precautions['cardiovascular_precautions'] = "Anticipate a moderate rise in cardiovascular cases. Ensure availability of cardiovascular specialists and resources."
    else:
        precautions['cardiovascular_precautions'] = "Significant increase in cardiovascular cases expected. Prepare for patient influx by allocating more beds and staff to cardiovascular care, and ensure critical care resources are in place."

    # Health impact score precautions for hospital administration
    if health_score < 80:
        precautions['health_impact_precautions'] = "No significant action required. Maintain standard operations and monitor air quality."
    elif 80 <= health_score < 120:
        precautions['health_impact_precautions'] = "Consider preventive measures. Keep a close watch on the patient flow and ensure extra capacity is available if needed."
    else:
        precautions['health_impact_precautions'] = "Severe health impact expected. Activate emergency protocols, mobilize staff, and ensure adequate supplies for high patient volume. Coordinate with emergency services if necessary."

    return precautions

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    city_name = data.get('city')
    
    if not city_name:
        return jsonify({"error": "City name is required."}), 400
    
    weather_data, error_message = get_weather_data(city_name)

    if error_message:
        return jsonify({"error": error_message}), 400

    try:
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        pressure = weather_data['main']['pressure']
        wind_direction = weather_data['wind'].get('deg', 0)
        
        lat = weather_data['coord']['lat']
        lon = weather_data['coord']['lon']
        
    except KeyError as e:
        return jsonify({"error": f"Missing weather data: {e}"}), 500

    air_pollution_data, error_message = get_air_pollution_data(lat, lon)

    if error_message:
        return jsonify({"error": error_message}), 400

    try:
        pm25 = air_pollution_data['list'][0]['components']['pm2_5']
        no2 = air_pollution_data['list'][0]['components']['no2']
        o3 = air_pollution_data['list'][0]['components']['o3']
        aqi = air_pollution_data['list'][0]['main']['aqi']
    except KeyError as e:
        return jsonify({"error": f"Missing air pollution data: {e}"}), 500

    features = np.array([[aqi, pm25, no2, o3, temp, humidity, wind_speed]])
    features1 = np.array([[aqi, pm25, no2, o3]])

    try:
        prediction1 = model1.predict(features)
        output1 = round(prediction1[0], 2)
        prediction2 = model2.predict(features)
        output2 = round(prediction2[0], 2)
        prediction3 = model3.predict(features1)
        output3 = round(prediction3[0], 2)
    except Exception as e:
        return jsonify({"error": f"Prediction error: {e}"}), 500

    # Determine weather condition
    weather_condition = ""
    if temp > 30:
        weather_condition = "hot_weather"
    elif temp < 10:
        weather_condition = "cold_weather"
    elif humidity > 80:
        weather_condition = "high_humidity"
    elif "rain" in weather_data['weather'][0]['description'].lower():
        weather_condition = "rainy"

    # Fetch medication based on weather condition
    medications = weather_disease_mapping.get(weather_condition, [])

    # Generate health advice
    health_advice = generate_health_advice(output1, output2, output3)
    health_advice1 = generate_health_advice1(output1, output2, output3)

    response_data = {
        "city": city_name,
        "country": weather_data['sys']['country'],
        "temperature": temp,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "pressure": pressure,
        "weather_description": weather_data['weather'][0]['description'],
        "pm25": pm25,
        "no2": no2,
        "o3": o3,
        "aqi": aqi,
        "respiratory_cases": output1,
        "cardiovascular_cases": output2,
        "health_impact_score": output3,
        "advice": health_advice,
        "precautions": health_advice1,
        "medications": medications
    }
    logging.info(f"Response data: {response_data}")
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True)
