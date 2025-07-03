import { defineConfig , loadEnv } from 'vite'

// https://vite.dev/config/
export default defineConfig( ({mode}) => {
  const env = loadEnv(mode,process.cwd());
  return {
  server: {
    proxy: {
      '/api': {
        target: `http://localhost:${env.VITE_PYTHON_SERVER_PORT}`, // backend server
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
};
})