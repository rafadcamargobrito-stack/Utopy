import { ThumbsUp } from 'lucide-react';
import type { MouseEvent } from 'react';
type Props={count:number;label:string;suffix?:string;onClick?:(event:MouseEvent<HTMLButtonElement>)=>void};
export function SupportButton({count,label,suffix='',onClick}:Props){return <button type="button" className="support" aria-label={`Apoiar “${label}” — ${count} apoios`} onClick={onClick}><ThumbsUp size={16} aria-hidden="true"/>{count}{suffix}</button>}
