import React from 'react';
import PDFViewer from './PDFViewer'; // Adjust path as needed

const About = () => {
  return (
    <div>
      <h2>About Me</h2>
      <p>Biography text...</p>

      {/* Embed PDF viewer component */}
      <PDFViewer />
    </div>
  );
};

export default About;
