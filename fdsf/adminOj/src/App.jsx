import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';

import MainComponent from './Pages/MainComponent';
import ExecutionServerList from './Pages/ExecutionServerList';
import Login from './Pages/login';

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Router>
      <div>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/login" element={<Login />} />
          <Route path="/servers" element={<MainComponent />} />
          {/* <Route path="*" element={<NotFound />} /> */}
        </Routes>
      </div>
    </Router>
    </>
  )
}

export default App
