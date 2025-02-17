
import React, { useEffect, useState } from "react";
import LanguagesDropdown from "./shared/LanguagesDropdown";
import ThemeDropdown from "./shared/ThemeDropdown";
import CodeEditorWindow from "./shared/CodeEditorWindow";
import OutputWindow from "./shared/OutputWindow";
import CustomInput from "./shared/CustomInput";
import Split from "react-split";
import { languagesData, mockComments } from "./constants";
import { AiOutlineFullscreen, AiOutlineFullscreenExit } from "react-icons/ai";
import Timer from "./shared/Timer";
import axios from "axios";
import Loader from "./shared/Loader";
import { useParams } from 'react-router-dom';
import FontSizeDropdown from "./shared/FontSizeDropdown";
import { axiosAuthInstance ,CONTEST_ID,API_DOMAIN, WEBSOCKETURL} from '../../Utils/AxiosConfig';
import {  toast } from 'react-toastify';
import { useCustomContext } from "../../context/CustomeContext";

const Playground = ({ problems, isForSubmission = true, setSubmitted }) => {
  
  const params = useParams();
  const QuestionId = params.questionId;
  // const subendPoint = `/submission/${CONTEST_ID}/submit2/`;
  // const runendPoint = `/submission/${CONTEST_ID}/runcode2/`;
  const subendPoint = `/submission/${CONTEST_ID}/submit/`;
  const runendPoint = `/submission/${CONTEST_ID}/runcode/`;
  const socketURL = `ws://${API_DOMAIN}/ws/submission/`

  const { confetiStart,setConfetistart } = useCustomContext();


  const [customInput, setCustomInput] = useState("");
  const [outputDetails, setOutputDetails] = useState(null);
  const [isCodeRunning, setIsCodeRunning] = useState(false);
  const [isCodeSubmitting, setIsCodeSubmitting] = useState(false);
  const [theme, setTheme] = useState({ value: "dark", label: "Dark" });
  const [language, setLanguage] = useState(languagesData[3]);
  const [code, setCode] = useState(mockComments[language.value]);
  const [fontSize, setFontSize] = useState({ value: '14', label: '14px' });
  const [isFullScreen, setIsFullScreen] = useState(false);
  const [clickedProblemId, setClickedProblemId] = useState(null);
  const [clickedProblem, setClickedProblem] = useState(null);

  

  useEffect(() => {
    if (problems) {
        problems.forEach((problem, index) => {
            if (problem.questionId === QuestionId) {
                // console.log("inside playeground ",problem)
              setClickedProblem(problem);
              setClickedProblemId(problem.questionId);
                setCustomInput(problem.sampleIp);
                setOutputDetails({'output':problem.sampleOp});
        }
        })
    }

}, [problems]);

useEffect(() => {
  const savedCode = localStorage.getItem(QuestionId+language.value);
  // Set the code to the saved code if it exists, otherwise set it to the default code
  setCode(savedCode ? savedCode : mockComments[language.value]);
}, [language]);


  const handleFullScreen = () => {
    if (isFullScreen) {
      document.exitFullscreen();
    } else {
      document.documentElement.requestFullscreen();
    }
    setIsFullScreen(!isFullScreen);
  };

  useEffect(() => {
    function exitHandler(e) {
      if (!document.fullscreenElement) {
        setIsFullScreen(false);
        return;
      }
      setIsFullScreen(true);
    }

    if (document.addEventListener) {
      document.addEventListener("fullscreenchange", exitHandler);
      document.addEventListener("webkitfullscreenchange", exitHandler);
      document.addEventListener("mozfullscreenchange", exitHandler);
      document.addEventListener("MSFullscreenChange", exitHandler);
    }
  }, [isFullScreen]);

  const onChange = (action, data) => {
    switch (action) {
      case "code": {
        setCode(data);
        localStorage.setItem(QuestionId+language.value, data)
        break;
      }
      default: {
        console.warn("case not handled!", action, data);
      }
    }
  };

  useEffect(() => {
    const handleKeyPress = (event) => {
      if (event.ctrlKey && event.shiftKey && event.key === 'Enter') {
        event.preventDefault();
        handleSubmit();
      }
      else if (event.ctrlKey && event.key === 'Enter') {
        event.preventDefault();
        handleRun(customInput);
      }
    };

    document.addEventListener('keydown', handleKeyPress);

    return () => {
      document.removeEventListener('keydown', handleKeyPress);
    };
  }, [code,customInput]);

  const handleRun = async (input) => {
    const id = toast.loading("Please wait..");  

    setIsCodeRunning(true);
    const submissionpayload = {
  
      'question':`${clickedProblemId}`,
      'code':`${code}`,
      'language': `${language.value}`,
    }

    if(input ===  '')
    {
        submissionpayload['input']=clickedProblem.sampleIp;
    }else{
      submissionpayload['input']=input;
    }    
    // e.preventDefault();
    // console.log(submissionpayload)
    axiosAuthInstance.post(runendPoint,submissionpayload)
            .then((response) => {
                if (response) {
                   var  data = response.data;
                  //  console.log("run data",data)
                   data['submitted']=false;
                    
                    // submission queued
                    toast.update(id, { render: data.msg, type: "success" })
                    


                    // Establish a WebSocket connection
                    const socket = new WebSocket(`${WEBSOCKETURL}/ws/submission/${data.submissionId}/`);

                    // Show a message when the connection is open
                    socket.onopen = () => {
                      // console.log('WebSocket connection established');
                    };

                    // Handle messages received through the WebSocket
                    socket.onmessage = (event) => {
                      
                      const messageData = JSON.parse(event.data);
                      // console.log('Received message:', messageData);

                      switch (messageData.type) {
                          case 'status_update':
                            // console.log('Status update:', messageData);
                            toast.update(id, { render: messageData.submission_data.status, type: "success"})
                              // Handle status update message
                              // Update your React state with the status data
                              break;

                          case 'final_status':
                              toast.update(id, { render: "Submission Executed Successfuly", type: "success", isLoading: false, autoClose:3000 })
                              // Handle final submission data message
                              setOutputDetails(messageData.submission_data)
                              // console.log('Final submission data:', messageData.submission_data);
                              // Update your React state with the final submission data
                              socket.close();
                              break;
                              
                          default:
                                console.error('Unknown message type:', messageData);
                                toast.update(id, { render: "Something Went Wrong", type: "error", isLoading: false, autoClose:3000 })
                      }
                    };

                    // Handle WebSocket errors
                    socket.onerror = (error) => {
                      console.error('WebSocket error:', error);
                      toast.update(id, { render:"WebSocket error occurred. Please try again.", type: "error", isLoading: false, autoClose:3000 })
                    };

                    // Handle WebSocket closure
                    socket.onclose = () => {
                      // console.log('WebSocket connection closed');
                    };

                    setIsCodeRunning(false);
                  
                }
                else {
                      setIsCodeRunning(false);                      
                    }
                })
                .catch((error) => {
                    setIsCodeRunning(false);
                    if (error.response?.data?.msg) {
                      toast.update(id, { render:error.response.data.msg, type: "error", isLoading: false, autoClose:3000 })
                    } else {
                      toast.update(id, { render:"An error occurred. Please try again later.(check input block should not blank)", type: "error", isLoading: false, autoClose:3000 })
                  }
                  
            })
  
  };


  const handleSubmit = async () => {
    setOutputDetails({});
    setIsCodeSubmitting(true); 
    const id = toast.loading("Please wait..");  

    const submissionpayload = {
  
      'question':`${clickedProblemId}`,
      'code':`${code}`,
      'language': `${language.value}`,
      
    }
    // console.log(submissionpayload)
    axiosAuthInstance.post(subendPoint,submissionpayload)
            .then((response) => {
                // console.log("enter in then ");
                if (response) {
                    setIsCodeSubmitting(false);
                    // console.log("enter in then if ");
                   var  data = response.data;
                  //  console.log("op=> ",data)
                  //  data['submitted']=true;
                  //  console.log(" op => ",data)
                  //  setOutputDetails(data);

                    // submission queued
                    toast.update(id, { render: data.msg, type: "success" })
                    


                    // Establish a WebSocket connection
                    const socket = new WebSocket(`${WEBSOCKETURL}/ws/submission/${data.submissionId}/`);

                    // Show a message when the connection is open
                    socket.onopen = () => {
                      // console.log('WebSocket connection established');
                    };

                    // Handle messages received through the WebSocket
                    socket.onmessage = (event) => {
                      
                      const messageData = JSON.parse(event.data);
                      // console.log('Received message:', messageData);

                      switch (messageData.type) {
                          case 'status_update':
                            // console.log('Status update:', messageData);
                            toast.update(id, { render: messageData.submission_data.status, type: "success"})
                              // Handle status update message
                              // Update your React state with the status data
                              break;

                          case 'final_status':
                              toast.update(id, { render: "Submission Executed Successfuly", type: "success", isLoading: false, autoClose:3000 })
                              // Handle final submission data message
                              setOutputDetails(messageData.submission_data)
                              // console.log('Final submission data:', messageData.submission_data);
                              socket.close();
                              break;
                              
                          default:
                                console.error('Unknown message type:', messageData);
                                toast.update(id, { render: "Something Went Wrong", type: "error", isLoading: false, autoClose:3000 })
                      }
                    };

                    // Handle WebSocket errors
                    socket.onerror = (error) => {
                      console.error('WebSocket error:', error);
                      toast.update(id, { render:"WebSocket error occurred. Please try again.", type: "error", isLoading: false, autoClose:3000 })
                    };

                    // Handle WebSocket closure
                    socket.onclose = () => {
                      // console.log('WebSocket connection closed');
                    };

                    setIsCodeRunning(false);

                   
                }})
                .catch((error) => {
                  
                    setIsCodeSubmitting(false);
                    if (error.response?.data?.msg) {
                        toast.update(id, { render:error.response.data.msg, type: "error", isLoading: false, autoClose:3000 })
                    } else {
                      toast.update(id, { render: "An error occurred. Please try again later.", type: "error", isLoading: false, autoClose:3000 })
                    }
                  
                // console.log("enter in error ",error);

            })
  
  };


  return (
    <div className="w-full flex flex-col overflow-y-auto">
      <div className="flex px-4 gap-2 justify-between">
        <div className="flex flex-row w-full justify-between">
          <div className="flex">
          <LanguagesDropdown onSelectChange={(lang) => {setLanguage(lang);setCode(mockComments[lang.value])}} />
          </div>

          {/* <ThemeDropdown handleThemeChange={(th) => setTheme(th)} /> */}
          <div className="flex gap-2">
            <span className="my-auto">
            Font Size:
            </span>
          <FontSizeDropdown onSelectChange={(f) => setFontSize(f)} />
          </div>
        </div>
        <div className="flex gap-2 items-center">
          {/* <Timer /> */}
          <button onClick={handleFullScreen} className="hover:bg-dark-4  hover:border-light-4 rounded-lg p-1">
            <div className="h-6 w-6 font-bold text-2xl text-white">
              {!isFullScreen ? (
                <AiOutlineFullscreen />
              ) : (
                <AiOutlineFullscreenExit />
              )}
            </div>
          </button>
        </div>
      </div>

      <Split
        className="!w-full flex-grow flex flex-col items-start px-4 pt-4"
        direction="vertical"
        minSize={100}
        // maxSize={400}
        expandToMin={true}
      >
        <CodeEditorWindow
          code={code}
          onChange={onChange}
          language={language.value}
          theme={theme.value}
          fontSize={fontSize.value}
        />

        <div className="!w-full min-h-[30%] flex flex-col">
          <div className="flex justify-end items-center gap-3">
            <button
              onClick={() => handleRun(customInput)}
              disabled={!code}
              className={`px-4 py-2 bg-dark-4 text-light-1 mt-2 rounded-lg text-sm`}
            >
              {isCodeRunning ? <Loader /> : "Run"}
            </button>
            {isForSubmission && (
              <button
                onClick={handleSubmit}
                disabled={!code}
                className={`px-4 py-2 bg-green-600 text-light-1 mt-2 rounded-lg text-sm`}
              >
                {isCodeSubmitting ? <Loader /> : "Submit"}
              </button>
            )}
          </div>

          <div className="flex gap-5 flex-grow">
              
            <div className="!w-full flex flex-col">
              <h1 className="font-bold text-lg">Custom Input</h1>
              <CustomInput
                customInput={customInput}
                setCustomInput={setCustomInput}
              />
            </div>
            <OutputWindow outputDetails={outputDetails} />
          </div>
        </div>
      </Split>
    </div>
  );
};

export default Playground;
