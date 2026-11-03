from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import AiAction, Task
from ..schemas import TaskCreate, TaskOut, TaskUpdate

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


def _snapshot(t: Task) -> dict:
    return TaskOut.model_validate(t).model_dump(mode="json")


def _decide(db: Session, ai_action_id: str | None, before: dict | None, task: Task | None):
    """Mark the audit row approved in the same transaction as the task change."""
    if not ai_action_id:
        return
    a = db.get(AiAction, ai_action_id)
    if a is None or a.status != "proposed":
        raise HTTPException(409, "ai action is not pending")
    a.status = "approved"
    a.decided_at = datetime.now(UTC)
    a.before = before
    a.after = _snapshot(task) if task else None
    if task:
        a.task_id = task.id


def _get_or_404(db: Session, task_id: int) -> Task:
    t = db.get(Task, task_id)
    if not t:
        raise HTTPException(404, "task not found")
    return t


@router.get("", response_model=list[TaskOut])
def list_tasks(status: str | None = Query(None), db: Session = Depends(get_db)):
    q = select(Task)
    if status:
        q = q.where(Task.status.in_(status.split(",")))
    return db.scalars(q.order_by(Task.due_date.is_(None), Task.due_date, Task.id)).all()


@router.post("", response_model=TaskOut, status_code=201)
def create_task(body: TaskCreate, db: Session = Depends(get_db)):
    data = body.model_dump(exclude={"ai_action_id"})
    t = Task(**data)
    if t.status == "done":
        t.completed_at = datetime.now(UTC)
    db.add(t)
    db.flush()
    _decide(db, body.ai_action_id, None, t)
    db.commit()
    return t


@router.patch("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, body: TaskUpdate, db: Session = Depends(get_db)):
    t = _get_or_404(db, task_id)
    if body.expected_updated_at and t.updated_at.replace(tzinfo=None) > body.expected_updated_at.replace(tzinfo=None):
        raise HTTPException(409, "task changed since the proposal")
    before = _snapshot(t)
    for k, v in body.model_dump(exclude_unset=True, exclude={"ai_action_id", "expected_updated_at"}).items():
        setattr(t, k, v)
    if t.status == "done" and not t.completed_at:
        t.completed_at = datetime.now(UTC)
    _decide(db, body.ai_action_id, before, t)
    db.commit()
    return t


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, ai_action_id: str | None = None, db: Session = Depends(get_db)):
    t = _get_or_404(db, task_id)
    before = _snapshot(t)
    db.delete(t)
    _decide(db, ai_action_id, before, None)
    db.commit()


@router.post("/{task_id}/complete", response_model=TaskOut)
def complete_task(task_id: int, ai_action_id: str | None = None, db: Session = Depends(get_db)):
    t = _get_or_404(db, task_id)
    before = _snapshot(t)
    t.status = "done"
    t.completed_at = datetime.now(UTC)
    _decide(db, ai_action_id, before, t)
    db.commit()
    return t


@router.post("/{task_id}/reopen", response_model=TaskOut)
def reopen_task(task_id: int, db: Session = Depends(get_db)):
    t = _get_or_404(db, task_id)
    t.status = "open"
    t.completed_at = None
    db.commit()
    return t
