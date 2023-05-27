import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Sidebar from '../SideBar/SideBar';
import { useLocation } from 'react-router-dom';

const TransactionsPage = () => {
  const [searchParams, setSearchParams] = useState({
    from_date: null,
    to_date: null,
    user: null,
    direction: null,
    limit: null,
    offset: null,
    sort: null,
    sort_by: null,
  });
  const [userSearchParams, setUserSearchParams] = useState({
    username: null
  });
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
  const [transactionAmount, setTransactionAmount] = useState(0); // Added missing declaration

  const fetchContacts = async () => {
    try {
      const response = await axios.get('/contacts', {
        headers: {
          Authorization: `Bearer "${localStorage.getItem('token')}"`,
        },
      });
      // Set the recipients state with the fetched contacts
      setRecipients(response.data);
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleSearch = async () => {
    try {
      const response = await axios.get('/users/search', {
        params: searchParams,
        headers: {
          Authorization: `Bearer "${localStorage.getItem('token')}"`,
        },
      });

      // Extract usernames from the response data
      const usernames = Object.values(response.data);

      // Check if the usernames array is not empty
      if (Array.isArray(usernames) && usernames.length > 0) {
        setRecipients(usernames);
      } else {
        // Show a message indicating no user found
        setRecipients([]);
        console.log('No user found.');
      }
    } catch (error) {
      console.error('Error searching users:', error);
    }
  };

  const handleSendMoney = async () => {
    const location = useLocation();
    try {
      const transactionData = {
        amount: transactionAmount,
        category: selectedCategory,
        recipient: selectedRecipient,
        wallet: location.state.walletId, // Example wallet (replace with the actual wallet ID)
        is_recurring: false, // Example recurring
      };

      const response = await axios.post('/transactions', transactionData, {
        headers: {
          Authorization: `Bearer "${localStorage.getItem('token')}"`,
        },
      });
      // Handle the response data
      console.log(response.data);
    } catch (error) {
      // Handle errors
      console.error(error);
    }
  };

  const handleRecipientSelection = (username) => {
    setSelectedRecipient(username);
    console.log(`Recipient set as: ${username}`);
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
              onChange={(e) => setTransactionAmount(Number(e.target.value))}
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
              <div className="contacts-option">
                <button className="contacts-button" onClick={fetchContacts}>
                  Contacts
                </button>
                {recipients.length > 0 && (
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
              </div>
              <span className="or-divider">or</span>
              <div className="search-option">
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
                <button className="search-button" onClick={handleSearch}>
                  Search
                </button>
                {selectedRecipient && (
                  <button className="select-button" onClick={() => handleRecipientSelection(selectedRecipient)}>
                    Select
                  </button>
                )}
              </div>
            </div>
            {selectedRecipient && <p>Recipient set as: {selectedRecipient}</p>}
          </div>
        </div>
        <button className="send-money" onClick={handleSendMoney}>
          Send Money
        </button>
      </div>
    </div>
  );
};

export default TransactionsPage;
