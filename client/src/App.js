import React from "react";
import "./App.css";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Home from "./pages/home";
import About from "./pages/about";
import Analyze from "./pages/analyze";
import InputURL from "./pages/inputURL";
import Input_Image_URL from "./pages/inputIMGURL";
import LoginPage from "./pages/loginPage";
import RegisterPage from "./pages/registerPage";
import LandingPage from "./pages/landingPage";
import LineChartExample from "./pages/charts";
import ImageUploader from "./pages/inputImage";
import Camera from "./pages/camera";

function ProtectedRoute({ element }) {
  const userEmail = localStorage.getItem("email");
  console.log(userEmail);
  return userEmail ? element : <Navigate to="/login" />;
}

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/charts" element={<LineChartExample />} />
          <Route path="/inputimage" element={<ImageUploader />} />
          <Route path="/camera" element={<Camera />} />

          <Route path="/" element={<ProtectedRoute element={<Home />} />} />
          <Route
            path="/analyze"
            element={<ProtectedRoute element={<Analyze />} />}
          />
          <Route
            path="/inputURL"
            element={<ProtectedRoute element={<InputURL />} />}
          />
          <Route
            path="/about"
            element={<ProtectedRoute element={<About />} />}
          />
          <Route
            path="/inputIMGURL"
            element={<ProtectedRoute element={<Input_Image_URL />} />}
          />
          <Route
            path="/landing"
            element={<ProtectedRoute element={<LandingPage />} />}
          />
          {/* <Route path="*" element={<LoginPage />} /> */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
