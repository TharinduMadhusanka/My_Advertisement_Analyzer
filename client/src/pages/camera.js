import React, { useState, useRef } from "react";
import { Button, Card, CardContent, CardMedia, Container } from "@mui/material";

function Camera() {
  const [imageSrc, setImageSrc] = useState(null);
  const [showCamera, setShowCamera] = useState(true);
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  const startWebcam = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
      streamRef.current = stream;
      videoRef.current.play();
      setImageSrc(null);
      setShowCamera(true);
    } catch (error) {
      console.error("Error accessing webcam:", error);
    }
  };

  const captureImage = () => {
    const canvas = document.createElement("canvas");
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    canvas
      .getContext("2d")
      .drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    const capturedImage = canvas.toDataURL("image/png");
    setImageSrc(capturedImage);
    setShowCamera(false);
    streamRef.current.getTracks().forEach((track) => track.stop());
  };

  const uploadImage = async () => {
    try {
      const response = await fetch("/upload", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ image: imageSrc }),
      });

      const data = await response.json();
      console.log(data); // You can handle the server response here
    } catch (error) {
      console.error("Error uploading image:", error);
    }
  };

  return (
    <Container maxWidth="sm">
      <Card>
        {showCamera && (
          <CardMedia
            component="video"
            ref={videoRef}
            style={{ maxHeight: "100%" }}
            muted
            autoPlay
          />
        )}
        <CardContent>
          {showCamera && (
            <Button variant="contained" color="primary" onClick={startWebcam}>
              Start Webcam
            </Button>
          )}
          {showCamera && (
            <Button variant="contained" color="primary" onClick={captureImage}>
              Capture Image
            </Button>
          )}
          {!showCamera && (
            <div>
              <Button
                variant="contained"
                color="primary"
                onClick={() => setShowCamera(true)}
              >
                Retake Photo
              </Button>
              <Button variant="contained" color="primary" onClick={uploadImage}>
                Upload Image
              </Button>
            </div>
          )}
          {imageSrc && (
            <div>
              <img src={imageSrc} alt="Captured" style={{ maxWidth: "100%" }} />
            </div>
          )}
        </CardContent>
      </Card>
    </Container>
  );
}

export default Camera;
