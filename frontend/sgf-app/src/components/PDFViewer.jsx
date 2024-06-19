// PDFViewer.jsx

import React, { useEffect } from 'react';
import { getDocument } from 'pdfjs-dist/build/pdf.mjs';

const PDFViewer = ({ pdfUrl }) => {
  useEffect(() => {
    const loadingTask = getDocument(pdfUrl);

    loadingTask.promise.then(pdf => {
      pdf.getPage(1).then(page => {
        const scale = 1.5; // Adjust scale as needed
        const viewport = page.getViewport({ scale });

        const canvas = document.getElementById('pdfViewerCanvas');
        const context = canvas.getContext('2d');
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        const renderContext = {
          canvasContext: context,
          viewport
        };
        page.render(renderContext);
      });
    });
  }, [pdfUrl]);

  return (
    <div>
      <canvas id="pdfViewerCanvas"></canvas>
    </div>
  );
};

export default PDFViewer;
