import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  plugins: [react()],
  // GitHub Pages 部署基础路径
  base: mode === 'production' ? '/andy-AI-xiaoyi/' : '/',
  // 开发服务器配置
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: false,
    allowedHosts: [
      '.sandbox.novita.ai',
      'localhost',
      '127.0.0.1'
    ]
  },
  // 构建配置
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    // 确保资源正确引用
    rollupOptions: {
      output: {
        manualChunks: undefined
      }
    }
  }
}))
