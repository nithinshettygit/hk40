import React, { useState } from "react";
import axios from "axios";
import './App.css';
import './mediaquery.css'; // Import the media query CSS for responsiveness

function App() {
  const [city, setCity] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    axios
      .post("http://localhost:5000/predict", { city })
      .then((response) => {
        setResult(response.data);
        setError("");
      })
      .catch((err) => {
        setError(err.response?.data?.error || "An error occurred");
        setResult(null);
      });
  };

  return (
    <div className="app-container">
      <header className="header">
        <nav>
          <div className="logo">Weather Health App</div>
          <ul className="nav-links">
            <li><a href="#profile">Profile</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#experience">Experience</a></li>
            <li><a href="#projects">Projects</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
          <div id="hamburger-nav" className="hamburger-menu" onClick={toggleMenu}>
            <div className="hamburger-icon">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <div className="menu-links">
              <a href="#profile">Profile</a>
              <a href="#about">About</a>
              <a href="#experience">Experience</a>
              <a href="#projects">Projects</a>
              <a href="#contact">Contact</a>
            </div>
          </div>
        </nav>
      </header>

      <section id="profile">
        <div className="section__pic-container">
          {/* Add profile picture here */}
        </div>
        <div className="section__text">
          <h2 className="title">Health Prediction Based on City Weather</h2>
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
              <h3 className="mt-4">{`Health Prediction for ${result.city}, ${result.country}`}</h3>

              <div className="mt-3">
                <h4>Health Data:</h4>
                <ul className="list-group">
                  <li className="list-group-item">
                    Respiratory Cases: <strong>{result.respiratory_cases}</strong>
                  </li>
                  <li className="list-group-item">
                    Cardiovascular Cases: <strong>{result.cardiovascular_cases}</strong>
                  </li>
                  <li className="list-group-item">
                    Health Impact Score: <strong>{result.health_impact_score}</strong>
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
                  <li className="list-group-item">Air Quality Index (AQI): {result.aqi}</li>
                </ul>
              </div>

              <div className="mt-4">
                <h4>Health Advice:</h4>
                <ul className="list-group">
                  <li className="list-group-item">
                    <strong>Respiratory Advice:</strong> {result.advice?.respiratory_advice || "Not available"}
                  </li>
                  <li className="list-group-item">
                    <strong>Cardiovascular Advice:</strong> {result.advice?.cardiovascular_advice || "Not available"}
                  </li>
                  <li className="list-group-item">
                    <strong>Overall Health Impact Advice:</strong> {result.advice?.health_impact_advice || "Not available"}
                  </li>
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
            </div>
          )}
        </div>
      </section>

      <footer>
        <div className="text-container">
          <p>© 2024 Your Name. All rights reserved.</p>
          <div id="socials-container">
            <img
              src="./assets/linkedin.png"
              alt="linkedin profile"
              className="icon"
              onClick={() => window.location.href = 'https://www.linkedin.com/in/your-profile/'}
            />
            <img
              src="./assets/github.png"
              alt="github profile"
              className="icon"
              onClick={() => window.location.href = 'https://github.com/your-profile'}
            />
          </div>
        </div>
      </footer>
    </div>
  );
}

function toggleMenu() {
  const menu = document.querySelector(".menu-links");
  const icon = document.querySelector(".hamburger-icon");
  menu.classList.toggle("open");
  icon.classList.toggle("open");
}

export default App;
