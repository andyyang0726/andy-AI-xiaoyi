import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: {
      '/api': {
        target: 'https://8000-ihia78ehq6oi6tkbljqri-02b9cc79.sandbox.novita.ai',
        changeOrigin: true,
        secure: false
      }
    }
  }
})
