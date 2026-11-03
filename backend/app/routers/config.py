from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..schemas import MaskSettings, Profile
from ..services import settings_store as store

router = APIRouter(prefix="/api", tags=["config"])


@router.get("/settings", response_model=MaskSettings)
def get_settings(db: Session = Depends(get_db)):
    return store.get_mask(db)


@router.put("/settings", response_model=MaskSettings)
def put_settings(body: MaskSettings, db: Session = Depends(get_db)):
    return store.put_mask(db, body)


@router.get("/profile", response_model=Profile)
def get_profile(db: Session = Depends(get_db)):
    return store.get_profile(db)


@router.put("/profile", response_model=Profile)
def put_profile(body: Profile, db: Session = Depends(get_db)):
    return store.put_profile(db, body)
