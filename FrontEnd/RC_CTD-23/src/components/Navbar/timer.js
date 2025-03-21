import React, { useState, useEffect } from 'react';
import { axiosNoAuthInstance, CONTEST_ID } from '../../Utils/AxiosConfig';
import { useNavigate ,useLocation} from "react-router-dom";
import { RiTimerFlashLine } from "react-icons/ri";
import { MdAlarm } from "react-icons/md";

const CountdownRedirect = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const [targetTime, setTargetTime] = useState(null); // Initialize with null
    const [remainingTime, setRemainingTime] = useState("00 : 00 : 00");
    const [contestEndTimeFetched, setContestEndTimeFetched] = useState(false);

    useEffect(() => {
        axiosNoAuthInstance.get(`/contest/gettime/${CONTEST_ID}/`)
            .then((response) => {
                setTargetTime(new Date(response.data.endTime));
                setContestEndTimeFetched(true);
            })
            .catch((error) => {
                console.error("Error fetching contest end time:", error);
            });
    }, []);

    useEffect(() => {
        if (targetTime) {
            const intervalId = setInterval(() => {
                const now = new Date().getTime();
                const remain = targetTime.getTime() - now;
                
                if (remain <= 0) {
                    clearInterval(intervalId); // Stop the timer
                    navigate("/result"); 
                }
                // else if(location.pathname==='/result'){
                //     navigate("/question"); 
                // }
                else {
                    let seconds = Math.floor((remain / 1000) % 60);
                    let minutes = Math.floor((remain / (1000 * 60)) % 60);
                    let hours = Math.floor((remain / (1000 * 60 * 60)) % 24);

                    hours = hours < 10 ? '0' + hours : hours;
                    minutes = minutes < 10 ? '0' + minutes : minutes;
                    seconds = seconds < 10 ? '0' + seconds : seconds;

                    setRemainingTime(`${hours} : ${minutes} : ${seconds}`);
                }
            }, 1000);

            return () => {
                clearInterval(intervalId);
            };
        }
    }, [targetTime, navigate]);

    if (!contestEndTimeFetched) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <p className="mb-0 flex gap-2"><MdAlarm size={24} color="white" />  {remainingTime}</p>
        </div>
    );
};

export default CountdownRedirect;
