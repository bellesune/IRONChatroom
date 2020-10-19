import * as React from 'react';

export function Message(props) {
  const type = props.type;
  const auth = props.auth;
  const users = props.users;
  const images = props.images;
  const messages = props.messages;
  const newMessages = [];
  
  const botStyle = {color: 'blue'};
  let divStyle = {color: 'black'};
  const d = {color: 'white'};
  const img = {width: '20px', heigh: "20px"}
  
    for (let i=0; i<type.length; i++){
    
      if (type[i] === 'bot'){
        newMessages.push(
          // insert image here <IMG[i]> then NAME <props.name[i]>
          <div>
            <span style={d}><img src="https://cdn4.iconfinder.com/data/icons/super-hero/154/super-hero-iron-man-head-skin-512.png" style={img}/>IRONBOT</span>
            <div style={botStyle} id="messageCard">
                {messages[i]}
            </div>
          </div>
        );
      }
      else if (type[i] === 'html'){
        newMessages.push(
          // <span style={d}><img src={} style={img}/>{}</span>
          <div style={divStyle} id="messageCard">
            <a href={messages[i]} target="_blank">
              {messages[i]}
            </a>  
          </div>
        );
      }
      // else if img 
      else{
        newMessages.push(
          <div style={divStyle} id="messageCard">
              {messages[i]}
          </div>
        );
      }
    }

  return (
    <div className="messagesGrid">
      {
        newMessages.map((message, index) => message)
      }
    </div>
  );
}