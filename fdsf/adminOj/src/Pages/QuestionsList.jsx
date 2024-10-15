import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { axiosNoAuthInstance } from '../Utils/AxiosConfig';


const QuestionsList = ({questionsData}) => {
    const [questions, setQuestions] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {

        if (questions !== null){
            setLoading(false);
        }
        setQuestions(questionsData);
    }, [questionsData]);


    if (loading) return <p>Loading questions...</p>;

    return (
        <div>
            <h2>Questions</h2>
            <ul>
                {questions.map(question => (
                    <li key={question.questionId}>{question.questionNumber}: {question.questionId}</li>
                ))}
            </ul>
        </div>
    );
};

export default QuestionsList;
