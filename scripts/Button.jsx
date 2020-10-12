import * as React from 'react';
import { Socket } from './Socket';
import { Input } from './Input';

export function Button(props) {
    
    const handleSubmit = (event) => {
        console.log("THIS IS BUTTON")
        let newText = props.text;
        let newUser = props.name;
        
        // props.text ? newText=props.name : newText=props.text
        
        
        console.log(`User ${newUser} added a message "${newText}"`)
        // console.log(`Added ${newText}`)
        
        if (newUser != undefined){
            Socket.emit('new message input', { 
                'user': newUser,
                'message': newText
            });
            console.log(`Sent the user:${newUser} and message "${newText}" to the server`)
        }
        
        // console.log(`Sent ${newText} to the server`)
    };

    return (
        <button onClick={handleSubmit}>Send!</button>
    );
}
