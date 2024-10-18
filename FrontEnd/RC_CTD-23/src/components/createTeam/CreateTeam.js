import React, { useState } from "react";
import "./createTeam.css";
import { axiosNoAuthInstance,CLASHID,RCID } from '../../Utils/AxiosConfig';
import { useNavigate } from "react-router";
import {toast} from 'react-toastify';
import { NavLink } from "react-router-dom";
const CreateTeam = () => {
//   const { loginState, setLoginState } = useContext(DataContext);
  const [loginState, setLoginState] = useState();

  if(loginState){};
  // const [isJunior,setIsJunior] = useState(false);
  const defaultDetails = {
    username1: "",
    username2: "",
    contestId :""
  };

  const [userDetails, setUserDetails] = useState(defaultDetails);
  const [isToggled, setIsToggled] = useState(false);
  const [contestID, setContestID] = useState(CLASHID);



    const handleToggleChange = (e) => {
          const newToggleState = !isToggled; // New toggle state
          setIsToggled(newToggleState); // Update the toggle state

          // Update contestID based on the new toggle state
          if (newToggleState) {
            setContestID(RCID); // If toggled, set to RCID
          } else {
            setContestID(CLASHID); // If not toggled, set to CLASHID
          }
        };

  const handleChange = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    const checked = e.target.checked;

    setUserDetails({ ...userDetails, [name]: value.trim() });

    if (name === 'isJunior') {
      setUserDetails({ ...userDetails, [name]: checked });
    }
    // e.tagrget==='isJunior'?
    // if(e.target.type=='checkbox') {

    //     setUserDetails({ ...userDetails, [name]: checked });

    // }
    // else{
    //     setUserDetails({ ...userDetails, [name]: value });
    // }

    // if('value' in e.target) {
    // this.setState({ [event.target.name]: event.target.value});

    // }

    // e.target.checked?setIsJunior(true):setIsJunior(false);

    // console.log(e.target.checked);

  };

  const navigate = useNavigate();

  const registerUser = (details) => {
    details.contestId = contestID;
    // console.log(details)
    const registerEndpoint = `/player/createteam/${contestID}/`;
    const id = toast.loading("Please wait...");

      axiosNoAuthInstance.post(registerEndpoint,details)
            .then((response) => {
                // console.log("enter in then ");
                if (response.status) {
                    // console.log("enter in then if ");
                    toast.update(id, { render: "Registered  successfully !", type: "success", isLoading: false, autoClose:3000 })
                    navigate("/");
                    // <Navigate to="/instruction" />
                    // window.location.reload(true);
                    // console.clear();
                
                }
                else {
                    toast.update(id, { render: response.data.error, type: "error", isLoading: false, autoClose:3000 })
                    // console.log("login failed");
                    // console.clear();
                }
            })
            .catch((error) => {
              // console.log("enter in error +",error);
              // toast.update(id, { render: error.response.data.msg[0], type: "error", isLoading: false, autoClose:3000 })
              // console.clear();
              if (error.response?.data?.msg){
                toast.update(id, { render: error.response.data.msg , type: "error", isLoading: false, autoClose:3000 })
              }else if(error.response?.data?.detail){

                toast.update(id, { render: error.response.data.detail , type: "error", isLoading: false, autoClose:3000 })
              }
              else if(error.response?.data?.username){

                toast.update(id, { render: error.response.data.username[0] , type: "error", isLoading: false, autoClose:3000 })
              }else if(error.response?.data?.password){

                toast.update(id, { render: error.response.data.password[0] , type: "error", isLoading: false, autoClose:3000 })
              }
              else{
                toast.update(id, { render: "An error occurred. Please try again later.", type: "error", isLoading: false, autoClose:3000 })
              }
            })
  };

  const submitDetails = (e) => {
    e.preventDefault();
    // console.log(userDetails);
    registerUser(userDetails);
  };

  // const handleCategoryChange = (e) =>{
  //   if(e.target.name == "junior"){
  //     setUserDetails({...userDetails, ["isJunior"]:true});
  //   }
  //   else{
  //     setUserDetails({...userDetails, ["isJunior"] : false})
  //   }
  // }

  return (
    <div className="fade-in">
      <div className="mt-0 p-sm-0 p-sm-1 ">
        <div className="container cont12 text-white p-3 p-sm-3 px-sm-4 mt-sm-0 log-style">
          <form onSubmit={submitDetails}>
            <div className="title mb-sm-3 mb-3 text-center">
              <h1>Create Team</h1>
              <small className="d-none">
                hello 
              </small>
            </div>
            <div className="input-group mb-2">
              <input
                type="text"
                className="form-control form-control-lg fs-6 input-style-register"
                placeholder=" Username 1"
                name="username1"
                value={userDetails.username1}
                onChange={handleChange}
                required={true}
              />
            </div>
            <div className="input-group mb-2">
              <input
                type="text"
                className="form-control form-control-lg fs-6 input-style-register"
                placeholder=" Username 2"
                name="username2"
                value={userDetails.username2}
                onChange={handleChange}
                required={true}
              />
            </div>

            


        <div className="flex items-center justify-center my-4">
              <span className="text-base font-medium text-gray-300">Clash</span>

              <div
                className={`mx-2 relative w-11 h-6 rounded-full transition-colors duration-200 ${
                  isToggled ? 'bg-blue-600' : 'bg-purple-700'
                }`}
                onClick={handleToggleChange} // Toggle when clicked
              >
                {/* Circle that moves when toggled */}
                <div
                  className={`absolute top-[2px] h-5 w-5 rounded-full bg-white border transition-transform duration-200 ${
                    isToggled ? 'translate-x-5' : 'translate-x-0'
                  }`}
                ></div>
              </div>

              <span className="text-base font-medium text-gray-300">RC</span>
            </div>

            <div className="input-group mb-2">
              <button className="btn btn-lg w-100 rounded-2 fs-6 btn12">
                Create Team
              </button>
            </div>

          </form>
        </div>
      </div>
    </div>
  );
};

export default CreateTeam;