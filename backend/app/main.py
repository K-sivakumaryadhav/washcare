import os
from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import models
from .database import get_db, engine, Base
from .routers import catalog, bookings, enquiries, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="WashCare India API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to your real domain(s) in production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(catalog.router)
app.include_router(bookings.router)
app.include_router(enquiries.router)
app.include_router(admin.router)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/", response_class=FileResponse)
def homepage():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.get("/admin", response_class=FileResponse)
@app.get("/admin/", response_class=FileResponse)
def admin_panel():
    return FileResponse(os.path.join(FRONTEND_DIR, "admin", "index.html"))


@app.get("/washing-machine-service-{slug}", response_class=HTMLResponse)
def city_seo_page(slug: str, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.slug == slug, models.City.is_active == True).first()  # noqa: E712
    if not city:
        raise HTTPException(status_code=404, detail="City page not found")
    settings = db.query(models.SiteSettings).first()
    services = db.query(models.ServiceType).filter(models.ServiceType.is_active == True).all()  # noqa: E712
    return templates.TemplateResponse("city_page.html", {
        "request": {},
        "slug": city.slug,
        "city_name": city.name,
        "seo_title": city.seo_title,
        "seo_description": city.seo_description,
        "intro_copy": city.intro_copy,
        "services": services,
        "business_name": settings.business_name,
        "business_mobile": settings.business_mobile,
        "business_whatsapp": settings.business_whatsapp.lstrip("+").replace(" ", ""),
    })


@app.get("/robots.txt", response_class=Response)
def robots():
    content = "User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n"
    return Response(content=content, media_type="text/plain")


@app.get("/sitemap.xml", response_class=Response)
def sitemap(db: Session = Depends(get_db)):
    cities = db.query(models.City).filter(models.City.is_active == True).all()  # noqa: E712
    urls = ["/", "/washing-machine-repair", "/washing-machine-installation", "/washing-machine-service"]
    urls += [f"/washing-machine-service-{c.slug}" for c in cities]
    body = "".join(f"<url><loc>{u}</loc></url>" for u in urls)
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>'
    return Response(content=xml, media_type="application/xml")


# Catch-all for the rest of the static site (about.html, contact.html, legal
# pages, manifest.json, sw.js, etc.) so links like "/contact.html" resolve
# directly — registered last so it never shadows the API routes or the more
# specific routes above.
app.mount("/", StaticFiles(directory=FRONTEND_DIR), name="frontend-pages")
