from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models import Official,Activity,OfficialProposal,Work,TransparencyDocument,Discussion,ProjectIdea,User
from app.models.user import UserRole
from app.schemas.content import OfficialOut,ActivityOut,OfficialProposalOut,WorkOut,DocumentOut
router=APIRouter(prefix="/public",tags=["public"])
@router.get("/officials",response_model=list[OfficialOut])
async def officials(db:AsyncSession=Depends(get_db)):
    rows=(await db.execute(select(Official).order_by(Official.name))).scalars().all();return [OfficialOut(id=x.id,name=x.name,role=x.role,party=x.party,projects=x.projects,activities=x.activities,updated=x.updated_at.strftime('%d %b %Y')) for x in rows]
@router.get("/activities",response_model=list[ActivityOut])
async def activities(db:AsyncSession=Depends(get_db)):
    rows=(await db.execute(select(Activity,Official.name).outerjoin(Official,Official.id==Activity.official_id).order_by(Activity.occurred_at.desc()).limit(30))).all()
    return [ActivityOut(id=a.id,title=a.title,description=a.description,occurred_at=a.occurred_at,official_name=name) for a,name in rows]
@router.get("/official-proposals",response_model=list[OfficialProposalOut])
async def official_proposals(db:AsyncSession=Depends(get_db)):
    rows=(await db.execute(select(OfficialProposal,Official.name,Official.role).join(Official,Official.id==OfficialProposal.official_id).order_by(OfficialProposal.created_at.desc()))).all()
    return [OfficialProposalOut(id=p.id,title=p.title,area=p.area,description=p.description,status=p.status,official_name=name,official_role=role,created_at=p.created_at) for p,name,role in rows]
@router.get("/works",response_model=list[WorkOut])
async def works(db:AsyncSession=Depends(get_db)):
    return (await db.execute(select(Work).order_by(Work.id))).scalars().all()
@router.get("/documents",response_model=list[DocumentOut])
async def documents(db:AsyncSession=Depends(get_db)):
    return (await db.execute(select(TransparencyDocument).order_by(TransparencyDocument.published_at.desc()))).scalars().all()
@router.get("/stats")
async def stats(db:AsyncSession=Depends(get_db)):
    from sqlalchemy import func
    return {"discussions":await db.scalar(select(func.count()).select_from(Discussion)),"works":await db.scalar(select(func.count()).select_from(Work)),"ideas":await db.scalar(select(func.count()).select_from(ProjectIdea)),"citizens":await db.scalar(select(func.count()).select_from(User).where(User.role==UserRole.citizen))}
