import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Proxy API requests to the Flask backend during development
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
    }
  },
  build: {
    // Build the frontend into a 'dist' folder in the project root
    outDir: '../dist',
    emptyOutDir: true, // Clean the output directory before each build
  }
})