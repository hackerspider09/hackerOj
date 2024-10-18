import React from 'react';
import './login.css';
import { useState } from "react";

import { useNavigate } from "react-router";

import { axiosNoAuthInstance, CONTEST_ID,CLASHID,RCID } from '../../Utils/AxiosConfig';
import {  toast } from 'react-toastify';
const endPoint = "/player/login/" 

export default function Login() {
    
    const navigate = useNavigate()
    const defaultCredentials ={
        username: "",
        password: "",
        isTeam:false,
        contestId:""
    }
    

    const [Logincred,setLogincred] = useState(defaultCredentials);
    const [LoginBtnClick,setLoginBtnClick] = useState(false);
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

        const handleChange = (event) => {
            const { name, type, value, checked } = event.target;
            
            // If the input is a checkbox, use `checked` instead of `value`
            const newValue = type === "checkbox" ? checked : value.trim();
        
            setLogincred({ ...Logincred, [name]: newValue });
        };
    
    const submitLoginForm = (e) => {
        e.preventDefault();
        userlogin(Logincred);  
    
    }


        const userlogin = (loginPayload)=>{
            // console.log("enter in login");
            // toast.dark('This is Toast Notification for Dark');
            // toast.info('This is Toast Notification for Dark');
            // toast.success('This is Toast Notification for Dark');
            // toast.warn('This is Toast Notification for Warn');
            // toast.error('This is Toast Notification for Error');
            const id = toast.loading("Please wait..");  
            if (!isToggled){
              setContestID(CLASHID);
            }else{
              setContestID(RCID);
            }
            loginPayload.contestId = contestID;
            setTimeout(() => {
              // console.log(endPoint)
              // console.log(loginPayload)
              axiosNoAuthInstance.post(endPoint,loginPayload)
            .then((response) => {
                // console.log("enter in then ");
                if (response.status) {
                    // console.log("enter in then if ");
                    // console.log(response)
                    setLoginBtnClick(false);
                    toast.update(id, { render: "Login Successful.", type: "success", isLoading: false, autoClose:3000 })
                    localStorage.setItem("isLogin", true);
                    localStorage.setItem("TOKEN", response.data.token);
                    localStorage.setItem("isJunior", response.data.isJunior);
                    localStorage.setItem("contestId", response.data.contestId);
                    localStorage.setItem("isContestEnded", false);
                    if (!isToggled){
                      localStorage.setItem("contestName", 'Clash');
                      
                    }else{
                      localStorage.setItem("contestName", 'RC');
                    }
                    navigate("/instruction");
                    window.location.reload(true);
                    // <Navigate to="/instruction" />
                    // window.location.reload(true);
                
                }
                else {
                  setLoginBtnClick(false);
                    // console.log("login failed");
                    toast.update(id, { render: "Please try again later." , type: "error", isLoading: false, autoClose:3000 })
                  }
                })
                .catch((error) => {
                  setLoginBtnClick(false);
                  setIsToggled(false)
                  setContestID(CLASHID)

                  console.clear();
                // console.log("enter in error +",error);
                if (error.response?.data?.msg){
                  toast.update(id, { render: error.response.data.msg , type: "error", isLoading: false, autoClose:3000 })
                }else if(error.response?.data?.detail){

                  toast.update(id, { render: error.response.data.detail , type: "error", isLoading: false, autoClose:3000 })
                }
                else{
                  toast.update(id, { render: "An error occurred. Please try again later.", type: "error", isLoading: false, autoClose:3000 })
                }
                setLogincred(Logincred)
            })
        }, 1000)

    }

//  const handleChange =(e) => {}
        
return (
    <>
<div className="LoginBox ">

<div className="controlheading">
    <h1>Login </h1>
  </div>
<form className="form" autoComplete="off"  onSubmit={submitLoginForm} >
 
  
  <div className="control block-cube block-input">
    <input name="username" type="text" placeholder="Username"  required={true} onChange={handleChange} />
    <div className="bg-top">
      <div className="bg-inner"></div>
    </div>
    <div className="bg-right">
      <div className="bg-inner"></div>
    </div>
    <div className="bg">
      <div className="bg-inner"></div>
    </div>
  </div>
  <div className="control block-cube block-input">
    <input name="password" type="password" placeholder="Password"  required={true} onChange={handleChange} />
    <div className="bg-top">
      <div className="bg-inner"></div>
    </div>
    <div className="bg-right">
      <div className="bg-inner"></div>
    </div>
    <div className="bg">
      <div className="bg-inner"></div>
    </div>
  </div>

  <div>
        <label>
          <input
            type="checkbox"
            name="isTeam"
            checked={Logincred.isTeam}
            onChange={handleChange}
          />
          IsTeam
        </label>
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

{/* 
            <div className="im-buttons">
                <label className="radio" id="a-button">
                    <input name="im-buttons" type="radio" id="a-button" checked="checked" />
                    <span>Junior</span></label><label className="radio" id="b-button"><input name="im-buttons"
                        type="radio" id="b-button" /><span>Senior</span></label></div> */}

  <button className="btn block-cube block-cube-hover" type="submit">
    <div className="bg-top">
      <div className="bg-inner"></div>
    </div>
    <div className="bg-right">
      <div className="bg-inner"></div>
    </div>
    <div className="bg">
      <div className="bg-inner"></div>
    </div>
    <div>
    {!LoginBtnClick ? (
                <div className="text" onClick={()=>{setLoginBtnClick(true)}}>
                    Login
                </div>
            )
            :
            (
                <div className="text" style={{ opacity: 0.5 }}>
                    Logging in...
                </div>
            )
            }
    </div>
    {/* <div className="text" onClick={()=>{setLoginBtnClick(true)} } >Login</div> */}
  </button>

</form>
</div>



</>
    
    )
}









    
