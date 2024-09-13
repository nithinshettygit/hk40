import React, { useState } from 'react';
import axios from 'axios';
import './App.css';  // Import the main stylesheet
import './mediaquery.css'; // Import the media query CSS for responsiveness

function App() {
  const [city, setCity] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false); // State to control form visibility

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Fetch health prediction and weather data
      const response = await axios.post('http://localhost:5000/predict', { city });
      setResult(response.data);
      setError("");
    } catch (err) {
      setError(err.response?.data?.error || "An error occurred");
      setResult(null);
    }
  };

  const toggleMenu = () => {
    const menu = document.querySelector(".menu-links");
    const icon = document.querySelector(".hamburger-icon");
    menu.classList.toggle("open");
    icon.classList.toggle("open");
  };

  // Ensure precautions is an array or an empty array if not defined
  const precautions = Array.isArray(result?.precautions) ? result.precautions : [];
  const medications = Array.isArray(result?.medications) ? result.medications : [];

  return (
    <div className="app-container">
      <header className="header">
        <nav>
          <div className="logo">HEALTH GO</div>
          <ul className="nav-links">
            <li><a href="#profile">Home</a></li>
            <li><a href="#about">Weather Data</a></li>
            <li><a href="#experience">Precautions</a></li>
            <li><a href="#contact" onClick={() => setShowForm(!showForm)}>Medication Orders</a></li>
          </ul>
          <div id="hamburger-nav" className="hamburger-menu" onClick={toggleMenu}>
            <div className="hamburger-icon">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <div className="menu-links">
              <a href="#profile">Home</a>
              <a href="#about">Weather Data</a>
              <a href="#experience">Precautions</a>
              <a href="#contact" onClick={() => setShowForm(!showForm)}>Medication Orders</a>
            </div>
          </div>
        </nav>
      </header>

      <section id="profile">
        <div className="section__text">
          <h2 className="title">Health Prediction based on Weather Condition</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="city">City</label>
              <input
                type="text"
                className="form-control"
                id="city"
                name="city"
                value={city}
                onChange={(e) => setCity(e.target.value)}
                placeholder="Enter city name"
                required
              />
            </div>
            <button type="submit" className="btn btn-primary">
              Get Prediction
            </button>
          </form>

          <br />

          {error && <h3 className="error text-danger">{error}</h3>}

          {result && (
            <div className="result">
              <h3 className="mt-4">Health Prediction for {result.city}, {result.country}</h3>

              <div className="mt-3">
                <h4>Health Data:</h4>
                <ul className="list-group">
                  <li className="list-group-item">
                    Respiratory Cases: <strong>{result.respiratory_cases} %</strong>
                  </li>
                  <li className="list-group-item">
                    Cardiovascular Cases: <strong>{result.cardiovascular_cases}%</strong>
                  </li>
                  <li className="list-group-item">
                    Health Impact Score: <strong>{result.health_impact_score}%</strong>
                  </li>
                </ul>
              </div>
              <div className="mt-4">
                <h4>Weather Data:</h4>
                <ul className="list-group">
                  <li className="list-group-item">Temperature: {result.temperature} °C</li>
                  <li className="list-group-item">Humidity: {result.humidity} %</li>
                  <li className="list-group-item">Wind Speed: {result.wind_speed} m/s</li>
                  <li className="list-group-item">Pressure: {result.pressure} hPa</li>
                  <li className="list-group-item">Weather Description: {result.weather_description}</li>
                </ul>
              </div>

              <div className="mt-4">
                <h4>Air Pollution Data:</h4>
                <ul className="list-group">
                  <li className="list-group-item">PM2.5: {result.pm25} µg/m³</li>
                  <li className="list-group-item">NO2: {result.no2} µg/m³</li>
                  <li className="list-group-item">O3: {result.o3} µg/m³</li>
                  {/* <li className="list-group-item">AQI: {result.aqi}</li> */}
                </ul>
              </div>

              <div className="mt-4">
                <h4>Precautions:</h4>
                <ul className="list-group">
                  {result.precautions ? (
                    Object.entries(result.precautions).map(([key, value]) => (
                      <li key={key} className="list-group-item">
                        <strong>{key}:</strong> {value}
                      </li>
                    ))
                  ) : (
                    <li className="list-group-item">No precautions available.</li>
                  )}
                </ul>
              </div>
              <div className="mt-4">
                <h4>Medication Suggestions:</h4>
                {medications.length > 0 ? (
                  <ul className="list-group">
                    {medications.map((med, index) => (
                      <li key={index} className="list-group-item">
                        {med}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p>No specific medications suggested for current weather conditions.</p>
                )}
              </div>

              
            </div>
          )}
        </div>
      </section>

      {showForm && (
        <section id="medications">
          <h1>Medication Orders</h1>
          {/* Removed AppointmentForm component */}
        </section>
      )}
    </div>
  );
}

export default App;
