
import React, { useState,useEffect } from 'react';

import TextField from '@mui/material/TextField';
import { axiosAuthInstance, CONTEST_ID } from '../../Utils/AxiosConfig';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
// import Submission from "../submission-comp/submission"
import { useNavigate } from "react-router";
import { useParams } from 'react-router-dom';
import {toast} from 'react-toastify';
import "./tinymce.css"
import HtmlReactParser from 'html-react-parser'


// const QuestionDetailSection = (props) => 
export default function QuestionDetailSection(props){

    const [isButtonDisabled, setIsButtonDisabled] = useState(false);
    const [inputText, setInputText] = useState('');
    const [outputText, setOutputText] = useState('');
    const [questionIDDDD, setquestionIDDDD] = useState('');
    const navigate = useNavigate()
    
    const { questionId } = useParams();

    const whiteText = {
      color: 'white',
    };
    const whiteBorder = {
      borderColor: 'white',
    };
  
  
    const whiteOutlinedInput = {
      '& .MuiOutlinedInput-root': {
        '& fieldset': {
          borderColor: 'white', // Change outline color to white
        },
      },
    };
  
    // const handleButtonClick = () => {
    //   // Replace this logic with your actual processing based on input
    //   // For now, we're just echoing the input as output
    //   setOutputText(inputText);
    // };
    const TakeIpOp = (e) => {
       setIsButtonDisabled(true);
      // console.log("RC run");
      // const id = toast.loading("Build Process Started");
      
      // toast.dark('This is Toast Notification for Dark');
      // toast.info('This is Toast Notification for Dark');
      // toast.success('This is Toast Notification for Dark');
      // toast.warn('This is Toast Notification for Warn');
      // toast.error('This is Toast Notification for Error');
      
        const takeIpopEndpoint = `submission/${CONTEST_ID}/runrccode2/`;
        const takeipoppayload = {
  
            'question':`${questionId}`,
      
            'input': `${inputText}`,
          }
        //   console.log(takeipoppayload)
        axiosAuthInstance.post(takeIpopEndpoint,takeipoppayload)
      .then((response) => {
          // console.log("enter in then ");
          if (response) {
            setIsButtonDisabled(false);
              // console.log(response.data);
              setOutputText(response.data.output)
              // toast.update(id, { render: "Build Process Finished", type: "success", isLoading: false, autoClose:3000 })
              // <Navigate to="/instruction" />
              // window.location.reload(true);
          
          }
          else {
            setIsButtonDisabled(false);
            toast.error("An error occurred.",{ autoClose: 2000 });
              // toast.update(id, { render: "Server is Busy", type: "error", isLoading: false, autoClose:3000 })
              // console.log("login failed");
          }
      })
      .catch((error) => {
        toast.error("An error occurred. Please try again later.",{ autoClose: 2000 });
        setIsButtonDisabled(false);
        console.clear();
          // console.log(" error => ",error.response);
      
      })

     
  
  }
    // Your question detail section JSX
    return (
      <div className="question-sec">  
        {/* {QuesData.map((item) => (
          <Question key={question.questionId} questionData={question} />
        ))} */}
          <div className="que-name">  
            
            <h2> {props.QuesData.title} </h2>
            <h8>Points : {props.QuesData.points}</h8>
  
            
          </div>
          <div className="quepart que-description" style={{ height: "auto" }}>
            <h6>Description</h6>
            {HtmlReactParser(String(props.QuesData.description))}
            
            <h6>Input Format</h6>
             {HtmlReactParser(String(props.QuesData.ipFormate))}
  
  
         <h6>Output Format</h6>
         {HtmlReactParser(String(props.QuesData.opFormate))}
  
         {/* <h6>Sample Input-Output</h6> */}
         {/* {HtmlReactParser(String(props.QuesData.inputOutputBlock))} */}
            
           
          
            <h6>Constraints</h6>
            {HtmlReactParser(String(props.QuesData.constraints))}
           
  
            <h6>Author</h6>
            <p>{props.QuesData.author}
            </p>
  
            
        </div>
        {/* <div className="iop">
          <div className="rc-input-output">
            <div className="inputrc">
              <h6>INPUT</h6>
              <textarea></textarea>
            </div>
            <div className="outputrc">
              <h6>OUTPUT</h6>
              <textarea className="inputs-output"></textarea>
            </div>
          </div>
          {"\n"}
          {"\n"}
    
          <div className="get-output">
            <button>GET OUTPUT</button>
          </div> 
        </div> */}
  
  <div>
  <div style={{ margin: '14x auto', display:'flex',justifyContent:'center', marginBottom:'17px'}}>
          {/* <Button variant="contained" color="primary" onClick={TakeIpOp} disabled={inputText.trim()  === '' ? 'disabled' : ''} > */}
          <Button variant="contained" type="button" color="info" onClick={TakeIpOp}     disabled={inputText.trim() === ''? true : !false ? isButtonDisabled : true } style={{border:'2px solid #157a93',color:'#F5F5F5'}}   >
            Process Input
          </Button>

        </div>
 
        <Grid container spacing={2}>
          <Grid item xs={6}>
            <div>
              <h2 style={{ fontSize: '1.5rem', ...whiteText }}>Input</h2>
              <TextField
           
                fullWidth
                variant="outlined"
                // label="Input"
                sx={{
                  // backgroundColor: '#ffd60a',
                  border: '2px solid white',
                  borderRadius:'5px',
                }}
                multiline
                rows={3}
                placeholder="Enter input here"
                InputProps={{
                  style: { ...whiteText },
                   // Text color and white border
                }}
                inputProps={{ maxLength: 15 }}
                // style={whiteBorder}
                value={inputText}
                maxLength={5}
                onChange={(e) => setInputText(e.target.value)}
              />
            </div>
          </Grid>
          <Grid item xs={6}>
            <div>
              <h2 style={{ fontSize: '1.5rem', ...whiteText }}>Output</h2>
              <TextField
                fullWidth
                variant="outlined"
                // label="Output"
                multiline
                sx={{
                  // backgroundColor: '#ffd60a',
                  border: '2px solid white',
                  borderRadius: '5px',
                }}
                rows={3}
                placeholder="Display output here"
                InputLabelProps={{ className: 'whiteText' }} // White label color
                className={whiteOutlinedInput} // Apply white outline
                InputProps={{
                  style: { ...whiteText, borderColor: 'white' ,readOnly: true}, // Text color and white border
                }}
                style={whiteBorder}
               
                value={outputText}
                
              />
            </div>
          </Grid>
        </Grid>


    
      
      </div>
  
        
      </div>
    );
  };


// export default QuestionDetailSection;