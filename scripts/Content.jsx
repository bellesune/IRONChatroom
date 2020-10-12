import * as React from 'react';
import { Input } from './Input';
import { Socket } from './Socket';

export function Content() {
    const [addresses, setAddresses] = React.useState([]);
    const [count, setCount] = React.useState([]);
    
    function getNewAddresses() {
        React.useEffect(() => {
            Socket.on('message received', (data) => {
                console.log(`Received message from server: ${data['allMessages']}`)
                // console.log("Received message from server: " + data['allMessages'] ++ data['user_count']);
                setAddresses(data['allMessages']);
                setCount(data['user_count'])
            });
        });
    }
    
    getNewAddresses();

    return (
        <div>
            <h2>Active user: {count}</h2>
            <h1>Your messages:</h1>
                <ol>
                    {
                    addresses.map((address, index) => 
                    <li key={index}>{address}</li>)
                    }
                </ol>
            <Input/>
        </div>
    );
}
