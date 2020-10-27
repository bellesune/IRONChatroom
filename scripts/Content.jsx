import React, { Message, Input, GoogleButton } from 'react';
import { Socket } from './Socket';

export default function Content() {
  const [type, setType] = React.useState([]);
  const [users, setUsers] = React.useState([]);
  const [images, setImages] = React.useState([]);
  const [messages, setMessages] = React.useState([]);
  const [count, setCount] = React.useState(0);

  function getNewMessages() {
    React.useEffect(() => {
      Socket.on('message received', (data) => {
        setType(data.type);
        setUsers(data.allUsers);
        setImages(data.allImages);
        setMessages(data.allMessages);
        setCount(data.user_count);
      });
    });
  }

  getNewMessages();

  return (
    <div className="body">
      <div id="title">
        <img id="img_title" src="./static/ironbot.jpg" alt="ironbot logo" />
        {' '}
        IRON Room
      </div>
      <div id="subtitle">Instant Real-time Online Notification</div>
      <GoogleButton />
      <div id="activeUsers">
        Active users:
        {count}
      </div>
      <Message type={type} users={users} images={images} messages={messages} />
      <Input />
    </div>
  );
}
