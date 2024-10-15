import React from "react";

const CustomInput = ({ customInput, setCustomInput,setDisable=false }) => {
  return (
    <>
      <textarea
      disabled={setDisable}
        value={customInput}
        onChange={(e) => setCustomInput(e.target.value)}
        className="flex-grow focus:outline-none w-full border-2 border-gray-500 bg-dark-3 mt-2 rounded-lg p-2 font-mono resize-none overflow-y-auto"
      ></textarea>
    </>
  );
};

export default CustomInput;
