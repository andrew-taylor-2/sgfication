import React from 'react';
import PDFViewer from './PDFViewer'; // Adjust path as needed

const About = () => {
  const pdfUrl = 'path/to/your/resume.pdf'; // Replace with your PDF URL

  return (
    <div>
      <h2>About Me</h2>
      <p>Biography text...</p>

      {/* Embed PDF viewer component */}
      <PDFViewer pdfUrl={pdfUrl} />
    </div>
  );
};

export default About;
