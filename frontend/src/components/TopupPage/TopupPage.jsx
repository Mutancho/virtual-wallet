import React, { useState, useEffect } from 'react';
import { useStripe, useElements, CardElement } from '@stripe/react-stripe-js';
import { useLocation, useNavigate } from 'react-router-dom';
import './TopupPage.css';
import Sidebar from '../SideBar/SideBar';

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

const TopupPage = () => {
  const stripe = useStripe();
  const elements = useElements();
  const [walletId, setWalletId] = useState(null);
  const [currency, setCurrency] = useState(null);
  const [amount, setAmount] = useState('');
  const [paymentMethods, setPaymentMethods] = useState([]);
  const [selectedCard, setSelectedCard] = useState('');
  const location = useLocation();
  const navigate = useNavigate();

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

    let paymentMethodId = selectedCard;

    if (!selectedCard) {
      const cardElement = elements.getElement(CardElement);

      const { paymentMethod, error } = await stripe.createPaymentMethod({
        type: 'card',
        card: cardElement,
      });

      if (error) {
        console.log('Stripe error:', error);
        return;
      }

      paymentMethodId = paymentMethod.id;
    }

    const response = await fetch('/users/transfers/payment-intent', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer "${localStorage.getItem('token')}"`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        amount,
        wallet_id: walletId,
        currency,
        payment_method_id: paymentMethodId,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    if (data.message === 'Payment succeeded') {
      console.log('Payment was successful');
      navigate('/payment/successful');
    } else {
      console.log('Payment failed');
    }
  };

  return (
    <div className="container">
      <Sidebar />
      <h1>Top Up Page</h1>

      <select value={selectedCard} onChange={handleCardSelection}>
        <option value="">Select a saved card (Optional)</option>
        {paymentMethods.map((method) => (
          <option key={method.id} value={method.id}>
            **** **** **** {method.card && method.card.last4}
          </option>
        ))}
      </select>

      <form onSubmit={handleSubmit}>
        <label htmlFor="amount">Amount</label>
        <input
          type="number"
          id="amount"
          value={amount}
          onChange={(event) => setAmount(event.target.value)}
          required
        />

        {!selectedCard && (
          <>
            <label htmlFor="card-element">Card Details</label>
            <CardElement id="card-element" />
          </>
        )}
        <button type="submit" disabled={!stripe}>
          Pay
        </button>
      </form>
    </div>
  );
};

export default TopupPage;
