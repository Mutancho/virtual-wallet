import React, { useState, useEffect } from 'react';
import { useStripe, useElements, CardElement } from '@stripe/react-stripe-js';
import { useLocation } from 'react-router-dom';
import './TopupPage.css';


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
  if (!Array.isArray(data)) {
    console.error('Data is not an array:', data);
    return [];
  }
  
  return data.data;
};

const TopupPage = () => {
  const stripe = useStripe();
  const elements = useElements();
  const [walletId, setWalletId] = useState(null);
  const [currency, setCurrency] = useState(null);
  const [amount, setAmount] = useState('');
  const [paymentMethods, setPaymentMethods] = useState([]);
  const [selectedCard, setSelectedCard] = useState('');
  const location = useLocation();

  useEffect(() => {
    if (location.state) {
      setWalletId(location.state.walletId);
      setCurrency(location.state.currency);
    }

    fetchPaymentMethods().then(setPaymentMethods).catch(error => console.error(error));
  }, [location]);

  const handleCardSelection = (event) => {
    setSelectedCard(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!stripe || !elements) {
      return;
    }

    if (!selectedCard) {
      console.error("No card selected");
      return;
    }

    const response = await fetch('/users/transfers/payment-intent', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer "${localStorage.getItem('token')}"`
      },
      body: JSON.stringify({
        amount,
        wallet_id: walletId,
        currency,
        payment_method_id: selectedCard,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    if (data.message === 'Payment succeeded') {
      console.log('Payment was successful');
    } else {
      console.log('Payment failed');
    }
  };

  return (
    <div className="container">
      <h1>Top Up Page</h1>

      <h2>Saved Cards</h2>
      <ul>
        {paymentMethods && paymentMethods.map((method) => (
          <li key={method.id}>
            <label>
              <input
                type="radio"
                name="selectedCard"
                value={method.id}
                checked={selectedCard === method.id}
                onChange={handleCardSelection}
              />
              **** **** **** {method.card && method.card.last4}
            </label>
          </li>
        ))}
      </ul>

      <form onSubmit={handleSubmit}>
        <label htmlFor="amount">Amount</label>
        <input
          type="number"
          id="amount"
          value={amount}
          onChange={(event) => setAmount(event.target.value)}
          required
        />

        <label htmlFor="card-element">Card Details</label>
        <CardElement id="card-element" />

        <button type="submit" disabled={!stripe}>
          Pay
        </button>
      </form>
    </div>
  );
};

export default TopupPage;
