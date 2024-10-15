import React, { useState, useEffect } from 'react';

import {BrowserRouter,Route, Routes ,Navigate} from "react-router-dom";
import Instruct from "./components/instruct-comp/instruct";
// import Mobileview from './components/codingpage-comp/mobileview/mobileview';
import Codingpage from "./components/codingpage-comp/codingpage";
// import Submission from "./components/submission-comp/submission";
import Leaderboard from "./components/leaderb-comp/leaderboard";
import Result from "./components/result-comp/result";
import Login from "./components/loginpage-comp/login";
import Form from "./components/regester/register";
// import QuestionHubPage from "./components/test_component/hello69";
// import axios from "./components/axios";
import { ToastContainer } from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';
import {isTimeOver} from './Utils/utils';
import ProtectedRoute from './ProtectedRoute';
import Workspace from './components/QuestionDetail/Workspace';
import Navbar from "./components/Navbar/Navbar";
import Hero from "./components/Questionhub/component/Hero"
import Register from './components/regester/register';
import CreateTeam from './components/createTeam/CreateTeam';
import OpenInVSCodeButton from './components/vscode/OpenInVSCodeButton';

// function displayOnlyOnDesktop() {
//   const isMobile = window.matchMedia("only screen and (max-width: 760px)").matches;

//   if(isMobile){
//     return <div>Sorry, this website is only available on desktop devices.</div>
// }
// }


function App() {

  const [loggedIn, setLoggedIn] = useState(false);
  const [accessExpired, setAccessExpired] = useState(false);
  const [IsAccepted, setIsAccepted] = useState(false);
  const [showMobileWarning, setShowMobileWarning] = useState(false);
  // Check local storage for login status on initial load


  
  useEffect(() => {
    if(window.innerWidth <= 800)
      setShowMobileWarning(true)
    const userIsLoggedIn = localStorage.getItem('isLogin') === 'true';
    const contractAccept = localStorage.getItem('contractAccept') === 'true';
    // console.log("cecking ",userIsLoggedIn);

    setLoggedIn(userIsLoggedIn);
    setIsAccepted(contractAccept);

  }, []);
  // }, [loggedIn,accessExpired]);


  const handleLogout = () => {
    localStorage.removeItem('isLogin');
    localStorage.removeItem('TOKEN');
    localStorage.removeItem('isJunior');
    setLoggedIn(false);
  };

  return (
   
    <>
  
  
    <BrowserRouter>
  
    <div className='max-h-screen' onCopy={(e) => {
        e.preventDefault();
        // alert('Copying is not allowed.');
      }}>
      <div>
        <Navbar />
      </div>
      
      <ToastContainer
        position="top-center"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="dark"
      />
      <div>

        <Routes>
          {/* <Route path="/vs" element={ <OpenInVSCodeButton code="print()" input="69" output="96" />} /> */}
          <Route path="/" element={loggedIn  ? IsAccepted ? <Navigate to="/question" /> : <Navigate to="/instruction" /> : <Login />} />
          <Route path="/register" element={loggedIn  ? <Navigate to="/question" /> : <Register />} />
          <Route path="/login" element={loggedIn  ? IsAccepted ? <Navigate to="/question" /> : <Navigate to="/instruction" /> : <Login />} />
          <Route path="/createTeam" element={ <CreateTeam /> } />
          <Route path="/instruction" element={loggedIn && !IsAccepted ?  <Instruct />  : loggedIn && IsAccepted ? <Navigate to="/question" /> : <Navigate to="/" />} />
          <Route path="/leaderboard" element={<Leaderboard /> } />
            <Route path="/result" element={ <Result />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/question/:questionId" element={<Workspace/>} />
            
            {/* <Route path="/questionHub" element={<Hero/>} /> */}
            {/* <Route path="/question" element={loggedIn ? <Quescards /> : <Navigate to="/" />} /> */}
            <Route path="/question" element={loggedIn ? <Hero/> : <Navigate to="/" />} />
          </Route>

        </Routes>
    
      </div>

    </div>
    </BrowserRouter>
  
    </>
  );
 
}

export default App;
