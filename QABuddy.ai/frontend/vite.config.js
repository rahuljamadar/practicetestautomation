import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Dev server proxies /api -> FastAPI on 8077, so the UI needs no extra config.
// (8077 chosen because another local service already holds 8000.)
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8077',
        changeOrigin: true,
      },
    },
  },
})
