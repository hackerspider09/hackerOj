import React, { useState } from 'react';
import axios from 'axios';
import { axiosAuthInstance, axiosNoAuthInstance } from '../Utils/AxiosConfig';


const Rctestcase = () => {
  const [questionId, setQuestionId] = useState('');

  const handleInputChange = (e) => {
    setQuestionId(e.target.value);
  };

  const handleButtonClick = async () => {
    try {
        console.log("wait")
        const response = await axiosAuthInstance.delete(`/contest/get_testcase/`,{
            data:{
                question:questionId
            }
        });
        console.log("responce ",response)
    } catch (error) {
        console.error('Error:', error);
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Enter questionId"
        value={questionId}
        onChange={handleInputChange}
      />
      <button onClick={handleButtonClick}>Delete Test Case RC</button>

      
    </div>
  );
};

export default Rctestcase;