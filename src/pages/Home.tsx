import { useEffect, useState } from 'react';
import {
  ArrowRight,
  ArrowUpRight,
  BarChart3,
  Building2,
  Check,
  FileText,
  Lightbulb,
  MessageCircle,
  Users,
} from 'lucide-react';
import { api } from '../lib/api';

export function Home() {
  const [stats, setStats] = useState<any>({
    discussions: '—',
    works: '—',
    ideas: '—',
    citizens: '—',
  });

  useEffect(() => {
    api.stats().then(setStats).catch(() => {});
  }, []);

  const metrics = [
    { Icon: FileText, label: 'Discussões', value: stats.discussions, caption: 'Na comunidade' },
    { Icon: Building2, label: 'Obras', value: stats.works, caption: 'Acompanhadas' },
    { Icon: BarChart3, label: 'Propostas', value: stats.ideas, caption: 'Apresentadas' },
    { Icon: Users, label: 'Cidadãos', value: stats.citizens, caption: 'Participantes' },
  ];

  const steps = [
    { Icon: MessageCircle, title: 'Conversar', detail: 'Compartilhe o que importa' },
    { Icon: Lightbulb, title: 'Propor', detail: 'Transforme ideias em projetos' },
    { Icon: Check, title: 'Acompanhar', detail: 'Veja cada etapa com clareza' },
  ];

  return (
    <>
      <section className="hero" id="home">
        <div className="container hero-grid">
          <div className="hero-copy">
            <span className="eyebrow light">Uma cidade feita por todos</span>
            <h1>Uma cidade melhor começa com a sua voz.</h1>
            <p>
              Um espaço para conversar sobre o que importa, transformar ideias em propostas e
              acompanhar as ações públicas com transparência.
            </p>
            <div className="hero-actions">
              <a className="btn light" href="#community">
                Participar da comunidade <ArrowUpRight size={18} />
              </a>
              <a className="btn ghost" href="#transparency">
                Acompanhar a transparência
              </a>
            </div>
            <div className="hero-note">
              <Users size={17} aria-hidden="true" />
              <span>Escuta, colaboração e informação ao alcance de todos.</span>
            </div>
          </div>

          <div className="hero-visual">
            <div className="visual-orbit" aria-hidden="true" />
            <article className="participation-card" aria-labelledby="participation-title">
              <div className="visual-card-head">
                <span className="visual-kicker">O caminho da participação</span>
                <span className="visual-mark" aria-hidden="true"><Users size={19} /></span>
              </div>
              <h2 id="participation-title">Da conversa à mudança.</h2>
              <p className="visual-intro">Cada pessoa pode fazer parte do que vem a seguir.</p>
              <ol className="participation-steps">
                {steps.map(({ Icon, title, detail }, index) => (
                  <li key={title}>
                    <span className="step-number">0{index + 1}</span>
                    <span className="step-icon"><Icon size={17} aria-hidden="true" /></span>
                    <span className="step-copy">
                      <strong>{title}</strong>
                      <small>{detail}</small>
                    </span>
                    {index < steps.length - 1 && <ArrowRight className="step-arrow" size={16} aria-hidden="true" />}
                  </li>
                ))}
              </ol>
              <div className="visual-card-foot">
                <span className="visual-foot-dot" aria-hidden="true" />
                <span>Uma plataforma para a cidade inteira</span>
              </div>
            </article>
            <span className="hero-badge" aria-hidden="true">Ideias que<br />movem a cidade</span>
          </div>
        </div>
      </section>

      <section className="container stats" aria-label="Indicadores da plataforma">
        {metrics.map(({ Icon, label, value, caption }) => (
          <article className="stat" key={label}>
            <div>{label}<Icon size={18} aria-hidden="true" /></div>
            <strong>{value}</strong>
            <small>{caption}</small>
          </article>
        ))}
      </section>

      <section className="container intro">
        <span className="eyebrow green">O que é a Utopy?</span>
        <h2>Uma ponte entre população e poder público.</h2>
        <p>
          A plataforma organiza conversas, propostas, acompanhamento de obras e informações de
          gestão para que a participação continue depois da ideia inicial.
        </p>
        <div className="feature-grid">
          <a className="feature-card" href="#community">
            <span className="feature-number">01</span>
            <span className="feature-icon"><MessageCircle size={21} aria-hidden="true" /></span>
            <h3>Participar</h3>
            <p>Converse sobre desafios locais e ajude a definir prioridades coletivas.</p>
            <span className="feature-link">Ir à comunidade <ArrowRight size={16} aria-hidden="true" /></span>
          </a>
          <a className="feature-card" href="#community">
            <span className="feature-number">02</span>
            <span className="feature-icon"><Lightbulb size={21} aria-hidden="true" /></span>
            <h3>Propor</h3>
            <p>Compartilhe uma ideia e acompanhe seu percurso de forma pública.</p>
            <span className="feature-link">Ver o laboratório <ArrowRight size={16} aria-hidden="true" /></span>
          </a>
          <a className="feature-card" href="#works">
            <span className="feature-number">03</span>
            <span className="feature-icon"><Building2 size={21} aria-hidden="true" /></span>
            <h3>Acompanhar</h3>
            <p>Veja o andamento de obras, propostas e ações da gestão pública.</p>
            <span className="feature-link">Explorar obras <ArrowRight size={16} aria-hidden="true" /></span>
          </a>
        </div>
      </section>
    </>
  );
}
