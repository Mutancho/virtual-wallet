import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import './SideBar.css';
import axios from 'axios';


const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = async () => {
    try {
      const token = localStorage.getItem('token');
      await axios.post('/users/logout', null, {
        headers: {
          Authorization: `Bearer "${token}"`
        }
      });
      localStorage.removeItem('token');
      localStorage.removeItem('is_admin');
      navigate('/');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2 className="sidebar-title">Virtual Wallet</h2>
      </div>
      <ul className="sidebar-menu">
        {location.pathname !== '/users/menu' && (
          <li className="sidebar-menu-item">
            <Link to="/users/menu" className="sidebar-link">
              Wallets
            </Link>
          </li>
        )}
        {location.pathname !== '/contacts' && (
        <li className="sidebar-menu-item">
          <Link to="/contacts" className="sidebar-link">
            Contacts
          </Link>
        </li>
        )}
        {location.pathname !== '/users/update' && (
        <li className="sidebar-menu-item">
          <Link to="/users/update" className="sidebar-link">
            Update Profile
          </Link>
        </li>
        )}
        {location.pathname !== '/users/payment-cards' && (
          <li className="sidebar-menu-item">
            <Link to="/users/payment-cards" className="sidebar-link">
              Manage Cards
            </Link>
          </li>
        )}
        {localStorage.getItem('is_admin') !== 'false' && location.pathname !== '/users/admin/view' && (
        <li className="sidebar-menu-item">
          <Link to='/users/admin/view' className="sidebar-link">
            Admin View Users
          </Link>
        </li>
        )}
        {localStorage.getItem('is_admin') !== 'false' && location.pathname !== '/transactions/admin/view' && (
        <li className="sidebar-menu-item">
          <Link to='/transactions/admin/view' className="sidebar-link">
            Admin View Transactions
          </Link>
        </li>
        )}
        {localStorage.getItem('is_admin') !== 'false' && location.pathname !== '/admin/block' && (
        <li className="sidebar-menu-item">
          <Link to='/admin/block' className="sidebar-link">
            Admin Block/Unblock Users
          </Link>
        </li>
        )}
        {location.pathname !== '/users/referrals' && (
        <li className="sidebar-menu-item">
          <Link to='/users/referrals' className="sidebar-link">
            Referrals
          </Link>
        </li>
        )}
        <li className="sidebar-menu-item">
          <button className="sidebar-link" onClick={handleLogout}>
            Logout
          </button>
        </li>
      </ul>
    </div>
  );
};


export default Sidebar;




// /* global bootstrap: false */
// (() => {
//   'use strict'
//   const tooltipTriggerList = Array.from(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
//   tooltipTriggerList.forEach(tooltipTriggerEl => {
//     new bootstrap.Tooltip(tooltipTriggerEl)
//   })
// })()
