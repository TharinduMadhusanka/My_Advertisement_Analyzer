import React from "react";
import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/home";
import About from "./pages/about";
import Analyze from "./pages/analyze";
import InputURL from "./pages/inputURL";
import Input_Image_URL from "./pages/inputIMGURL";
import LoginPage from "./pages/loginPage";
import RegisterPage from "./pages/registerPage";
import LandingPage from "./pages/landingPage";

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/analyze" element={<Analyze />} />
          <Route path="/inputURL" element={<InputURL />} />
          <Route path="/about" element={<About />} />
          <Route path="/inputIMGURL" element={<Input_Image_URL />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/landing" element={<LandingPage />} />

          {/* <Route path="*" element={<NoPage />} /> */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
