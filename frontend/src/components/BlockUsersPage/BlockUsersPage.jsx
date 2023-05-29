import React, { useState } from 'react';
import axios from 'axios';
import Sidebar from "../SideBar/SideBar";

const BlockUsersPage = () => {
  const [userId, setUserId] = useState('');
  const [action, setAction] = useState('');

  const handleBlockUnblock = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(`/users/${userId}/blocks`, { action: action }, {
        headers: {
          Authorization: `Bearer "${token}"`,
        },
      });

      console.log(response.data); // Handle the response as needed
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="container">
        <Sidebar />
      <h1>Block Users</h1>
      <div className="form-group">
        <label htmlFor="userId">User ID</label>
        <input
          type="number"
          id="userId"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          min={0}
        />
      </div>
      <div className="form-group">
        <label htmlFor="action">Action</label>
        <select
          id="action"
          value={action}
          onChange={(e) => setAction(e.target.value)}
        >
          <option value="">Select an action</option>
          <option value="block">Block</option>
          <option value="unblock">Unblock</option>
        </select>
      </div>
      <button className="btn" onClick={handleBlockUnblock}>
        Submit
      </button>
    </div>
  );
};

export default BlockUsersPage;
