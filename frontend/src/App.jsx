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
import Sidebar from './components/SideBar/SideBar';
import ContactsPage from './components/ContactsPage/ContactsPage';
import UserUpdatePage from "./components/UserUpdatePage/UserUpdatePage";
import SuccessfulPaymentPage from './components/SuccessfulPaymentPage/SuccessfulPaymentPage';
import UnsuccessfulPaymentPage from './components/UnsuccessfulPaymentPage/UnsuccessfulPaymentPage';
import ManageCards from './components/ManageCards/ManageCards';
import WithdrawPage from './components/WithdrawPage/WithdrawPage';
import AdminViewUsersPage from "./components/AdminViewUsersPage/AdminViewUsersPage";
import AdminViewTransactionPage from "./components/AdminViewTransactionPage/AdminViewTransactionPage";
import BlockUsersPage from "./components/BlockUsersPage/BlockUsersPage";

const stripePromise = loadStripe('pk_test_51N8aWKBoGCspooGJW8aKWZUM6W8IOJTjhJcwwN3Mez7j9lWGxazkmyPxNM1jcCPNAeOko2GlrAyFYmyitl7c8Fnu00njr03PIO');

const App = () => {
  const shouldShowSidebar = !(
    window.location.pathname === '/users/menu' ||
    window.location.pathname === '/users/transactions' ||
    window.location.pathname === '/users/payments/top-up' ||
    window.location.pathname === '/contacts' 
  );

  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegistrationPage />} />
          <Route path="/verify-email" element={<EmailVerificationPage />} />
          <Route path="/users/menu" element={<MenuPage />} />
          <Route path="/payment/successful" element={<SuccessfulPaymentPage />} />
          <Route path="/payment/unsuccessful" element={<UnsuccessfulPaymentPage />} />
          <Route path='/users/transactions' element={<TransactionsPage />} />
          <Route path='/users/payment-cards' 
            element={
              <Elements stripe={stripePromise}>
                <ManageCards />
              </Elements>
            } 
          />
          <Route path='/users/payments/top-up' 
            element={
              <Elements stripe={stripePromise}>
                <BankDetailsForm />
              </Elements>
            } 
          />
          <Route path="/contacts" element={<ContactsPage />} />
          <Route path="/users/update" element={<UserUpdatePage />} />
          <Route path="/users/payments/withdraws" 
            element={
              <Elements stripe={stripePromise}>
                <WithdrawPage />
              </Elements>
            } 
          />
            <Route path='/users/admin/view' element={<AdminViewUsersPage />} />
            <Route path='/transactions/admin/view' element={<AdminViewTransactionPage />} />
          <Route path='/admin/block' element={<BlockUsersPage />} />
        </Routes>
      </div>
    </Router>
  );
};
  
export default App;
