import React from 'react';
import { useNavigate } from "react-router-dom";
import './UnsuccessfulPaymentPage.css';

const UnsuccessfulPaymentPage = () => {
    let navigate = useNavigate();

    return (
        <div className="payment-unsuccessful-container">
            <h1 className="payment-unsuccessful-title">Payment Unsuccessful!</h1>
            <p className="payment-unsuccessful-message">Your payment has been unsuccessful, please contact your group wallet admin.</p>
            <button className="payment-unsuccessful-btn" onClick={() => navigate('/users/menu')}>Continue to Menu</button>
        </div>
    )
}

export default UnsuccessfulPaymentPage;
