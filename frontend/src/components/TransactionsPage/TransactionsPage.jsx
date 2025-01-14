import React, { useState } from 'react';
import axios from 'axios';
import Sidebar from '../SideBar/SideBar';
import { json, useLocation } from 'react-router-dom';
import './TransactionsPage.css'; 
import alertify from 'alertifyjs';
import 'alertifyjs/build/css/alertify.css';
import { API_BASE_URL } from '../../config';

const TransactionsPage = () => {
  const [activeTab, setActiveTab] = useState('contacts');
  const [showSendMoneyConfirmation, setShowSendMoneyConfirmation] = useState(false);
  const [searchResult, setSearchResult] = useState(null);
  const [searchParams, setSearchParams] = useState({ username: null });
  const categories = [
    'Rent',
    'Utilities',
    'Food & Groceries',
    'Transportation',
    'Health & Fitness',
    'Shopping & Entertainment',
    'Travel',
    'Education',
    'Personal Care',
    'Investments & Savings',
    'Other',
  ];
  const [recipients, setRecipients] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedRecipient, setSelectedRecipient] = useState('');
  const [transactionAmount, setTransactionAmount] = useState('');
  const location = useLocation();
  const [isLoading, setIsLoading] = useState(false);


  const [isRecurring, setIsRecurring] = useState(false);
  const [recurringTransaction, setRecurringTransaction] = useState({
    startDate: undefined,
    interval: undefined,
  });

  const fetchContacts = async () => {
    setActiveTab('contacts');
    try {
      const response = await axios.get(`${API_BASE_URL}contacts`, {
        headers: {
          Authorization: `Bearer "${localStorage.getItem('token')}"`,
          'Content-Type': 'application/json',
        },
      });
      setRecipients(response.data);
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleSearch = async () => {
    setActiveTab('search');
    try {
      const response = await axios.get(`${API_BASE_URL}users/searches`, {
        params: searchParams,
        headers: {
          Authorization: `Bearer "${localStorage.getItem('token')}"`,
        },
      });
      const user = response.data;
      if (user && user.username) {
        setSearchResult(user.username);
      } else {
        setSearchResult(null);
        console.log('No user found.');
      }
    } catch (error) {
      console.error('Error searching users:', error);
    }
  };

  const handleSendMoney = async () => {

    setIsLoading(true);

    if (transactionAmount > 10000) {
      const confirmation = window.confirm(
        "Your transaction amount exceeds $10,000. For your security, we have sent a confirmation link to your registered email address. Please check your email and click the link to authorize this transaction."
      );
      if (!confirmation) {
        return;
      }
    }
    try {
      const transactionData = {
        amount: transactionAmount,
        category: selectedCategory,
        recipient: selectedRecipient,
        wallet: location.state.walletId,
        is_recurring: isRecurring,
        recurring_transaction: isRecurring ? recurringTransaction : null,
        interval: recurringTransaction.interval,
        start_date: recurringTransaction.startDate
      };
  
      const response = await axios.post(`${API_BASE_URL}transactions`, transactionData, {
        headers: {
          Authorization: `Bearer "${localStorage.getItem('token')}"`,
        },
      });
      alertify.alert('Money sent successfully!', function(){
        alertify.success('Ok');
        window.location.reload();
      });
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }finally {
      setIsLoading(false);
    }
  };
  

  const handleRecipientSelection = (username) => {
    setSelectedRecipient(username);
    console.log(`Recipient set as: ${username}`);
  };

  const handleRecurringOptionChange = (e) => {
    setIsRecurring(e.target.checked);
  };

  const handleRecurringDataChange = (field, value) => {
    setRecurringTransaction((prevData) => ({
      ...prevData,
      [field]: value,
    }));
  };

  return (
    <div className="transactions-page">
      <Sidebar />
      <div className="transaction-box">
        <h3>Make a Transaction</h3>
        <div className="transaction-form">
          <div className="form-group">
            <label htmlFor="amount">Amount:</label>
            <input
              type="number"
              id="amount"
              value={transactionAmount}
              onChange={(e) => {
                const amount = Number(e.target.value);
                setTransactionAmount(amount !== 0 ? amount : '');
              }}
              min={0}
            />
          </div>
          <div className="form-group">
            <label htmlFor="category">Category:</label>
            <select
              id="category"
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
            >
              <option value="">Select Category</option>
              {categories.map((category, index) => (
                <option key={index} value={category}>
                  {category}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Recipient:</label>
            <div className="recipient-options">
              <div className="option-tabs">
                <button
                  className={`tab-button ${activeTab === 'contacts' ? 'active' : ''}`}
                  onClick={fetchContacts}
                >
                  Contacts
                </button>
                <button
                  className={`tab-button ${activeTab === 'search' ? 'active' : ''}`}
                  onClick={handleSearch}
                >
                  Search Users
                </button>
              </div>
              {activeTab === 'contacts' && recipients.length > 0 && (
                <select
                  id="recipient-contacts"
                  value={selectedRecipient}
                  onChange={(e) => setSelectedRecipient(e.target.value)}
                >
                  <option value="">Select Recipient from Contacts</option>
                  {recipients.map((recipient) => (
                    <option key={recipient.username}>{recipient.username}</option>
                  ))}
                </select>
              )}
              {activeTab === 'search' && (
                <div>
                  <input
                    type="text"
                    placeholder="Search for App Users"
                    className={`search-input ${selectedRecipient ? 'user-found' : 'user-not-found'}`}
                    onChange={(e) =>
                      setSearchParams((prevParams) => ({
                        ...prevParams,
                        username: e.target.value,
                      }))
                    }
                  />
                  {searchResult && (
                    <div>
                      <p>Search Result: {searchResult}</p>
                      <button
                        className="select-button"
                        onClick={() => handleRecipientSelection(searchResult)}
                      >
                        Select
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
            {selectedRecipient && <p>Recipient set as: {selectedRecipient}</p>}
          </div>
          <div className="form-group">
            <div className="recurring-transaction-option">
              <input
                type="checkbox"
                id="recurring-option"
                checked={isRecurring}
                onChange={handleRecurringOptionChange}
              />
              <label htmlFor="recurring-option">Enable recurring transaction</label>
            </div>
          </div>
          {isRecurring && (
            <div className="recurring-transaction-section">
              <div className="form-group">
                <label htmlFor="start-date">Start Date:</label>
                <input
                  type="date"
                  id="start-date"
                  value={recurringTransaction.startDate}
                  onChange={(e) => handleRecurringDataChange('startDate', e.target.value)}
                />
              </div>
              <div className="form-group">
                <label htmlFor="interval">Interval (in days):</label>
                <input
                  type="number"
                  id="interval"
                  value={recurringTransaction.interval}
                  onChange={(e) => handleRecurringDataChange('interval', e.target.value)}
                  min={1}
                  max={1000}
                />
              </div>
            </div>
          )}
        </div>
          <button
            className="send-money"
            type="button"
            onClick={() => setShowSendMoneyConfirmation(true)}
          >
            Send Money
          </button>

      {showSendMoneyConfirmation && (
        <div className="send-money-confirmation">
          <div className="confirmation-text">Are you sure you want to finish this transaction?</div>
          <div className="confirmation-buttons">
            <button className="confirmation-button" onClick={handleSendMoney} disabled={isLoading}>{isLoading ? 'Sending...' : 'Yes'}</button>
            <button className="confirmation-button" onClick={() => setShowSendMoneyConfirmation(false)}>No</button>
          </div>
      </div>
          )}
    </div>
      </div>
  );
};

export default TransactionsPage;
