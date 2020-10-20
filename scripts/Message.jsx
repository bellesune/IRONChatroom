import * as React from 'react';

export function Message(props) {
  const type = props.type;
  const users = props.users;
  const images = props.images;
  const messages = props.messages;
  const newMessages = [];

  for (let i=0; i<type.length; i++){
    if (type[i] === 'bot'){
      newMessages.push(
        <div>
          <span id="ironbot"><img id="img_bot" src="./static/ironbot.jpg"/> IRONBOT</span>
            <div id="messageCard_bot">
              {messages[i]}
            </div>
        </div>
      );
    }
    else if (type[i] === 'html'){
      newMessages.push(
        <div>
          <span><img id="img_user" src={images[i]}/> {users[i]}</span>
          <div id="messageCard">
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
          <span><img id="img_user" src={images[i]}/> {users[i]}</span>
          <div id="messageCard">
            <a href={messages[i]} target="_blank">
              {messages[i]}<img id="img_link" src={messages[i]}/>
            </a>  
          </div>
        </div>
      );
    }
    else{
      newMessages.push(
        <div>
        <span><img id="img_user" src={images[i]}/> {users[i]}</span>
          <div id="messageCard">
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