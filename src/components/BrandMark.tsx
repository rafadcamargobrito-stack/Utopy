/** Losango concêntrico da identidade Utopy. Decorativo: o nome acessível fica no link/botão pai. */
export function BrandMark({ size = 28 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 64 64" aria-hidden="true" focusable="false">
      <path d="M32 4 60 32 32 60 4 32Z" fill="none" stroke="currentColor" strokeWidth="6" />
      <path d="M32 17 47 32 32 47 17 32Z" fill="none" stroke="currentColor" strokeWidth="4" />
      <path d="M32 26 38 32 32 38 26 32Z" fill="currentColor" />
    </svg>
  );
}
