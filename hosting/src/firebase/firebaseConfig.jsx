// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
import { getDatabase } from "firebase/database";


// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCAp1QvnTgfjv8cWTf65togmd3l3bQHsvs",
  authDomain: "crypto-board-csci578.firebaseapp.com",
  databaseURL: "https://crypto-board-csci578-default-rtdb.firebaseio.com",
  projectId: "crypto-board-csci578",
  storageBucket: "crypto-board-csci578.firebasestorage.app",
  messagingSenderId: "604703673680",
  appId: "1:604703673680:web:c00ead5e36e6655f4f3055",
  measurementId: "G-BZBDHVXT11"
};

// Initialize Firebase+
const fbapp = initializeApp(firebaseConfig);
const analytics = getAnalytics(fbapp);
export const auth = getAuth(fbapp);
export const db = getDatabase(fbapp);



export default fbapp;