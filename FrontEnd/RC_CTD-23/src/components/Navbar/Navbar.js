import { Link,useNavigate,useLocation } from 'react-router-dom'  
import React,{useEffect,useState} from 'react'
// import NavLinks from './NavLinks'
import CountdownRedirect from "./timer"

const Navbar =() => {
    const nav = useNavigate();

  const location = useLocation();
  
  const [loggedIn, setLoggedIn] = useState(false);
  const [isClash, setIsClash] = useState(1);


  // Check local storage for login status on initial load
  useEffect(() => {
    
    const userIsLoggedIn = localStorage.getItem('isLogin') === 'true';
    if(localStorage.getItem('contestName')==='Clash'){
      setIsClash(2);
    }else if(localStorage.getItem('contestName')==='RC'){
      setIsClash(3);
    }else{
      setIsClash(1);
    }
    setLoggedIn(userIsLoggedIn);
  }, []);

  const handleLogout = () => {
        localStorage.clear();
        setLoggedIn(false);
        // <Navigate to = "/" />
        // Redirect("/")
        // Redirect("/login");
        nav("/");
        window.location.reload(true);
    };


  return (
    <div className='w-full bg-navbar-bg-col '>

      <div className='mx-4 flex justify-between items-center '>

        <div className='flex justify-between items-center gap-7'>
          {/* <Link href='/'>
            <h2 className='font-bold text-xl'>
              Clash
            </h2>
          </Link> */}
            <div className='h-full'>
                <a 
                    // href="https://ctd.credenz.in"
                    >
                      {
                        isClash === 1 ? <img src="https://i.postimg.cc/Xq8WxPwn/Credenz-24.png" alt="PISBLogo" className='h-16'/> :
                        isClash === 2 ? <img src="https://i.postimg.cc/KzG14QPw/clash.png" alt="PISBLogo" className='h-16'/> : <img src="https://i.postimg.cc/50nbjgvw/revb.png" alt="PISBLogo" className='h-14'/>
                      }
                      {/* <img src="https://i.postimg.cc/50nbjgvw/revb.png" alt="PISBLogo" className='h-14'/> */}
                      {/* <img src="https://i.postimg.cc/KzG14QPw/clash.png" alt="PISBLogo" className='h-16'/> */}
                      
                    </a>
            </div>
            {/* <NavLinks /> */}
          </div>
        <div className='flex justify-between items-center gap-7'>
            {loggedIn && <CountdownRedirect />}
                

                    {/* <ul> { !loggedIn ? <Link to="/register"  className='nav-link' >Register</Link> : "" } </ul> */}
                    <ul> { loggedIn && localStorage.getItem("contractAccept") ? <Link to="/question"  className='nav-link' >QuestionHub</Link> : "" } </ul>
                    <ul> <Link to="/leaderboard"  className='nav-link' >Leaderboard</Link>  </ul>
                    <ul> { loggedIn ?  "" : <Link to="/register"  className='nav-link' >Register</Link> } </ul>
                    <ul> { loggedIn ?  "" : <Link to="/login"  className='nav-link' >Login</Link> } </ul>
                    <ul> { loggedIn ?  "" : <Link to="/createTeam"  className='nav-link' >Create Team</Link> } </ul>
                    <ul> {loggedIn && (<button onClick={handleLogout} className = "btn border border-white rounded text-light btnlog">Log Out</button>)} </ul>
        </div>


      </div>
    </div>
  )
}

export default Navbar