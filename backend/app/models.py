import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, ForeignKey, Text, Enum as SAEnum
)
from sqlalchemy.orm import relationship

from .database import Base


def short_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"


class BookingStatus(str, enum.Enum):
    NEW = "New"
    CONTACTED = "Contacted"
    CONFIRMED = "Confirmed"
    TECHNICIAN_ASSIGNED = "Technician Assigned"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class State(Base):
    __tablename__ = "states"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    cities = relationship("City", back_populates="state", cascade="all, delete-orphan")


class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(120), unique=True, nullable=False, index=True)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    # Unique SEO copy per city page (section 13 - no duplicate content)
    seo_title = Column(String(200))
    seo_description = Column(String(300))
    intro_copy = Column(Text)

    state = relationship("State", back_populates="cities")
    areas = relationship("Area", back_populates="city", cascade="all, delete-orphan")


class Area(Base):
    __tablename__ = "areas"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    pincode = Column(String(10))
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)

    city = relationship("City", back_populates="areas")


class ServiceType(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False)
    slug = Column(String(140), unique=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)


class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)


class Technician(Base):
    __tablename__ = "technicians"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    mobile = Column(String(20), nullable=False)
    whatsapp = Column(String(20))
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    area = Column(String(120))
    services = Column(String(300))  # comma separated service slugs
    is_available = Column(Boolean, default=True)
    status = Column(String(30), default="Active")  # Active / Inactive

    city = relationship("City")
    bookings = relationship("Booking", back_populates="technician")


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    booking_id = Column(String(20), unique=True, default=lambda: short_id("WC"))
    customer_name = Column(String(120), nullable=False)
    mobile = Column(String(20), nullable=False)
    whatsapp = Column(String(20))
    state_name = Column(String(100), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=True)
    area_pincode = Column(String(120), nullable=False)
    city_name_other = Column(String(120), nullable=True)  # used when customer's city isn't in our list
    brand = Column(String(80))
    machine_type = Column(String(40))  # Front Load / Top Load / Semi Automatic / Fully Automatic
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    problem_description = Column(Text)
    preferred_date = Column(String(20))
    preferred_time = Column(String(20))
    address = Column(Text)
    status = Column(SAEnum(BookingStatus), default=BookingStatus.NEW)
    technician_id = Column(Integer, ForeignKey("technicians.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    city = relationship("City")
    service = relationship("ServiceType")
    technician = relationship("Technician", back_populates="bookings")


class Enquiry(Base):
    __tablename__ = "enquiries"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    mobile = Column(String(20), nullable=False)
    city_name = Column(String(100))
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_resolved = Column(Boolean, default=False)


class AdminUser(Base):
    __tablename__ = "admin_users"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)


class SiteSettings(Base):
    """Single-row table for business-wide configurable settings (never hard-coded)."""
    __tablename__ = "site_settings"
    id = Column(Integer, primary_key=True, default=1)
    business_name = Column(String(150), default="WashCare India")
    business_mobile = Column(String(20), default="+91 90000 00000")
    business_whatsapp = Column(String(20), default="+91 90000 00000")
    business_email = Column(String(120), default="support@washcareindia.com")
    working_hours = Column(String(120), default="7:00 AM - 10:00 PM, All days")
