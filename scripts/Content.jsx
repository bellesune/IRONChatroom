import * as React from 'react';
import { Input } from './Input';
import { Socket } from './Socket';
import { GoogleButton } from './GoogleButton';

export function Content() {
    const [messages, setMessage] = React.useState([]);
    const [count, setCount] = React.useState(0);
    
    function getNewMessages() {
        React.useEffect(() => {
            Socket.on('message received', (data) => {
                console.log(data)
                console.log(`Received message from server: ${data['allMessages']}`)
                setMessage(data['allMessages']);
                setCount(data['user_count']);
            });
        });
    }
    getNewMessages();
    
    const x = "PRINT ME";

    return (
        <div className="body">
            <div id="title">IRON Chatroom</div>
            <a href="https://www.wikipedia.org" target="_blank">CLICK</a>
            <div id="subtitle">Instant Real-time Online Notification</div>
            <div>{<a href="https://www.wikipedia.org" target="_blank">{x}</a>}</div>
            <GoogleButton />
            
            <div id="activeUsers">Active users: {count}</div>
                <div className="messagesGrid">
                    {
                    messages.map((message, index) => 
                    <div id="messageCard" key={index}>
                        {message}
                        {}
                    </div>)
                    }
                </div>
            <Input/>
        </div>
    );
}
