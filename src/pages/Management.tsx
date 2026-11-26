import { useEffect, useState, type FormEvent } from 'react';
import { Activity, CalendarDays, CheckCircle2, FileCheck2, Search, ShieldCheck, Users } from 'lucide-react';
import { SectionTitle } from '../components/SectionTitle';
import { api, type AdminUser, type Idea, type OfficialActivity, type OfficialProposal, type UserRole } from '../lib/api';
import { useAuth } from '../context/AuthContext';

const statuses = ['Ideia inicial','Em análise comunitária','Em análise técnica','Aprovada','Rejeitada','Em execução','Concluída'];
const roleLabels:Record<UserRole,string>={citizen:'Cidadão',moderator:'Moderador',public_agent:'Agente público',admin:'Administrador'};

export function Management(){
 const [query,setQuery]=useState('');
 const [officials,setOfficials]=useState<any[]>([]);
 const [activities,setActivities]=useState<OfficialActivity[]>([]);
 const [ideas,setIdeas]=useState<Idea[]>([]);
 const [officialProposals,setOfficialProposals]=useState<OfficialProposal[]>([]);
 const [users,setUsers]=useState<AdminUser[]>([]);
 const [error,setError]=useState('');
 const [notice,setNotice]=useState('');
 const {user}=useAuth();

 async function loadPublic(){
  try{
   const [o,a,i,p]=await Promise.all([api.officials(),api.activities(),api.ideas(),api.officialProposals()]);
   setOfficials(o);setActivities(a);setIdeas(i);setOfficialProposals(p);
  }catch(e){setError(e instanceof Error?e.message:'Falha ao carregar o painel.')}
 }
 useEffect(()=>{void loadPublic()},[]);
 useEffect(()=>{
  if(user?.role!=='admin'){setUsers([]);return}
  api.adminUsers().then(setUsers).catch(e=>setError(e instanceof Error?e.message:'Falha ao carregar usuários.'));
 },[user?.role]);

 const filtered=officials.filter(o=>`${o.name} ${o.role}`.toLowerCase().includes(query.toLowerCase()));
 const canReview=['admin','public_agent','moderator'].includes(user?.role??'');
 async function review(id:number,status:string){
  const note=window.prompt(`Registre a justificativa/observação para “${status}”.`);
  if(!note?.trim())return;
  try{
   await api.reviewIdea(id,{status,note,decision_reason:['Aprovada','Rejeitada'].includes(status)?note:undefined});
   await loadPublic();
  }catch(e){setError(e instanceof Error?e.message:'Não foi possível atualizar a proposta.')}
 }
 async function publishProposal(data:{title:string;area?:string;description:string}){
  if(!data.area){setError('Selecione uma área para a proposta.');return}
  try{await api.createOfficialProposal({title:data.title,area:data.area,description:data.description});setNotice('Proposta institucional publicada.');await loadPublic()}
  catch(e){setError(e instanceof Error?e.message:'Não foi possível publicar a proposta.')}
 }
 async function publishActivity(data:{title:string;description:string}){
  try{await api.createOfficialActivity(data);setNotice('Atividade pública registrada.');await loadPublic()}
  catch(e){setError(e instanceof Error?e.message:'Não foi possível registrar a atividade.')}
 }
 async function saveUserRole(id:number,data:{role:UserRole;official_title?:string;party?:string}){
  try{
   const updated=await api.updateUserRole(id,data);
   setUsers(current=>current.map(account=>account.id===id?updated:account));
   setNotice(`Perfil de ${updated.name} atualizado para ${roleLabels[updated.role]}.`);
   await loadPublic();
  }catch(e){setError(e instanceof Error?e.message:'Não foi possível atualizar o perfil.');throw e}
 }

 return <div className="container page">
  <SectionTitle eyebrow="Gestão pública" title="Acompanhe quem administra a cidade" description="Uma visão organizada de propostas, atividades e indicadores institucionais."/>
  {error&&<div className="api-error" role="alert">{error}<button onClick={()=>setError('')}>Fechar</button></div>}
  {notice&&<div className="role-notice" role="status">{notice}<button onClick={()=>setNotice('')}>Fechar</button></div>}
  <div className="management-hero">
   <div><span className="eyebrow light">Painel institucional</span><h2>Do compromisso à atividade registrada.</h2><p>Compare propostas, acompanhe reuniões e consulte atualizações de agentes e equipes públicas.</p></div>
   <div className="management-metrics"><div><strong>{officials.reduce((n,o)=>n+o.projects,0)}</strong><span>propostas cadastradas</span></div><div><strong>{officials.reduce((n,o)=>n+o.activities,0)}</strong><span>atividades registradas</span></div><div><strong>{activities.length}</strong><span>atividades recentes</span></div></div>
  </div>
  <label className="search large"><Search size={18}/><span className="sr-only">Buscar agente público ou equipe</span><input type="search" value={query} onChange={e=>setQuery(e.target.value)} placeholder="Buscar prefeito, vereador ou equipe..."/></label>
  <div className="official-grid">{filtered.map(o=><article className="official-card" key={o.id}><div className="avatar" aria-hidden="true">{o.name.split('—')[1]?.trim().slice(0,1)??o.name.slice(0,1)}</div><div className="official-info"><span className="eyebrow green">{o.role}</span><h3>{o.name}</h3><p>{o.party}</p><div className="official-stats"><span><FileCheck2 size={16}/><b>{o.projects}</b> propostas</span><span><CalendarDays size={16}/><b>{o.activities}</b> atividades</span></div><small>Atualizado em {o.updated}</small></div></article>)}</div>

  {user?.role==='public_agent'&&<section className="publisher-panel"><div className="publisher-heading"><span className="eyebrow green">Área institucional</span><h2>Publicar no painel público</h2><p>Os registros ficam associados ao seu perfil e podem ser consultados pela comunidade.</p></div><div className="publisher-grid"><PublishForm kind="proposal" onSubmit={publishProposal}/><PublishForm kind="activity" onSubmit={publishActivity}/></div></section>}

  {user?.role==='admin'&&<RoleAdminPanel users={users} onSave={saveUserRole}/>}

  <section className="activity-section">
   <div><span className="eyebrow green">Propostas de agentes públicos</span><h2>Compromissos apresentados</h2></div>
   {officialProposals.length?<div className="institutional-proposal-list">{officialProposals.map(p=><article className="institutional-proposal" key={p.id}><div className="idea-top"><span className="tag">{p.area}</span><span className="status-badge review">{p.status}</span></div><h3>{p.title}</h3><p>{p.description}</p><small>Apresentada por {p.official_name} · {p.official_role} · {new Date(p.created_at).toLocaleDateString('pt-BR')}</small></article>)}</div>:<p className="muted">Ainda não há propostas institucionais publicadas.</p>}
  </section>

  <section className="activity-section"><div><span className="eyebrow green">Atividade pública</span><h2>O que merece acompanhamento?</h2></div><div className="activity-list">{activities.slice(0,6).map((a,i)=><div key={a.id}>{i===0?<CheckCircle2/>:i===1?<Activity/>:<Users/>}<div><b>{a.title}</b><p>{a.description}</p><small>{a.official_name?`Publicado por ${a.official_name}`:'Registro institucional'}</small></div><span>{new Date(a.occurred_at).toLocaleDateString('pt-BR')}</span></div>)}</div></section>

  <section className="review-panel"><div className="review-panel-head"><div><span className="eyebrow green">Participação institucional</span><h2>Propostas da população</h2><p>Quando uma proposta chega à análise pública, a mudança de etapa e sua justificativa ficam registradas para consulta.</p></div>{canReview&&<span className="role-note"><ShieldCheck size={16}/>Você pode registrar análises</span>}</div><div className="proposal-list">{ideas.map(i=><article className="proposal-row" key={i.id}><div><div className="idea-top"><span className="tag">{i.area}</span><span>{i.supports} apoios</span></div><h3>{i.title}</h3><p>{i.description}</p><StatusPath status={i.status}/>{i.decision_reason&&<div className="decision-note"><b>Justificativa:</b> {i.decision_reason}</div>}</div>{canReview&&i.status!=='Concluída'&&<div className="proposal-actions"><label className="sr-only" htmlFor={`review-${i.id}`}>Atualizar etapa de {i.title}</label><select id={`review-${i.id}`} defaultValue="" onChange={e=>e.target.value&&review(i.id,e.target.value)}><option value="">Atualizar etapa</option>{statuses.filter(s=>s!==i.status).map(s=><option key={s} value={s}>{s}</option>)}</select></div>}</article>)}</div>{!ideas.length&&<p>Nenhuma proposta cadastrada.</p>}</section>
 </div>
}

