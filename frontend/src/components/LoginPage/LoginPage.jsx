import React, { useState } from 'react';
import './LoginPage.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import {API_BASE_URL} from "../../config";

const LoginPage = (props) =>{
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(`${API_BASE_URL}users/login`, {
        username: username,
        password: password,
      })
      // .then((r) => props.onAuth({info: response.data.response_data,pass: password }));
      const token = response.data.access_token;
      const is_admin = response.data.is_admin;
      props.onAuth({info: response.data.response_data, pass: password});
      // console.log(props)

      localStorage.setItem('token', token);
      localStorage.setItem('is_admin',is_admin);
      localStorage.setItem('username', response.data.response_data.username);
      localStorage.setItem( 'pass', password);
      // localStorage.setItem('props',{info: response.data.response_data, pass: password});

      axios.defaults.headers.common['Authorization'] = `Bearer "${token}"`;

      navigate('/users/menu');
    } catch (error) {
      if (error.response && error.response.data) {
        const { data } = error.response;
        setErrorMessage(data)
        // alert(data)
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
