import { useEffect, useRef, useState } from 'react';
import { Header, PAGES, type Page } from './components/Header';
import { Footer } from './components/Footer';
import { AuthProvider } from './context/AuthContext';
import { Home } from './pages/Home';
import { Community } from './pages/Community';
import { Management } from './pages/Management';
import { Works } from './pages/Works';
import { Transparency } from './pages/Transparency';

const TITLES: Record<Page, string> = { home: 'Início', community: 'Comunidade', management: 'Gestão pública', works: 'Obras', transparency: 'Transparência' };

function readPage(): Page {
  const p = location.hash.replace('#', '') as Page;
  return PAGES.includes(p) ? p : 'home';
}

export function App() {
  const [page, setPage] = useState<Page>(readPage);
  const [notice, setNotice] = useState('');
  const mainRef = useRef<HTMLElement>(null);
  const firstRender = useRef(true);

  useEffect(() => {
    const onHash = () => setPage(readPage());
    window.addEventListener('hashchange', onHash);
    return () => window.removeEventListener('hashchange', onHash);
  }, []);

  // A cada troca de página: título, topo e foco (leitores de tela anunciam o novo conteúdo).
  useEffect(() => {
    document.title = `${TITLES[page]} — Utopy | Plataforma Digital de Participação Cidadã e Transparência Pública`;
    if (firstRender.current) { firstRender.current = false; return; }
    window.scrollTo({ top: 0 });
    mainRef.current?.focus();
  }, [page]);

  useEffect(() => {
    if (!notice) return;
    const t = setTimeout(() => setNotice(''), 6000);
    return () => clearTimeout(t);
  }, [notice]);

  return (
    <AuthProvider>
    <>
      <a className="skip-link" href="#conteudo" onClick={e => { e.preventDefault(); mainRef.current?.focus(); }}>Ir para o conteúdo</a>
      <div className="demo-banner">Protótipo acadêmico · todos os dados, nomes e valores são fictícios</div>
      <Header page={page} onDemo={setNotice} />
      <main id="conteudo" ref={mainRef} tabIndex={-1}>
        {page === 'home' && <Home />}
        {page === 'community' && <Community />}
        {page === 'management' && <Management />}
        {page === 'works' && <Works />}
        {page === 'transparency' && <Transparency />}
      </main>
      <Footer />
      <div className="toast" role="status" aria-live="polite">{notice}</div>
    </>
    </AuthProvider>
  );
}
