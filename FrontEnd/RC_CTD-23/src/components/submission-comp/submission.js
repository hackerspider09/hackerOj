import React from 'react'
import DataTable from "react-data-table-component";
import Modal from "react-modal"; 
import {  toast } from 'react-toastify';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import { useState,useEffect } from 'react';
import './submission.css'
import { axiosAuthInstance,CONTEST_ID ,addAuthToken} from '../../Utils/AxiosConfig';
import { getToken} from '../../Utils/utils';
import color from 'material-ui-core/colors/amber';



// const getFormatedTime = (timestamp) => {
//   const date = new Date(timestamp);
//   const hours = date.getHours().toString().padStart(2, '0');
//   const minutes = date.getMinutes().toString().padStart(2, '0');
//   const seconds = date.getSeconds().toString().padStart(2, '0');
  
//   const formattedTime = `${hours}:${minutes}:${seconds}`;
  
//   return formattedTime // Display formatted time in h:mm:ss format
// }

const statusColors = {
  "AC": "white", // Define the color for "AC" status
  "WA": "white",   // Define the color for other status, e.g., "WA"
  "CE": "black",
};


const statusColorsnew = {
  "AC": "green", // Define the color for "AC" status
  "WA": "red",   // Define the color for other status, e.g., "WA"
  "CE": "yellow",
};

const customStyles = {
  rows: {
      style: {
          minHeight: '72px', // override the row height
           color: 'aqua',
           borderWidth: '7px',
           background: 'white',
           
        },
  },
  headCells: {
      style: {
          paddingLeft: '8px', // override the cell padding for head cells
          paddingRight: '8px',
          background:'#45096d',
      },
  },
  cells: {
      style: {
          paddingLeft: '8px', // override the cell padding for data cells
          paddingRight: '8px',
          color: 'white',
          background: '#2d0c53',
      },
  },
  pagination: {
    style: {
      background:'#45096d',
      borderColor:"white",
      color:'white',
      borderWidth:'2px',
    },
  },
};
// var data={};
// const customStyles2 = {
//   pagination: {
//     style: {
//       background:'red',
//     },
//   },
// };


const paginationComponentOptions = {
  noRowsPerPage:true
};


export default function Submission(props) {





  const [searchText] = useState('');
  const [selectedCode, setSelectedCode] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [copied, setCopied] = useState(false);   //for copy code
  const endPoint = `/submission/${CONTEST_ID}/submissions/?question=${props.questionId}`;
  
  const columns = [
    // {name:"ID",selector:"id",sortable: true },
    // { name: "Team", selector: "team", sortable: true },
    // { name: "Username", selector: "question", sortable: true },
    { name: "Language", selector: "language", sortable: true },
    { name: "Points", selector: "points", sortable: true },
    { name: "SubmissionTime", selector: "submissionTime", sortable: true, format: row => {
      const dateTime = new Date(row.submissionTime);
      const hours = dateTime.getUTCHours();
      const minutes = dateTime.getUTCMinutes();
      const seconds = dateTime.getUTCSeconds();
      const timeString = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
      return timeString;
    }, },
    { name: "Status", selector: "status", sortable: true,cell: row => (
      <span
        style={{
          color: statusColors[row.status], // Set the color based on the status value
          backgroundColor:statusColorsnew[row.status]

        }}
      >
        {row.status}
      </span>
    ) },
    { name: "Code", selector: "code", sortable: true, cell: (row) => <button className='viewbts bg-dark px-1 py-2 text-light btn-outline-warning' onClick={() => handleViewCode(row.code)}>View</button>
  },




]
const handleViewCode = (code) => {
  setSelectedCode(code);
  setIsModalOpen(true);
};

const closeModal = () => {
  setIsModalOpen(false);
  setSelectedCode("");
};     
      
const [Subdata,setSubdata] = useState([]);
    useEffect(()=>{
      // console.log(endPoint);
        axiosAuthInstance.get(endPoint)
                .then((response) => {
                    // console.log("enter in then ");
                    if (response.status) {
                        // console.log("enter in then if ");
                        // console.log(response.data);
                        
                        setSubdata(response.data)
                    }
                    else {
                        
                        // console.log("Error In fetch");
                    }
                })
                .catch((error) => {
                  console.clear();
                    // console.log("enter in error ",error);
    
                })

                // const products = [{}]
      },[]);

      const handleCopy = () => {
        setCopied(true);
        toast.success("Copied",{autoClose:1000});
      };


  return (
    
    <div className="container">
        
    <div className="row">
      {/* <h1 className="mt-8 mb-7">Submissions</h1> */}
      {/* <div className='searchbar'>
      <input className='search-input'
          type="text"
          placeholder="Search by ID..."
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
        />
          </div> */}
      <div className="Hello">
    
        <DataTable
        
          columns={columns}
          
          data={Subdata.filter((item) =>
            item.id.toString().includes(searchText.toLowerCase())
          )}
          pagination
          customStyles={customStyles}
          paginationPerPage={5} 
          paginationComponentOptions={paginationComponentOptions}
          className="submissiontable"
  
        />
        <Modal className="modalpanti" isOpen={isModalOpen} onRequestClose={closeModal}>
          <div className='modalinside'>
         
          <CopyToClipboard text={selectedCode}>
            <button  className='copybtn' onClick={handleCopy}>
              {copied ? 'Copied!' : 'Copy'}
            </button>
          </CopyToClipboard>
          <button  className="closebtn" onClick={closeModal}>Close✖️</button>
          {/* <button className='closebtn' onClick={closeModal}>Close</button> */}
          </div>
          <div className='Codecopycontent'>
          <pre>{selectedCode}</pre>
          </div>
         
        </Modal>
      </div>
    </div>
  </div>
  )
}
