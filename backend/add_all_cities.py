#!/usr/bin/env python3
"""Add all SEO cities to the database."""

from app.database import SessionLocal, engine, Base
from app.models import State, City
from dotenv import load_dotenv

load_dotenv()

# Ensure tables exist
Base.metadata.create_all(bind=engine)

session = SessionLocal()

# All cities with SEO content
cities_data = [
    {
        "state": "Gujarat",
        "name": "Ahmedabad",
        "slug": "ahmedabad",
        "seo_title": "Washing Machine Repair & Service in Ahmedabad | WashCare India",
        "seo_description": "Professional washing machine repair and service in Ahmedabad. Same-day technician, warranty service, all brands - LG, Samsung, IFB, Whirlpool, Bosch.",
        "intro_copy": "Expert washing machine repair and installation services in Ahmedabad. Our certified technicians provide same-day service for all brands of washing machines."
    },
    {
        "state": "Karnataka",
        "name": "Bengaluru",
        "slug": "bengaluru",
        "seo_title": "Washing Machine Repair Service in Bengaluru | Same-Day Service | WashCare India",
        "seo_description": "Fast washing machine repair service in Bengaluru. Certified technicians, genuine spare parts, all brands covered. Book online or call for same-day service.",
        "intro_copy": "Get professional washing machine repair and service in Bengaluru. From routine maintenance to major repairs, our experienced technicians handle all brands and models."
    },
    {
        "state": "Madhya Pradesh",
        "name": "Bhopal",
        "slug": "bhopal",
        "seo_title": "Washing Machine Repair in Bhopal | Expert Technicians | WashCare India",
        "seo_description": "Reliable washing machine repair service in Bhopal. Same-day technician visit, warranty service, all major brands covered.",
        "intro_copy": "Professional washing machine repair and maintenance in Bhopal. We service all major brands and offer same-day technician visits."
    },
    {
        "state": "Chandigarh",
        "name": "Chandigarh",
        "slug": "chandigarh",
        "seo_title": "Washing Machine Repair & Service in Chandigarh | WashCare India",
        "seo_description": "Expert washing machine repair in Chandigarh. Same-day service, genuine parts, warranty coverage for all washing machine brands.",
        "intro_copy": "Trusted washing machine repair service in Chandigarh. Our certified technicians provide prompt service for all brands and types of washing machines."
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
        "state": "Tamil Nadu",
        "name": "Coimbatore",
        "slug": "coimbatore",
        "seo_title": "Washing Machine Repair Service in Coimbatore | WashCare India",
        "seo_description": "Professional washing machine repair and service in Coimbatore. Same-day technician, warranty service, all major brands.",
        "intro_copy": "Expert washing machine repair in Coimbatore. We provide same-day service for all major brands with genuine spare parts and warranty."
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
        "state": "Haryana",
        "name": "Gurgaon",
        "slug": "gurgaon",
        "seo_title": "Washing Machine Repair in Gurgaon | Same-Day Service | WashCare India",
        "seo_description": "Fast washing machine repair service in Gurgaon. Certified technicians, genuine spare parts, all brands covered.",
        "intro_copy": "Professional washing machine repair and service in Gurgaon. Same-day technician visits for all brands and models."
    },
    {
        "state": "Telangana",
        "name": "Hyderabad",
        "slug": "hyderabad",
        "seo_title": "Washing Machine Repair & Service in Hyderabad | WashCare India",
        "seo_description": "Professional washing machine repair and service in Hyderabad. Same-day technician, warranty service, all brands - LG, Samsung, IFB, Whirlpool, Bosch.",
        "intro_copy": "Expert washing machine repair and installation services in Hyderabad. Our certified technicians provide same-day service for all brands of washing machines."
    },
    {
        "state": "Madhya Pradesh",
        "name": "Indore",
        "slug": "indore",
        "seo_title": "Washing Machine Repair & Service in Indore | WashCare India",
        "seo_description": "Professional washing machine repair in Indore. Same-day technician, warranty service, all major brands.",
        "intro_copy": "Expert washing machine repair and service in Indore. Fast and reliable technicians available for same-day service."
    },
    {
        "state": "Rajasthan",
        "name": "Jaipur",
        "slug": "jaipur",
        "seo_title": "Washing Machine Repair Service in Jaipur | WashCare India",
        "seo_description": "Reliable washing machine repair service in Jaipur. Same-day technician visit, warranty service, all major brands.",
        "intro_copy": "Professional washing machine repair in Jaipur. We offer same-day service for all brands with genuine spare parts."
    },
    {
        "state": "Kerala",
        "name": "Kochi",
        "slug": "kochi",
        "seo_title": "Washing Machine Repair in Kochi | Expert Service | WashCare India",
        "seo_description": "Professional washing machine repair service in Kochi. Same-day technician, all major brands covered.",
        "intro_copy": "Trusted washing machine repair service in Kochi. Our experienced technicians handle all brands and models."
    },
    {
        "state": "West Bengal",
        "name": "Kolkata",
        "slug": "kolkata",
        "seo_title": "Washing Machine Repair & Service in Kolkata | WashCare India",
        "seo_description": "Expert washing machine repair in Kolkata. Same-day service, genuine parts, warranty coverage for all brands.",
        "intro_copy": "Professional washing machine repair service in Kolkata. Same-day technician visits for all major brands."
    },
    {
        "state": "Uttar Pradesh",
        "name": "Lucknow",
        "slug": "lucknow",
        "seo_title": "Washing Machine Repair Service in Lucknow | WashCare India",
        "seo_description": "Reliable washing machine repair in Lucknow. Same-day technician, warranty service, all major brands.",
        "intro_copy": "Professional washing machine repair in Lucknow. Fast service for all brands of washing machines."
    },
    {
        "state": "Maharashtra",
        "name": "Mumbai",
        "slug": "mumbai",
        "seo_title": "Washing Machine Repair in Mumbai | Same-Day Service | WashCare India",
        "seo_description": "Fast washing machine repair service in Mumbai. Certified technicians, genuine spare parts, all brands covered.",
        "intro_copy": "Professional washing machine repair and service in Mumbai. From routine maintenance to major repairs, our experienced technicians handle all brands."
    },
    {
        "state": "Maharashtra",
        "name": "Nagpur",
        "slug": "nagpur",
        "seo_title": "Washing Machine Repair in Nagpur | WashCare India",
        "seo_description": "Professional washing machine repair service in Nagpur. Same-day technician, all major brands.",
        "intro_copy": "Expert washing machine repair in Nagpur. Same-day service available for all brands and models."
    },
    {
        "state": "Uttar Pradesh",
        "name": "Noida",
        "slug": "noida",
        "seo_title": "Washing Machine Repair Service in Noida | WashCare India",
        "seo_description": "Fast washing machine repair in Noida. Certified technicians, genuine spare parts, all brands covered.",
        "intro_copy": "Professional washing machine repair in Noida. Same-day service for all major brands."
    },
    {
        "state": "Bihar",
        "name": "Patna",
        "slug": "patna",
        "seo_title": "Washing Machine Repair in Patna | Expert Service | WashCare India",
        "seo_description": "Reliable washing machine repair service in Patna. Same-day technician, all major brands.",
        "intro_copy": "Professional washing machine repair in Patna. Fast and reliable technicians for all brands."
    },
    {
        "state": "Maharashtra",
        "name": "Pune",
        "slug": "pune",
        "seo_title": "Washing Machine Repair & Service in Pune | WashCare India",
        "seo_description": "Expert washing machine repair in Pune. Same-day service, genuine parts, warranty coverage for all brands.",
        "intro_copy": "Professional washing machine repair service in Pune. Our technicians handle all major brands and models."
    },
    {
        "state": "Gujarat",
        "name": "Surat",
        "slug": "surat",
        "seo_title": "Washing Machine Repair Service in Surat | WashCare India",
        "seo_description": "Professional washing machine repair in Surat. Same-day technician, warranty service, all major brands.",
        "intro_copy": "Expert washing machine repair in Surat. Same-day service for all brands with genuine spare parts."
    },
    {
        "state": "Andhra Pradesh",
        "name": "Tirupati",
        "slug": "tirupati",
        "seo_title": "Washing Machine Repair in Tirupati | WashCare India",
        "seo_description": "Professional washing machine repair service in Tirupati. Same-day technician, all major brands.",
        "intro_copy": "Expert washing machine repair in Tirupati. Fast service for all brands of washing machines."
    },
    {
        "state": "Andhra Pradesh",
        "name": "Vijayawada",
        "slug": "vijayawada",
        "seo_title": "Washing Machine Repair & Service in Vijayawada | WashCare India",
        "seo_description": "Professional washing machine repair in Vijayawada. Same-day technician, warranty service, all major brands.",
        "intro_copy": "Expert washing machine repair in Vijayawada. Same-day service available for all brands."
    },
    {
        "state": "Andhra Pradesh",
        "name": "Visakhapatnam",
        "slug": "visakhapatnam",
        "seo_title": "Washing Machine Repair Service in Visakhapatnam | WashCare India",
        "seo_description": "Reliable washing machine repair in Visakhapatnam. Same-day technician, all major brands covered.",
        "intro_copy": "Professional washing machine repair in Visakhapatnam. Fast and reliable service for all brands."
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
    print("\n✅ అన్ని 23 నగరాలు జోడించబడ్డాయి!")

except Exception as e:
    session.rollback()
    print(f"❌ Error: {e}")
finally:
    session.close()
