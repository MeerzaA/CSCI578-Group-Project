import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  root: ".", // Set root to the 'hosting' directory
  serve: { port: 5173 },
  build: {
    outDir: "dist", // Output build files to 'hosting/dist'
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"), // Adjust alias to match the src location
    },
  },
});
