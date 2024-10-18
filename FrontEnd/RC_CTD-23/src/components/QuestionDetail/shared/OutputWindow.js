import React,{useEffect,useState} from "react";
import { useCustomContext } from "../../../context/CustomeContext";


const AnimatedCounter = ({ targetNumber }) => {
  const [currentCount, setCurrentCount] = useState(0);
  useEffect(() => {
    let count = 0;
    if(count<targetNumber){

      const interval = setInterval(() => {
        count += 1;
        setCurrentCount(count);
        if (count >= targetNumber) {
          clearInterval(interval);
        }
      }, 400); // Adjust the speed of the counting by changing the interval duration (in milliseconds)
      return () => clearInterval(interval); // Cleanup on unmount
    }

  }, [targetNumber]);

  return <span>{currentCount}</span>;
};


const OutputWindow = ({ outputDetails }) => {
  const { confetiStart,setConfetistart } = useCustomContext();
  // console.log(outputDetails)

  const difficultyColors = {
    'OA' : 'bg-red-500' ,
    'WA': 'bg-orange-500' ,
    'AC': 'bg-green-500'
};

useEffect(() => {
  // setConfetistart(true);
  if (outputDetails?.submitted && outputDetails?.finalStat==="AC") {
    // console.log("zulmule")
    setConfetistart(true);
    const timer = setTimeout(() => {
      setConfetistart(false);
    }, 5000);

    // Clear the timer and set isActive to false when component unmounts or when the status changes
    return () => clearTimeout(timer);
  }
}, [outputDetails?.submitted]);

  return (
    <div className="!w-full flex-grow flex flex-col ">
      <h3 className="font-bold text-lg mb-2">Output</h3>
      
      {outputDetails?
        (outputDetails.submitted ? (
          <div className="w-full flex flex-col justify-center content-center flex-grow bg-dark-2 rounded-lg text-white p-2 font-mono text-sm overflow-y-auto">
            <div className="text-lg flex-col justify-center content-center text-center">
              <p>
                Status:{" "}
              </p>
              <p
                className={`${outputDetails.finalStat==="AC" ? "text-green-500" : "text-red-500"}`}
              >
                {outputDetails.finalStat}
              </p>
            </div>
            <div className="text-lg flex-col justify-center content-center text-center">
              <p>
              Test Cases Passed:{" "}
              </p>
              <p className="text-blue-500">
              <AnimatedCounter targetNumber={outputDetails.correctSubmissions} /> / {outputDetails.totalSubmissions}
              </p>
            </div>
            
          </div>
        ) : (
          <div className="w-full flex flex-col flex-grow bg-dark-2 rounded-lg text-white p-2 font-mono text-sm overflow-y-auto">

            <textarea
              value={outputDetails.error ? outputDetails.error : outputDetails.output}
              className="flex-grow bg-dark-2 resize-none"
              disabled
            ></textarea>
            </div>
        )) : (
          <div className="w-full flex flex-col flex-grow bg-dark-2 rounded-lg text-white p-2 font-mono text-sm overflow-y-auto" />
        )}
    </div>
  );
};

export default OutputWindow;
