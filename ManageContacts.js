import React, { useState, useEffect } from 'react';

const ManageContacts = () => {
  const [contacts, setContacts] = useState([]);

  useEffect(() => {
    // Implement logic to fetch contacts from the backend
  }, []);

  return (
    <div>
      <h2>Manage Contacts</h2>
      <ul>
        {contacts.map(contact => (
          <li key={contact.id}>
            Name: {contact.name}, Phone: {contact.phone}, Email: {contact.email}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ManageContacts;
