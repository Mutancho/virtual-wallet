// Navbar.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
    return (
        <nav className="navbar">
            <h2>Virtual Wallet</h2>
            <div className="navbar-links">
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
        </div>
        </nav>
    );
}

export default Navbar;
