import * as React from 'react';
import { Button } from './Button';
import { Socket } from './Socket';

export function Content() {
    const [addresses, setAddresses] = React.useState([]);
    
    function getNewAddresses() {
        React.useEffect(() => {
            Socket.on('message received', (data) => {
                console.log("Received message from server: " + data['allMessages']);
                setAddresses(data['allMessages']);
            })
        });
    }
    
    getNewAddresses();

    return (
        <div>
            <h1>USPS Addresses!</h1>
                <ol>
                    {
                    addresses.map((address, index) => 
                    <li key={index}>{address}</li>)
                    }
                </ol>
            <Button />
        </div>
    );
}
