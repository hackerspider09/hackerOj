import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom';
import { TiInputChecked ,} from "react-icons/ti";
import Loader from "./shared/Loader";
import { axiosAuthInstance ,CONTEST_ID,addAuthToken} from '../../Utils/AxiosConfig';  
import {  toast } from 'react-toastify';
import CustomInput from "./shared/CustomInput";
import "./tinymce.css"

export default function DescriptionPart({questionData}) {
    const QuestionId = questionData?.questionId;
    const [isCodeRunning, setIsCodeRunning] = useState(false);

    const [customInput, setCustomInput] = useState("");
    const [customOutput, setCustomOutput] = useState("");
    const [clickedProblems, setClickedProblems] = useState();
    const [clickedProblemsId, setClickedProblemId] = useState('"is_even"');
    const [like, setLike] = useState(false);
    const [disLike, setDisLike] = useState(false);
    const [favorite, setFavorite] = useState(false);
    const [crntSection, setCrntSection] = useState(true);


    const difficultyColors = {
        'Hard' : 'bg-red-500' ,
        'Medium': 'bg-orange-500' ,
        'Easy': 'bg-green-500'
    };

    const TakeIpOp = (input) => {
        setIsCodeRunning(true);
       console.log("RC run");
       
         const takeIpopEndpoint = `submission/${CONTEST_ID}/runrccode2/`;
         const takeipoppayload = {
   
             'question':`${QuestionId}`,
       
             'input': `${input}`,
           }
         //   console.log(takeipoppayload)
         axiosAuthInstance.post(takeIpopEndpoint,takeipoppayload)
       .then((response) => {
           // console.log("enter in then ");
           if (response) {
            setIsCodeRunning(false);
            let data = response.data;
            setCustomOutput(data.output)
               console.log(response.data);
               // toast.update(id, { render: "Build Process Finished", type: "success", isLoading: false, autoClose:3000 })
               // <Navigate to="/instruction" />
               // window.location.reload(true);
           
           }
           else {
            setIsCodeRunning(false);
               // toast.update(id, { render: "Server is Busy", type: "error", isLoading: false, autoClose:3000 })
               // console.log("login failed");
           }
       })
       .catch((error) => {
        setIsCodeRunning(false);
        // console.clear();
           console.log(" error => ",error.response);
           if (error.response?.data?.msg) {
            toast.error(error.response.data.msg, { 
                type: "error", 
                isLoading: false, 
                autoClose: 3000 
            });
        } else {
            toast.error("An error occurred. Please try again later.", { 
                type: "error", 
                isLoading: false, 
                autoClose: 3000 
            });
        }
       
       })
 
      
   
   }

    return (
    <div className='bg-section-cl rounded-b-lg flex-grow p-2' >
                <h2 className='font-semibold text-xl py-2 mx-5'>
                    {questionData?.questionNumber}. {questionData?.title}
                </h2>
                {/* section 1 */}
                <div className='flex items-center justify-start py-2 mx-5'>
                    <div className={`px-4 py-1 rounded-full text-sm text-light-1 ${difficultyColors[questionData?.difficultyText]}`} >
                        {questionData?.difficultyText}
                    </div>
                    {/*  Solved Section  */}
                    <div className='mx-2 cursor-pointer' >
                        {questionData?.solvedByTeam && <TiInputChecked size={30} color={'green'} />}
                        
                    </div>
                    
                </div>
                {/* section 2 */}
                <div className='  py-2 mx-5 '>
                    {/* For HTML content Rendering */}
                    <div dangerouslySetInnerHTML={{ __html: questionData?.description || '' }} />
                </div>
                {/* section 3 */}
                {/* <div className='mt-4 px-5'>
                    <h2 className='font-bold'>Input Format</h2>
                    <div dangerouslySetInnerHTML={{ __html: questionData?.ipFormate || '' }} />
                </div>
                <div className='mt-4 px-5'>
                    <h2 className='font-bold'>Output Format</h2>
                    <div dangerouslySetInnerHTML={{ __html: questionData?.opFormate || '' }} />
                </div>
                <div className='mt-4 px-5'>
                    <h2 className='font-bold'>Sample Input</h2>
                    <div className='bg-light-3 font-mono mt-1 py-2 px-3 rounded-lg'>
                        <div dangerouslySetInnerHTML={{ __html: questionData?.sampleIp || '' }} />
                    </div>
                </div>
                <div className='mt-4 px-5'>
                    <h2 className='font-bold'>Sample Output</h2>
                    <div className='bg-light-3 font-mono mt-1 py-2 px-3 rounded-lg'>
                        <div dangerouslySetInnerHTML={{ __html: questionData?.sampleOp || '' }} />
                    </div>
                </div>
                <div className='mt-2 px-5 py-2'>
                    {questionData?.constraints && (
                        <>
                            <p className='font-bold'>Constraints:</p>
                            <div className='font-medium' 
                                dangerouslySetInnerHTML={{ __html: questionData?.constraints || '' }} 
                            />
                        </>
                    )}
                </div> */}

                <div className="flex  flex-grow my-2 mx-5">
                    {
                            localStorage.getItem('contestName') ==='RC' &&

                    <>
                    <div className="!w-full flex flex-col">
                    <h1 className="font-bold text-lg">Custom Input</h1>
                    <CustomInput
                        customInput={customInput}
                        setCustomInput={setCustomInput}
                    />
                    </div>
                    <div className='w-full flex justify-center items-center flex-col'>
                        
                        
                        <button
                            onClick={() => TakeIpOp(customInput)}
                            disabled={!customInput}
                            className={`px-4 py-2  bg-dark-4 text-light-1 mt-2 rounded-lg text-sm`}
                            >
                            {isCodeRunning ? <Loader /> : "Get O/P"}
                            </button>
                    </div>
                    <div className="!w-full flex flex-col">
                    <h1 className="font-bold text-lg">Custom Output</h1>
                    <CustomInput
                        customInput={customOutput}
                        setCustomInput={setCustomOutput}
                        setDisable={true}
                        />
                    </div>
                    </>
                        }
                </div>

            </div>
  )
}
