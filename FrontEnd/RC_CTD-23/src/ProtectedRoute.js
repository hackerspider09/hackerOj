import { Outlet, Navigate } from 'react-router-dom'
import React, { useContext } from 'react';

const ProtectedRoute = () => {
    const storedToken = localStorage.getItem("TOKEN");
    return(
        storedToken ? <Outlet/> : <Navigate to="/login"/>
    )
}

export default ProtectedRoute