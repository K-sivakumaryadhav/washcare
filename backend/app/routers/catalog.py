from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/catalog", tags=["catalog"])


@router.get("/states", response_model=List[schemas.StateOut])
def list_states(db: Session = Depends(get_db)):
    return db.query(models.State).order_by(models.State.name).all()


@router.get("/cities", response_model=List[schemas.CityOut])
def list_cities(state_id: Optional[int] = None, db: Session = Depends(get_db)):
    q = db.query(models.City).filter(models.City.is_active == True)  # noqa: E712
    if state_id:
        q = q.filter(models.City.state_id == state_id)
    return q.order_by(models.City.name).all()


@router.get("/cities/{slug}/areas", response_model=List[schemas.AreaOut])
def list_areas(slug: str, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.slug == slug).first()
    if not city:
        return []
    return city.areas


@router.get("/services", response_model=List[schemas.ServiceOut])
def list_services(db: Session = Depends(get_db)):
    return db.query(models.ServiceType).filter(models.ServiceType.is_active == True).all()  # noqa: E712


@router.get("/brands", response_model=List[schemas.BrandOut])
def list_brands(db: Session = Depends(get_db)):
    return db.query(models.Brand).filter(models.Brand.is_active == True).all()  # noqa: E712


@router.get("/settings", response_model=schemas.SettingsOut)
def public_settings(db: Session = Depends(get_db)):
    """Business phone/WhatsApp numbers, pulled from DB — never hard-coded in frontend."""
    settings = db.query(models.SiteSettings).first()
    return settings
