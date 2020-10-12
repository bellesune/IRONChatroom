import * as React from 'react';
import { Button } from "./Button";

export function User(props) {
  console.log("THIS IS USER")
  const [name, setName] = React.useState("Louis");
  
  const handleText = (event) => {
    const newName = event.target.value;
    setName(newName);
    
  };

  return (
    <div>
      <input
        placeholder="Enter name"
        value={name}
        onChange={handleText}
      />
      <Button name={name} />
    </div>
  );
}