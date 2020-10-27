import React, { Button } from 'react';

export default function Input() {
  const [text, setText] = React.useState('');

  const handleText = (event) => {
    const newText = event.target.value;
    setText(newText);
  };

  return (
    <div>
      <input
        placeholder="Enter message here"
        value={text}
        onChange={handleText}
      />
      <Button text={text} />
    </div>
  );
}
