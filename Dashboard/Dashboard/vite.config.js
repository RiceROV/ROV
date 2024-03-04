// Import the defineConfig function from Vite
import { defineConfig } from 'vite';

// Export the configuration object
export default defineConfig({
  server: {
    // Specify the server port
    port: 5173,
    // Uncomment the next line if you want to make the server accessible from outside localhost
    // host: true,
  },
  // Include other configuration options as needed...
});
