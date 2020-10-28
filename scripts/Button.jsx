import React from 'react';
import { Socket } from './Socket';

export function Button({ text }) {
  const newText = text;
  const [isLoggedIn, setIsLoggedIn] = React.useState(false);

  function login() {
    React.useEffect(() => {
      Socket.on('login successful', (data) => {
        setIsLoggedIn(data['isLoggedIn']);
      });
    });
  }

  login();

  const handleSubmit = () => {
    if (isLoggedIn === false) {
      alert("Please logged with Google first!");
    }
    else {
      console.log(`User added a message "${newText}"`);
   
      Socket.emit('new message input', { 
        'message': newText
      });
      console.log(`Sent the message "${newText}" to the server`);  
    }
  };

  return (
    <button type="button" id="Button_btn" onClick={handleSubmit}>Send</button>
  );
}
