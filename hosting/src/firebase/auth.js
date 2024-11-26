import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut } from "firebase/auth";
import app from "./firebaseConfig";

// Initialize Auth
const auth = getAuth(app);

/**
 * Sign in 
 * @param {string} email - User email
 * @param {string} password - User password
 */
export const signIn = async (email, password) => {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    return userCredential.user; // authenticated user
  } catch (error) {
    console.error("Error signing in:", error.message);
    throw error;
  }
};

/**
 * email and password
 * @param {string} email - User email
 * @param {string} password - User password
 */
export const signUp = async (email, password) => {
  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    return userCredential.user; // newly user
  } catch (error) {
    console.error("Error signing up:", error.message);
    throw error;
  }
};

/**
 * Sign out
 */
export const logout = async () => {
  try {
    await signOut(auth);
    console.log("User signed out successfully.");
  } catch (error) {
    console.error("Error signing out:", error.message);
    throw error;
  }
};
