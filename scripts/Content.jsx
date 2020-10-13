import * as React from 'react';
import { Input } from './Input';
import { Socket } from './Socket';


export function Content() {
    const [messages, setMessage] = React.useState([]);
    const [count, setCount] = React.useState(0);
    const [bot, setBot] = React.useState([]);
    
    function getNewMessages() {
        React.useEffect(() => {
            Socket.on('message received', (data) => {
                console.log(`Received message from server: ${data['allMessages']}`)
                setMessage(data['allMessages']);
                setCount(data['user_count']);
                // console.log("THIS IS ",data['allMessages'].slice(0,7))
                
                // for (let i=0; i<data['allMessages'].length; i++){
                //     if (data['allMessages'][i].slice(0,7) === "IronBot"){
                        // setBot(data['allMessages'][i])
                        // console.log(data['allMessages'][i])
                        
                //     }    
                // }
                
            });
        });
    }
    
    getNewMessages();

    return (
        <div class="body">
            <div id="title">IRON Chatroom</div>
            <div id="subtitle">Instant Real-time Online Navigator</div>
            
            <div id="activeUsers">Active users: {count}</div>
                <div class="messagesGrid">
                    {
                    messages.map((message, index) => 
                    <div id="messageCard" key={index}>
                        {message}
                    </div>)
                    }
                </div>
            <Input/>
        </div>
    );
}
