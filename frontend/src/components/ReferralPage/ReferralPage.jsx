import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Sidebar from '../SideBar/SideBar';
import './ReferralPage.css';

const ReferralPage = () => {
  const [referrals, setReferrals] = useState([]);
  const [newEmail, setNewEmail] = useState('');
  const [createReferralError, setCreateReferralError] = useState('');

  const fetchReferrals = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/users/referrals', {
        headers: {
          Authorization: `Bearer "${token}"`,
        },
      });
      setReferrals(response.data);
    } catch (error) {
      console.error('Error fetching referrals:', error);
    }
  };

  const copyToClipboard = (referralLink) => {
    navigator.clipboard.writeText(referralLink);
  };

  useEffect(() => {
    fetchReferrals();
  }, []);

  const handleCreateReferral = async () => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(
        '/users/referrals',
        { email: newEmail },
        {
          headers: {
            Authorization: `Bearer "${token}"`,
          },
        }
      );
      fetchReferrals();
      setNewEmail('');
      setCreateReferralError('');
    } catch (error) {
      console.error('Error creating referral:', error);
      setCreateReferralError('Failed to create referral. Please try again.');
    }
  };

  return (
    <div className="referral-page-container">
      <Sidebar />
      <div className="referral-container">
        <h1 className="referral-page-title">Referrals</h1>
        <div className="referral-input">
          <input
            type="text"
            placeholder="Enter email"
            value={newEmail}
            onChange={(e) => setNewEmail(e.target.value)}
          />
          <button onClick={handleCreateReferral}>Create Referral</button>
        </div>
        {createReferralError && <p className="referral-error">{createReferralError}</p>}
        <div className="referral-list">
          <div className="referral-legend">
            <div className="legend-item">
              <span className="status-indicator green"></span> - Used referral
            </div>
            <div className="legend-item">
              <span className="status-indicator red"></span> - Unused referral
            </div>
          </div>
          {referrals.map((referral) => (
            <div className="referral-item" key={referral.email}>
              <span className={`status-indicator ${referral.is_used ? 'green' : 'red'}`}></span>
              <div className="referral-email-container">
                <span className="referral-email">{referral.email}</span>
              </div>
              <button className="copy-button" onClick={() => copyToClipboard(referral.link)}>Copy</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ReferralPage;
