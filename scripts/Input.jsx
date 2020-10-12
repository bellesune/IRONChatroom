import * as React from 'react';
import { Button } from "./Button";

export function Input(props) {
  console.log("THIS IS INPUT")
  const [text, setText] = React.useState("");
  
  const handleText = (event) => {
    const newText = event.target.value;
    setText(newText);
  
  };

  return (
    <div>
      <input
        placeholder="Enter message"
        value={text}
        onChange={handleText}
      />
      <Button text={text} />
    </div>
  );
}