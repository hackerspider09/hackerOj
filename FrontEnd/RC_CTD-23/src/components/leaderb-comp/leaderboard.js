import React, { useEffect, useState } from "react";
// import 'bootstrap/dist/css/bootstrap.min.css';
// import 'datatables.net-dt/css/jquery.dataTables.min.css';
import DataTable from "react-data-table-component";  
import "./leaderboard.css";
import { axiosNoAuthInstance ,CLASHID,RCID} from '../../Utils/AxiosConfig';
import { getToken} from '../../Utils/utils';

import LoaderComponent from "../loader/loader"; 


var data={};

// var data1={};
const customStyles = {
  rows: {
      style: {
          // minHeight: '72px', // override the row height
           color: 'aqua',
           borderWidth: '2px',
           background: 'white',
           borderColor:"inherit",
           
        },
  },
  headCells: {
      style: {
        background :'#12223a',
        borderColor:"inherit",
      },
  },
  cells: {
      style: {
          // paddingLeft: '8px', // override the cell padding for data cells
          // paddingRight: '8px',
          color: 'white',
          background: '#123b5a',
          borderColor:"inherit",
      },
  },
  pagination: {
    style: {
      background:'#12223a',
      borderColor:"inherit",
      color:'white',
      borderWidth:'2px',
    },
  },
};
// var data={};
const customStyles2 = {
  buttons: {
      style: {
          minHeight: '72px', // override the row height
           color: 'aqua',
           borderWidth: '4px',
           background: 'white',
           
        },
  },
};


const paginationComponentOptions = {
  noRowsPerPage:true
};

const Leaderboard = () => {
  const [loading, setLoading] = useState(false);

  const [dataSet, setDataSet] = useState([]);
  const [displayData, setDisplayData] = useState([]);
  const [juniorSelected, setJuniorSelected] = useState(true);  //use to show which option is selected

  const [searchQuery, setSearchQuery] = useState('');
  const numberOfQuestions = 5;

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

    const endPoint = `/core/${contestID}/leaderboard/`;

  useEffect(()=>{
    setDataSet([]);
    setDisplayData([]);

    console.clear();
    setLoading(true);
    // addAuthToken(getToken());
    axiosNoAuthInstance.get(endPoint)
            .then((response) => {
                // console.log("enter in then ");
                if (response.status) {
                    // console.log("enter in then if ");
                    data = response.data;
                    // if (localStorage.getItem("isJunior")){
                      // console.log("junior")
                      var jdata = data;
                    // }else{
                    //   // console.log("senior")
                    //    jdata = data.seniorLeaderboard;
                    // }
                    // console.log(data);
                    // console.log(jdata);
                    
                    // console.log(typeof(data));
                    // console.log(typeof(jdata));
                    // console.log(Object.values(jdata));
                    // console.log(typeof(Object.values(jdata)));
                    
                    
                    setDataSet(jdata);
                    setDisplayData(jdata.juniorLeaderboard);

                    // console.log("data ",typeof(dataSet));
                    // console.log(dataSet);
                    setTimeout(()=>{
                      setLoading(false);

                    },2000);
                    // console.log(response.data.juniorLeaderboard);

                }
                else {
                    
                    // console.log("Error In fetch");
                }
            })
            .catch((error) => {
              console.clear();
                // console.log("enter in error ",error);

            })
  },[contestID]);


  const columns = [
    { name: "Rank",  selector: (row, i) => row['rank'], sortable: true },
    { name: "Username", selector: (row, i) =>{
              const user1 = row['user1'];
              const user2 = row['user2'];
              return user2 ? `${user1}, ${user2}` : user1; 
          },  sortable: true },
    // { name: "Q1", selector: "questionSolvedByUser.Q1", sortable: true },
    // { name: "Q2", selector: "questionSolvedByUser.Q2", sortable: true },
    // { name: "Q3", selector: "questionSolvedByUser.Q3", sortable: true },
    // { name: "Q4", selector: "questionSolvedByUser.Q4", sortable: true },
    // { name: "Q5", selector: "questionSolvedByUser.Q5", sortable: true },
    // { name: "Q6", selector: "questionSolvedByUser.Q6", sortable: true },
    // numberOfQuestion is responsible to show question colum in table
    ...Array.from({ length: numberOfQuestions }, (_, i) => (
      { name: `Q${i + 1}`, selector: `questionSolvedByUser.Q${i + 1}`, sortable: true }
  )),
    // { name: "Q6", selector: "questionSolvedByUser.Q6", sortable: true },

    { name: "Time", selector: "lastUpdate", sortable: true ,format: (row) => {
      const dateTime = new Date(row.lastUpdate);
      const timezoneOffset = 5.5 * 60; // +05:30 in minutes
      dateTime.setMinutes(dateTime.getMinutes() + timezoneOffset);
      const hours = dateTime.getUTCHours();
      const minutes = dateTime.getUTCMinutes();
      const seconds = dateTime.getUTCSeconds();
      const timeString = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
      return timeString;
    },},



    { name: "Score", selector: "score", sortable: true },
  ];

  return (
    <>
    <body>
      {/* <div> {loading && <LoaderComponent show={true} />}</div> */}
      <div className=" flex-col gap-4 row rawdat">
        <h1 className="mt-3 mb-2 text-center">Leaderboard</h1>
        <div className="flex  pl-28 justify-center">
        <div className="  searchFunc w-[80%] items-center">
        <input className="searchFunc2 px-3 py-2  mx-5" 
            type="text"
             value={searchQuery}
               onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search by UserName..."
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

        <div className="  md:flex-col   lg:flex-row w-[80%] pl-28 ">
        <button onClick={() => {setDisplayData(dataSet.juniorLeaderboard); setJuniorSelected(true)}}  class="console-btn  btn-outline-dark">Junior</button>
        <button onClick={() => {setDisplayData(dataSet.seniorLeaderboard); setJuniorSelected(false)}}  class="console-btn  btn-outline-dark">Senior</button>
      </div>
        </div>

      



        <div className="Hello w-[80%] mx-auto">
          <DataTable

            columns={columns}
          
            data={displayData.filter((item) =>
               item.user1.toLowerCase().includes(searchQuery.toLowerCase())
            )}
            pagination
            paginationPerPage={6} 
            customStyles={customStyles}
            paginationComponentOptions={paginationComponentOptions}
            highlightOnHover
            responsive
            className="leaderboardtable border-2 border-slate-500"
          />
        </div>
      </div>
    
    </body>
    </>

  );
};

export default Leaderboard;
