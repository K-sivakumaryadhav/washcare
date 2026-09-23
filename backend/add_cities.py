#!/usr/bin/env python3
"""Add SEO cities to the database."""

from app.database import SessionLocal, engine, Base
from app.models import State, City
from dotenv import load_dotenv

load_dotenv()

# Ensure tables exist
Base.metadata.create_all(bind=engine)

session = SessionLocal()

# Cities with SEO content
cities_data = [
    {
        "state": "Andhra Pradesh",
        "name": "Hyderabad",
        "slug": "hyderabad",
        "seo_title": "Washing Machine Repair & Service in Hyderabad | WashCare India",
        "seo_description": "Professional washing machine repair and service in Hyderabad. Same-day technician, warranty service, all brands - LG, Samsung, IFB, Whirlpool, Bosch.",
        "intro_copy": "Expert washing machine repair and installation services in Hyderabad. Our certified technicians provide same-day service for all brands of washing machines. Call now for free diagnosis."
    },
    {
        "state": "Maharashtra",
        "name": "Mumbai",
        "slug": "mumbai",
        "seo_title": "Washing Machine Repair in Mumbai | Same-Day Service | WashCare India",
        "seo_description": "Fast washing machine repair service in Mumbai. Certified technicians, genuine spare parts, all brands covered. Book online or call for same-day service.",
        "intro_copy": "Get professional washing machine repair and service in Mumbai. From routine maintenance to major repairs, our experienced technicians handle all brands and models."
    },
    {
        "state": "Delhi",
        "name": "Delhi",
        "slug": "delhi",
        "seo_title": "Washing Machine Repair Service in Delhi | WashCare India",
        "seo_description": "Reliable washing machine repair service in Delhi. Same-day technician visit, warranty service, all major brands - LG, Samsung, IFB, Whirlpool, Bosch.",
        "intro_copy": "Professional washing machine repair and maintenance in Delhi. We service all major brands and offer same-day technician visits throughout Delhi."
    },
    {
        "state": "Tamil Nadu",
        "name": "Chennai",
        "slug": "chennai",
        "seo_title": "Washing Machine Repair & Service in Chennai | WashCare India",
        "seo_description": "Expert washing machine repair in Chennai. Same-day service, genuine parts, warranty coverage for all washing machine brands.",
        "intro_copy": "Trusted washing machine repair service in Chennai. Our certified technicians provide prompt service for all brands and types of washing machines."
    },
    {
        "state": "Karnataka",
        "name": "Bangalore",
        "slug": "bangalore",
        "seo_title": "Washing Machine Repair Service in Bangalore | WashCare India",
        "seo_description": "Professional washing machine repair and service in Bangalore. Same-day technician, all brands covered, genuine spare parts, warranty service.",
        "intro_copy": "Bangalore's trusted washing machine repair service. Same-day technician availability, warranty service, and expert repairs for all brands."
    }
]

try:
    for city_info in cities_data:
        # Get or create state
        state = session.query(State).filter_by(name=city_info["state"]).first()
        if not state:
            state = State(name=city_info["state"])
            session.add(state)
            session.flush()
            print(f"✓ Created state: {city_info['state']}")

        # Check if city already exists
        existing_city = session.query(City).filter_by(slug=city_info["slug"]).first()
        if existing_city:
            # Update if exists
            existing_city.seo_title = city_info["seo_title"]
            existing_city.seo_description = city_info["seo_description"]
            existing_city.intro_copy = city_info["intro_copy"]
            print(f"✓ Updated city: {city_info['name']}")
        else:
            # Create new city
            city = City(
                name=city_info["name"],
                slug=city_info["slug"],
                state_id=state.id,
                is_active=True,
                seo_title=city_info["seo_title"],
                seo_description=city_info["seo_description"],
                intro_copy=city_info["intro_copy"]
            )
            session.add(city)
            print(f"✓ Added city: {city_info['name']}")

    session.commit()
    print("\n✅ అన్ని నగరాలు జోడించబడ్డాయి!")

except Exception as e:
    session.rollback()
    print(f"❌ Error: {e}")
finally:
    session.close()
