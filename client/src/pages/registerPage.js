import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import TextField from "@mui/material/TextField";
import Checkbox from "@mui/material/Checkbox";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const navigate = useNavigate();



  const showVerificationPopup = () => {
    const verificationCode = window.prompt("Enter verification code:");
    if (verificationCode) {
      axios
        .post("http://127.0.0.1:5000/verify", {
          email: email,
          verificationCode: verificationCode,
        })
        .then(function (response) {
          console.log(response);
          if (response.data.success) {
            alert("Registration successful!");
            navigate("/login");
          } else {
            alert("Verification code is incorrect or expired.");
          }
        })
        .catch(function (error) {
          console.log(error, "error");
        });
    }
  };

  
  const handleRegister = () => {
    if (email === "" || password === "") {
      alert("Please fill all the fields");
      return;
    }

    axios
      .post("http://127.0.0.1:5000/signup", {
        email: email,
        password: password,
      })
      .then(function (response) {
        console.log(response);
        showVerificationPopup();
        // navigate("/");
      })
      .catch(function (error) {
        console.log(error, "error");
        if (error.response && error.response.status === 409) {
          alert("User already exists");
        }
      });
  };

  return (
    <Container component="main" maxWidth="xs">
      <div>
        <Typography component="h1" variant="h5" marginTop="100px">
          Create Your Account
        </Typography>
        <Box sx={{ mt: 3 }}>
          <TextField
            label="Email Address"
            variant="outlined"
            fullWidth
            margin="normal"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <TextField
            label="Password"
            variant="outlined"
            fullWidth
            margin="normal"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <Checkbox
            checked={rememberMe}
            onChange={(e) => setRememberMe(e.target.checked)}
            inputProps={{ "aria-label": "controlled" }}
            id="rememberMe"
          />
          <label htmlFor="rememberMe">Remember me</label>
          <div>
            <Button variant="contained" onClick={handleRegister}>
              Sign Up
            </Button>
            <Typography variant="body2" mt={2}>
              Already have an account?{" "}
              <a href="/login" className="link-danger">
                Login
              </a>
            </Typography>
          </div>
        </Box>
      </div>
    </Container>
  );
}
