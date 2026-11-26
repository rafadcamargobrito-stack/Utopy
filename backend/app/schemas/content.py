from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class DiscussionCreate(BaseModel):
    title: str = Field(min_length=5, max_length=180)
    category: str = Field(min_length=2, max_length=60)
    excerpt: str = Field(min_length=10, max_length=3000)

class DiscussionOut(BaseModel):
    id: int; title: str; category: str; excerpt: str; author: str; time: str; replies: int; supports: int

class ReplyCreate(BaseModel):
    body: str = Field(min_length=1, max_length=5000)

class IdeaCreate(BaseModel):
    title: str = Field(min_length=5, max_length=180)
    area: str = Field(min_length=2, max_length=60)
    description: str = Field(min_length=10, max_length=5000)

class IdeaCommentCreate(BaseModel):
    body: str = Field(min_length=1, max_length=3000)

class IdeaCommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; author: str; body: str; created_at: datetime

class IdeaHistoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; actor: str; from_status: str | None; to_status: str; note: str | None; created_at: datetime

class IdeaOut(BaseModel):
    id: int; title: str; area: str; description: str; author: str; supports: int; status: str
    technical_note: str | None = None; decision_reason: str | None = None
    responsible_department: str | None = None; estimated_cost: float | None = None
    created_at: datetime; updated_at: datetime

class IdeaDetailOut(IdeaOut):
    comments: list[IdeaCommentOut] = []
    history: list[IdeaHistoryOut] = []

class IdeaReviewUpdate(BaseModel):
    status: str
    note: str = Field(min_length=3, max_length=5000)
    technical_note: str | None = Field(default=None, max_length=5000)
    decision_reason: str | None = Field(default=None, max_length=5000)
    responsible_department: str | None = Field(default=None, max_length=160)
    estimated_cost: float | None = Field(default=None, ge=0)

class OfficialOut(BaseModel):
    id: int; name: str; role: str; party: str; projects: int; activities: int; updated: str
class ActivityOut(BaseModel):
    id: int; title: str; description: str; occurred_at: datetime; official_name: str | None = None
class OfficialProposalCreate(BaseModel):
    title: str = Field(min_length=5, max_length=180)
    area: str = Field(min_length=2, max_length=60)
    description: str = Field(min_length=10, max_length=5000)
class OfficialProposalOut(BaseModel):
    id: int; title: str; area: str; description: str; status: str; official_name: str; official_role: str; created_at: datetime
class ActivityCreate(BaseModel):
    title: str = Field(min_length=5, max_length=180)
    description: str = Field(min_length=10, max_length=3000)
class WorkOut(BaseModel):
    id: int; name: str; area: str; progress: int; value: float; deadline: str
class DocumentOut(BaseModel):
    id: int; title: str; file_url: str; year: int; source: str; published_at: datetime
