import * as React from "react";
import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import InputURL from "../pages/inputURL";
import Input_Image_URL from "../pages/inputIMGURL";
import LineChartExample from "../pages/charts";

export default function CenteredTabs() {
  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <Box sx={{ width: "100%", bgcolor: "background.paper" }}>
      <Tabs value={value} onChange={handleChange} centered>
        <Tab label="Input_URL" />
        <Tab label="Item Two" />
        <Tab label="Charts" />
      </Tabs>

      {/* Add the content for each tab */}
      {value === 0 && (
        <Box p={3}>
          <h2>Analyze advertisement by URL</h2>
          <InputURL />
        </Box>
      )}
      {value === 1 && (
        <Box p={3}>
          <h2>Analyze advertisement by URL of the image</h2>
          <Input_Image_URL />
        </Box>
      )}
      {value === 2 && (
        <Box p={3}>
          <h2>Charts</h2>
          <LineChartExample/>
        </Box>
      )}
    </Box>
  );
}
