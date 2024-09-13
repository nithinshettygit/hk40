import React, { useState } from 'react';
import axios from 'axios';

function AppointmentForm() {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        date: '',
        time: '',
        symptoms: '',
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post('http://127.0.0.1:8000/api/create-appointment/', formData)
            .then(response => alert('Appointment created successfully!'))
            .catch(error => console.error('Error creating appointment:', error));
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Doctor's Appointment Form</h2>
            <input type="text" name="name" placeholder="Name" onChange={handleChange} required />
            <input type="email" name="email" placeholder="Email" onChange={handleChange} required />
            <input type="date" name="date" onChange={handleChange} required />
            <input type="time" name="time" onChange={handleChange} required />
            <textarea name="symptoms" placeholder="Symptoms" onChange={handleChange} required></textarea>
            <button type="submit">Submit</button>
        </form>
    );
}

export default AppointmentForm;