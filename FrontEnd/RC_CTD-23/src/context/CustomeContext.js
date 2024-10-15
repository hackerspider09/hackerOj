import React, { createContext, useContext, useState } from 'react';

const CustomContext = createContext();

export const CustomProvider = ({ children }) => {
const [confetiStart,setConfetistart] = useState(false);

  return (
    <CustomContext.Provider value={{ confetiStart,setConfetistart }}>
      {children}
    </CustomContext.Provider>
  );
};

// Custom hook to consume the context
export const useCustomContext = () => useContext(CustomContext);
