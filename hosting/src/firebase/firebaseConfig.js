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
  apiKey: "AIzaSyDzJMpQSR-FQWe-T-PyPnpmG0LvLmj8DaA",
  authDomain: "csci578-cryptoboard-test.firebaseapp.com",
  databaseURL: "https://csci578-cryptoboard-test-default-rtdb.firebaseio.com",
  projectId: "csci578-cryptoboard-test",
  storageBucket: "csci578-cryptoboard-test.firebasestorage.app",
  messagingSenderId: "913517409743",
  appId: "1:913517409743:web:53871a4deb00dc2328ceba",
  measurementId: "G-JGPMBXCJCC"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
export const auth = getAuth(app);
export const db = getDatabase(app);

const fbapp = initializeApp(firebaseConfig);


export default fbapp;