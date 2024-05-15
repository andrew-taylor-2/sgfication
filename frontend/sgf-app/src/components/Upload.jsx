import React, { useState } from 'react';
import axios from 'axios';

function Upload() {
  const [file, setFile] = useState(null);
  const [visualization, setVisualization] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post('http://127.0.0.1:5000/analyze/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setVisualization(response.data); // Assuming the server sends back the visualization URL or data
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div>
      <h2>Upload File</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleFileUpload}>Upload</button>
      {visualization && <img src={visualization} alt="Visualization" />}
    </div>
  );
}

export default Upload;
