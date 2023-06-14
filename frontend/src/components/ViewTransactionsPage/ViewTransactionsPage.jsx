import React, { useState } from 'react';
import axios from 'axios';
import Sidebar from '../SideBar/SideBar';

const ViewTransactionsPage = () => {
  const [fromDate, setFromDate] = useState(undefined);
  const [toDate, setToDate] = useState(undefined);
  const [user, setUser] = useState(undefined);
  const [direction, setDirection] = useState(undefined);
  const [limit, setLimit] = useState('' | 10);
  const [offset, setOffset] = useState('' | 0);
  const [sort, setSort] = useState(undefined);
  const [sortBy, setSortBy] = useState(undefined);
  const [transactions, setTransactions] = useState([]);

  const handleSearch = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/transactions/searches', {
        params: {
          from_date: fromDate,
          to_date: toDate,
          user: user,
          direction: direction,
          limit: limit,
          offset: offset,
          sort: sort,
          sort_by: sortBy,
        },
        headers: {
          Authorization: `Bearer "${token}"`,
        },
      });

      setTransactions(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="container">
      <Sidebar />
      <h1>View Transactions</h1>
      <div className="form-group">
        <label htmlFor="fromDate">From Date</label>
        <input
          type="date"
          id="fromDate"
          value={fromDate}
          onChange={(e) => setFromDate(e.target.value)}
          className="input-large"
        />
      </div>
      <div className="form-group">
        <label htmlFor="toDate">To Date</label>
        <input
          type="date"
          id="toDate"
          value={toDate}
          onChange={(e) => setToDate(e.target.value)}
          className="input-large"
        />
      </div>
      <div className="form-group">
        <label htmlFor="user">User</label>
        <input
          type="text"
          id="user"
          value={user}
          onChange={(e) => setUser(e.target.value)}
          className="input-large"
        />
      </div>
      <div className="form-group">
  <label htmlFor="direction">Direction</label>
  <select id="direction" value={direction} onChange={(e) => setDirection(e.target.value)}>
    <option value="">Select</option>
    <option value="incoming">Incoming</option>
    <option value="outgoing">Outgoing</option>
  </select>
</div>


      <div className="form-group">
        <label htmlFor="limit">Limit</label>
        <input
          type="number"
          id="limit"
          value={limit}
          onChange={(e) => setLimit(e.target.value)}
          min={0}
        />
      </div>
      <div className="form-group">
        <label htmlFor="offset">Offset</label>
        <input
          type="number"
          id="offset"
          value={offset}
          onChange={(e) => setOffset(e.target.value)}
          min={0}
        />
      </div>
      <div className="form-group">
        <label htmlFor="sort">Sort</label>
        <select id="sort" value={sort} onChange={(e) => setSort(e.target.value)}>
          <option value="">Select</option>
          <option value="ASC">ASC</option>
          <option value="DESC">DESC</option>
        </select>
      </div>
      <div className="form-group">
        <label htmlFor="sortBy">Sort By</label>
        <select id="sortBy" value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          <option value="">Select</option>
          <option value="amount">Amount</option>
          <option value="sent_at">Sent At</option>
          <option value="received_at">Received At</option>
        </select>
      </div>
      <button className="btn" onClick={handleSearch}>
        Search
      </button>
      <div className="transaction-list">
        <ul>
          {transactions.map((transaction) => (
            <li key={transaction.id}>
              <div>
                <strong>Amount:</strong> {transaction.amount} {transaction.currency}
              </div>
              <div>
                <strong>Category:</strong> {transaction.category}
              </div>
              <div>
                <strong>Recipient:</strong> {transaction.recipient}
              </div>
              <div>
                <strong>Sender:</strong> {transaction.wallet}
              </div>
              <div>
                <strong>Recurring:</strong> {transaction.is_recurring ? 'Yes' : 'No'}
              </div>
              <div>
                <strong>Sent_at:</strong> {transaction.sent_at}
              </div>
              <div>
                <strong>Accepted:</strong> {transaction.accepted ? 'Yes' : 'No'}
              </div>
              <div>
                <strong>Received_at:</strong> {transaction.received_at ? transaction.received_at : 'Outstanding'}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ViewTransactionsPage;
