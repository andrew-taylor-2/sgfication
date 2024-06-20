import React from 'react';
import { Viewer, Worker } from '@react-pdf-viewer/core';
import '@react-pdf-viewer/core/lib/styles/index.css'; // Styles for the viewer
import '@react-pdf-viewer/default-layout/lib/styles/index.css'; // Styles for the default layout
import './PDFViewer.css'; // Import your custom CSS

// Import PDF.js and the worker script
import * as pdfjs from 'pdfjs-dist/legacy/build/pdf'; // Use legacy build for better compatibility

const PDFViewer = () => {
  const pdfUrl = '../../public/resume.pdf'; // Replace with your PDF URL

  pdfjs.GlobalWorkerOptions.workerSrc = `https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js`;

  return (
    <div className="pdf-viewer-container">
      <Worker workerUrl={`https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js`}>
        <div className="pdf-viewer">
          <Viewer fileUrl={pdfUrl} />
        </div>
      </Worker>
    </div>
  );
};

export default PDFViewer;


// workerUrl is busted but it sets up a fake one, slight performance hit