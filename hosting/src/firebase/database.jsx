import { getDatabase, ref, set, get, onValue } from "firebase/database";
import app from "./firebaseConfig";

const db = getDatabase(app);

// Write Data
export const writeData = (path, data) => {
  const dbRef = ref(db, path);
  return set(dbRef, data);
};

// Read Data Once
export const readData = async (path) => {
  const dbRef = ref(db, path);
  const snapshot = await get(dbRef);
  if (snapshot.exists()) {
    return snapshot.val();
  } else {
    return null;
  }
};

// Subscribe to Data Changes
export const subscribeToData = (path, callback) => {
  const dbRef = ref(db, path);
  onValue(dbRef, (snapshot) => {
    if (snapshot.exists()) {
      callback(snapshot.val());
    } else {
      callback(null);
    }
  });
};
