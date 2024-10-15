import React, { useState } from 'react';
import './instructs.css';

import { Link } from 'react-router-dom'


function Instruct() {
  const [termsChecked, setTermsChecked] = useState(false);
  const [isButtonEnabled, setIsButtonEnabled] = useState(false);
  const instructions = [ 
    "The following coding competition can be played in THREE languages ",
    "These rounds consists of 6 questions of in the order of increasing marks. For first right submission, the first participant to submit will receive full marks. For next right submissions, following participants will receive (max-marks)-1, (max-marks)-2 and so on marks.",
    "The following contest will consist of two text boxes -a) Input textbox b) Output textbox. Participants are expected to put custom input in textbox and  corresponding output will be generated.",
    "Based on output generated upon customized inputs provided, find the relation, and code it accordingly in the editor provided on the page.",
    "To run the code and check for semantics , Press run button",
    "To check Testcases passed and to  do submission of the code , Press Submit button.",
    "Once pressed on the run button, you can authenticate the code in the custom input textbox and check the corresponding output to verify the validity of the code.",
    "After every submission, leaderboard will be updated. Users can check their rank on leaderboard page.",
    "Submissions done can be viewed on the submission page of the website.",
  
  ];

  const handleTermsChange = () => {
    setTermsChecked(!termsChecked);
    setIsButtonEnabled(!isButtonEnabled);
}

const btnstyle = {
  textDecoration: "none",
  color: "#ffffff",
}


  return (
    
      <div className="row align instruct">  
        <div className="col-1 col-sm-1 col-md-2 col-lg-2 col-xl-2 col-xxl-2"></div>
        <div className="col-10 col-sm-10 col-md-8 col-lg-8 col-xl-8 col-xxl-8">  
          <div className="heading instr">
            <h3 className="title">INSTRUCTIONS</h3>
          </div>
          <div className="scrollon" id="style-8">  
            {instructions.map((instruction, index) => (  
              <div className="outerbox" key={index}>
                <div className="infobox">{instruction}</div>
                <div className={`numbox ${index + 1}`}>{String(index + 1).padStart(2, '0')}</div>
              </div>
            ))}
          </div>
          <div>
            <form action="" method="post">
              <div className="form-check checkboxouter">
                <input
                  className="form-check-input checkbox"
                  type="checkbox"
                  value="checked"
                  id="flexCheckDefault"
                  name="checked"
                  checked={termsChecked}
                  onChange={handleTermsChange}
                  
                  required
                />
                <label className="form-check-label" htmlFor="flexCheckDefault">
                  I have read all the instructions carefully.
                </label>
              </div>
              <div className="buttonboxouter" >
              <Link to="/question/" style={btnstyle} onClick={() => 
                    localStorage.setItem("contractAccept", true)}>
                <button 
                  // className={termsChecked ? 'enabled' : 'disabled'}
                  className={termsChecked? 'button':'proceed'}
              
                  id="submit_button"
                  name="submitbutton"
                  disabled={!isButtonEnabled} 
                
                  
                >
                   Proceed
                  
                </button></Link>
              </div>
            </form>
          </div>
        </div>
        <div className="col-1 col-sm-1 col-md-2 col-lg-2 col-xl-2 col-xxl-2"></div>
      </div>
    
  );
}

export default Instruct;
