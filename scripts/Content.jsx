import * as React from 'react';
import { Input } from './Input';
import { Socket } from './Socket';

const bodyStyle = {
    textAlign: 'center',
};

const activeUserStyle = {
    fontFamily: 'Roboto',
    color: 'thistle',
};

const titleStyle = {
    fontFamily: 'Serif',
    color: 'rgb(212, 111, 212)'
};

const messagesGrid = {
    textAlign: 'left',
    backgroundColor: 'papayaWhip',
    opacity: '0.83',
    borderRadius: '15px',
    width: '65%',
    marginLeft: 'auto',
    marginRight: 'auto',
    padding: '28px',
    
};

export function Content() {
    const [messages, setMessage] = React.useState([]);
    const [count, setCount] = React.useState([]);
    
    function getNewAddresses() {
        React.useEffect(() => {
            Socket.on('message received', (data) => {
                console.log(`Received message from server: ${data['allMessages']}`)
                setMessage(data['allMessages']);
                setCount(data['user_count']);
            });
        });
    }
    
    getNewAddresses();

    return (
        <div style={bodyStyle}>
            <h1 style={titleStyle}>IRON Chatroom</h1>
            <h4 id="subtitle">Instant Real-time Online Navigator</h4>
            
            <h2 style={activeUserStyle}>Active users: {count}</h2>
                <div style={messagesGrid}>
                    {
                    messages.map((message, index) => 
                    <div key={index}>{message}</div>)
                    }
                </div>
            <Input/>
        </div>
    );
}
