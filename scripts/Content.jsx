import * as React from 'react';
import { Input } from './Input';
import { Socket } from './Socket';
import { User } from './User';

export function Content() {
    const [addresses, setAddresses] = React.useState([]);
    
    function getNewAddresses() {
        React.useEffect(() => {
            Socket.on('message received', (data) => {
                console.log("Received message from server: " + data['allMessages']);
                setAddresses(data['allMessages']);
            });
        });
    }
    
    getNewAddresses();

    return (
        <div>
            
            <h1>Your messages:</h1>
                <ol>
                    {
                    addresses.map((address, index) => 
                    <li key={index}>{address}</li>)
                    }
                </ol>
            <User/>
            <Input/>
        </div>
    );
}
