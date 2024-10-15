

import { vscodeDark } from "@uiw/codemirror-theme-vscode";
import { eclipse } from "@uiw/codemirror-theme-eclipse";
import { python } from "@codemirror/lang-python";
import { javascript } from "@codemirror/lang-javascript";
import { java } from "@codemirror/lang-java";
import { cpp } from "@codemirror/lang-cpp";
import ReactCodeMirror from "@uiw/react-codemirror";
import { useState } from "react";

const CodeEditorWindow = ({ onChange, language, code, theme, fontSize, forProblemsPage=true, isInterview=false }) => {
  
  const handleEditorChange = (value) => {
    if (isInterview) onChange(value);
    else onChange('code', value);
    
  };



  return (
    // <div className={`flex flex-col !w-full justify-start items-end overlay rounded-md overflow-hidden shadow-4xl bg-dark-1 ${forProblemsPage? 'min-h-[20%]' : 'h-[500px]'}`}>
    <div className={`flex flex-col !w-full justify-start items-end overlay rounded-md overflow-hidden shadow-4xl bg-dark-1 max-h-[58vh]`}>
        <ReactCodeMirror
          value={code}
          onChange={handleEditorChange}
          extensions={[language==='python'? python() : language==='cpp'? cpp() : language==='java'? java() : javascript()]}
          // extensions={[python()]}

          theme={theme==='dark'? vscodeDark : eclipse}
          style={{ fontSize: fontSize }}
        />
    </div>
  );
};
export default CodeEditorWindow;
