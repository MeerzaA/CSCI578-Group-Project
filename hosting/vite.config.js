<<<<<<< Updated upstream
import path from "path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
=======
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
>>>>>>> Stashed changes

export default defineConfig({
  root: "./", // Root is the hosting folder where index.html resides
  plugins: [react()],
  resolve: {
    alias: {
<<<<<<< Updated upstream
      "@": path.resolve(__dirname, "./src"),
    },
  },
=======
      "@": "/src",
    },
  },
  build: {
    outDir: "dist", // Output the build to hosting/dist
    emptyOutDir: true, // Clear the dist folder before building
  },
>>>>>>> Stashed changes
});
