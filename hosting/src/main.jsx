import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import './styles/index.css';

// Initialize Firebase Configuration
import './firebase/firebaseConfig.js';
import ErrorBoundary from './components/ErrorBoundary';

createRoot(document.getElementById('root')).render(
<<<<<<< Updated upstream
  // <StrictMode>
    <App />
  // </StrictMode>,
)
=======
  <StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </StrictMode>
);




>>>>>>> Stashed changes
