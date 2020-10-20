import * as React from 'react';
import { Input } from './Input';
import { Message } from './Message';
import { Socket } from './Socket';
import { GoogleButton } from './GoogleButton';

export function Content() {
    const [type, setType] = React.useState([]);
    const [auth, setAuth] = React.useState([]);
    const [users, setUsers] = React.useState([]);
    const [images, setImages] = React.useState([]);
    const [messages, setMessages] = React.useState([]);
    const [count, setCount] = React.useState(0);

    function getNewMessages() {
        React.useEffect(() => {
            Socket.on('message received', (data) => {
                console.log(`Received message from server: ${data['allMessages']} and type: ${data['type']}`);
                setType(data['type']);
                setAuth(data['allAuth']);
                setUsers(data['allUsers']);
                setImages(data['allImages']);
                setMessages(data['allMessages']);
                setCount(data['user_count']);
            });
        });
    }

    getNewMessages();

    return (
        <div className="body">
            <div id="title">
                <img id="img_title" src="./static/ironbot.jpg"/> IRON Room
            </div>
            <div id="subtitle">Instant Real-time Online Notification</div>
            <GoogleButton/>
            <div id="activeUsers">Active users: {count}</div>
            <Message type={type} users={users} images={images} messages={messages} />
            <Input/>
        </div>
    );
}