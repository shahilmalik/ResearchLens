import React from "react";

function Search() {
  return (
    <input
      type="text"
      placeholder="Search"
      className="focus:border-2 focus:border-black border-black border-1 h-[3.5rem] rounded-[10px] p-2"
      style={{ width: "50%" }}
    />
  );
}

export default Search;
