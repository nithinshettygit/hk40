import React, { useState } from 'react';
import axios from 'axios';

function WeatherComponent() {
    const [weatherCondition, setWeatherCondition] = useState('');
    const [medications, setMedications] = useState({});

    const getMedications = async () => {
        try {
            const response = await axios.post('http://localhost:5000/get-medications', {
                weather_condition: weatherCondition
            });
            setMedications(response.data);
        } catch (error) {
            console.error('Error fetching medications:', error);
        }
    };

    return (
        <div>
            <h1>Weather-Based Medication Suggestions</h1>
            <input
                type="text"
                placeholder="Enter weather condition"
                value={weatherCondition}
                onChange={(e) => setWeatherCondition(e.target.value)}
            />
            <button onClick={getMedications}>Get Medications</button>

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
                    <p>No medications available for the given weather condition.</p>
                )}
            </div>
        </div>
    );
}

export default WeatherComponent;