function RoleAdminPanel({users,onSave}:{users:AdminUser[];onSave:(id:number,data:{role:UserRole;official_title?:string;party?:string})=>Promise<void>}){
 return <section className="role-admin-panel"><div className="review-panel-head"><div><span className="eyebrow green">Controle de acesso</span><h2>Usuários e permissões</h2><p>Somente administradores podem atribuir perfis. Agentes públicos precisam de cargo institucional validado.</p></div><span className="role-note"><ShieldCheck size={16}/>Administrador</span></div><div className="role-user-list">{users.map(account=><RoleEditor key={account.id} account={account} onSave={onSave}/>)}</div></section>
}

function RoleEditor({account,onSave}:{account:AdminUser;onSave:(id:number,data:{role:UserRole;official_title?:string;party?:string})=>Promise<void>}){
 const [role,setRole]=useState<UserRole>(account.role);
 const [title,setTitle]=useState(account.official_title??'');
 const [party,setParty]=useState('');
 const [busy,setBusy]=useState(false);
 const [error,setError]=useState('');
 async function submit(event:FormEvent){
  event.preventDefault();setError('');setBusy(true);
  try{await onSave(account.id,{role,...(role==='public_agent'?{official_title:title,party}: {})})}
  catch(e){setError(e instanceof Error?e.message:'Não foi possível salvar.')}
  finally{setBusy(false)}
 }
 return <form className="role-user-row" onSubmit={submit}>
  <div className="role-user-identity"><strong>{account.name}</strong><span>{account.email}</span></div>
  <label>Perfil<select value={role} onChange={e=>setRole(e.target.value as UserRole)}>{Object.entries(roleLabels).map(([value,label])=><option key={value} value={value}>{label}</option>)}</select></label>
  {role==='public_agent'&&<div className="official-role-fields"><label>Cargo público<input required minLength={2} maxLength={100} value={title} onChange={e=>setTitle(e.target.value)} placeholder="Ex.: Vereadora"/></label><label>Partido/órgão<input maxLength={120} value={party} onChange={e=>setParty(e.target.value)} placeholder="Opcional"/></label></div>}
  <button className="btn outline" disabled={busy}>{busy?'Salvando...':'Salvar perfil'}</button>
  {error&&<p className="form-error" role="alert">{error}</p>}
 </form>
}

