from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from app.models import *
from app.api import auth,community,public,admin,management

@asynccontextmanager
async def lifespan(app:FastAPI):
    if settings.app_env == "development":
        async with engine.begin() as conn: await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
app=FastAPI(title="Utopy API",version="1.0.0",description="API da Plataforma Digital de Participação Cidadã e Transparência Pública",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_list,allow_credentials=False,allow_methods=["GET","POST","PATCH","DELETE","OPTIONS"],allow_headers=["Authorization","Content-Type"])
@app.get("/health")
async def health(): return {"status":"ok"}
app.include_router(auth.router,prefix="/api/v1")
app.include_router(community.router,prefix="/api/v1")
app.include_router(public.router,prefix="/api/v1")
app.include_router(admin.router,prefix="/api/v1")
app.include_router(management.router,prefix="/api/v1")
