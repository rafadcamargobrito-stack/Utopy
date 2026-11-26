export const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api/v1';

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('utopy_access_token');
  const headers = new Headers(options.headers);
  if (options.body && !headers.has('Content-Type')) headers.set('Content-Type', 'application/json');
  if (token) headers.set('Authorization', `Bearer ${token}`);
  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail ?? 'Não foi possível concluir a operação.');
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export type Idea = {
  id:number; title:string; area:string; description:string; author:string; supports:number; status:string;
  technical_note?:string|null; decision_reason?:string|null; responsible_department?:string|null; estimated_cost?:number|null;
  created_at:string; updated_at:string;
};
export type IdeaDetail = Idea & {comments:{id:number;author:string;body:string;created_at:string}[];history:{id:number;actor:string;from_status:string|null;to_status:string;note:string|null;created_at:string}[]};
export type UserRole = 'citizen'|'moderator'|'public_agent'|'admin';
export type AdminUser = {id:number;name:string;email:string;role:UserRole;is_active:boolean;official_title:string|null};
export type OfficialProposal = {id:number;title:string;area:string;description:string;status:string;official_name:string;official_role:string;created_at:string};
export type OfficialActivity = {id:number;title:string;description:string;occurred_at:string;official_name:string|null};

export const api = {
  login: (email: string, password: string) => request<{access_token:string}>('/auth/login', {method:'POST', body:JSON.stringify({email,password})}),
  register: (name:string,email:string,password:string) => request<{access_token:string}>('/auth/register', {method:'POST', body:JSON.stringify({name,email,password})}),
  me: () => request<{id:number,name:string,email:string,role:UserRole}>('/auth/me'),
  adminUsers: () => request<AdminUser[]>('/admin/users'),
  updateUserRole: (id:number,data:{role:UserRole;official_title?:string;party?:string}) => request<AdminUser>(`/admin/users/${id}/role`,{method:'PATCH',body:JSON.stringify(data)}),
  discussions: (category?:string,q?:string) => request<any[]>(`/community/discussions?${new URLSearchParams({...(category&&category!=='Todas'?{category}:{}),...(q?{q}:{})})}`),
  createDiscussion: (data:{title:string,category:string,excerpt:string}) => request<any>('/community/discussions',{method:'POST',body:JSON.stringify(data)}),
  supportDiscussion: (id:number) => request<{supports:number,action:string}>(`/community/discussions/${id}/support`,{method:'POST'}),
  ideas: (status?:string) => request<Idea[]>(`/community/ideas${status?`?status=${encodeURIComponent(status)}`:''}`),
  idea: (id:number) => request<IdeaDetail>(`/community/ideas/${id}`),
  createIdea: (data:{title:string,area:string,description:string}) => request<Idea>('/community/ideas',{method:'POST',body:JSON.stringify(data)}),
  supportIdea: (id:number) => request<{supports:number,action:string}>(`/community/ideas/${id}/support`,{method:'POST'}),
  commentIdea: (id:number, body:string) => request<any>(`/community/ideas/${id}/comments`,{method:'POST',body:JSON.stringify({body})}),
  reviewIdea: (id:number,data:{status:string;note:string;technical_note?:string;decision_reason?:string;responsible_department?:string;estimated_cost?:number}) => request<any>(`/admin/ideas/${id}/review`,{method:'PATCH',body:JSON.stringify(data)}),
  officials: () => request<any[]>('/public/officials'),
  activities: () => request<any[]>('/public/activities'),
  officialProposals: () => request<OfficialProposal[]>('/public/official-proposals'),
  createOfficialProposal: (data:{title:string;area:string;description:string}) => request<OfficialProposal>('/management/proposals',{method:'POST',body:JSON.stringify(data)}),
  createOfficialActivity: (data:{title:string;description:string}) => request<OfficialActivity>('/management/activities',{method:'POST',body:JSON.stringify(data)}),
  works: () => request<any[]>('/public/works'),
  documents: () => request<any[]>('/public/documents'),
  stats: () => request<any>('/public/stats'),
};
