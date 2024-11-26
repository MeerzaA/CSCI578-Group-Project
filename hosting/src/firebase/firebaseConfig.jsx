// src/firebase.js
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyCAp1QvnTgfjv8cWTf65togmd3l3bQHsvs",
  authDomain: "crypto-board-csci578.firebaseapp.com",
  databaseURL: "https://crypto-board-csci578-default-rtdb.firebaseio.com",
  projectId: "crypto-board-csci578",
  storageBucket: "crypto-board-csci578.firebasestorage.app",
  messagingSenderId: "604703673680",
  appId: "1:604703673680:web:c00ead5e36e6655f4f3055",
  measurementId: "G-BZBDHVXT11",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Analytics (optional)
const analytics = getAnalytics(app);

export default app;