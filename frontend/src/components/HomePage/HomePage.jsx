import React, { useState } from 'react';
import Navbar from '../Navbar/Navbar';
import './HomePage.css';

import image1 from '../../images/wallet.png';
import image2 from '../../images/group_wallet.jpg';
import image3 from '../../images/currency_exchange.png';
import image4 from '../../images/lightning.jpg';
import image5 from '../../images/saving.png';
import image6 from '../../images/recurring_transaction.jpg';


function HomePage() {
  const [cardData, setCardData] = useState([
    { id: 1, frontTitle: 'Wallets', backTitle: 'Experience seamless financial management with our sophisticated virtual wallet', image: image1 },
    { id: 2, frontTitle: 'Group Wallets', backTitle: 'Unlock the power of collaborative finance with our Group Wallets, enabling effortless group money management and sharing', image: image2},
    { id: 3, frontTitle: 'Currency Exchange', backTitle: 'Secure currency exchange for hassle-free international transactions, ensuring your funds are seamlessly converted at competitive rates', image: image3},
    { id: 4, frontTitle: 'Instant Cash Transfer', backTitle: ' Enjoy the convenience of instant cash transfers, allowing you to send and receive funds swiftly, anytime, anywhere', image: image4},
    { id: 5, frontTitle: 'Budget Assistant', backTitle: 'Effortlessly track and optimize expenses with our intuitive budgeting tool, providing you with better control over your finances', image: image5},
    { id: 6, frontTitle: 'Recurring Transactions', backTitle: 'Streamline your finances with our recurring transactions feature. Automate regular payments and save time managing your bills', image: image6},
  ]);

  const handleCardFlip = (id) => {
    const updatedCardData = cardData.map((card) =>
      card.id === id ? { ...card, flipped: true } : card
    );
    setCardData(updatedCardData);
  };

  return (
    
    <div>
      <section>
        <div className="homepage">
          <Navbar />
          <h1>Welcome to Virtual Wallet!</h1>
          <p>Your one-stop solution for managing your virtual currency.</p>
          <div className="homepage-buttons"></div>
        </div>
      </section>
      <section class="card-group">
        <div className="flip-card-container">
          {cardData.map((card) => (
            <div className="flip-card" key={card.id} tabIndex="0">
              <div
                className={`flip-card-inner ${card.flipped ? 'flipped' : ''}`}
                onClick={() => handleCardFlip(card.id)}
              >
                <div className="flip-card-front">
                  {card.image && <img src={card.image} alt="Front of Flip Card" />}
                  <h3>{card.frontTitle}</h3>
                </div>
                <div className="flip-card-back">
                  <h3>{card.backTitle}</h3>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default HomePage;
