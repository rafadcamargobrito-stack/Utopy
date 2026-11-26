from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.session import get_db
from app.models import User, Discussion, DiscussionReply, DiscussionSupport, ProjectIdea, ProjectIdeaSupport, ProjectIdeaComment, ProjectIdeaStatusHistory
from app.schemas.content import DiscussionCreate, DiscussionOut, ReplyCreate, IdeaCreate, IdeaOut, IdeaDetailOut, IdeaCommentCreate, IdeaCommentOut, IdeaHistoryOut
from app.api.deps import current_user

router = APIRouter(prefix="/community", tags=["community"])

async def count_for(db, model, field, value):
    return int((await db.scalar(select(func.count()).select_from(model).where(field == value))) or 0)

@router.get("/discussions", response_model=list[DiscussionOut])
async def discussions(db: AsyncSession = Depends(get_db), category: str | None = None, q: str | None = None):
    stmt = select(Discussion, User.name).join(User, User.id == Discussion.author_id).where(Discussion.is_published.is_(True)).order_by(Discussion.created_at.desc())
    if category and category != "Todas": stmt = stmt.where(Discussion.category == category)
    if q: stmt = stmt.where((Discussion.title.ilike(f"%{q}%")) | (Discussion.excerpt.ilike(f"%{q}%")))
    rows = (await db.execute(stmt)).all(); out = []
    for d, name in rows:
        replies = await count_for(db, DiscussionReply, DiscussionReply.discussion_id, d.id)
        supports = await count_for(db, DiscussionSupport, DiscussionSupport.discussion_id, d.id)
        out.append(DiscussionOut(id=d.id, title=d.title, category=d.category, excerpt=d.excerpt, author=name, time="recentemente", replies=replies, supports=supports))
    return out

@router.post("/discussions", response_model=DiscussionOut, status_code=201)
async def create_discussion(data: DiscussionCreate, db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    d = Discussion(**data.model_dump(), author_id=user.id); db.add(d); await db.commit(); await db.refresh(d)
    return DiscussionOut(id=d.id, title=d.title, category=d.category, excerpt=d.excerpt, author=user.name, time="agora", replies=0, supports=0)

@router.post("/discussions/{discussion_id}/support")
async def support_discussion(discussion_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    if not await db.scalar(select(Discussion).where(Discussion.id == discussion_id)): raise HTTPException(404, "Discussão não encontrada")
    existing = await db.scalar(select(DiscussionSupport).where(DiscussionSupport.discussion_id == discussion_id, DiscussionSupport.user_id == user.id))
    if existing: await db.delete(existing); action = "removed"
    else: db.add(DiscussionSupport(discussion_id=discussion_id, user_id=user.id)); action = "added"
    await db.commit(); return {"action": action, "supports": await count_for(db, DiscussionSupport, DiscussionSupport.discussion_id, discussion_id)}

@router.post("/discussions/{discussion_id}/replies", status_code=201)
async def reply(discussion_id: int, data: ReplyCreate, db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    if not await db.scalar(select(Discussion).where(Discussion.id == discussion_id)): raise HTTPException(404, "Discussão não encontrada")
    db.add(DiscussionReply(discussion_id=discussion_id, author_id=user.id, body=data.body)); await db.commit(); return {"ok": True}

async def idea_out(db, idea, author):
    return IdeaOut(id=idea.id, title=idea.title, area=idea.area, description=idea.description, author=author,
        supports=await count_for(db, ProjectIdeaSupport, ProjectIdeaSupport.project_idea_id, idea.id), status=idea.status,
        technical_note=idea.technical_note, decision_reason=idea.decision_reason, responsible_department=idea.responsible_department,
        estimated_cost=float(idea.estimated_cost) if idea.estimated_cost is not None else None, created_at=idea.created_at, updated_at=idea.updated_at)

@router.get("/ideas", response_model=list[IdeaOut])
async def ideas(db: AsyncSession = Depends(get_db), status: str | None = None, area: str | None = None):
    stmt = select(ProjectIdea, User.name).join(User, User.id == ProjectIdea.author_id).order_by(ProjectIdea.created_at.desc())
    if status: stmt = stmt.where(ProjectIdea.status == status)
    if area: stmt = stmt.where(ProjectIdea.area == area)
    rows = (await db.execute(stmt)).all()
    return [await idea_out(db, i, name) for i, name in rows]

@router.get("/ideas/{idea_id}", response_model=IdeaDetailOut)
async def idea_detail(idea_id: int, db: AsyncSession = Depends(get_db)):
    row = (await db.execute(select(ProjectIdea, User.name).join(User, User.id == ProjectIdea.author_id).where(ProjectIdea.id == idea_id))).first()
    if not row: raise HTTPException(404, "Ideia não encontrada")
    idea, author = row
    comments = (await db.execute(select(ProjectIdeaComment, User.name).join(User, User.id == ProjectIdeaComment.author_id).where(ProjectIdeaComment.project_idea_id == idea_id).order_by(ProjectIdeaComment.created_at.asc()))).all()
    history = (await db.execute(select(ProjectIdeaStatusHistory, User.name).join(User, User.id == ProjectIdeaStatusHistory.actor_id).where(ProjectIdeaStatusHistory.project_idea_id == idea_id).order_by(ProjectIdeaStatusHistory.created_at.asc()))).all()
    base = await idea_out(db, idea, author)
    return IdeaDetailOut(**base.model_dump(), comments=[IdeaCommentOut(id=c.id, author=n, body=c.body, created_at=c.created_at) for c,n in comments], history=[IdeaHistoryOut(id=h.id, actor=n, from_status=h.from_status, to_status=h.to_status, note=h.note, created_at=h.created_at) for h,n in history])

@router.post("/ideas", response_model=IdeaOut, status_code=201)
async def create_idea(data: IdeaCreate, db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    idea = ProjectIdea(**data.model_dump(), author_id=user.id); db.add(idea); await db.flush()
    db.add(ProjectIdeaStatusHistory(project_idea_id=idea.id, actor_id=user.id, from_status=None, to_status=idea.status, note="Ideia enviada pela comunidade."))
    await db.commit(); await db.refresh(idea)
    return await idea_out(db, idea, user.name)

@router.post("/ideas/{idea_id}/support")
async def support_idea(idea_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    idea = await db.scalar(select(ProjectIdea).where(ProjectIdea.id == idea_id))
    if not idea: raise HTTPException(404, "Ideia não encontrada")
    existing = await db.scalar(select(ProjectIdeaSupport).where(ProjectIdeaSupport.project_idea_id == idea_id, ProjectIdeaSupport.user_id == user.id))
    if existing: await db.delete(existing); action = "removed"
    else: db.add(ProjectIdeaSupport(project_idea_id=idea_id, user_id=user.id)); action = "added"
    await db.commit(); return {"action": action, "supports": await count_for(db, ProjectIdeaSupport, ProjectIdeaSupport.project_idea_id, idea_id)}

@router.post("/ideas/{idea_id}/comments", response_model=IdeaCommentOut, status_code=201)
async def comment_idea(idea_id: int, data: IdeaCommentCreate, db: AsyncSession = Depends(get_db), user: User = Depends(current_user)):
    if not await db.scalar(select(ProjectIdea).where(ProjectIdea.id == idea_id)): raise HTTPException(404, "Ideia não encontrada")
    comment = ProjectIdeaComment(project_idea_id=idea_id, author_id=user.id, body=data.body); db.add(comment); await db.flush(); await db.commit(); await db.refresh(comment)
    return IdeaCommentOut(id=comment.id, author=user.name, body=comment.body, created_at=comment.created_at)
