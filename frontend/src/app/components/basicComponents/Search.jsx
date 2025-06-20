/*
This is a React component that renders a search input field.
It allows users to type in a search query and triggers an action when the Enter key is pressed.
*/

import React from "react";
import TextField from '@mui/material/TextField';

function Search({onChange, onEnter}) {
  // allow user to press enter to trigger search for convenience
  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      onEnter()
    }
  }

  return (
    <TextField
      type="text"
      placeholder="Search"
      style={{ width: "50%" }}
      onChange={onChange}
      onKeyUp={handleKeyDown}
    />
  );
}

export default Search;
