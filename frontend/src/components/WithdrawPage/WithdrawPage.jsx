import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './WithdrawPage.css';

const fetchPaymentMethods = async () => {
  const response = await fetch('/users/cards/payment-methods/list', {
    headers: {
      'Authorization': `Bearer "${localStorage.getItem('token')}"`,
    },
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();

  return data.data || [];
};

const WithdrawPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { walletId } = location.state; // retrieve walletId from location.state
  const [amount, setAmount] = useState(0);
  const [paymentMethods, setPaymentMethods] = useState([]);
  const [selectedCard, setSelectedCard] = useState('');
  const token = localStorage.getItem('token');

  useEffect(() => {
    fetchPaymentMethods().then(setPaymentMethods).catch(error => console.error(error));
  }, []);

  const handleCardSelection = (event) => {
    setSelectedCard(event.target.value);
  };

  const handleWithdraw = async () => {
    try {
      const response = await fetch('/users/transfers/create-payout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer "${token}"`,
        },
        body: JSON.stringify({
          amount: amount,
          wallet_id: walletId,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      navigate('/payment/successful');

    } catch (error) {
      console.error('Error:', error);

      navigate('/payment/unsuccessful');
    }
  };

  return (
    <div className="container">
      <h2>Withdraw</h2>

      <select value={selectedCard} onChange={handleCardSelection}>
        <option value="">Select a card (Optional)</option>
        {paymentMethods.map((method) => (
          <option key={method.id} value={method.id}>
            **** **** **** {method.card && method.card.last4}
          </option>
        ))}
      </select>

      <input
        type="number"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        placeholder="Amount"
      />

      <button onClick={handleWithdraw}>Withdraw</button>
    </div>
  );
};

export default WithdrawPage;
