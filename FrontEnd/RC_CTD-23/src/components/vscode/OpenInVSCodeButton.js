import React from 'react';

const OpenInVSCodeButton = ({ code, input, output }) => {
  const constructVSCodeURI = (code, input, output) => {
    const base64Code = btoa(code);
    const base64Input = btoa(input);
    const base64Output = btoa(output);

    // Fixed path known to both React app and VS Code extension
    const workspacePath = 'my-oj-workspace'; // Adjust this path accordingly
    return `vscode://file/${workspacePath}?code=${base64Code}&input=${base64Input}&output=${base64Output}`;
  };

  const handleClick = () => {
    const vscodeUri = constructVSCodeURI(code, input, output);
    window.location.href = vscodeUri;
  };

  return (
    <button onClick={handleClick}>
      Open in VS Code
    </button>
  );
};

export default OpenInVSCodeButton;
