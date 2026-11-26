import type { ReactNode } from 'react';

type Props = { eyebrow: string; title: string; description?: string; action?: ReactNode };

export function SectionTitle({ eyebrow, title, description, action }: Props) {
  return (
    <div className="section-title">
      <div>
        <span className="eyebrow">{eyebrow}</span>
        <h1>{title}</h1>
        {description && <p>{description}</p>}
      </div>
      {action}
    </div>
  );
}
