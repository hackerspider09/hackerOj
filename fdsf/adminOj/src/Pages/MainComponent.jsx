import React, { useState, useEffect } from 'react';
import ExecutionServerList from './ExecutionServerList';
import QuestionsList from './QuestionsList';
import TestCaseStatusTable from './TestCaseStatusTable';
import axios from 'axios';
import { axiosAuthInstance, axiosNoAuthInstance } from '../Utils/AxiosConfig';


const MainComponent = () => {
    const [servers, setServers] = useState([]);
    const [questions, setQuestions] = useState([]);
    const [contestId,setContestId] = useState("7e315")

    useEffect(() => {
        fetchServers();
        fetchQuestions();
    }, []);

    const fetchServers = async () => {
        try {
            const response = await axiosAuthInstance.get('/contest/list_execution_server/');
            setServers(response.data);
            console.log("exec ",response)
        } catch (error) {
            console.error('Error fetching servers:', error);
        }
    };

    const fetchQuestions = async () => {
        try {
            const response = await axiosAuthInstance.get(`/question/${contestId}/get_questions_id/`);
            setQuestions(response.data);
            console.log("ques",response)
        } catch (error) {
            console.error('Error fetching questions:', error);
        }
    };

    return (
        <div>
            <ExecutionServerList serversData={servers} setServersData={setServers} />
            <QuestionsList questionsData={questions} />
            <TestCaseStatusTable servers={servers} questions={questions} />
        </div>
    );
};

export default MainComponent;
