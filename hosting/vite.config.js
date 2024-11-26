import path from "path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  root: "./", // Root is the hosting folder where index.html resides
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    outDir: "dist", // Output the build to hosting/dist
    emptyOutDir: true, // Clear the dist folder before building
  },
});