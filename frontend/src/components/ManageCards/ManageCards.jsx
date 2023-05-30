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
    fetchPaymentMethods()
      .then((data) => {
        console.log(data); // Check if data is being fetched
        setPaymentMethods(data);
      })
      .catch((error) => console.error(error));
  }, []);

  const addCard = async (event) => {
    event.preventDefault();
    
    if (!stripe || !elements) {
      return;
    }

    const cardElement = elements.getElement(CardElement);

    const { error, paymentMethod } = await stripe.createPaymentMethod({
      type: 'card',
      card: cardElement,
      billing_details: {
        address: {
          postal_code: '', // Empty string to omit zip code
        },
      },
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
      body: JSON.stringify({ id: paymentMethod.id }),
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
      body: JSON.stringify({ id: cardId }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    fetchPaymentMethods().then(setPaymentMethods).catch(error => console.error(error));
  };

  return (
    <div id="manage-cards-container" className="container">
      <h1 id="manage-cards-title">Manage Cards</h1>
      <form id="manage-cards-form" onSubmit={addCard} className="add-card-container">
        <CardElement options={{ hidePostalCode: true }} id="card-element" />
        <button id="manage-cards-add-card-btn" type="submit" className="add-card" disabled={!stripe}>Add Card</button>
      </form>
      <ul id="manage-cards-list">
        {paymentMethods.map((method) => (
          <li key={method.id} className="card-item">
            <div className="card-details">
              <span className="card-number">**** **** **** {method.card && method.card.last4}</span>
              <button id={`remove-card-${method.id}`} onClick={() => detachCard(method.id)} className="remove-card-button">Remove</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ManageCards;
