import React, { useEffect, useState } from 'react';
import './ContactsPage.css';
import axios from 'axios';
import Sidebar from '../SideBar/SideBar';

const ContactsPage = () => {
  const [contacts, setContacts] = useState([]);
  const [newContactUsername, setNewContactUsername] = useState('');
  const [addContactError, setAddContactError] = useState('');

  const fetchContacts = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/contacts', {
        headers: {
          Authorization: `Bearer "${token}"`,
        },
      });
      setContacts(response.data);
    } catch (error) {
      console.error('Error fetching contacts:', error);
    }
  };

  useEffect(() => {
    fetchContacts();
  }, []);

  const removeContact = async (username) => {
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`/contacts/${username}`, {
        headers: {
          Authorization: `Bearer "${token}"`,
        },
      });
      // Refresh the contact list after removal
      fetchContacts();
    } catch (error) {
      console.error('Error removing contact:', error);
    }
  };

  const handleAddContact = async () => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(
        `/contacts/${newContactUsername}`,
        null,
        {
          headers: {
            Authorization: `Bearer "${token}"`,
          },
        }
      );
      // Refresh the contact list after adding
      fetchContacts();
      setNewContactUsername('');
      setAddContactError('');
    } catch (error) {
      console.error('Error adding contact:', error);
      setAddContactError('Failed to add contact. Please try again.');
    }
  };

  return (
    <div>
      <Sidebar />
      <h2 className="contacts-heading">Contacts</h2>
      <div className="add-contact">
        <input
          type="text"
          placeholder="Enter username"
          value={newContactUsername}
          onChange={(e) => setNewContactUsername(e.target.value)}
        />
        <button onClick={handleAddContact}>Add Contact</button>
      </div>
      {addContactError && <p className="add-contact-error">{addContactError}</p>}
      <div className="contacts-container">
        {contacts.map((contact) => (
          <div className="contact-box" key={contact.username}>
            <span className="username">{contact.username}</span>
            <button className="remove-button" onClick={() => removeContact(contact.username)}>Remove</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ContactsPage;