function PublishForm({kind,onSubmit}:{kind:'proposal'|'activity';onSubmit:(data:{title:string;area?:string;description:string})=>Promise<void>}){
 const [title,setTitle]=useState('');
 const [area,setArea]=useState('Infraestrutura');
 const [description,setDescription]=useState('');
 const [busy,setBusy]=useState(false);
 const [error,setError]=useState('');
 const isProposal=kind==='proposal';
 async function submit(event:FormEvent){
  event.preventDefault();setError('');setBusy(true);
  try{await onSubmit(isProposal?{title,area,description}:{title,description});setTitle('');setDescription('')}
  catch(e){setError(e instanceof Error?e.message:'Não foi possível publicar.')}
  finally{setBusy(false)}
 }
 return <form className="publish-form" onSubmit={submit}>
  <h3>{isProposal?'Nova proposta institucional':'Registrar atividade'}</h3>
  <label>Título<input required minLength={5} maxLength={180} value={title} onChange={e=>setTitle(e.target.value)}/></label>
  {isProposal&&<label>Área<select value={area} onChange={e=>setArea(e.target.value)}>{['Infraestrutura','Saúde','Educação','Meio ambiente','Mobilidade','Tecnologia'].map(option=><option key={option}>{option}</option>)}</select></label>}
  <label>Descrição<textarea required minLength={10} maxLength={isProposal?5000:3000} rows={4} value={description} onChange={e=>setDescription(e.target.value)}/></label>
  {error&&<p className="form-error" role="alert">{error}</p>}
  <button className="btn primary" disabled={busy}>{busy?'Publicando...':isProposal?'Publicar proposta':'Registrar atividade'}</button>
 </form>
}

function StatusPath({status}:{status:string}){return <div className="status-path">{statuses.map(s=><span key={s} className={statuses.indexOf(s)<=statuses.indexOf(status)?'done':''}>{s}</span>)}</div>}
