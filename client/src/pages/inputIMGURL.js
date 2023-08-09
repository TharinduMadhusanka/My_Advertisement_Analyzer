import React, { useState } from "react";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import LinearProgress from "@mui/material/LinearProgress";

function Input_Image_URL() {
  const [inputUrl, setInputUrl] = useState("");
  const [backendResponse, setBackendResponse] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleUrlSubmit = (e) => {
    e.preventDefault();
    setLoading(true);

    // Send URL to backend
    fetch("/sendIMGurl", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ imageUrl: inputUrl }),
    })
      .then((response) => response.json())
      .then((responseData) => {
        console.log("Response from backend:", responseData);
        setBackendResponse(responseData.results); // Assuming 'results' is the key holding the array
      })
      .catch((error) => {
        console.error("Error sending URL to backend:", error);
      })
      .finally(() => {
        setLoading(false); // Set loading to false after fetch operation is complete
      });
  };

  return (
    <div>
      <form onSubmit={handleUrlSubmit}>
        <label>
          <p>Enter Image URL to be analyzed:</p>
          <Box
            sx={{
              width: 500,
              maxWidth: "100%",
            }}
          >
            <TextField
              fullWidth
              label="Enter IMAGE URL"
              value={inputUrl}
              onChange={(e) => setInputUrl(e.target.value)}
              placeholder="https://............jpg"
              required
            />
          </Box>
        </label>
        <Button variant="contained" type="submit">
          Analyze
        </Button>
      </form>
      <br />

      {loading && (
        <div>
          <p>Analyzing...</p>
          <LinearProgress />
        </div>
      )}

      {backendResponse.length > 0 && (
        <div>
          <p>Results:</p>
          <div>
                      {backendResponse.map((item, index) => (
                          <div key={index}>
                              <p>{item}</p>
                          </div>
                        ))
                      
                      }
          </div>
        </div>
      )}
    </div>
  );
}

export default Input_Image_URL;
