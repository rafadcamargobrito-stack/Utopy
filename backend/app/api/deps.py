from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.user import User, UserRole
from app.core.security import decode_access_token
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
async def current_user(token:str=Depends(oauth2_scheme), db:AsyncSession=Depends(get_db)):
    try: payload=decode_access_token(token)
    except Exception: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")
    if payload.get("type")!="access": raise HTTPException(status_code=401, detail="Token inválido")
    user=await db.scalar(select(User).where(User.id==int(payload["sub"]), User.is_active.is_(True)))
    if not user: raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return user
def require_roles(*roles):
    async def dep(user=Depends(current_user)):
        if user.role not in roles: raise HTTPException(status_code=403, detail="Permissão insuficiente")
        return user
    return dep
