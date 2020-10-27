import React from 'react';

export default function Message({
  type, users, images, messages,
}) {
  const newMessages = [];

  for (let i = 0; i < type.length; i += 1) {
    if (type[i] === 'bot') {
      newMessages.push(
        <div>
          <span id="ironbot">
            <img id="img_bot" src="./static/ironbot.jpg" alt="logo img" />
            {' '}
            IRONBOT
          </span>
          <div id="messageCard_bot">
            {messages[i]}
          </div>
        </div>,
      );
    } else if (type[i] === 'html') {
      newMessages.push(
        <div>
          <span>
            <img id="img_user" src={images[i]} alt="user img" />
            {' '}
            {users[i]}
          </span>
          <div id="messageCard">
            <a href={messages[i]} rel="noreferrer" target="_blank">
              {messages[i]}
            </a>
          </div>
        </div>,
      );
    } else if (type[i] === 'jpg') {
      newMessages.push(
        <div>
          <span>
            <img id="img_user" src={images[i]} alt="user img" />
            {' '}
            {users[i]}
          </span>
          <div id="messageCard">
            <a href={messages[i]} rel="noreferrer" target="_blank">
              {messages[i]}
              <img id="img_link" src={messages[i]} alt="user img" />
            </a>
          </div>
        </div>,
      );
    } else {
      newMessages.push(
        <div>
          <span>
            <img id="img_user" src={images[i]} alt="user img" />
            {' '}
            {users[i]}
          </span>
          <div id="messageCard">
            {messages[i]}
          </div>
        </div>,
      );
    }
  }

  return (
    <div className="messagesGrid">
      {
        newMessages.map((message) => message)
      }
    </div>
  );
}
