import { BrandMark } from './BrandMark';

export function Footer() {
  return (
    <footer className="footer">
      <div className="footer-divider" aria-hidden="true"><span /></div>
      <div className="container footer-grid">
        <div>
          <div className="brand footer-brand"><span aria-hidden="true">UT</span><BrandMark size={26} /><span aria-hidden="true">PY</span><span className="sr-only">Utopy</span></div>
          <p><strong className="tagline">Plataforma Digital de Participação Cidadã e Transparência Pública</strong><br />Participação cidadã, planejamento e transparência em um só lugar.</p>
        </div>
        <div>
          <strong>Plataforma</strong>
          <p className="muted">Sobre o projeto, Acessibilidade e Privacidade (LGPD): páginas em breve.</p>
        </div>
        <div>
          <strong>Importante</strong>
          <p className="muted">Os dados desta versão são fictícios. Uma versão real deve consumir bases oficiais e possuir autenticação, moderação e auditoria.</p>
        </div>
      </div>
      <div className="container footer-bottom">© 2026 Utopy · Protótipo acadêmico</div>
    </footer>
  );
}
