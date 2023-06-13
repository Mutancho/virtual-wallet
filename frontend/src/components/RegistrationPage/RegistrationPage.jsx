import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import './RegistrationPage.css';

function RegistrationPage() {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    email: '',
    first_name: '',
    last_name: '',
    phone_number: '',
    // two_factor_method: '',
    title: '',
    gender: '',
    date_of_birth: '',
    address: '',
    photo_selfie: null,
    identity_document: null,
    referral_id: null,
  });
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();
  const { referralId } = useParams();

  useEffect(() => {
    if (referralId) {
      setFormData((prevState) => ({ ...prevState, referral_id: referralId }));
    }
  }, [referralId]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onloadend = () => {
      setFormData({
        ...formData,
        [e.target.name]: reader.result,
      });
    };

    reader.readAsDataURL(file);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const currentDate = new Date();
    const selectedDate = new Date(formData.date_of_birth);
    const age = currentDate.getFullYear() - selectedDate.getFullYear();

    if (age < 18) {
      setErrorMessage('You must be at least 18 years old to register.');
      return;
    }

    const data = new FormData();
    Object.entries(formData).forEach(([key, value]) => {
      if (value instanceof File) {
        data.append(key, value, value.name);
      } else {
        data.append(key, value);
      }
    });

    try {
      const response = await axios.post('/users/registrations', data, {
        params: {
          referral_id: formData.referral_id,
        },
        headers: {
          'Content-Type': 'application/json',
        },
      });
      navigate('/verify-email');
    } catch (error) {
      if (error.response && error.response.data) {
        const { data } = error.response;
        setErrorMessage('Failed to register. Please try again later.');
        console.log(data);
      } else {
        console.error('An unexpected error occurred:', error);
      }
    }
  };

  return (
    <div className="registration-form">
      <h2>Create Your E-Wallet Account</h2>
      {errorMessage && <p className="error-message">{errorMessage}</p>}
      <form onSubmit={handleSubmit}>
        <label>
          Username:<span className="required">*</span>
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Password:<span className="required">*</span>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Email:<span className="required">*</span>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          First Name:<span className="required">*</span>
          <input
            type="text"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Last Name:<span className="required">*</span>
          <input
            type="text"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Phone Number:<span className="required">*</span>
          <input
            type="text"
            name="phone_number"
            value={formData.phone_number}
            onChange={handleChange}
            required
          />
        </label>
        {/* <label className="form-label">
          Two Factor Method:<span className="required">*</span>
          <div className="radio-group">
            <div className="radio-option">
              <input
                type="radio"
                id="twoFactorMethodEmail"
                name="two_factor_method"
                value="email"
                onChange={handleChange}
                checked={formData.two_factor_method === 'email'}
              />
              <label htmlFor="twoFactorMethodEmail">Email</label>
            </div>
            <div className="radio-option">
              <input
                type="radio"
                id="twoFactorMethodSms"
                name="two_factor_method"
                value="sms"
                onChange={handleChange}
                checked={formData.two_factor_method === 'sms'}
              />
              <label htmlFor="twoFactorMethodSms">SMS</label>
            </div> */}
          {/* </div>
        </label> */}
        <label className="form-label">
          Gender:<span className="required">*</span>
          <div className="radio-group">
            <div className="radio-option">
              <input
                type="radio"
                id="genderMale"
                name="gender"
                value="male"
                onChange={handleChange}
                checked={formData.gender === 'male'}
              />
              <label htmlFor="genderMale">Male</label>
            </div>
            <div className="radio-option">
              <input
                type="radio"
                id="genderFemale"
                name="gender"
                value="female"
                onChange={handleChange}
                checked={formData.gender === 'female'}
              />
              <label htmlFor="genderFemale">Female</label>
            </div>
            <div className="radio-option">
              <input
                type="radio"
                id="genderOther"
                name="gender"
                value="other"
                onChange={handleChange}
                checked={formData.gender === 'other'}
              />
              <label htmlFor="genderOther">Other</label>
            </div>
          </div>
        </label>
        <label>
          Title:<span className="required">*</span>
          <select
            name="title"
            value={formData.title}
            onChange={handleChange}
            className="form-select"
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
          Date of Birth:<span className="required">*</span>
          <input
            type="date"
            name="date_of_birth"
            value={formData.date_of_birth}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Address:<span className="required">*</span>
          <input
            type="text"
            name="address"
            value={formData.address}
            onChange={handleChange}
            required
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
            required
          />
        </label>
        <button className="form-submit" type="submit">
          Register
        </button>
      </form>
    </div>
  );
}

export default RegistrationPage;
