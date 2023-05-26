import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Elements } from '@stripe/react-stripe-js';
import { loadStripe } from '@stripe/stripe-js';

import HomePage from './components/HomePage/HomePage';
import LoginPage from './components/LoginPage/LoginPage';
import RegistrationPage from './components/RegistrationPage/RegistrationPage';
import EmailVerificationPage from './components/EmailVerificationPage/EmailVerificationPage';
import MenuPage from './components/MenuPage/MenuPage';
import BankDetailsForm from './components/TopupPage/TopupPage';
import TransactionsPage from './components/TransactionsPage/TransactionsPage'



const stripePromise = loadStripe('pk_test_51N8aWKBoGCspooGJW8aKWZUM6W8IOJTjhJcwwN3Mez7j9lWGxazkmyPxNM1jcCPNAeOko2GlrAyFYmyitl7c8Fnu00njr03PIO');

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegistrationPage />} />
                <Route path="/verify-email" element={<EmailVerificationPage />} />
                <Route path="/users/menu" element={<MenuPage />} />
                {<Route path='/users/transactions' element={<TransactionsPage />} />}
                <Route path='/users/payments/top-up' 
                    element={
                        <Elements stripe={stripePromise}>
                            <BankDetailsForm />
                        </Elements>
                    } 
                />
                {/* Other routes go here */}
            </Routes>
        </Router>
    );
}

export default App;
