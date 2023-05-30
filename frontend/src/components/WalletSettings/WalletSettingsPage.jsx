import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import './WalletSettingsPage.css';
import Sidebar from '../SideBar/SideBar';

const WalletSettingsPage = () => {
  const { id: walletId } = useParams(); 
  const [name, setName] = useState('');
  const [status, setStatus] = useState('');
  const [username, setUsername] = useState('');
  const [action, setAction] = useState('');
  const [userAccess, setUserAccess] = useState('');

  const handleFormSubmit = async (e) => {
    e.preventDefault();

    const payload = { name, status };

    if (username) {
      payload[action] = username;
      if (action === 'change_user_access') {
        payload[action] = userAccess;
      }
    }

    try {
      const response = await axios.put(`/users/wallets/${walletId}/settings`, payload, {
        headers: {
          'Authorization': `Bearer "${localStorage.getItem('token')}"`,
        },
      });

      if (response.status === 200) {
        console.log('Settings updated successfully.');
      }
    } catch (error) {
      if (error.response) {
        console.log('Error:', error.response.data);
        if (error.response.status === 401) {
          console.log('Unauthorized');
        } else if (error.response.status === 404) {
          console.log('Not found');
        } else {
          console.log('Unknown error');
        }
      } else {
        console.log('Error:', error);
      }
    }
  };

  return (
    <div className="wallet-settings-page">
        <Sidebar></Sidebar>
      <h1>Wallet Settings</h1>
      <form onSubmit={handleFormSubmit}>
        <label>
          New Wallet Name:
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
        </label>
        <label>
          Status:
          <select value={status} onChange={(e) => setStatus(e.target.value)}>
            <option value="">Select status</option>
            <option value="active">Activate</option>
            <option value="inactive">Deactivate</option>
          </select>
        </label>
        <label>
          Enter Username To Perform An Action:
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
        </label>
        <label>
          Action:
          <select value={action} onChange={(e) => setAction(e.target.value)}>
            <option value="">Select action</option>
            <option value="add_username">Add user</option>
            <option value="remove_username">Remove user</option>
            <option value="change_user_access">Change access</option>
          </select>
        </label>
        {action === 'change_user_access' && (
          <label>
            User Access:
            <select value={userAccess} onChange={(e) => setUserAccess(e.target.value)}>
              <option value="">Select access</option>
              <option value="null">Null</option>
              <option value="top_up_only">Top up only</option>
              <option value="full">Full</option>
            </select>
          </label>
        )}
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default WalletSettingsPage;
