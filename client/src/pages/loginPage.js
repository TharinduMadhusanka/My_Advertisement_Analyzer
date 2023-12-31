import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

import TextField from "@mui/material/TextField";
import Checkbox from "@mui/material/Checkbox";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";

import { auth, provider } from "../googlesignin/config";
import { signInWithPopup } from "firebase/auth";

import GoogleButton from "react-google-button";

import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from "@mui/material";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const navigate = useNavigate();

  const [value, setValue] = useState("");

  const [openforgot, setOpenforgot] = useState(false);

  const toggleDialogforgot = () => {
    setOpenforgot(!openforgot);
  };

  const handleClick = () => {
    signInWithPopup(auth, provider).then((data) => {
      setValue(data.user.email);
      localStorage.setItem("email", data.user.email); // Setting email in local storage
      navigate("/");
    });
  };

  useEffect(() => {
    setValue(localStorage.getItem("email"));
  });

  const handleLogin = () => {
    if (!email || !password) {
      alert("Please enter both email and password");
      return;
    }

    axios
      .post("http://127.0.0.1:5000/login", {
        email,
        password,
      })
      .then(function (response) {
        console.log(response);

        // Doing changes
        setValue(email);
        localStorage.setItem("email", email); // Setting email in local storage
        navigate("/"); // Redirecting to home page
      })
      .catch(function (error) {
        console.log(error, "error");
        if (error.response && error.response.status === 401) {
          alert(error.response.data.error);
        }
      });
  };

  return (
    <Container component="main" maxWidth="xs">
      <form>
        <div className="d-flex flex-row align-items-center justify-content-center justify-content-lg-start">
          <Typography component="h1" variant="h5" marginTop="100px">
            Log Into Your Account
          </Typography>
        </div>
        <Box sx={{ mt: 3 }}>
          <TextField
            label="Email Address"
            variant="outlined"
            fullWidth
            margin="normal"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter a valid email address"
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
            placeholder="Enter your password"
            required
          />

          <div className="d-flex justify-content-between align-items-center">
            <div className="form-check mb-0">
              <Checkbox
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                inputProps={{ "aria-label": "controlled" }}
                id="rememberMe"
              />
              <label htmlFor="rememberMe">Remember me</label>
            </div>
          </div>

          <div className="text-center text-lg-start mt-4 pt-2">
            <Button variant="contained" onClick={handleLogin}>
              Log In
            </Button>
            <Typography variant="body2" mt={2}>
              <div>
                <a href="#!" className="text-body" onClick={toggleDialogforgot}>
                  Forgot password?
                </a>
                <Dialog open={openforgot} onClose={toggleDialogforgot}>
                  <DialogTitle>Forgot Password</DialogTitle>
                  <DialogContent>
                    <p>Enter your email to reset your password.</p>
                    {/* Add your input fields or any other content */}
                  </DialogContent>
                  <DialogActions>
                    <Button onClick={toggleDialogforgot} color="primary">
                      Cancel
                    </Button>
                    <Button onClick={toggleDialogforgot} color="primary">
                      Submit
                    </Button>
                  </DialogActions>
                </Dialog>
              </div>
              <div>
                Don't have an account?{" "}
                <a href="/register" className="link-danger">
                  Register
                </a>
              </div>
            </Typography>
          </div>
        </Box>
      </form>
      <div>
        <p>________or login with Google________ </p>
        <GoogleButton onClick={handleClick} />
      </div>
    </Container>
  );
}
