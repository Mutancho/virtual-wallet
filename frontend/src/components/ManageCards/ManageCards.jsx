import React, { useState, useEffect } from 'react';
import { useStripe, useElements, CardElement } from '@stripe/react-stripe-js';
import './ManageCards.css';

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

const ManageCards = () => {
  const stripe = useStripe();
  const elements = useElements();
  const [paymentMethods, setPaymentMethods] = useState([]);

  useEffect(() => {
    fetchPaymentMethods().then(setPaymentMethods).catch(error => console.error(error));
  }, []);

  const addCard = async (event) => {
    event.preventDefault();
    
    if (!stripe || !elements) {
      return;
    }

    const cardElement = elements.getElement(CardElement);

    const {error, paymentMethod} = await stripe.createPaymentMethod({
      type: 'card',
      card: cardElement,
    });

    if (error) {
      console.log('Stripe error:', error);
      return;
    }

    const response = await fetch('/users/cards/payment-methods/attach', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer "${localStorage.getItem('token')}"`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ payment_method_id: paymentMethod.id }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    fetchPaymentMethods().then(setPaymentMethods).catch(error => console.error(error));
  };

  const detachCard = async (cardId) => {
    const response = await fetch('/users/cards/payment-methods/detach', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer "${localStorage.getItem('token')}"`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ payment_method_id: cardId }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    fetchPaymentMethods().then(setPaymentMethods).catch(error => console.error(error));
  };

  return (
    <div className="container">
      <h1>Manage Cards</h1>
      <form onSubmit={addCard} className="add-card-container">
        <CardElement />
        <button type="submit" className="add-card" disabled={!stripe}>Add Card</button>
      </form>
      <ul>
        {paymentMethods.map((method) => (
          <li key={method.id} className="card-item">
            **** **** **** {method.card && method.card.last4}
            <button onClick={() => detachCard(method.id)} className="remove-card">Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ManageCards;
