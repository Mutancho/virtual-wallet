import React from 'react';
import { useNavigate } from "react-router-dom";
import './SuccessfulPaymentPage.css';

const SuccessfulPaymentPage = () => {
    let navigate = useNavigate();

    return (
        <div className="payment-success-container">
            <h1 className="payment-success-title">Payment Successful!</h1>
            <p className="payment-success-message">Your payment has been successfully processed.</p>
            <button className="payment-success-btn" onClick={() => navigate('/users/menu')}>Continue to Menu</button>
        </div>
    )
}

export default SuccessfulPaymentPage;
