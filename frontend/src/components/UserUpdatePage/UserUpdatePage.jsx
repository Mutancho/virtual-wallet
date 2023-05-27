import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './UserUpdatePage.css';
import Sidebar from '../SideBar/SideBar';
import jwt_decode from 'jwt-decode';


const decoded = jwt_decode(localStorage.getItem('token'));
console.log(decoded);
function UserUpdatePage() {
  const [formData, setFormData] = useState({
    old_password: '',
    new_password: '',
    repeat_password: '',
    email: '',
    first_name: '',
    last_name: '',
    phone_number: '',
    two_factor_method: '',
    title: '',
    gender: '',
    address: '',
    photo_selfie: null,
    identity_document: null,
  });
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleFileChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.files[0],
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = new FormData();
    Object.entries(formData).forEach(([key, value]) => {
      if (value instanceof File) {
        data.append(key, value, value.name);
      } else {
        data.append(key, value);
      }
    });

    try {
      const response = await axios.put(`/users/${decoded.user_id}`, data, {
        headers: {
          Authorization: `Bearer "${localStorage.getItem('token')}"`,
          'Content-Type': 'multipart/form-data',
        },
      });
      navigate('/profile');
    } catch (error) {
      if (error.response && error.response.data) {
        const { data } = error.response;
        setErrorMessage('Failed to update user. Please try again later.');
        console.log(data);
      } else {
        console.error('An unexpected error occurred:', error);
      }
    }
  };

  return (
    <div className="user-update-form">
        <Sidebar />
      <h2>Update User Information</h2>
      {errorMessage && <p className="error-message">{errorMessage}</p>}
      <form onSubmit={handleSubmit}>
        <label>
          Old Password:
          <input
            type="password"
            name="old_password"
            value={formData.old_password}
            onChange={handleChange}
          />
        </label>
        <label>
          New Password:
          <input
            type="password"
            name="new_password"
            value={formData.new_password}
            onChange={handleChange}
          />
        </label>
        <label>
          Repeat Password:
          <input
            type="password"
            name="repeat_password"
            value={formData.repeat_password}
            onChange={handleChange}
          />
        </label>
        <label>
          Email:
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
          />
        </label>
        <label>
          First Name:
          <input
            type="text"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
          />
        </label>
        <label>
          Last Name:
          <input
            type="text"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
          />
        </label>
        <label>
          Phone Number:
          <input
            type="text"
            name="phone_number"
            value={formData.phone_number}
            onChange={handleChange}
          />
        </label>
        <label>
          Two Factor Method:
          <select
            name="two_factor_method"
            value={formData.two_factor_method}
            onChange={handleChange}
          >
            <option value="">--Please choose an option--</option>
            <option value="email">Email</option>
            <option value="sms">SMS</option>
          </select>
        </label>
        <label>
          Title:
          <select
            name="title"
            value={formData.title}
            onChange={handleChange}
          >
            <option value="">--Please choose an option--</option>
            <option value="Mr">Mr</option>
            <option value="Mrs">Mrs</option>
            <option value="Miss">Miss</option>
            <option value="Ms">Ms</option>
            <option value="Dr">Dr</option>
            <option value="Prof">Prof</option>
          </select>
        </label>
        <label>
          Gender:
          <select
            name="gender"
            value={formData.gender}
            onChange={handleChange}
          >
            <option value="">--Please choose an option--</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
        </label>
        <label>
          Address:
          <input
            type="text"
            name="address"
            value={formData.address}
            onChange={handleChange}
          />
        </label>
        <label>
          Photo Selfie:
          <input
            type="file"
            name="photo_selfie"
            onChange={handleFileChange}
          />
        </label>
        <label>
          Identity Document:
          <input
            type="file"
            name="identity_document"
            onChange={handleFileChange}
          />
        </label>
        <button className="form-submit" type="submit">
          Update User
        </button>
      </form>
    </div>
  );
}

export default UserUpdatePage;
