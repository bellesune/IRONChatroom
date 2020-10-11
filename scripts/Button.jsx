import * as React from 'react';
import { Socket } from './Socket';

export function Button(props) {
    
    const handleSubmit = (event) => {
        let newText = props.text;
        
        // props.text ? newText=props.name : newText=props.text
        
        
        // console.log(`User ${newUser} added a message ${newAddress}`)
        console.log(`Added ${newText}`)
        
        Socket.emit('new message input', { 
            'message': newText,
                                    
        });
        // console.log(`Sent the user:${newUser} and message ${newAddress} to the server`)
        console.log(`Sent ${newText} to the server`)
    };

    return (
        <button onClick={handleSubmit}>Send!</button>
    );
}
