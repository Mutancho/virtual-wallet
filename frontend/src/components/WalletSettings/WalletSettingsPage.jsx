import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import './WalletSettingsPage.css';
import Sidebar from '../SideBar/SideBar';
import { API_BASE_URL } from '../../config';

const WalletSettingsPage = () => {
  const { state } = useLocation();
  const { walletId } = state;
  const { type } = state;

  const [name, setName] = useState('');
  const [status, setStatus] = useState('');
  const [username, setUsername] = useState('');
  const [action, setAction] = useState('');
  const [userAccess, setUserAccess] = useState('');
  const [defaultWallet, setDefaultWallet] = useState(false);
  const [members, setMembers] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchWalletData();
    fetchMembers();
  }, [walletId]);

  const fetchWalletData = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}users/wallets/${walletId}`, {
        headers: {
          'Authorization': `Bearer "${localStorage.getItem('token')}"`,
        },
      });

      if (response.status === 200) {
        setName(response.data.name);
        setStatus(response.data.is_active ? 'active' : 'inactive');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const fetchMembers = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}users/wallets/${walletId}`, {
        headers: {
          'Authorization': `Bearer "${localStorage.getItem('token')}"`,
        },
      });

      if (response.status === 200) {
        const wallet = response.data;
        setMembers(wallet.members);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    const requestBody = {
      name: name || undefined,
      status: status === 'active' ? true : status === 'inactive' ? false : undefined,
      add_username: action === 'add_username' ? username : undefined,
      remove_username: action === 'remove_username' ? username : undefined,
      username: username || undefined,
      change_user_access: action === 'change_user_access' ? userAccess : undefined
    };

    try {
      const response = await axios.put(`${API_BASE_URL}users/wallets/${walletId}/settings`, requestBody, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer "${localStorage.getItem('token')}"`,
        },
      });

      if (response.status === 200) {
        console.log('Settings updated successfully.');
        alert("Instructions was successful")
        fetchWalletData();
        fetchMembers();
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleDefaultWallet = async () => {
    try {
      const response = await axios.patch(`${API_BASE_URL}users/wallets/${walletId}`, {}, {
        headers: {
          'Authorization': `Bearer "${localStorage.getItem('token')}"`,
        },
      });

      if (response.status === 200) {
        setDefaultWallet(true);
        alert('Default wallet set successfully.');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleDeleteWallet = async () => {
    const confirmDelete = window.confirm('Are you sure you want to delete this wallet?');
    if (confirmDelete) {
      try {
        const response = await axios.delete(`${API_BASE_URL}users/wallets/${walletId}`, {
          headers: {
            'Authorization': `Bearer "${localStorage.getItem('token')}"`,
          },
        });

        if (response.status === 204) {
          console.log('Wallet deleted successfully.');
          navigate('/users/menu');
        }
      } catch (error) {
        console.error('Error:', error);
        alert("Empty wallet before deleting!")
      }
    }
  };
  const accessLevelMapping = {
    "null": "View Only",
    "top_up_only": "Top Up Only",
    "full": "Full Access"
  };

  const isJointWallet = type !== 'Personal';

  return (
    <section id="wallet-settings-page" className="wallet-settings-page">
    <div id="wallet-settings-page" className="wallet-settings-page">
      <Sidebar />
      <h1 id="wallet-settings-title">Wallet Settings</h1>

      <form id="wallet-settings-form" onSubmit={handleFormSubmit}>

        {type !== 'Personal' && (
          <React.Fragment>
            
            <label>
              Wallet Status:
              <select value={status} onChange={(e) => setStatus(e.target.value)}>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
            </label>
            <div className="members-section">
            <h2>MEMBERS</h2>
            <table id="members-table">
                <thead>
                <tr>
                    <th>Username</th>
                    <th>Access Level</th>
                </tr>
                </thead>
                <tbody>
                {members.map((member, index) => (
                    <tr key={index}>
                    <td>{member.name}</td>
                    <td>{accessLevelMapping[member.access_level]}</td>
                    </tr>
                ))}
                </tbody>
            </table>
            </div>

            <label>
              Username:
              <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
            </label>
            <label>
              Action:
              <select value={action} onChange={(e) => setAction(e.target.value)}>
                <option value="">Select an action</option>
                <option value="add_username">Add user</option>
                <option value="remove_username">Remove user</option>
                <option value="change_user_access">Change user access</option>
              </select>
            </label>
            {action === 'change_user_access' && (
              <label>
                User Access:
                <select value={userAccess} onChange={(e) => setUserAccess(e.target.value)}>
                  <option value="">Select user access</option>
                  <option value="null">View Only</option>
                  <option value="top_up_only">Top Up Only</option>
                  <option value="full">Full</option>
                </select>
              </label>
            )}
          </React.Fragment>
        )}
        {isJointWallet && (
          <button id="wallet-settings-submit" type="submit">Confirm Instruction</button>
        )}
      </form>
      <button id="wallet-set-default" onClick={handleDefaultWallet}>Set as Default Wallet</button>
      <button id="wallet-delete" onClick={handleDeleteWallet}>Delete Wallet</button>
    </div>
    </section>
  );
};

export default WalletSettingsPage;
