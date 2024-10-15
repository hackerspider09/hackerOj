import React from 'react';
import Popups from "./Popups";
import { useState } from "react";
import Hero from "../component/Hero";
import SetQuestions from "../component/SetQuestion";
import funcStatus from "../component/Hero";
import images from '../asset';
import { Link } from "react-router-dom";

const Boxes = (props) => {
    let ID = props.id;
    let quesData = props.quesData;
    let quesNum =props.num;
    let display = props.dis;
    let waterLevel = props.level;
    function interpolate(minOutput, maxOutput, minValue, maxValue, value) {
        return maxOutput + (minOutput - maxOutput) * ((value - minValue) / (maxValue - minValue));
    }
    
    
    // let waterLevel = props.level ;
    let wateraccuracylevel = interpolate(-180, 80, 0, 100, waterLevel);
    // let wateraccuracylevel = interpolate(-180, 13, 0, 100, 100); //by def
    // let wateraccuracylevel = interpolate(-180, 50, 0, 100, 100);


    const [ques,setques] = useState([]);
    const [text,setText] = useState([]);
    const [buttonPopup, setButtonPopup] = useState(false);
    
    let Display = (id) => { 
        const newDisplay = ques.filter(ques => ques.id===id);
        setText(newDisplay);
    };
    

    const waveStyles = {
        position: 'absolute',
        width: '600px',
        height: '600px',
        top: wateraccuracylevel,
        left: '50%',
        background: '#fff',
        backgroundColor: '#4973ff',
        zIndex: '-1',
        borderRadius: '45%',
        background: 'red',
        animation: 'animate 10s linear infinite',
    };

    if (window.innerWidth <= 468) {
        waveStyles.width = '300px';
        waveStyles.height = '300px';
        waveStyles.borderRadius = '40%';
    }

    const waveAfterStyles = {
        position: 'absolute',
        width: '600px',
        height: '600px',
        top: wateraccuracylevel,
        left: '50%',
        background: 'rgba(0,0,0,0.5)',
        zIndex: '99',
        borderRadius: '40%',
        animation: 'animate 10s linear infinite',
    };

    if (window.innerWidth <= 468) {
        waveAfterStyles.width = '300px';
        waveAfterStyles.height = '300px';
        waveAfterStyles.borderRadius = '40%';
    }

    const waveBeforeStyles = {
        position: 'absolute',
        width: '600px',
        height: '600px',
        top: wateraccuracylevel,
        left: '50%',
        background: 'rgba(0,0,0,1)',
        zIndex: '1',
        borderRadius: '45%',
        animation: 'animate 10s linear infinite',
    };

    if (window.innerWidth <= 468) {
        waveBeforeStyles.width = '300px';
        waveBeforeStyles.height = '300px';
        waveBeforeStyles.borderRadius = '45%';
    }

    return (
        <React.Fragment>
            <style>{`
                    @keyframes animate {
                        0% {
                            transform: translate(-50%, -70%) rotate(0deg);
                        }
                        100% {
                            transform: translate(-50%, -70%) rotate(360deg);
                        }
                    }
                     @media only screen and (max-width: 468px) {
                        .bigBox {
                          /* Your styles for .bigBox on small screens */
                        }

                        .box{
                            width:125px;
                            height:120px;
                            z-index:;
                        }

                        .wave{
                            position: absolute;
                            width: 100px;
                            height: 100px;
                            top: waterLevel;
                            left: 50%;
                            background: #fff;
                            backgroundColor:#4973ff;
                            zIndex: -1;
                            borderRadius:45%;
                        }
                        .popups {
                            display: none; // Hide the Popups component on small screens
                            transition: all linear 1000ms;
                        }
                      }
                `}</style>
            <div className="box p-20  font-semibold border-[1px] border-solid border-[#424242] relative overflow-hidden rounded-[20px] flex justify-center items-center flex-wrap cursor-pointer z-[100] bg-[#1D3995] max-sm:py-[50px] " onClick={() => {
                    Display(ID);
                    display(ID);
                    setButtonPopup(true); 
                }}>
                {(waterLevel <=0) ? (
                    <>
                        <img className="h-[60px] w-[60px] z-[1000] rounded-[0%] absolute bottom-[5px] lefts-[10px] transition translate-y-3 coinAnime" src={images.treasureChest} alt="" />
                        <img className="h-[30px] w-[30px] z-[10] rounded-[0%] absolute bottom-[12px] right-[0px] transition translate-y-3 coinAnime" src={images.key1} alt="" />
                    </>
                ) : (
                    <>
                        <img className="h-[60px] w-[60px] z-[1000] rounded-[0%] absolute bottom-[10px] lefts-[10px] transition translate-y-3 coinAnime" src={images.treasureChestOpen} alt="" />
                        <img className="h-[60px] w-[60px] z-[1000] rounded-[0%] absolute bottom-[0px] right-[15px] transition translate-y-3 coinAnime" src={images.stackOfCoins} alt="" />
                    </>
                )}
                <div className='flex flex-col items-center gap-2'>
                    {/* <h1 className="Qname text-white text-[30px] z-[999] text-center">Q{quesNum}</h1> */}
                    <h2 className=" text-white text-xl z-[999] text-center">{quesData.title}</h2>
                    <p className=" text-white  z-[999] text-center">Points: {quesData.points}</p>
                    <p className=" text-white  z-[999] text-center">Accuracy: {waterLevel}%</p>
                    <button className='z-[999] px-2 py-1 text-black bg-white rounded-[10px] hover:scale-[1.05] hover:duration-[150ms] hover:bg-[#4973ff] hover:border-none hover:font-semibold hover:text-white'><Link to={`/question/${quesData.questionId}`}>{quesData.solvedByTeam ? "Solved" : "Solve"}</Link> </button>
                </div>
                <div className="wave  relative w-[100%] h-[100%] z-[98] flex justify-center items-center" style={waveStyles}></div>
                <div className="wave " style={waveAfterStyles}></div>
                <div className="wave" style={waveBeforeStyles}></div>
            </div>
            {/* {(window.innerWidth <= 468) && (
                <Popups trigger={buttonPopup} setTrigger={setButtonPopup} className="popups md:hidden">
                    <SetQuestions water={waterLevel} ques={text.filter((text) => text.id)} />
                </Popups>
            )} */}
        </React.Fragment>
    );
};
 
export default Boxes;
