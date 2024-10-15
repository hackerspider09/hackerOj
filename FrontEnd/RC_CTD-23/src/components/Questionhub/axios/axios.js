import axios from "axios";
const API_URL = ' http://127.0.0.1/';
const contestId = '8acff';

// we need to pass the baseURL as an object
const axiosNoAuthInstance = axios.create({
  baseURL: API_URL ,
});

const axiosAuthInstance = axios.create({
  baseURL: API_URL,
});

axiosAuthInstance.interceptors.request.use(
  (config) => {
      // const token = localStorage.getItem('TOKEN');
      const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEzMDI4MDI2LCJpYXQiOjE3MTMwMTcyMjYsImp0aSI6IjI2ZGE2YmNhODliYjRmMDU5NWQwMzZlOGFhOTU3NzA0IiwidXNlcl9pZCI6MX0.gKCdfrtIR4Sa9Ne8iBjNLtDUhrbDpgicNj0ozihwQMg';
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }

      return config;
  },
  (error) => {
      return Promise.reject(error);
  }
)

export {axiosNoAuthInstance, axiosAuthInstance, contestId };