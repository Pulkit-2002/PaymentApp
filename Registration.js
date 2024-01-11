import React, { useState } from 'react';

const Registration = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleRegistration = () => {
    // Implement logic to send registration data to the backend
  };

  return (
    <div>
      <h2>Registration</h2>
      <form onSubmit={handleRegistration}>
        <label>Username: <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} /></label>
        <label>Password: <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} /></label>
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Registration;
