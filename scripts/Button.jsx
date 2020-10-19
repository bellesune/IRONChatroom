import * as React from 'react';
import { Socket } from './Socket';

export function Button(props) {
    let newText = props.text;
    // let isLoggedIn = false;
    const [isLoggedIn, setIsLoggedIn] = React.useState(false);
        
    // function login() {
    //     React.useEffect(() => {
    //         Socket.on('login successful', (data) => {
    //             console.log(`Login receive from server: ${data['isLoggedIn']}`);
    //              setIsLoggedIn(data['isLoggedIn']);
    //         });
    //     });
    // }
    // login();
    Socket.on('login successful', (data) => {
        console.log(`Login receive from server: ${data['isLoggedIn']}`);
        setIsLoggedIn(data['isLoggedIn']);
        
    });
    
    console.log("LOGGGG THIS", isLoggedIn)
    const handleSubmit = (event) => {
    
        console.log("LOGGGG", isLoggedIn)
        if (!isLoggedIn) {
            alert("Please logged in first");
        }
        else {
            console.log(`User added a message "${newText}"`)
       
            Socket.emit('new message input', { 
                'message': newText
            });
            console.log(`Sent the message "${newText}" to the server`)    
        }
    }

    return (
        <button onClick={handleSubmit}>Send</button>
    );
}
