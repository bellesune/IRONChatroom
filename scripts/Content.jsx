import * as React from 'react';
import { Input } from './Input';
import { Socket } from './Socket';
// import bg from './bg.jpg';

const bodyStyle = {
    textAlign: 'center',
};

const activeUserStyle = {
    fontFamily: 'Roboto',
    color: 'thistle',
};

const titleStyle = {
    fontFamily: 'Serif',
    color: 'rgb(212, 111, 212)'
};

const messagesGrid = {
    textAlign: 'left',
    backgroundColor: 'papayaWhip',
    opacity: '0.83',
    borderRadius: '15px',
    width: '65%',
    marginLeft: 'auto',
    marginRight: 'auto',
    padding: '28px',
    // backgroundImage: {bg},
    // backgroundPosition: 'center',
    // backgroundSize: 'cover',
};

const messageCard = {
    borderRadius: '15px',
    padding: '10px',
    color: 'black',
    backgroundColor: 'white',
    marginTop: '10px',
    margin: '10px',
};


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
        <div style={bodyStyle}>
            <h1 style={titleStyle}>IRON Chatroom</h1>
            <h4 id="subtitle">Instant Real-time Online Navigator</h4>
            
            <h3 style={activeUserStyle}>Active users: {count}</h3>
                <div style={messagesGrid}>
                    {
                    messages.map((message, index) => 
                    <div style={messageCard} key={index}>
                        {message}
                    </div>)
                    }
                </div>
            <Input/>
        </div>
    );
}
