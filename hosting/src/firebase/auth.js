import { auth } from "./firebaseConfig";
import { createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut } from "firebase/auth";
import { db } from "./firebaseConfig";
import { ref, set } from "firebase/database";

// Sign Up and Add User to Database
export const signUp = async (email, password, name) => {
  const userCredential = await createUserWithEmailAndPassword(auth, email, password);
  const user = userCredential.user;

  // Add user to Realtime Database
  const dbRef = ref(db, `users/${user.uid}`);
  await set(dbRef, { email, name, uid: user.uid });

  return user;
};

// Sign In
export const signIn = (email, password) => {
  return signInWithEmailAndPassword(auth, email, password);
};

// Sign Out
export const logOut = () => {
  return signOut(auth);
};
