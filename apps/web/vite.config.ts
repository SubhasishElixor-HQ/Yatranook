
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [react(), tailwindcss()],

  server: {
    port: 5173,
    strictPort: true,
  },

  preview: {
    port: 4173,
    strictPort: true,
  },

  test: {
    environment: 'jsdom',

    setupFiles: './src/test/setup.ts',

    css: true,
    globals: true,

    // Only run Vitest unit tests inside src.
    // Playwright E2E tests are kept in ./e2e.
    include: [
      'src/**/*.test.ts',
      'src/**/*.test.tsx',
      'src/**/*.spec.ts',
      'src/**/*.spec.tsx',
    ],
  },
});
