from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..auth import verify_password, create_access_token, get_current_admin

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = db.query(models.AdminUser).filter(models.AdminUser.username == form_data.username).first()
    if not admin or not verify_password(form_data.password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token({"sub": admin.username})
    return schemas.Token(access_token=token)


@router.get("/dashboard", response_model=schemas.DashboardStats, dependencies=[Depends(get_current_admin)])
def dashboard(db: Session = Depends(get_db)):
    B = models.Booking
    total = db.query(B).count()
    def count(status):
        return db.query(B).filter(B.status == status).count()
    return schemas.DashboardStats(
        total_bookings=total,
        new_bookings=count(models.BookingStatus.NEW),
        pending_bookings=count(models.BookingStatus.CONTACTED) + count(models.BookingStatus.TECHNICIAN_ASSIGNED),
        confirmed_bookings=count(models.BookingStatus.CONFIRMED),
        completed_bookings=count(models.BookingStatus.COMPLETED),
        cancelled_bookings=count(models.BookingStatus.CANCELLED),
        total_enquiries=db.query(models.Enquiry).count(),
    )


@router.get("/bookings", response_model=List[schemas.BookingOut], dependencies=[Depends(get_current_admin)])
def list_bookings(status: Optional[models.BookingStatus] = None, city_id: Optional[int] = None,
                   db: Session = Depends(get_db)):
    q = db.query(models.Booking)
    if status:
        q = q.filter(models.Booking.status == status)
    if city_id:
        q = q.filter(models.Booking.city_id == city_id)
    return q.order_by(models.Booking.created_at.desc()).all()


@router.patch("/bookings/{booking_id}", response_model=schemas.BookingOut, dependencies=[Depends(get_current_admin)])
def update_booking(booking_id: str, payload: schemas.BookingStatusUpdate, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.status = payload.status
    if payload.technician_id is not None:
        booking.technician_id = payload.technician_id
    db.commit()
    db.refresh(booking)
    return booking


@router.get("/enquiries", response_model=List[schemas.EnquiryOut], dependencies=[Depends(get_current_admin)])
def list_enquiries(db: Session = Depends(get_db)):
    return db.query(models.Enquiry).order_by(models.Enquiry.created_at.desc()).all()


# ---------- Technicians ----------

@router.get("/technicians", response_model=List[schemas.TechnicianOut], dependencies=[Depends(get_current_admin)])
def list_technicians(city_id: Optional[int] = None, db: Session = Depends(get_db)):
    q = db.query(models.Technician)
    if city_id:
        q = q.filter(models.Technician.city_id == city_id)
    return q.all()


@router.post("/technicians", response_model=schemas.TechnicianOut, dependencies=[Depends(get_current_admin)])
def create_technician(payload: schemas.TechnicianIn, db: Session = Depends(get_db)):
    tech = models.Technician(**payload.model_dump())
    db.add(tech)
    db.commit()
    db.refresh(tech)
    return tech


@router.delete("/technicians/{tech_id}", dependencies=[Depends(get_current_admin)])
def delete_technician(tech_id: int, db: Session = Depends(get_db)):
    tech = db.query(models.Technician).filter(models.Technician.id == tech_id).first()
    if tech:
        db.delete(tech)
        db.commit()
    return {"ok": True}


# ---------- Catalog management ----------

@router.post("/cities", response_model=schemas.CityOut, dependencies=[Depends(get_current_admin)])
def add_city(payload: schemas.CityIn, db: Session = Depends(get_db)):
    city = models.City(**payload.model_dump())
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


@router.post("/services", response_model=schemas.ServiceOut, dependencies=[Depends(get_current_admin)])
def add_service(payload: schemas.ServiceIn, db: Session = Depends(get_db)):
    service = models.ServiceType(**payload.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


# ---------- Settings ----------

@router.get("/settings", response_model=schemas.SettingsOut, dependencies=[Depends(get_current_admin)])
def get_settings(db: Session = Depends(get_db)):
    return db.query(models.SiteSettings).first()


@router.put("/settings", response_model=schemas.SettingsOut, dependencies=[Depends(get_current_admin)])
def update_settings(payload: schemas.SettingsIn, db: Session = Depends(get_db)):
    settings = db.query(models.SiteSettings).first()
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(settings, field, value)
    db.commit()
    db.refresh(settings)
    return settings
