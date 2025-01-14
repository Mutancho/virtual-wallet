import React, {useState} from 'react';
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
import ReferralPage from './components/ReferralPage/ReferralPage';
import NewWalletPage from './components/AddWalletPage/AddWalletPage';
import WalletSettingsPage from './components/WalletSettings/WalletSettingsPage';
import PendingTransactionsPage from "./components/PendingTransactionsPage/PendingTransactionsPage"
import ViewTransactionsPage from "./components/ViewTransactionsPage/ViewTransactionsPage";
import ChatPage from "./components/ChatPage/ChatPage";

const stripePromise = loadStripe('pk_test_51N8aWKBoGCspooGJW8aKWZUM6W8IOJTjhJcwwN3Mez7j9lWGxazkmyPxNM1jcCPNAeOko2GlrAyFYmyitl7c8Fnu00njr03PIO');

const App = () => {

  const [user, setUser] = useState();
  const handleAuth = (userData) => {
    console.log('User Data:', userData); // Log the user data
    setUser(userData);
  };


  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage onAuth={handleAuth}/>} />
          <Route path="/register/:referralId?" element={<RegistrationPage />} />
          <Route path="/verify-email" element={<EmailVerificationPage />} />
          <Route path="/users/menu" element={<MenuPage />} />
          <Route path="/payment/successful" element={<SuccessfulPaymentPage />} />
          <Route path="/payment/unsuccessful" element={<UnsuccessfulPaymentPage />} />
          <Route path='/users/transactions' element={<TransactionsPage />} />
          <Route path='/users/wallets/settings' element={<WalletSettingsPage />} />
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
          <Route path="/users/wallets" element={<NewWalletPage />} />
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
          <Route path='/pending/transactions' element={<PendingTransactionsPage />} />
          <Route path='/users/referrals' element={<ReferralPage />} />
          <Route path='/transactions' element={<ViewTransactionsPage />} />
          <Route path='/chat' element={<ChatPage user={user}/>} />
        </Routes>
      </div>
    </Router>
  );
};
  
export default App;
