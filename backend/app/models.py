import uuid
from datetime import UTC, date, datetime

from sqlalchemy import JSON, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


def utcnow() -> datetime:
    return datetime.now(UTC)


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    due_date: Mapped[date | None] = mapped_column(Date)
    priority: Mapped[str] = mapped_column(String, default="medium")  # low/medium/high
    status: Mapped[str] = mapped_column(String, default="open")  # open/in_progress/done
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, onupdate=utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)


class ChatDay(Base):
    """One row per working day; empty summary_generated_at = summary not yet created."""

    __tablename__ = "chat_days"

    day: Mapped[date] = mapped_column(Date, primary_key=True)
    summary_generated_at: Mapped[datetime | None] = mapped_column(DateTime)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    day: Mapped[date] = mapped_column(ForeignKey("chat_days.day"), index=True)
    role: Mapped[str] = mapped_column(String)  # user/assistant
    kind: Mapped[str] = mapped_column(String, default="message")  # message/daily_summary
    content: Mapped[str] = mapped_column(Text)  # original text, unmasked
    payload: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class AiAction(Base):
    """Audit log: rows are never deleted or edited apart from the status transition."""

    __tablename__ = "ai_actions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    message_id: Mapped[int | None] = mapped_column(ForeignKey("chat_messages.id"))
    response_id: Mapped[str | None] = mapped_column(String)
    action_type: Mapped[str] = mapped_column(String)
    task_id: Mapped[int | None] = mapped_column(Integer)
    proposed: Mapped[dict | None] = mapped_column(JSON)
    before: Mapped[dict | None] = mapped_column(JSON)
    after: Mapped[dict | None] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String, default="proposed")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime)


class AppSetting(Base):
    """Key/value store for masking toggles and profile (not in the spec's 4 tables)."""

    __tablename__ = "app_settings"

    key: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[dict] = mapped_column(JSON)
