import React , {useState,useEffect} from "react";
import Select from "react-select";
import { customStyles } from "./constants/customstyles.js"
import { languageOptions } from "./constants/languageOptions";

const LanguagesDropdown = ({ onSelectChange ,selectedLanguag}) => {
  const [lang, setlang] = useState("cpp");
  useEffect(() => {
    setlang(selectedLanguag);
  },[selectedLanguag]);
  return (
    <Select
      // placeholder={`select a language`}
      options={languageOptions}
      styles={customStyles}
      defaultValue={languageOptions[0]}
      // defaultValue={lang}
      
      onChange={(selectedOption) => onSelectChange(selectedOption)}
    />
  );
};

export default LanguagesDropdown;