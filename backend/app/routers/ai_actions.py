from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import AiAction
from ..schemas import AiActionOut

router = APIRouter(prefix="/api/ai-actions", tags=["ai-actions"])


@router.get("", response_model=list[AiActionOut])
def list_actions(
    status: str | None = None,
    action_type: str | None = None,
    limit: int = Query(50, le=200),
    offset: int = 0,
    db: Session = Depends(get_db),
):
    q = select(AiAction)
    if status:
        q = q.where(AiAction.status == status)
    if action_type:
        q = q.where(AiAction.action_type == action_type)
    return db.scalars(q.order_by(AiAction.created_at.desc()).limit(limit).offset(offset)).all()


@router.post("/{action_id}/reject", response_model=AiActionOut)
def reject(action_id: str, db: Session = Depends(get_db)):
    a = db.get(AiAction, action_id)
    if not a:
        raise HTTPException(404, "ai action not found")
    if a.status != "proposed":
        raise HTTPException(409, "ai action is not pending")
    a.status = "rejected"
    a.decided_at = datetime.now(UTC)
    db.commit()
    return a
