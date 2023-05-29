import React, { useState, useEffect } from 'react';
import { useStripe, useElements, CardElement } from '@stripe/react-stripe-js';
import { useLocation } from 'react-router-dom';
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
  const stripe = useStripe();
  const elements = useElements();
  const location = useLocation();
  const { currency } = location.state;
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

    const response = await fetch('/users/transfers/create-payout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer "${token}"`,
      },
      body: JSON.stringify({
        amount: amount,
        currency: currency,
        payment_method_id: paymentMethodId,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    alert(data.message);
  };

  return (
    <div className="container">
      <h2>Withdraw</h2>
      <p>Currency: {currency}</p>

      <select value={selectedCard} onChange={handleCardSelection}>
        <option value="">Select a card (Optional)</option>
        {paymentMethods.map((method) => (
          <option key={method.id} value={method.id}>
            **** **** **** {method.card && method.card.last4}
          </option>
        ))}
      </select>

      {!selectedCard && (
        <>
          <label htmlFor="card-element">Card Details</label>
          <CardElement options={{hidePostalCode: true}} id="card-element" />
        </>
      )}

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
