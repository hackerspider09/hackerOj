import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom';
import { AiOutlineLike, AiFillLike, AiOutlineDislike, AiFillDislike } from "react-icons/ai";
import { FaRegStar, FaStar } from "react-icons/fa";
import { TiInputChecked ,} from "react-icons/ti";
// import TextSolutions from './TextSolutions';
import CustomInput from "./shared/CustomInput";
import { mockLearnPath } from './constants/modelQuestion';
import { axiosAuthInstance ,CONTEST_ID,addAuthToken} from '../../Utils/AxiosConfig';  
import Loader from "./shared/Loader";
import {  toast } from 'react-toastify';
import DescriptionPart from './DescriptionPart'
import SubmissionPart from './SubmissionPart'

const ProblemDesc = ({ problems }) => {

    const params = useParams();
    const QuestionId = params.questionId;
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

    

    useEffect(() => {
        if (problems) {
            // console.log(problems)
            problems.forEach((problem, index) => {
                // console.log("inside problemdes",problem," ",params)
                if (problem.questionId === params.questionId) {
                    setClickedProblems(problem);
                    setClickedProblemId(problem.questionId);
                }
            })
        }

    }, [problems]);

    const handelLikedproblems = async () => {

    }

    const handelDisLikedproblems = async () => {

    }

    const handelFavoritesproblems = async () => {
    
    }

    return (
        <div className='w-full flex flex-col overflow-x-hidden overflow-y-auto px-1'>
            <div className='flex h-11 w-full gap-3 items-center pt-2 bg-dark-3 rounded-t-lg px-2'>
                <div className={` ${crntSection ? 'bg-section-cl' : 'bg-dark-4'}  rounded-t-md px-5 py-[10px] text-sm cursor-pointer`} onClick={() => setCrntSection(true)}>
                    Description
                </div>
                <div className={`${crntSection ? 'bg-dark-4' : 'bg-section-cl'}  rounded-t-md px-5 py-[10px] text-sm cursor-pointer`} onClick={() => setCrntSection(false)}>
                    Submission
                </div>
            </div>
            {  
                crntSection ?
                <>
                <DescriptionPart questionData={clickedProblems} />
                
                </>

                :
                <SubmissionPart questionId={QuestionId}/> 
            }

            
        </div>
    )
}

export default ProblemDesc
