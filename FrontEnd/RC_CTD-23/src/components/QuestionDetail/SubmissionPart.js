
'use client'
import React, { useEffect, useState } from 'react';
import { AiOutlineSolution } from "react-icons/ai";
import { ImYoutube2 } from "react-icons/im";
import { ImCheckboxChecked } from "react-icons/im";
import { useParams,useNavigate } from 'react-router-dom';
import { mockProblemsData } from './constants';
import { mockLearnPath } from './constants/modelQuestion';
import { axiosAuthInstance ,CONTEST_ID,addAuthToken} from '../../Utils/AxiosConfig';  
import { CopyToClipboard } from 'react-copy-to-clipboard';


const SubmissionPart = ({questionId}) => {
    
    const router = useNavigate();
    const endPoint = `/submission/${CONTEST_ID}/submissions/?question=${questionId}`;

    const [problems, setProblems] = useState([]);
    const [selectedCode, setSelectedCode] = useState('');
    const [Subdata,setSubdata] = useState([]);
    const [copied, setCopied] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);
    const [submissionsPerPage] = useState(10);



    useEffect(() => {
        const fetchProblems = async () => {
            // const response = await fetch('/api/getAllProblems');
            // const data = await response.json();
            setProblems(mockLearnPath);
        }
        fetchProblems();
    }, []);

    const indexOfLastSubmission = currentPage * submissionsPerPage;
    const indexOfFirstSubmission = indexOfLastSubmission - submissionsPerPage;
    const currentSubmissions = Subdata.slice(indexOfFirstSubmission, indexOfLastSubmission);

    const paginate = (pageNumber) => setCurrentPage(pageNumber);


    const getSubmissionTime=(submissionTime)=>{
        const dateTime = new Date(submissionTime);
        const hours = dateTime.getUTCHours();
        const minutes = dateTime.getUTCMinutes();
        const seconds = dateTime.getUTCSeconds();
        const timeString = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        return timeString;
    }

    useEffect(()=>{
      // console.log(endPoint);
        axiosAuthInstance.get(endPoint)
                .then((response) => {
                    // console.log("enter in then ");
                    if (response.status) {
                        // console.log("enter in then if ");
                        // console.log(response.data);
                        
                        setSubdata(response.data)
                    }
                    else {
                        
                        // console.log("Error In fetch");
                    }
                })
                .catch((error) => {
                  console.clear();
                    // console.log("enter in error ",error);
    
                })

                // const products = [{}]
      },[]);

    const difficultyColors = {
        'OA' : 'bg-red-500' ,
        'WA': 'bg-orange-500' ,
        'AC': 'bg-green-500'
    };

    // const openVideoPopup = (videoUrl) => {
    //     setSelectedVideo('8-k1C6ehKuw');
    // };

    const closeVideoPopup = () => {
        setCopied(false);
        setSelectedCode('');
    };

    return (
        <div className='z-50  bg-section-cl h-full'>
            <div className="p-10">
                <div className="relative overflow-x-auto sm:rounded-lg shadow-lg">
                    <table className="w-full text-sm text-left rtl:text-right ">
                        <thead className="text-xs text-white uppercase bg-dark-3">
                            <tr>
                                <th scope="col" className="p-4 text-slate-100">
                                    Language
                                </th>
                                <th scope="col" className="px-6 py-3 text-slate-100">
                                    Points
                                </th>
                                <th scope="col" className="px-6 py-3 text-slate-100">
                                    Time
                                </th>
                                <th scope="col" className="px-6 py-3 text-slate-100">
                                    Status
                                </th>
                                <th scope="col" className="px-6 py-3 text-slate-100">
                                    Code
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            {currentSubmissions.map((submisson, index) => (
                                <tr key={index} className="bg-dakr-2 hover:bg-dark-4">
                                    <td className="w-4 px-6 py-3">
                                        <div>
                                        {submisson.language}
                                        </div>
                                    </td>
                                    <td className="px-6 py-3 ">
                                        <div>
                                            {submisson.points}
                                        </div>
                                    </td>
                                    <td className="px-6 py-3 ">
                                        <div >
                                            {/* {submisson.submissionTime} */}
                                            {getSubmissionTime(submisson.submissionTime)}
                                        </div>
                                    </td>
                                    <td className="px-6 py-3">
                                        <div className={`w-fit mx-auto px-3 py-1 rounded-full text-sm text-light-1 ${ submisson.status ==='AC' || submisson.status ==='WA'  ? difficultyColors[submisson.status] : difficultyColors['OA'] }`}>
                                        {submisson.status}
                                        </div>
                                    </td>
                                    <td className="px-6 py-3 hover:cursor-pointer ">
                                        <span onClick={() => setSelectedCode(submisson.code)}>
                                            View
                                        </span>
                                    </td>
                                    {/* <td className="px-6 py-4 cursor-pointer">
                                        <ImYoutube2 color={'red'} size={35} onClick={() => openVideoPopup(problem.videoId)} />
                                    </td> */}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                <div >

                    <ul className="flex justify-center mt-4 flex-wrap gap-1">
                        {Array.from({ length: Math.ceil(Subdata.length / submissionsPerPage) }).map((_, index) => (
                            <li key={index} className="mx-1 list-none">
                                <button
                                    className={`px-4 py-2 ${currentPage === index + 1 ? 'bg-blue-500 text-white' : 'bg-gray-500 text-gray-800'} rounded`}
                                    onClick={() => paginate(index + 1)}
                                    >
                                    {index + 1}
                                </button>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>

            {selectedCode && (
                <div className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-75 flex justify-center items-center z-50">
                    <div className="bg-dark-1 p-8 rounded-lg flex flex-col items-end gap-2 h-3/5 w-2/4">
                        <div>
                            <CopyToClipboard text={selectedCode}>
                                <button  className="text-white border-1 px-3 py-2 rounded-md hover:text-gray-800 focus:outline-none mx-5" onClick={()=>{setCopied(true)}}>
                                {copied ? 'Copied!' : 'Copy'}
                                </button>
                            </CopyToClipboard>
                            <button onClick={closeVideoPopup} className="text-white border-1 px-3 py-2 rounded-md hover:text-gray-800 focus:outline-none">
                                Close
                            </button>

                        </div>
                        <div className='w-full overflow-y-auto'>
                            <pre>{selectedCode}</pre>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}

export default SubmissionPart;