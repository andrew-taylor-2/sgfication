import React from 'react';
import { Viewer } from '@react-pdf-viewer/core';
import '@react-pdf-viewer/core/lib/styles/index.css'; // Styles for the viewer
import '@react-pdf-viewer/default-layout/lib/styles/index.css'; // Styles for the default layout

const PDFViewer = () => {
  const pdfUrl = '../../public/resume.pdf';

  return (
    <div style={{ height: '100vh' }}>
      <Viewer fileUrl={pdfUrl} />
    </div>
  );
};

export default PDFViewer;
