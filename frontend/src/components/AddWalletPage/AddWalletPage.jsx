import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './AddWalletPage.css'
import Sidebar from '../SideBar/SideBar';

const AddWalletPage = () => {
  const [name, setName] = useState('');
  const [type, setType] = useState('');
  const [currency, setCurrency] = useState('');
  const navigate = useNavigate();

  const handleFormSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      name,
      type,
      currency,
    };

    try {
      const response = await fetch('/users/wallets', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer "${localStorage.getItem('token')}"`,
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      alert("Wallet successfully created!");  // Notification about successful wallet creation.
      navigate('/users/menu'); // Redirect to /users/menu page

    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="add-wallet-page">
        <Sidebar></Sidebar>
      <h1>Create a new Wallet</h1>
      <form onSubmit={handleFormSubmit}>
        <label>
          Name:
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
        </label>
        <label>
          Type:
          <select value={type} onChange={(e) => setType(e.target.value)} required>
            <option value="">Select type</option>
            <option value="personal">Personal</option>
            <option value="joint">Joint</option>
          </select>
        </label>
        <label>
          Currency:
          <select value={currency} onChange={(e) => setCurrency(e.target.value)} required>
            <option value="">Select currency</option>
            <option value="USD">USD</option>
            <option value="EUR">EUR</option>
            <option value="GBP">GBP</option>
            <option value="JPY">JPY</option>
            <option value="CAD">CAD</option>
            <option value="AUD">AUD</option>
            <option value="TRY">TRY</option>
            <option value="BGN">BGN</option>
          </select>
        </label>
        <button type="submit">Create Wallet</button>
      </form>
    </div>
  );
};

export default AddWalletPage;
