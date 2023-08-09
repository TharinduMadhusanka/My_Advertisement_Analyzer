import React from "react";
import "./App.css";
import ResponsiveAppBar from "./components/appBar";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/home";
import About from "./pages/about";
import Analyze from "./pages/analyze";
import InputURL from "./pages/inputURL";

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/analyze" element={<Analyze />} />
          <Route path="/inputURL" element={<InputURL />} />
          <Route path="/about" element={<About />} />
          {/* <Route path="*" element={<NoPage />} /> */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
