from urllib.parse import quote
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..notifications import send_email_notification

router = APIRouter(prefix="/api/enquiries", tags=["enquiries"])


@router.post("", response_model=schemas.EnquiryConfirmation)
def create_enquiry(payload: schemas.EnquiryCreate, db: Session = Depends(get_db)):
    enquiry = models.Enquiry(**payload.model_dump())
    db.add(enquiry)
    db.commit()
    db.refresh(enquiry)

    settings = db.query(models.SiteSettings).first()
    business_whatsapp = (settings.business_whatsapp if settings else "").lstrip("+").replace(" ", "")

    message = (
        "New Website Enquiry\n"
        f"Name: {enquiry.name}\n"
        f"Mobile: {enquiry.mobile}\n"
        f"City: {enquiry.city_name or '-'}\n"
        f"Message: {enquiry.message or '-'}"
    )
    whatsapp_link = f"https://wa.me/{business_whatsapp}?text={quote(message)}"

    send_email_notification(subject=f"New enquiry from {enquiry.name}", body=message)

    return schemas.EnquiryConfirmation(id=enquiry.id, name=enquiry.name, whatsapp_link=whatsapp_link)
