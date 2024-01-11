import React, { useState } from 'react';

const MoneyTransfer = () => {
  const [amount, setAmount] = useState(0);
  const [receiverUsername, setReceiverUsername] = useState('');

  const handleMoneyTransfer = () => {
    // Implement logic to send money transfer data to the backend
  };

  return (
    <div>
      <h2>Money Transfer</h2>
      <form onSubmit={handleMoneyTransfer}>
        <label>Amount: <input type="number" value={amount} onChange={(e) => setAmount(e.target.value)} /></label>
        <label>Receiver Username: <input type="text" value={receiverUsername} onChange={(e) => setReceiverUsername(e.target.value)} /></label>
        <button type="submit">Send Money</button>
      </form>
    </div>
  );
};

export default MoneyTransfer;
