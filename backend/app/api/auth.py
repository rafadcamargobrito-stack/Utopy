from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import RegisterIn, LoginIn, TokenOut, UserOut
from app.core.security import hash_password, verify_password, create_access_token
from app.api.deps import current_user
router=APIRouter(prefix="/auth", tags=["auth"])
@router.post("/register", response_model=TokenOut, status_code=201)
async def register(data:RegisterIn, db:AsyncSession=Depends(get_db)):
    email=data.email.lower()
    if await db.scalar(select(User).where(User.email==email)): raise HTTPException(409,"E-mail já cadastrado")
    user=User(name=data.name.strip(),email=email,password_hash=hash_password(data.password))
    db.add(user); await db.commit(); await db.refresh(user)
    return TokenOut(access_token=create_access_token(str(user.id),user.role.value))
@router.post("/login", response_model=TokenOut)
async def login(data:LoginIn, db:AsyncSession=Depends(get_db)):
    user=await db.scalar(select(User).where(User.email==data.email.lower()))
    if not user or not user.is_active or not verify_password(data.password,user.password_hash): raise HTTPException(401,"E-mail ou senha inválidos")
    return TokenOut(access_token=create_access_token(str(user.id),user.role.value))
@router.get("/me", response_model=UserOut)
async def me(user=Depends(current_user)): return UserOut(id=user.id,name=user.name,email=user.email,role=user.role.value)
