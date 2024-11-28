
import reactLogo from './assets/react.svg'
//import viteLogo from '/vite.svg'

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useState } from 'react'

import "./Styles/App.css";

//pages
import CryptoPage from './pages/CryptoPage';
import Home from './pages/Home';
import AuthPage from "./pages/AuthPage";

function App() {
  return (
    <>
      <Router>
        <div>
          <Routes>
            <Route path="/" element={<Home/>} />
            <Route path="/:name" element={<CryptoPage />} />
            <Route path="/auth" element={<AuthPage />} />
          </Routes>
        </div>
      </Router>
    </>
  )
}

export default App;