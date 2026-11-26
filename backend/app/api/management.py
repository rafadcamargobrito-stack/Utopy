from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_roles
from app.db.session import get_db
from app.models import Activity, Official, OfficialProposal, User, UserRole
from app.schemas.content import ActivityCreate, OfficialProposalCreate, OfficialProposalOut

router = APIRouter(prefix="/management", tags=["management"])


async def current_official(user: User, db: AsyncSession) -> Official:
    official = await db.scalar(select(Official).where(Official.user_id == user.id))
    if not official:
        raise HTTPException(403, "Este perfil público ainda não está vinculado a um registro institucional")
    return official


@router.post("/proposals", response_model=OfficialProposalOut, status_code=201)
async def create_proposal(
    data: OfficialProposalCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles(UserRole.public_agent)),
):
    official = await current_official(user, db)
    proposal = OfficialProposal(official_id=official.id, **data.model_dump())
    official.projects += 1
    db.add(proposal)
    await db.commit()
    await db.refresh(proposal)
    return OfficialProposalOut(
        id=proposal.id,
        title=proposal.title,
        area=proposal.area,
        description=proposal.description,
        status=proposal.status,
        official_name=official.name,
        official_role=official.role,
        created_at=proposal.created_at,
    )


@router.post("/activities", status_code=201)
async def create_activity(
    data: ActivityCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles(UserRole.public_agent)),
):
    official = await current_official(user, db)
    activity = Activity(official_id=official.id, **data.model_dump())
    official.activities += 1
    db.add(activity)
    await db.commit()
    await db.refresh(activity)
    return {
        "id": activity.id,
        "title": activity.title,
        "description": activity.description,
        "occurred_at": activity.occurred_at,
        "official_name": official.name,
    }
