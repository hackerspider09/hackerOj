import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { axiosNoAuthInstance } from '../Utils/AxiosConfig';


const TestCaseStatusTable = ({ servers, questions }) => {
    const [testCaseStatus, setTestCaseStatus] = useState({});

    useEffect(() => {
        servers.forEach(server => {
            fetchTestCaseStatus(server);
        });
    }, [servers, questions]);

    const fetchTestCaseStatus = async (server) => {
        try {
            const response = await axios.get(`http://${server.address}:${server.port}/core/get_testcase_detail/`);
            console.log("serve ",response.data)

            let server_data = {}

            response.data.forEach(ques => {
                server_data[ques.question] = ques.isFetched
            });

            console.log(server_data)
            setTestCaseStatus(prevStatus => ({
                ...prevStatus,
                [server.address]: server_data,
            }));
            // console.log(testCaseStatus)
        } catch (error) {
            console.error('Error fetching test case status:', error);
        }
    };

    return (
        <div>
            <h2>Test Case Status</h2>
            <table>
                <thead>
                    <tr>
                        <th>Server</th>
                        {questions.map(question => (
                            <th key={question.questionNumber}>{question.questionId}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {servers && servers.map(server => (
                        <tr key={server.address}>
                            <td>{server.address}:{server.port}</td>
                            {questions && questions.map(question => (
                                 <td key={question.questionNumber}>
                                    {testCaseStatus[server.address]?.[question.questionId] ? 'Fetched' : 'Not Fetched'}
                                 </td>
                            ))}
                            {/* {questions.map(question => (
                                <td key={question.id}>
                                    {testCaseStatus[server.address]?.[question.question]?.question.isFetched ? 'Fetched' : 'Not Fetched'}
                                </td>
                            ))} */}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default TestCaseStatusTable;




