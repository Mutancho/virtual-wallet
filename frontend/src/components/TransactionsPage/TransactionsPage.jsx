import React, { useState } from 'react';
import axios from 'axios';

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

  const handleSearch = async () => {
    try {
      const response = await axios.get('/api/transactions/search', {
        params: searchParams,
        headers: {
          Authorization: 'YourAuthorizationToken',
        },
      });
      // Handle the response data
      console.log(response.data);
    } catch (error) {
      // Handle errors
      console.error(error);
    }
  };

  const handleSendMoney = async () => {
    try {
      const transactionData = {
        amount: 100, // Example amount
        category: 'Rent', // Example category
        recipient: 123, // Example recipient
        wallet: 456, // Example wallet
        is_recurring: false, // Example recurring
      };

      const response = await axios.post('/api/transactions', transactionData, {
        headers: {
          Authorization: 'YourAuthorizationToken',
        },
      });
      // Handle the response data
      console.log(response.data);
    } catch (error) {
      // Handle errors
      console.error(error);
    }
  };

  return (
    <div className="transactions-page">
      <div className="search-box">
        <input
          type="text"
          placeholder="From Date"
          onChange={(e) =>
            setSearchParams((prevParams) => ({
              ...prevParams,
              from_date: e.target.value,
            }))
          }
        />
        <input
          type="text"
          placeholder="To Date"
          onChange={(e) =>
            setSearchParams((prevParams) => ({
              ...prevParams,
              to_date: e.target.value,
            }))
          }
        />
        <input
          type="text"
          placeholder="User"
          onChange={(e) =>
            setSearchParams((prevParams) => ({
              ...prevParams,
              user: e.target.value,
            }))
          }
        />
        {/* Add more search parameters as needed */}
        <button onClick={handleSearch}>Search</button>
      </div>

      {/* Display the transaction listing */}
      <div className="transaction-list">
        {/* Iterate over the transactions and display them */}
        {/* Example transaction rendering */}
        <div className="transaction">
          <span>Transaction 1</span>
        </div>
        <div className="transaction">
          <span>Transaction 2</span>
        </div>
        {/* Add more transaction components dynamically */}
      </div>

      {/* Send money button */}
      <button className="send-money" onClick={handleSendMoney}>
        Send Money
      </button>
    </div>
  );
};

export default TransactionsPage;
