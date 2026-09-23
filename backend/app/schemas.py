import re
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict, field_validator

from .models import BookingStatus

INDIAN_MOBILE_REGEX = re.compile(r'^[6-9]\d{9}$')


def normalize_and_validate_mobile(v: str) -> str:
    """Strips spaces/dashes/+91 and requires a valid 10-digit Indian mobile number."""
    digits = re.sub(r'\D', '', v or '')
    if digits.startswith('0'):
        digits = digits.lstrip('0')
    if len(digits) == 12 and digits.startswith('91'):
        digits = digits[2:]
    if not INDIAN_MOBILE_REGEX.match(digits):
        raise ValueError('Enter a valid 10-digit mobile number')
    return digits


# ---------- Catalog ----------

class StateOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class AreaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    pincode: Optional[str] = None


class CityOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    slug: str
    state_id: int
    is_active: bool


class CityIn(BaseModel):
    name: str
    slug: str
    state_id: int
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    intro_copy: Optional[str] = None


class ServiceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    is_active: bool


class ServiceIn(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None


class BrandOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    is_active: bool


# ---------- Bookings ----------

class BookingCreate(BaseModel):
    customer_name: str = Field(min_length=2, max_length=120)
    mobile: str
    whatsapp: Optional[str] = None
    state_name: str
    city_id: Optional[int] = None
    city_name_other: Optional[str] = None
    area_pincode: str
    brand: Optional[str] = None
    machine_type: Optional[str] = None
    service_id: int
    problem_description: Optional[str] = None
    preferred_date: Optional[str] = None
    preferred_time: Optional[str] = None
    address: Optional[str] = None

    @field_validator('mobile')
    @classmethod
    def validate_mobile(cls, v):
        return normalize_and_validate_mobile(v)

    @field_validator('whatsapp')
    @classmethod
    def validate_whatsapp(cls, v):
        if v in (None, ''):
            return None
        return normalize_and_validate_mobile(v)


class BookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    booking_id: str
    customer_name: str
    mobile: str
    whatsapp: Optional[str]
    city_id: Optional[int]
    city_name_other: Optional[str]
    area_pincode: str
    brand: Optional[str]
    machine_type: Optional[str]
    service_id: int
    problem_description: Optional[str]
    preferred_date: Optional[str]
    preferred_time: Optional[str]
    address: Optional[str]
    status: BookingStatus
    technician_id: Optional[int]
    created_at: datetime


class BookingConfirmation(BaseModel):
    booking_id: str
    customer_name: str
    city_name: str
    service_name: str
    preferred_date: Optional[str]
    preferred_time: Optional[str]
    whatsapp_link: str
    message: str = "Your service request has been received successfully. Our service team will contact you shortly."


class BookingStatusUpdate(BaseModel):
    status: BookingStatus
    technician_id: Optional[int] = None


# ---------- Enquiries ----------

class EnquiryCreate(BaseModel):
    name: str
    mobile: str
    city_name: Optional[str] = None
    message: Optional[str] = None

    @field_validator('mobile')
    @classmethod
    def validate_mobile(cls, v):
        return normalize_and_validate_mobile(v)


class EnquiryConfirmation(BaseModel):
    id: int
    name: str
    whatsapp_link: str
    message: str = "Thanks — we've received your message and will get back to you shortly."


class EnquiryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    mobile: str
    city_name: Optional[str]
    message: Optional[str]
    created_at: datetime
    is_resolved: bool


# ---------- Technicians ----------

class TechnicianIn(BaseModel):
    name: str
    mobile: str
    whatsapp: Optional[str] = None
    city_id: int
    area: Optional[str] = None
    services: Optional[str] = None
    is_available: bool = True


class TechnicianOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    mobile: str
    whatsapp: Optional[str]
    city_id: int
    area: Optional[str]
    services: Optional[str]
    is_available: bool
    status: str


# ---------- Admin / Settings ----------

class AdminLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SettingsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    business_name: str
    business_mobile: str
    business_whatsapp: str
    business_email: str
    working_hours: str


class SettingsIn(BaseModel):
    business_name: Optional[str] = None
    business_mobile: Optional[str] = None
    business_whatsapp: Optional[str] = None
    business_email: Optional[str] = None
    working_hours: Optional[str] = None


class DashboardStats(BaseModel):
    total_bookings: int
    new_bookings: int
    pending_bookings: int
    confirmed_bookings: int
    completed_bookings: int
    cancelled_bookings: int
    total_enquiries: int
