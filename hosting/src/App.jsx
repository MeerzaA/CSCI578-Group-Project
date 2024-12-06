
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import "./Styles/App.css";

//pages
import CryptoPage from './pages/CryptoPage';
import Home from './pages/Home';
/*import AuthPage from "./pages/AuthPage";*/

function App() {
  return (
    <>
      <Router>
        <div>
          <Routes>
            <Route path="/" element={<Home/>} />
            <Route path="/:name" element={<CryptoPage />} />
          </Routes>
        </div>
      </Router>
    </>
  )
}

export default App;