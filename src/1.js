import React, { useState, useEffect } from 'react';
import axios from 'axios';

function WeatherComponent() {
    const [cityName, setCityName] = useState('');
    const [medications, setMedications] = useState({});
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const getMedications = async () => {
        if (!cityName) {
            setError('City name is required.');
            return;
        }

        setLoading(true);
        try {
            // Fetch weather data
            const weatherResponse = await axios.post('http://localhost:5000/get-weather', {
                city: cityName
            });

            const weatherCondition = weatherResponse.data.weather_condition;
            
            // Fetch medications
            const medicationsResponse = await axios.post('http://localhost:5000/get-medications', {
                weather_condition: weatherCondition
            });

            setMedications(medicationsResponse.data);
            setError(''); // Clear previous error
        } catch (error) {
            console.error('Error fetching data:', error);
            setError('Error fetching data. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (cityName) {
            getMedications();
        }
    }, [cityName]);

    return (
        <div>
            <h1>Weather-Based Medication Suggestions</h1>
            <input
                type="text"
                placeholder="Enter city name"
                value={cityName}
                onChange={(e) => setCityName(e.target.value)}
            />
            <button onClick={getMedications} disabled={loading}>
                {loading ? 'Loading...' : 'Get Medications'}
            </button>

            {error && <p style={{ color: 'red' }}>{error}</p>}

            <div>
                <h2>Medications:</h2>
                {Object.keys(medications).length > 0 ? (
                    <ul>
                        {Object.entries(medications).map(([disease, medication]) => (
                            <li key={disease}>
                                <strong>{disease}:</strong> {medication}
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>No medications available for the current weather condition.</p>
                )}
            </div>
        </div>
    );
}

export default WeatherComponent;
