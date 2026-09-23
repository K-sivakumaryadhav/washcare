"""Run once to populate initial catalog data: python -m app.seed"""
import re
from .database import SessionLocal, engine, Base
from .models import State, City, ServiceType, Brand, AdminUser, SiteSettings
from .auth import hash_password

STATE_CITY_MAP = {
    "Karnataka": ["Bengaluru"],
    "Telangana": ["Hyderabad"],
    "Tamil Nadu": ["Chennai", "Coimbatore"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
    "Delhi": ["Delhi"],
    "Haryana": ["Gurgaon"],
    "Uttar Pradesh": ["Noida", "Lucknow"],
    "West Bengal": ["Kolkata"],
    "Gujarat": ["Ahmedabad", "Surat"],
    "Rajasthan": ["Jaipur"],
    "Andhra Pradesh": ["Vijayawada", "Visakhapatnam", "Tirupati"],
    "Kerala": ["Kochi"],
    "Chandigarh": ["Chandigarh"],
    "Madhya Pradesh": ["Indore", "Bhopal"],
    "Bihar": ["Patna"],
}

SERVICES = [
    ("Washing Machine Repair", "Diagnose and fix any washing machine fault at your doorstep."),
    ("Washing Machine Installation", "Professional installation for new front load, top load and semi-automatic machines."),
    ("Washing Machine Uninstallation", "Safe uninstallation before you shift or replace your machine."),
    ("Washing Machine General Service", "Routine cleaning and maintenance to keep your machine running smoothly."),
    ("Drainage Problem", "Fix water not draining or slow draining issues."),
    ("Not Starting", "Troubleshoot and repair a washing machine that won't power on or start a cycle."),
    ("Water Leakage", "Stop leaks from the drum, hose or door seal."),
    ("Noise / Vibration", "Resolve excessive noise or vibration during the wash or spin cycle."),
    ("Other Problems", "Any other washing machine issue not listed above."),
]

BRANDS = ["LG", "Samsung", "Whirlpool", "IFB", "Bosch", "Panasonic", "Haier", "Godrej", "Others"]


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(SiteSettings).first():
            db.add(SiteSettings(id=1))

        if not db.query(AdminUser).filter_by(username="admin").first():
            db.add(AdminUser(username="admin", hashed_password=hash_password("ChangeMe123!")))

        for state_name, cities in STATE_CITY_MAP.items():
            state = db.query(State).filter_by(name=state_name).first()
            if not state:
                state = State(name=state_name)
                db.add(state)
                db.flush()
            for city_name in cities:
                slug = slugify(city_name)
                if not db.query(City).filter_by(slug=slug).first():
                    db.add(City(
                        name=city_name,
                        slug=slug,
                        state_id=state.id,
                        seo_title=f"Washing Machine Repair & Service in {city_name} | Doorstep Technicians",
                        seo_description=(
                            f"Book verified washing machine repair, installation and service in {city_name}. "
                            f"Same-day doorstep visits for all major brands."
                        ),
                        intro_copy=(
                            f"Looking for a reliable washing machine technician in {city_name}? "
                            f"We connect you with experienced local professionals who handle repairs, "
                            f"installation, uninstallation and general service for all major brands, "
                            f"right at your doorstep in {city_name}."
                        ),
                    ))

        for name, desc in SERVICES:
            slug = slugify(name)
            if not db.query(ServiceType).filter_by(slug=slug).first():
                db.add(ServiceType(name=name, slug=slug, description=desc))

        for brand_name in BRANDS:
            if not db.query(Brand).filter_by(name=brand_name).first():
                db.add(Brand(name=brand_name))

        db.commit()
        print("Seed complete. Default admin login -> username: admin / password: ChangeMe123!")
        print("IMPORTANT: change this password immediately after first login.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
