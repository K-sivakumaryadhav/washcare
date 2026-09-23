from urllib.parse import quote
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..notifications import send_email_notification

router = APIRouter(prefix="/api/bookings", tags=["bookings"])


def build_whatsapp_message(booking: models.Booking, city_name: str, service_name: str) -> str:
    return (
        "New Washing Machine Service Booking\n"
        f"Booking ID: {booking.booking_id}\n"
        f"Customer Name: {booking.customer_name}\n"
        f"Mobile: {booking.mobile}\n"
        f"WhatsApp: {booking.whatsapp or '-'}\n"
        f"City: {city_name}\n"
        f"Area/Pincode: {booking.area_pincode}\n"
        f"Brand: {booking.brand or '-'}\n"
        f"Machine Type: {booking.machine_type or '-'}\n"
        f"Service Required: {service_name}\n"
        f"Problem: {booking.problem_description or '-'}\n"
        f"Preferred Date: {booking.preferred_date or '-'}\n"
        f"Preferred Time: {booking.preferred_time or '-'}\n"
        f"Address: {booking.address or '-'}"
    )


@router.post("", response_model=schemas.BookingConfirmation)
def create_booking(payload: schemas.BookingCreate, db: Session = Depends(get_db)):
    city = None
    city_name = payload.city_name_other

    if payload.city_id:
        city = db.query(models.City).filter(models.City.id == payload.city_id).first()
        if not city:
            raise HTTPException(status_code=400, detail="Invalid city selected")
        city_name = city.name

    if not city_name:
        raise HTTPException(status_code=400, detail="Please select a city or enter your city name")

    service = db.query(models.ServiceType).filter(models.ServiceType.id == payload.service_id).first()
    if not service:
        raise HTTPException(status_code=400, detail="Invalid service selected")

    booking = models.Booking(
        customer_name=payload.customer_name,
        mobile=payload.mobile,
        whatsapp=payload.whatsapp,
        state_name=payload.state_name,
        city_id=payload.city_id,
        city_name_other=payload.city_name_other,
        area_pincode=payload.area_pincode,
        brand=payload.brand,
        machine_type=payload.machine_type,
        service_id=payload.service_id,
        problem_description=payload.problem_description,
        preferred_date=payload.preferred_date,
        preferred_time=payload.preferred_time,
        address=payload.address,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    settings = db.query(models.SiteSettings).first()
    business_whatsapp = (settings.business_whatsapp if settings else "").lstrip("+").replace(" ", "")
    message = build_whatsapp_message(booking, city_name, service.name)
    whatsapp_link = f"https://wa.me/{business_whatsapp}?text={quote(message)}"

    send_email_notification(subject=f"New booking {booking.booking_id} — {city_name}", body=message)

    return schemas.BookingConfirmation(
        booking_id=booking.booking_id,
        customer_name=booking.customer_name,
        city_name=city_name,
        service_name=service.name,
        preferred_date=booking.preferred_date,
        preferred_time=booking.preferred_time,
        whatsapp_link=whatsapp_link,
    )


@router.get("/{booking_id}", response_model=schemas.BookingOut)
def get_booking(booking_id: str, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking
