import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './PendingTransactionsPage.css';
import { Link } from 'react-router-dom';
import Sidebar from '../SideBar/SideBar';

const Wallet = ({ wallet }) => {
  const [showDetails, setShowDetails] = useState(false);

  return (
    <div className={`wallet ${showDetails ? 'expanded' : ''}`} onClick={() => setShowDetails(!showDetails)}>
      <div className="wallet-header">
        <h2>{wallet.name}</h2>
        <p>{wallet.currency}</p>
      </div>
      <div className={`wallet-details ${showDetails ? 'visible' : ''}`}>
        <p>Type: {wallet.type}</p>
        <p>Balance: {wallet.balance.toFixed(2)}</p>
        <div className="active-status">
          <span>{wallet.is_active ? 'Active' : 'Inactive'}</span>
          <div className={`status-indicator ${wallet.is_active ? 'active' : 'inactive'}`}></div>
        </div>
        <div className="button-group">
          <Link to='/users/payments/top-up'
            state={{ walletId: wallet.wallet_id, currency: wallet.currency }}
          >
            <button className="action-button">TOP UP</button>
          </Link>

          <Link to='/users/payments/withdraws'
            state={{ walletId: wallet.wallet_id }}
          >
            <button className="action-button">WITHDRAW</button>
          </Link>

          <Link
            to='/users/transactions'
            state={{ walletId: wallet.wallet_id }}
          >
            <button className="action-button">TRANSACTIONS</button>
          </Link>

        </div>
      </div>
      <button className="view-button">{showDetails ? 'See Less' : 'See More'}</button>
    </div>
  );
};

const PendingTransactionsPage = () => {
  const [transactions, setTransactions] = useState([]);
  const [wallets, setWallets] = useState([]);
  const [selectedWallets, setSelectedWallets] = useState({});
  const [acceptError, setAcceptError] = useState('');

  const fetchTransactions = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/transactions/pending', {
        headers: {
          Authorization: `Bearer "${token}"`,
        },
      });
      setTransactions(response.data);
    } catch (error) {
      console.error('Error fetching pending transactions:', error);
    }
  };

  const fetchWallets = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/users/wallets', {
        headers: {
          Authorization: `Bearer "${token}"`,
        },
      });
      setWallets(response.data.wallets);
    } catch (error) {
      console.error('Error fetching wallets:', error);
    }
  };

  useEffect(() => {
    fetchTransactions();
    fetchWallets();
  }, []);

  const handleSelectWallet = (transactionId, walletId) => {
    setSelectedWallets(prevState => ({
      ...prevState,
      [transactionId]: walletId,
    }));
  };

  const handleAcceptTransaction = async (transactionId) => {
    try {
      const token = localStorage.getItem('token');
      const selectedWalletId = selectedWallets[transactionId];
      await axios.post(
        `/transactions/accept_confirmation/${transactionId}`,
        { wallet: selectedWalletId },
        {
          headers: {
            Authorization: `Bearer "${token}"`,
          },
        }
      );
      // Refresh the transaction list after accepting
      fetchTransactions();
      setAcceptError('');
    } catch (error) {
      console.error('Error accepting transaction:', error);
      setAcceptError('Failed to accept transaction. Please try again.');
    }
  };

  return (
    <div className="pending-transactions-container">
      <Sidebar />
      <h2 className="page-heading">Pending Transactions</h2>
      <div className="transaction-list">
        {transactions.map((transaction) => (
          <div className="transaction" key={transaction.id}>
            <div className="transaction-details">
              <p>
                <span className="detail-label">Amount:</span>{transaction.amount} {transaction.currency}
              </p>
              <p>
                <span className="detail-label">Category:</span> {transaction.category}
              </p>
              <p>
                <span className="detail-label">Recurring:</span>{' '}
                {transaction.is_recurring ? 'Yes' : 'No'}
              </p>
              <p>
                <span className="detail-label">Sent At:</span> {transaction.sent_at}
              </p>
              <p>
                <span className="detail-label">Accepted:</span>{' '}
                {transaction.accepted ? 'Yes' : 'No'}
              </p>
            </div>
            <div className="transaction-actions">
              <select
                className="select-wallet"
                value={selectedWallets[transaction.id]} // Use selected wallet for the specific transaction
                onChange={(e) =>
                  handleSelectWallet(transaction.id, e.target.value) // Update the selected wallet for the specific transaction
                }
              >
                <option value="">Select Wallet</option>
                {wallets.map((wallet, index) => (
                  <option key={index} value={wallet.wallet_id}>
                    {wallet.name} - {wallet.currency}
                  </option>
                ))}
              </select>
              <button
                className="accept-button"
                onClick={() => handleAcceptTransaction(transaction.id)}
              >
                Accept
              </button>
            </div>
          </div>
        ))}
      </div>
      {acceptError && <p className="accept-error">{acceptError}</p>}
    </div>
  );
};

export default PendingTransactionsPage;
