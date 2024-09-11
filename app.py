import numpy as np
import requests
from flask import Flask, request, jsonify
import pickle
import logging
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from your React frontend

# Load the trained models
model1 = pickle.load(open('RespiratoryCases.pkl', 'rb'))
model2 = pickle.load(open('CardiovascularCases.pkl', 'rb'))
model3 = pickle.load(open('himpact.pkl', 'rb'))

API_KEY = 'ef76c046cf45aaf0f94784dbf8f826fc'

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

def get_air_pollution_data(lat, lon):
    air_pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    logging.info(f"Requesting air pollution data for coordinates ({lat}, {lon})")

    try:
        response = requests.get(air_pollution_url)
        response.raise_for_status()
        data = response.json()

        if data.get('cod') == 404:
            logging.error(f"Air pollution data not found: {data.get('message')}")
            return None, "Air pollution data unavailable."

        return data, None

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        return None, "Air pollution data unavailable."
    except Exception as err:
        logging.error(f"Other error occurred: {err}")
        return None, "Air pollution data unavailable."

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    city_name = data.get('city')
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
        return jsonify({"error": f"Missing data: {e}"}), 500

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

    return jsonify({
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
        "health_impact_score": output3
    })

if __name__ == "__main__":
    app.run(debug=True)
