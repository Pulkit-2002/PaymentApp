import React, { useEffect, useState } from 'react';

const TransactionHistory = () => {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    // Implement logic to fetch transaction history from the backend
  }, []);

  return (
    <div>
      <h2>Transaction History</h2>
      <ul>
        {transactions.map(transaction => (
          <li key={transaction.id}>
            Amount: {transaction.amount}, Sender: {transaction.sender}, Receiver: {transaction.receiver}, Timestamp: {transaction.timestamp}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TransactionHistory;
