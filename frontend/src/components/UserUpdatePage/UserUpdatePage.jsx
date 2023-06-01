import React, { useState } from 'react';
import axios from 'axios';
import jwt_decode from 'jwt-decode';
import './UserUpdatePage.css';
import Sidebar from '../SideBar/SideBar';
import {useNavigate} from "react-router-dom";

function UpdateUser() {
  const [data, setData] = useState({});
  const [showDeleteConfirmation, setShowDeleteConfirmation] = useState(false);
  const navigate = useNavigate();

  const handleChange = e => {
    setData({
      ...data,
      [e.target.name]: e.target.value || null
    });
  };

  const handleChangeFile = e => {
    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onloadend = () => {
      setData({
        ...data,
        [e.target.name]: reader.result
      });
    };

    if (file) {
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async e => {
    e.preventDefault();

    try {
      const token = localStorage.getItem('token');
      const decoded = jwt_decode(token);
      const res = await axios.put(`/users/${decoded.user_id}`, data, {
        headers: {
          Authorization: `Bearer "${token}"`,
          'Content-Type': 'application/json',
        }
      });
      console.log(res.data);
      alert("Profile Successfully updated");
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async () => {
    try {
      const token = localStorage.getItem('token');
      const decoded = jwt_decode(token);
      await axios.delete(`/users/${decoded.user_id}`, {
        headers: {
          Authorization: `Bearer "${token}"`,
        }
      });
      // Perform any necessary clean-up or redirection after deleting the user
      navigate('/')
      console.log('User deleted');
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <form className="update-user-form" onSubmit={handleSubmit}>
        <Sidebar />
        <h2>Update Personal Info</h2>
        <input
          className="form-input"
          name="old_password"
          type="password"
          placeholder="Old password"
          onChange={handleChange}
        />
        <input
          className="form-input"
          name="new_password"
          type="password"
          placeholder="New password"
          onChange={handleChange}
        />
        <input
          className="form-input"
          name="repeat_password"
          type="password"
          placeholder="Repeat password"
          onChange={handleChange}
        />
        <input
          className="form-input"
          name="email"
          type="email"
          placeholder="Email"
          onChange={handleChange}
        />
        <input
          className="form-input"
          name="first_name"
          placeholder="First name"
          onChange={handleChange}
        />
        <input
          className="form-input"
          name="last_name"
          placeholder="Last name"
          onChange={handleChange}
        />
        <input
          className="form-input"
          name="phone_number"
          placeholder="Phone number"
          onChange={handleChange}
        />
        <select className="form-input" name="two_factor_method" onChange={handleChange}>
          <option value="">Select two-factor method</option>
          <option value="email">Email</option>
          <option value="sms">SMS</option>
        </select>
        <select className="form-input" name="title" onChange={handleChange}>
          <option value="">Select title</option>
          <option value="Mr">Mr</option>
          <option value="Mrs">Mrs</option>
          <option value="Miss">Miss</option>
          <option value="Ms">Ms</option>
          <option value="Dr">Dr</option>
          <option value="Prof">Prof</option>
        </select>
        <select className="form-input" name="gender" onChange={handleChange}>
          <option value="">Select gender</option>
          <option value="male">Male</option>
          <option value="female">Female</option>
          <option value="other">Other</option>
        </select>
        <input
          className="form-input"
          name="address"
          placeholder="Address"
          onChange={handleChange}
        />
        <label>
          Photo Selfie:
          <input
            className="form-file-input"
            name="photo_selfie"
            type="file"
            onChange={handleChangeFile}
          />
        </label>
        <label>
          Identity Document:
          <input
            className="form-file-input"
            name="identity_document"
            type="file"
            onChange={handleChangeFile}
          />
        </label>
        <button className="form-submit-button" type="submit">Update User</button>
        <div className="action-buttons">
          <button
            className="delete-button"
            type="button"
            onClick={() => setShowDeleteConfirmation(true)}
          >
            Delete Account
          </button>
        </div>
      </form>

      {showDeleteConfirmation && (
        <div className="delete-confirmation">
          <div className="confirmation-text">Are you sure you want to delete the user?</div>
          <div className="confirmation-buttons">
            <button className="confirmation-button" onClick={handleDelete}>Yes</button>
            <button className="confirmation-button" onClick={() => setShowDeleteConfirmation(false)}>No</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default UpdateUser;
