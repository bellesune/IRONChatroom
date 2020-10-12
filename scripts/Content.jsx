import * as React from 'react';
import { Input } from './Input';
import { Socket } from './Socket';

export function Content() {
    const [messages, setMessage] = React.useState([]);
    const [count, setCount] = React.useState([]);
    
    function getNewAddresses() {
        React.useEffect(() => {
            Socket.on('message received', (data) => {
                console.log(`Received message from server: ${data['allMessages']}`)
                setMessage(data['allMessages']);
                setCount(data['user_count'])
            });
        });
    }
    
    getNewAddresses();

    return (
        <div>
            <h2>Active users: {count}</h2>
            <h1>Your messages:</h1>
                <ol>
                    {
                    messages.map((address, index) => 
                    <li key={index}>{address}</li>)
                    }
                </ol>
            <Input/>
        </div>
    );
}
