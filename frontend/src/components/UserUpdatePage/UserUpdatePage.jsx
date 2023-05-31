import React, { useState } from 'react';
import axios from 'axios';
import jwt_decode from 'jwt-decode';
import './UserUpdatePage.css';
import Sidebar from '../SideBar/SideBar';

function UpdateUser() {
    const [data, setData] = useState({});

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
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <Sidebar/>
            <h2>Update Personal Info</h2>
            <input name="old_password" type="password" placeholder="Old password" onChange={handleChange} />
            <input name="new_password" type="password" placeholder="New password" onChange={handleChange} />
            <input name="repeat_password" type="password" placeholder="Repeat password" onChange={handleChange} />
            <input name="email" type="email" placeholder="Email" onChange={handleChange} />
            <input name="first_name" placeholder="First name" onChange={handleChange} />
            <input name="last_name" placeholder="Last name" onChange={handleChange} />
            <input name="phone_number" placeholder="Phone number" onChange={handleChange} />
            <select name="two_factor_method" onChange={handleChange}>
                <option value="">Select two-factor method</option>
                <option value="email">Email</option>
                <option value="sms">SMS</option>
            </select>
            <select name="title" onChange={handleChange}>
                <option value="">Select title</option>
                <option value="Mr">Mr</option>
                <option value="Mrs">Mrs</option>
                <option value="Miss">Miss</option>
                <option value="Ms">Ms</option>
                <option value="Dr">Dr</option>
                <option value="Prof">Prof</option>
            </select>
            <select name="gender" onChange={handleChange}>
                <option value="">Select gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
            </select>
            <input name="address" placeholder="Address" onChange={handleChange} />
            <label>
                Photo Selfie:
                <input name="photo_selfie" type="file" onChange={handleChangeFile} />
            </label>
            <label>
                Identity Document:
                <input name="identity_document" type="file" onChange={handleChangeFile} />
            </label>
            <button type="submit">Update User</button>
        </form>
    );
}

export default UpdateUser;
