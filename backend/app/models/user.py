from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Boolean, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
import enum
class UserRole(str, enum.Enum): citizen="citizen"; moderator="moderator"; public_agent="public_agent"; admin="admin"
class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(120))
    email: Mapped[str]=mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str]=mapped_column(String(255))
    role: Mapped[UserRole]=mapped_column(SAEnum(UserRole), default=UserRole.citizen)
    is_active: Mapped[bool]=mapped_column(Boolean, default=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
