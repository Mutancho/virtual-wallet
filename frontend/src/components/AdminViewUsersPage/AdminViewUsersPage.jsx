import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Sidebar from '../SideBar/SideBar';
import './AdminViewUsersPage.css';
import {API_BASE_URL} from "../../config";

function AdminViewUsersPage() {
  const [users, setUsers] = useState([]);
  const [usernameSearchTerm, setUsernameSearchTerm] = useState('');
  const [emailSearchTerm, setEmailSearchTerm] = useState('');
  const [phoneSearchTerm, setPhoneSearchTerm] = useState('');
  const [limit, setLimit] = useState(10);
  const [offset, setOffset] = useState(0);

  useEffect(() => {
    fetchUsers();
  }, [limit, offset]);

  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_BASE_URL}users`, {
        params: {
          username: usernameSearchTerm,
          email: emailSearchTerm,
          phone: phoneSearchTerm,
          limit: Math.abs(limit),
          offset: Math.abs(offset),
        },
        headers: {
          Authorization: `Bearer "${token}"`,
        },
      });
      setUsers(response.data);
    } catch (error) {
      console.error('Failed to fetch users:', error);
    }
  };

  const handleUsernameSearchTermChange = (event) => {
    setUsernameSearchTerm(event.target.value);
  };

  const handleEmailSearchTermChange = (event) => {
    setEmailSearchTerm(event.target.value);
  };

  const handlePhoneSearchTermChange = (event) => {
    setPhoneSearchTerm(event.target.value);
  };

  const handleLimitChange = (event) => {
    setLimit(parseInt(event.target.value, 10));
  };

  const handleOffsetChange = (event) => {
    setOffset(parseInt(event.target.value, 10));
  };

  const handleSearch = () => {
    fetchUsers();
  };

  return (
    <div className="admin-view-users-page">
      <Sidebar />
      <div className="admin-view-users-content">
        <h2>Admin View Users</h2>
        <div className="search-bar">
          <input
            type="text"
            id="username"
            value={usernameSearchTerm}
            onChange={handleUsernameSearchTermChange}
            placeholder="Search by username"
          />
          <input
            type="text"
            id="email"
            value={emailSearchTerm}
            onChange={handleEmailSearchTermChange}
            placeholder="Search by email"
          />
          <input
            type="text"
            id="phone"
            value={phoneSearchTerm}
            onChange={handlePhoneSearchTermChange}
            placeholder="Search by phone number"
          />
          <button className="submit-button" onClick={handleSearch}>
            Search
          </button>
        </div>
        <div className="pagination-controls">
          <label htmlFor="limit">
            Limit:
            <input
              type="number"
              id="limit"
              value={limit}
              onChange={handleLimitChange}
              min={0}
            />
          </label>
          <label htmlFor="offset">
            Offset:
            <input
              type="number"
              id="offset"
              value={offset}
              onChange={handleOffsetChange}
              min={0}
            />
          </label>
        </div>
        <div className="user-list-wrapper">
          <ul className="user-list">
            {users.map((user) => (
              <li key={user.id}>
                <div>
                  <strong>Username:</strong> {user.username}
                </div>
                <div>
                  <strong>Email:</strong> {user.email}
                </div>
                <div>
                  <strong>Phone Number:</strong> {user.phone_number}
                </div>
                <div>
                  <strong>First Name:</strong> {user.first_name}
                </div>
                <div>
                  <strong>Last Name:</strong> {user.last_name}
                </div>
                <div>
                  <strong>Address:</strong> {user.address}
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default AdminViewUsersPage;
