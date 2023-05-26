import React, { useState } from 'react';
import './LoginPage.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('/users/login', {
        username: username,
        password: password,
      });
      const token = response.data.access_token;
      // Store the token in local storage
      localStorage.setItem('token', token);
      // Set the default header for all axios requests
      axios.defaults.headers.common['Authorization'] = `Bearer "${token}"`;
      // After successful login, make a request to /users/1/wallets
      // Navigate to the specified URL
      navigate('/users/menu');
    } catch (error) {
      if (error.response && error.response.data) {
        const { data } = error.response;
        // Access the error response data here
        console.log(data);
      } else {
        console.error('An unexpected error occurred:', error);
      }
    }

  };

  return (
    <div className="login-form">
      <h2>Login</h2>
      {errorMessage && <p className="error-message">{errorMessage}</p>}
      <form onSubmit={handleSubmit}>
        <label>
          Username:
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </label>
        <label>
          Password:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default LoginPage;
