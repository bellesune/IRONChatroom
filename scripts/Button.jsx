import * as React from 'react';
import { Socket } from './Socket';

function handleSubmit(event) {
    let newAddress = document.getElementById("address_input");
    
    console.log('User added a message: ', newAddress.value);
    
    Socket.emit('new message input', { 'message': newAddress.value });
    
    console.log('Sent the address ' + newAddress.value + ' to server!');
    newAddress.value = '';
    
    event.preventDefault();
}

export function Button() {
    return (
        <form onSubmit={handleSubmit}>
            <input id="address_input" placeholder="Enter a USPS address"></input>
            <button>Add to DB!</button>
        </form>
    );
}
