// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// import { getAnalytics } from "firebase/analytics";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBHtgDg35s3egKqDBnz-QiXIAnpWL8ubl8",
  authDomain: "learning-3419a.firebaseapp.com",
  databaseURL:
    "https://learning-3419a-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "learning-3419a",
  storageBucket: "learning-3419a.appspot.com",
  messagingSenderId: "820732401908",
  appId: "1:820732401908:web:b61096c29435eeb49ca6a1",
  measurementId: "G-MDZ1DK8YLG",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();
export { auth, provider };
