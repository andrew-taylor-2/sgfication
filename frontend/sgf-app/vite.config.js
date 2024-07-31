import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      preact: 'react',
      'preact/hooks': 'react',
      'pdfjs-dist': path.resolve(__dirname, 'node_modules/pdfjs-dist'),
    }
  }
});
