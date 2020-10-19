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
  const img = {width: '20px', heigh: "20px"};
  const imgLink = {width: '120px', heigh: "110px"};
  
  for (let i=0; i<type.length; i++){
    if (type[i] === 'bot'){
      newMessages.push(
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
        <div>
          <span style={d}><img src={images[i]} style={img}/> {users[i]}</span>
          <div style={divStyle} id="messageCard">
            <a href={messages[i]} target="_blank">
              {messages[i]}
            </a>  
          </div>
        </div>
      );
    }
    else if (type[i] === 'jpg'){
      newMessages.push(
        <div>
          <span style={d}><img src={images[i]} style={img}/> {users[i]}</span>
          <div style={divStyle} id="messageCard">
            <a href={messages[i]} target="_blank">
              {messages[i]}<img src={messages[i]} style={imgLink}/>
            </a>  
          </div>
        </div>
      );
    }
    else{
      newMessages.push(
        <div>
        <span style={d}><img src={images[i]} style={img}/> {users[i]}</span>
          <div style={divStyle} id="messageCard">
              {messages[i]}
          </div>
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