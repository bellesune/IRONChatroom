import * as React from 'react';
import { Socket } from './Socket';
import { Input } from './Input';

export function Button(props) {
    
    const handleSubmit = (event) => {
        let newText = props.text;
       
        console.log(`User added a message "${newText}"`)
       
        Socket.emit('new message input', { 
            'message': newText
        });
        console.log(`Sent the message "${newText}" to the server`)
}

    return (
        <button onClick={handleSubmit}>Send!</button>
    );
}
