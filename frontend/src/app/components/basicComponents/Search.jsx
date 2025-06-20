/*
This is a React component that renders a search input field.
It allows users to type in a search query and triggers an action when the Enter key is pressed.
*/

import React from "react";

function Search({onChange, onEnter}) {
  // allow user to press enter to trigger search for convenience
  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      onEnter()
    }
  }

  return (
    <input
      type="text"
      placeholder="Search"
      className="focus:border-2 focus:border-black border-black border-1 h-[3.5rem] rounded-[10px] p-2"
      style={{ width: "50%" }}
      onChange={onChange}
      onKeyUp={handleKeyDown}
    />
  );
}

export default Search;
