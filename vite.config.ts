import { defineConfig, type Plugin } from 'vite';
import react from '@vitejs/plugin-react';

const apiUrl = process.env.VITE_API_URL ?? 'http://localhost:8000/api/v1';
const apiOrigin = new URL(apiUrl).origin;

// CSP só no build: em dev o Vite injeta scripts inline (HMR) e seriam bloqueados.
// Cabeçalhos como frame-ancestors não funcionam via <meta>: veja public/_headers.
const csp: Plugin = {
  name: 'utopy-csp',
  apply: 'build',
  transformIndexHtml: () => [{
    tag: 'meta',
    attrs: {
      'http-equiv': 'Content-Security-Policy',
      content: `default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self' ${apiOrigin}; object-src 'none'; base-uri 'self'; form-action 'self'`,
    },
    injectTo: 'head-prepend',
  }],
};

export default defineConfig({
  plugins: [react(), csp],
  base: process.env.GITHUB_ACTIONS === 'true' ? '/Utopy/' : '/',
  build: { sourcemap: false, assetsInlineLimit: 0 },
});
