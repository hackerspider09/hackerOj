import React from "react";
import { Link } from "react-router-dom";

const SetQuestions = ({ ques }) => {
    const waterLevel = ques.accuracy;
  
    return (
      React.createElement(React.Fragment, null,
        React.createElement('div', { className: 'ques h-[100%] w-[100%] bg-[#0a082d] rounded-[20px] flex flex-col justify-center items-center p-[2vw] gap-[20px]', key: ques.id },
          React.createElement('h1', { className: 'text-white text-[30px]' }, ques.questionNumber),
          React.createElement('h1', { className: 'text-white text-[30px]' }, ques.title),
          React.createElement('p', { className: 'text-white text-center' }, `Points: ${ques.points}`),
          <Link to={`/question/${ques.questionId}`}>{
          (waterLevel <= 0) ? (React.createElement('button', { className: 'px-[20px] py-[10px] text-black bg-white rounded-[10px] hover:scale-[1.05] hover:duration-[150ms] hover:bg-[#4973ff] hover:border-none hover:font-semibold hover:text-white', id: 'ques-btn' }, 'SOLVE')) : (React.createElement('div', { className: 'px-[20px] py-[10px] text-black bg-white rounded-[10px] hover:scale-[1.05] hover:duration-[150ms] hover:bg-zinc-700 hover:border-none hover:font-semibold hover:text-white', id: 'ques-btn' }, 'SOLVED'))}
          </Link>
        )
      )
    );
  };
  
  export default SetQuestions;