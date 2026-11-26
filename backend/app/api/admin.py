from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.db.session import get_db
from app.models import Official, ProjectIdea, ProjectIdeaStatusHistory, User, UserRole
from app.schemas.auth import AdminUserOut, UserRoleUpdate
from app.schemas.content import IdeaReviewUpdate
from app.api.deps import require_roles

router = APIRouter(prefix="/admin", tags=["admin"])
ALLOWED = {"Ideia inicial", "Em análise comunitária", "Em análise técnica", "Aprovada", "Rejeitada", "Em execução", "Concluída"}
TRANSITIONS = {
    "Ideia inicial": {"Em análise comunitária", "Rejeitada"},
    "Em análise comunitária": {"Em análise técnica", "Rejeitada"},
    "Em análise técnica": {"Aprovada", "Rejeitada", "Em análise comunitária"},
    "Aprovada": {"Em execução", "Rejeitada"},
    "Em execução": {"Concluída", "Rejeitada"},
    "Concluída": set(),
    "Rejeitada": {"Em análise comunitária"},
}

@router.get("/users", response_model=list[AdminUserOut])
async def list_users(db: AsyncSession = Depends(get_db), _=Depends(require_roles(UserRole.admin))):
    rows = (await db.execute(
        select(User, Official.role)
        .outerjoin(Official, Official.user_id == User.id)
        .order_by(User.name)
    )).all()
    return [
        AdminUserOut(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
            official_title=official_title,
        )
        for user, official_title in rows
    ]

@router.patch("/users/{user_id}/role", response_model=AdminUserOut)
async def update_user_role(
    user_id: int,
    data: UserRoleUpdate,
    db: AsyncSession = Depends(get_db),
    actor: User = Depends(require_roles(UserRole.admin)),
):
    user = await db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(404, "Usuário não encontrado")
    if user.id == actor.id and data.role != UserRole.admin:
        raise HTTPException(409, "Não é possível remover seu próprio perfil de administrador")
    if user.role == UserRole.admin and data.role != UserRole.admin:
        admin_count = await db.scalar(select(func.count()).select_from(User).where(User.role == UserRole.admin, User.is_active.is_(True)))
        if admin_count <= 1:
            raise HTTPException(409, "O sistema precisa manter ao menos um administrador ativo")

    official = await db.scalar(select(Official).where(Official.user_id == user.id))
    if data.role == UserRole.public_agent:
        if not data.official_title or not data.official_title.strip():
            raise HTTPException(422, "Informe o cargo público para este perfil")
        if official is None:
            official = Official(
                user_id=user.id,
                name=user.name,
                role=data.official_title.strip(),
                party=(data.party or "Não informado").strip(),
            )
            db.add(official)
        else:
            official.role = data.official_title.strip()
            official.party = (data.party or "Não informado").strip()
            official.name = user.name
    elif official is not None:
        official.user_id = None

    user.role = data.role
    await db.commit()
    await db.refresh(user)
    return AdminUserOut(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
        official_title=official.role if data.role == UserRole.public_agent and official else None,
    )

@router.patch("/ideas/{idea_id}/review")
async def review_idea(idea_id: int, data: IdeaReviewUpdate, db: AsyncSession = Depends(get_db), user=Depends(require_roles(UserRole.admin, UserRole.public_agent, UserRole.moderator))):
    if data.status not in ALLOWED: raise HTTPException(400, "Status inválido")
    idea = await db.scalar(select(ProjectIdea).where(ProjectIdea.id == idea_id))
    if not idea: raise HTTPException(404, "Ideia não encontrada")
    if data.status != idea.status and data.status not in TRANSITIONS.get(idea.status, set()):
        raise HTTPException(409, f"Transição não permitida de '{idea.status}' para '{data.status}'.")
    if data.status in {"Aprovada", "Rejeitada"} and not (data.decision_reason or data.note).strip():
        raise HTTPException(422, "Uma decisão de aprovação ou rejeição precisa de justificativa pública.")
    previous = idea.status
    idea.status = data.status
    idea.technical_note = data.technical_note
    idea.decision_reason = data.decision_reason or data.note
    idea.responsible_department = data.responsible_department
    idea.estimated_cost = data.estimated_cost
    db.add(ProjectIdeaStatusHistory(project_idea_id=idea.id, actor_id=user.id, from_status=previous, to_status=data.status, note=data.note))
    await db.commit()
    return {"id": idea.id, "status": idea.status}
