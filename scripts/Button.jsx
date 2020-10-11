import * as React from 'react';
import { Socket } from './Socket';

export function Button(props) {
    
    const handleSubmit = (event) => {
        let newAddress = props.text;
        
        console.log('User added a message: ', newAddress);
        
        Socket.emit('new message input', { 'message': newAddress });
        
        console.log('Sent the address ' + newAddress + ' to server!');
    };

    return (
        <button onClick={handleSubmit}>Send!</button>
    );
}
