import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    sourcemap: true
  },
  resolve: {
    alias: {
      'preact/hooks': 'react',
      preact: 'react',
      'pdfjs-dist': path.resolve(__dirname, 'node_modules/pdfjs-dist')
    },
    extensions: ['*', '.js', '.jsx', '.ts', '.tsx']
  }
});
