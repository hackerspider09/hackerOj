
import Split from "react-split";
import ProblemDesc from "./ProblemDesc";
import Playground from "./Playground";
import { useState ,useEffect} from "react";
import Confetti from "react-confetti";
import { axiosAuthInstance ,CONTEST_ID,addAuthToken} from '../../Utils/AxiosConfig';  
import { useCustomContext } from "../../context/CustomeContext";


const Workspace = () => {
    const endPoint = `/question/${CONTEST_ID}/questions/`

    const { confetiStart } = useCustomContext();

	const [submitted, setSubmitted] = useState(false);
	const [problems, setProblems] = useState([]);
    const [loading, setLoading] = useState(true);

  useEffect(()=>{
   
    // setLoading(true);
    
    axiosAuthInstance.get(endPoint) 
            .then((response) => {
                // console.log("enter in then ");
                if (response.status) { 
                    // console.log("enter in then if ");
                    // console.log("from workspace",response.data);
                    setProblems(response.data)
                    const questionDetails = {};  
                  for(let i = 1; i <=response.data.length; i++) {
                    
                       questionDetails[i] = response.data[i-1].questionId;

                   }
                   localStorage.setItem("qdata",JSON.stringify(questionDetails));
                  //  setTimeout(()=>{
                    // setLoading(false);

                  // },5000);
                  setLoading(false);
                  }
                else {
                  // console.log("Error In fetch");
                }
              })
              .catch((error) => {
                // nav("/question");
              // console.log("enter in error ",error);
              console.clear();
            //   setLoading(false);


            })


  },[]);
	
	return (
		<>
			{confetiStart && <Confetti gravity={0.3} tweenDuration={5000} />}
            {!loading ?
			<Split className='split px-1 h-[92vh]' minSize={500}>
				<ProblemDesc problems={problems} />
				<Playground problems={problems} setSubmitted={setSubmitted} />
			</Split>
            :
            "Wait loading"
            }
		</>
	);
}

export default Workspace
