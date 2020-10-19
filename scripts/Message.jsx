import * as React from 'react';

export function Message(props) {
  const type = props.type;
  const newMessages = [];
  let botStyle = {color: "blue"};
  let divStyle = {color: 'black'};
  let d = {color: 'white'};
  
  const img = {width: '20px', heigh: "20px"}
  
    for (let i=0; i<type.length; i++){
    
      if (type[i] === 'bot'){
        newMessages.push(
          // insert image here <IMG[i]> then NAME <props.name[i]>
          <div>
            <span style={d}><img src="https://cdn4.iconfinder.com/data/icons/super-hero/154/super-hero-iron-man-head-skin-512.png" style={img}/>ROBOT</span>
            <div style={botStyle} id="messageCard">
                {props.passMessage[i]}
            </div>
          </div>
        );
      }
      else if (type[i] === 'html'){
        newMessages.push(
          <div style={divStyle} id="messageCard">
            <a href={props.passMessage[i]} target="_blank">
              {props.passMessage[i]}
            </a>  
          </div>
        );
      }
      // else if img 
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