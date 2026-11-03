import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// In dev, proxy /api to the FastAPI server on the local machine.
export default defineConfig({
  plugins: [react()],
  server: { port: 5173, proxy: { "/api": "http://127.0.0.1:8000" } },
});
