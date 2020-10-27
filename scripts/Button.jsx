import React from 'react';
import { Socket } from './Socket';

export default function Button({ text }) {
  const newText = text;
  const [isLoggedIn, setIsLoggedIn] = React.useState(false);

  function login() {
    React.useEffect(() => {
      Socket.on('login successful', (data) => {
        setIsLoggedIn(data.isLoggedIn);
      });
    });
  }

  login();

  const handleSubmit = () => {
    if (isLoggedIn === true) {
      Socket.emit('new message input', {
        message: newText,
      });
    }
  };

  return (
    <button type="button" id="Button_btn" onClick={handleSubmit}>Send</button>
  );
}
