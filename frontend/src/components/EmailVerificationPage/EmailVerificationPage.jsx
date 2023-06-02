import React from 'react';
import { Link } from 'react-router-dom';
import './EmailVerificationPage.css';

function EmailVerificationPage() {
  return (
    <div className="email-verification-container">
      <h2>Verify Your Email Address</h2>
      <p>We have sent you an email with a link to verify your account. Please check your inbox and follow the instructions to complete your registration.</p>
      <Link to="/">Go to Home Page</Link>
    </div>
  );
}

export default EmailVerificationPage;
