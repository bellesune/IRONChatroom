import * as React from 'react';
import { Input } from './Input';
import { Message } from './Message';
import { Socket } from './Socket';
import { GoogleButton } from './GoogleButton';

export function Content() {
    const [messages, setMessage] = React.useState([]);
    const [count, setCount] = React.useState(0);
    const [type, setType] = React.useState("");

    function getNewMessages() {
        React.useEffect(() => {
            Socket.on('message received', (data) => {
                console.log(`Received message from server: ${data['allMessages']} and type: ${data['type']}`);
                setMessage(data['allMessages']);
                setCount(data['user_count']);
                setType(data['type']);
            });
        });
    }

    getNewMessages();

    return (
        <div className="body">
            <div id="title">IRON Chatroom</div>
            <div id="subtitle">Instant Real-time Online Notification</div>
            <GoogleButton />
            
            <div id="activeUsers">Active users: {count}</div>
                <Message type={type} passMessage={messages} />
            <Input/>
        </div>
    );
}