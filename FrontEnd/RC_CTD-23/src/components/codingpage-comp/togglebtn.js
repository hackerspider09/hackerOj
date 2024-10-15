import React, { useState } from 'react';

import TextField from '@mui/material/TextField';
import { AxiosInstance } from '../../Utils/AxiosConfig';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import Submission from "../submission-comp/submission"
import { useNavigate } from "react-router";
import {toast} from 'react-toastify';
import "./tinymce.css"
import HtmlReactParser from 'html-react-parser'
import QuestionDetailSection from './questiondetail'
const QuestionHubPage = (props) => {
  const [viewType, setViewType] = useState('question'); // Default to showing questions
  const qdata = localStorage.getItem('qdata');
  // console.log(qdata);


  



  return (

    <div>
      
      <div>
        <button onClick={() => setViewType('question')}  class="console-btn  btn-outline-dark">Question</button>
        <button onClick={() => setViewType('submissions')}  class="console-btn  btn-outline-dark">Submissions</button>
      </div>
      {viewType === 'question' ? <QuestionDetailSection QuesData={props.QuesData}/> : <SubmissionsSection questionId={props.QuesData.questionId} />}
    </div>
  );
};



const SubmissionsSection = (props) => {
  // Your submissions section JSX
  return (
    <Submission questionId = {props.questionId}/>
  );
};

export default QuestionHubPage;
