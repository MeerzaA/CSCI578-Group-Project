import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import CryptoPage from './CryptoPage';
import './App.css'
import Home from './Home';

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

export default App
