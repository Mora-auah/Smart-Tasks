from sqlalchemy.orm import Session

from ..models import AppSetting
from ..schemas import MaskSettings, Profile


def _get(db: Session, key: str, default: dict) -> dict:
    row = db.get(AppSetting, key)
    return row.value if row else default


def _put(db: Session, key: str, value: dict) -> None:
    row = db.get(AppSetting, key)
    if row:
        row.value = value
    else:
        db.add(AppSetting(key=key, value=value))
    db.commit()


def get_mask(db: Session) -> MaskSettings:
    return MaskSettings(**_get(db, "mask", {}))


def put_mask(db: Session, v: MaskSettings) -> MaskSettings:
    _put(db, "mask", v.model_dump())
    return v


def get_profile(db: Session) -> Profile:
    return Profile(**_get(db, "profile", {}))


def put_profile(db: Session, v: Profile) -> Profile:
    _put(db, "profile", v.model_dump())
    return v
