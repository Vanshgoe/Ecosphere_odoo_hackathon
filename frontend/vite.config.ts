import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, '.', 'VITE_');
  return {
    plugins: [react()],
    build: {
      chunkSizeWarningLimit: 1100,
      rollupOptions: {
        output: {
          manualChunks: {
            echarts: ['echarts', 'echarts-for-react'],
            vendor: ['react', 'react-dom', 'react-router-dom'],
            query: ['@tanstack/react-query'],
          },
        },
      },
    },
    server: {
      proxy: {
        '/odoo': {
          target: env.VITE_ODOO_URL || 'http://localhost:8069',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/odoo/, ''),
        },
      },
    },
  };
});
