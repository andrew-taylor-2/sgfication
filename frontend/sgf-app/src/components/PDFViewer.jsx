// PDFViewer.jsx

import React, { useEffect } from 'react';
import { getDocument } from 'pdfjs-dist/build/pdf';
import { PDFViewer } from 'pdfjs-dist/web/pdf_viewer';

const PDFViewerComponent = ({ pdfUrl }) => {
  useEffect(() => {
    const pdfViewer = new PDFViewer({
      container: document.getElementById('pdfViewerContainer')
    });

    // Load the PDF document
    const loadPDF = async () => {
      try {
        const pdf = await getDocument(pdfUrl).promise;
        pdfViewer.setDocument(pdf);
      } catch (error) {
        console.error('Error loading PDF:', error);
      }
    };

    loadPDF();

    // Cleanup function
    return () => {
      // Clean up PDF viewer instance
      pdfViewer.cleanup();
    };
  }, [pdfUrl]);

  return (
    <div id="pdfViewerContainer" style={{ width: '100%', height: '100vh' }}>
      {/* This div will contain the PDF viewer */}
    </div>
  );
};

export default PDFViewerComponent;
