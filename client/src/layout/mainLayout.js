import React from "react";
import ResponsiveAppBar from "../components/appBar";

function MainLayout({ children }) {
  return (
    <div>
      <ResponsiveAppBar />
      {children}
    </div>
  );
}

export default MainLayout;
