import React, { useState, useEffect } from 'react';
import './MenuPage.css';
import { Link } from 'react-router-dom';
import Sidebar from '../SideBar/SideBar';

const Wallet = ({ wallet }) => {
  const [showDetails, setShowDetails] = useState(false);

  const trimmedName = wallet.name.length > 15 ? wallet.name.substring(0, 12) + '...' : wallet.name;

  return (
    <div className={`wallet ${showDetails ? 'expanded' : ''}`} onClick={() => setShowDetails(!showDetails)}>
      <div className="wallet-header">
        <h2>{trimmedName}</h2>
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
          state={{ walletId: wallet.wallet_id}}
          >
          <button className="action-button">WITHDRAW</button>
          </Link>

          <Link 
            to='/users/transactions'
            state={{ walletId: wallet.wallet_id }}
          >
            <button className="action-button">TRANSACTIONS</button>
          </Link>
          <Link
            to='/users/wallets/settings'
            state={{ walletId: wallet.wallet_id, type: wallet.type }}
          >
            <button className="action-button">SETTINGS</button>
          </Link>

        </div>
      </div>
      <button className="view-button">{showDetails ? 'See Less' : 'See More'}</button>
    </div>
  );
};




const MenuPage = ({ user }) => {
  const [owner, setOwner] = useState('');
  const [wallets, setWallets] = useState([]);
  const token = localStorage.getItem('token');

  useEffect(() => {
    fetch('/users/wallets', {
      headers: {
        'Authorization': `Bearer "${token}"`
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        setOwner(data.owner);
        setWallets(data.wallets);
      })
      .catch((error) => console.error('Error:', error));
  }, []);

  return (
    <div className="menu-page">
      <Sidebar />
      <h1 id="unique-h1">Welcome {owner}</h1>
      <Link to='/users/wallets'>
        <button className="add-wallet-button">Add Wallet</button>
      </Link>
      <div className="wallets">
        {wallets.map((wallet, index) => (
          <Wallet key={index} wallet={wallet} />
        ))}
      </div>
    </div>
  );
};

export default MenuPage;
