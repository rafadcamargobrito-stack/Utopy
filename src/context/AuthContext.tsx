import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';
import { api, type UserRole } from '../lib/api';

export type User = { id:number; name:string; email:string; role:UserRole };
type AuthContextValue = { user:User|null; loading:boolean; login:(email:string,password:string)=>Promise<void>; register:(name:string,email:string,password:string)=>Promise<void>; logout:()=>void };
const AuthContext=createContext<AuthContextValue|null>(null);
export function AuthProvider({children}:{children:ReactNode}){
  const [user,setUser]=useState<User|null>(null); const [loading,setLoading]=useState(true);
  useEffect(()=>{ if(localStorage.getItem('utopy_access_token')) api.me().then(setUser).catch(()=>localStorage.removeItem('utopy_access_token')).finally(()=>setLoading(false)); else setLoading(false); },[]);
  const save=async (token:string)=>{localStorage.setItem('utopy_access_token',token);setUser(await api.me());};
  const login=async(e:string,p:string)=>{const r=await api.login(e,p);await save(r.access_token)};
  const register=async(n:string,e:string,p:string)=>{const r=await api.register(n,e,p);await save(r.access_token)};
  const logout=()=>{localStorage.removeItem('utopy_access_token');setUser(null)};
  return <AuthContext.Provider value={{user,loading,login,register,logout}}>{children}</AuthContext.Provider>
}
export function useAuth(){const ctx=useContext(AuthContext);if(!ctx)throw new Error('useAuth deve ser usado dentro de AuthProvider');return ctx}
