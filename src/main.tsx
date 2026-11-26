import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import '@fontsource/cinzel/600.css';
import '@fontsource/cinzel/700.css';
import '@fontsource/dm-sans/400.css';
import '@fontsource/dm-sans/500.css';
import '@fontsource/dm-sans/700.css';
import { App } from './App';
import './styles/global.css';
import './styles/theme.css';

const el = document.getElementById('root');
if (!el) throw new Error('Elemento #root não encontrado');
createRoot(el).render(<StrictMode><App /></StrictMode>);
