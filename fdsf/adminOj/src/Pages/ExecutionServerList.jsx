import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { axiosAuthInstance, axiosNoAuthInstance,CONTEST_ID } from '../Utils/AxiosConfig';


const ExecutionServerList = ({serversData,setServersData}) => {
    const [servers, setServers] = useState(null);
    const [address, setAddress] = useState('');
    const [port, setPort] = useState('');
    const [loading, setLoading] = useState(true);

    // Fetch servers on mount
    useEffect(() => {
        if (servers !== null){
            setLoading(false);
        }
        setServers(serversData);
    }, [serversData]);


    const createServer = async () => {
        try {
            const response = await axiosAuthInstance.post('/contest/list_execution_server/', { address, port });
            setServers([...servers, response.data]);
            setAddress('');
            setPort('');
        } catch (error) {
            console.error('Error creating server:', error);
        }
    };

    const deleteServer = async (address) => {
        try {
            await axiosAuthInstance.delete(`/contest/list_execution_server/${address}/`);
            setServers(servers.filter(server => server.address !== address));
        } catch (error) {
            console.error('Error deleting server:', error);
        }
    };

    //! build this it is not comple
    const fetchTestcases = async (address,port) => {
        const payload={
            'address':address,
            'port':port,
            'contest':CONTEST_ID
        }
        try {
            await axiosAuthInstance.post(`/contest/get_testcase_on_execution_server/`,payload);
        } catch (error) {
            console.error('Error in fetch testcase :', error);
        }
    };
    const deleteFetchTestcases = async (address, port) => {
        const payload = {
            address: address,
            port: port,
            contest: CONTEST_ID
        };
        await axiosAuthInstance.delete(`/contest/get_testcase_on_execution_server/`, {data:payload})
        .then(response => {
            console.log('Successfully deleted:', response);
        })
        .catch(error => {
            console.error('Error in delete fetch testcase:', error);
        });
    };
    

    if (loading) return <p>Loading servers...</p>;

    return (
        <div>
            <h2>Execution Servers</h2>
            <ul>
                {servers.map(server => (
                    <li key={server.address}>
                        {server.address}:{server.port}
                        <button onClick={() => deleteServer(server.id)}>Delete</button>
                        <button onClick={() => fetchTestcases(server.address,server.port)}>Fetch all TC</button>
                        <button onClick={() => deleteFetchTestcases(server.address,server.port)}>Delete all TC</button>
                    </li>
                ))}
            </ul>
            <div>
                <h3>Add New Server</h3>
                <input
                    type="text"
                    placeholder="Address"
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Port"
                    value={port}
                    onChange={(e) => setPort(e.target.value)}
                />
                <button onClick={createServer}>Create Server</button>
            </div>
        </div>
    );
};

export default ExecutionServerList;
