import * as React from 'react';
import { Input } from './Input';
import { Socket } from './Socket';

export function Content() {
    const [messages, setMessage] = React.useState([]);
    const [count, setCount] = React.useState(0);
    
    function getNewMessages() {
        React.useEffect(() => {
            Socket.on('message received', (data) => {
                console.log(`Received message from server: ${data['allMessages']}`)
                setMessage(data['allMessages']);
                setCount(data['user_count']);
            });
        });
    }
    
    getNewMessages();

    return (
        <div className="body">
            <div id="title">IRON Chatroom</div>
            <div id="subtitle">Instant Real-time Online Navigator</div>
            
            <div id="activeUsers">Active users: {count}</div>
                <div className="messagesGrid">
                    {
                    messages.map((message, index) => 
                    <div id="messageCard" key={index}>
                        {message}
                    </div>)
                    }
                </div>
            <Input/>
        </div>
    );
}
