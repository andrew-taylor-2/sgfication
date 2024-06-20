import React from 'react';
import { Viewer, Worker } from '@react-pdf-viewer/core';
import '@react-pdf-viewer/core/lib/styles/index.css'; // Styles for the viewer
import '@react-pdf-viewer/default-layout/lib/styles/index.css'; // Styles for the default layout
import pdfjs from 'pdfjs-dist/build/pdf'; // Import pdfjs-dist

// Import the PDF.js worker script (if not handled by default by your build tool)
import 'pdfjs-dist/build/pdf.worker.js'; // Ensure this path matches the location of your worker script

const PDFViewer = () => {
  const pdfUrl = '../../public/resume.pdf'; // Replace with your PDF URL

  // Set PDF.js worker source
  //pdfjs.GlobalWorkerOptions.workerSrc = `https://mozilla.github.io/pdf.js/build/pdf.worker.min.js`;

  return (
    <div style={{ height: '100vh' }}>
      <Worker workerUrl={`https://mozilla.github.io/pdf.js/build/pdf.worker.min.js`}>
        <Viewer fileUrl={pdfUrl} />
      </Worker>
    </div>
  );
};

export default PDFViewer;
