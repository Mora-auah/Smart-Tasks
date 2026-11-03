from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Priority = Literal["low", "medium", "high"]
Status = Literal["open", "in_progress", "done"]
Page = Literal["tasks", "settings", "archive", "profile"]


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    due_date: date | None = None
    priority: Priority = "medium"
    status: Status = "open"


class TaskCreate(TaskBase):
    ai_action_id: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    due_date: date | None = None
    priority: Priority | None = None
    status: Status | None = None
    ai_action_id: str | None = None
    # Optimistic-concurrency token: updated_at as seen when the AI proposed the change
    expected_updated_at: datetime | None = None


class TaskOut(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None


class AiActionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    message_id: int | None
    response_id: str | None
    action_type: str
    task_id: int | None
    proposed: dict | None
    before: dict | None
    after: dict | None
    status: str
    created_at: datetime
    decided_at: datetime | None


class MaskSettings(BaseModel):
    phone: bool = True
    id: bool = True
    account: bool = True
    card: bool = True
    email: bool = True


class Profile(BaseModel):
    name: str = ""
    business: str = ""
