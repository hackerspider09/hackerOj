import React, { useEffect, useState } from 'react';
import Boxes from '../props/Boxes.js';
import SetQuestions from './SetQuestion.js';
import Popups from '../props/Popups.js';
import { axiosAuthInstance, CONTEST_ID } from '../../../Utils/AxiosConfig.js';

function Hero() {
  const [ques, setques] = useState({});
  const [text, setText] = useState([]);
  const [isError, setIsError] = useState('');

  const [buttonPopup, setButtonPopup] = useState(false);

  const getData = async () => {
    try {
      const res = await axiosAuthInstance.get(`/question/${CONTEST_ID}/questions/`);
      setques(res.data);
      // console.log(res.data);
      setText(res.data[0]);
    } catch (error) {
      setIsError(error.message);
    }
  };

  useEffect(() => {
    getData();
  }, []);

  let display = (id) => {
    const newDisplay = ques.filter((ques) => ques.questionNumber === id);
    setText(newDisplay[0]);
  };

  return React.createElement(
    'div',
    { className: 'container h-[86.5vh] w-full flex justify-center items-center bg-transparent overflow-y-auto ' },
    React.createElement(
      'div',
      { className: 'cont-left bg-blue- h-[100%] w-[100%] flex justify-center items-center flex-wrap gap-[100px] bg-transparent relative p-[80px]' },
      Array.isArray(ques) &&
        ques.map((question) =>
          React.createElement(Boxes, {
            key: question.questionNumber,
            dis: display,
            id: question.questionNumber,
            num: question.questionNumber,
            level: question.accuracy,
            quesData:question,
          })
        )
    ),
    // React.createElement(
    //   'div',
    //   { className: 'cont-right w-[30%] h-[100%] flex justify-center items-center bg-transparent max-sm:w-[0%]' },
    //   React.createElement(
    //     'div',
    //     { className: 'bigBox text-white h-[500px] w-[80%] border-[2px] border-solid border-white rounded-[20px] flex flex-col justify-center items-center max-sm:hidden' },
    //     React.createElement(SetQuestions, { ques: text })
    //   )
    // )
  );
}

export default Hero;
