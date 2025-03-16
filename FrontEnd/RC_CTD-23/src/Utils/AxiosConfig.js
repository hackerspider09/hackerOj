import axios from "axios";
// export const CONTEST_ID = "96e83";
let CONTEST_ID = "";


if (localStorage.getItem('contestId')){
    CONTEST_ID = localStorage.getItem('contestId')
}



// export const API_URL = "https://clashrc.admin.credenz.in";
export const API_URL = "https://clashrcbackend.credenz.co.in";
export const API_DOMAIN = "clashrcbackend.credenz.co.in";
export const WEBSOCKETURL = "wss://clashrcbackend.credenz.co.in";

export const CLASHID = "7f9f5";
export const RCID = "d7b53"


const axiosNoAuthInstance = axios.create({
    baseURL: API_URL,
});

const axiosAuthInstance = axios.create({
    baseURL: API_URL,
});

axiosAuthInstance.interceptors.request.use(
    (config) => {
        if(localStorage.getItem("TOKEN")){
            config.headers.Authorization = `Bearer ${localStorage.getItem("TOKEN")}`;
        }        
        return config;
    },
    (error) => {
        
        return Promise.reject(error);
    }
)

axiosAuthInstance.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        // console.log("erro rfrom axios conf",error)
        if (error.response && error.response.status === 401) {
            
            // Unauthorized access, redirect to login page
            localStorage.removeItem("TOKEN");
            localStorage.removeItem("isJunior");
            localStorage.removeItem("isLogin");
            localStorage.removeItem("contractAccept");
            window.location.href = "/login"; 
            // else if delete message check if needed
        }else if (error.response && error.response.status === 403 && error.response.data.detail==="Contest Has Ended."){
            window.location.href = "/result"; 

        }
        // else{
        //     localStorage.clear();
        //     window.location.href = "/login"; 
        // }
        return Promise.reject(error);
    }
);

export {axiosAuthInstance, axiosNoAuthInstance,CONTEST_ID};
