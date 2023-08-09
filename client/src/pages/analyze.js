import React from "react"; // Make sure to import React for functional components
import CenteredTabs from "../components/tabs";
import MainLayout from "../layout/mainLayout";

function Analyze() {
  return (
    <MainLayout>
      <h2>This is the analyze page</h2>
      <CenteredTabs />
    </MainLayout>
  );
}

export default Analyze; // Export the Home component so it can be used in other files
