import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './Styles/index.css'

// firebase config
import './firebase/firebaseConfig'; // Ensure Firebase is initialized


createRoot(document.getElementById('root')).render(
    <App />,
)
