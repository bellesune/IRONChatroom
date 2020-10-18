import * as React from 'react';

export function Message(props) {
  const type = props.type;
  const newMessages = [];
  let botStyle = {color: "blue"};
  let divStyle = {color: 'black'};
  
    for (let i=0; i<type.length; i++){
    
      if (type[i] === 'bot'){
        newMessages.push(
          <div style={botStyle} id="messageCard">
              {props.passMessage[i]}
          </div>
        );
      }
      else{
        newMessages.push(
          <div style={divStyle} id="messageCard">
              {props.passMessage[i]}
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