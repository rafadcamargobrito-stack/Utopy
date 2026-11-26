from datetime import datetime, timezone
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, Boolean, Numeric, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


def utcnow():
    return datetime.now(timezone.utc)


class Discussion(Base):
    __tablename__ = "discussions"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(180))
    category: Mapped[str] = mapped_column(String(60), index=True)
    excerpt: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)


class DiscussionReply(Base):
    __tablename__ = "discussion_replies"
    id: Mapped[int] = mapped_column(primary_key=True)
    discussion_id: Mapped[int] = mapped_column(ForeignKey("discussions.id", ondelete="CASCADE"), index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class DiscussionSupport(Base):
    __tablename__ = "discussion_supports"
    __table_args__ = (UniqueConstraint("discussion_id", "user_id", name="uq_discussion_support_user"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    discussion_id: Mapped[int] = mapped_column(ForeignKey("discussions.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)


class ProjectIdea(Base):
    __tablename__ = "project_ideas"
    __table_args__ = (
        CheckConstraint("length(title) >= 5", name="ck_project_idea_title"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(180))
    area: Mapped[str] = mapped_column(String(60), index=True)
    description: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(50), default="Ideia inicial", index=True)
    technical_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    decision_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    responsible_department: Mapped[str | None] = mapped_column(String(160), nullable=True)
    estimated_cost: Mapped[float | None] = mapped_column(Numeric(14, 2), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)


class ProjectIdeaSupport(Base):
    __tablename__ = "project_idea_supports"
    __table_args__ = (UniqueConstraint("project_idea_id", "user_id", name="uq_project_idea_support_user"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    project_idea_id: Mapped[int] = mapped_column(ForeignKey("project_ideas.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)


class ProjectIdeaComment(Base):
    __tablename__ = "project_idea_comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_idea_id: Mapped[int] = mapped_column(ForeignKey("project_ideas.id", ondelete="CASCADE"), index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class ProjectIdeaStatusHistory(Base):
    __tablename__ = "project_idea_status_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_idea_id: Mapped[int] = mapped_column(ForeignKey("project_ideas.id", ondelete="CASCADE"), index=True)
    actor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    from_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    to_status: Mapped[str] = mapped_column(String(50))
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Official(Base):
    __tablename__ = "officials"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(150))
    role: Mapped[str] = mapped_column(String(100))
    party: Mapped[str] = mapped_column(String(120))
    projects: Mapped[int] = mapped_column(Integer, default=0)
    activities: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Activity(Base):
    __tablename__ = "activities"
    id: Mapped[int] = mapped_column(primary_key=True)
    official_id: Mapped[int | None] = mapped_column(ForeignKey("officials.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(180))
    description: Mapped[str] = mapped_column(Text)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class OfficialProposal(Base):
    __tablename__ = "official_proposals"
    id: Mapped[int] = mapped_column(primary_key=True)
    official_id: Mapped[int] = mapped_column(ForeignKey("officials.id"), index=True)
    title: Mapped[str] = mapped_column(String(180))
    area: Mapped[str] = mapped_column(String(60))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="Apresentada")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Work(Base):
    __tablename__ = "works"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(180))
    area: Mapped[str] = mapped_column(String(60))
    progress: Mapped[int] = mapped_column(Integer, default=0)
    value: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    deadline: Mapped[str] = mapped_column(String(40))


class TransparencyDocument(Base):
    __tablename__ = "transparency_documents"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(220))
    file_url: Mapped[str] = mapped_column(String(500))
    year: Mapped[int] = mapped_column(Integer)
    source: Mapped[str] = mapped_column(String(250))
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
