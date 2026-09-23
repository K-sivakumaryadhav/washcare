# WashCare India — Washing Machine Repair & Service Marketplace

A working, deployable Pan-India washing machine repair/service booking site:
FastAPI (Python) backend + plain HTML/CSS/JavaScript frontend, mobile-first and
installable as a PWA on phones (no separate native app needed).

## What's included

- **Customer site** (`frontend/`): homepage with hero, service list, city
  picker, "how it works", booking form (modal), trust/brand sections, contact
  form, floating WhatsApp button, sticky mobile Call/WhatsApp/Book bar,
  About/Contact/legal pages.
- **Admin dashboard** (`frontend/admin/`): secure login, booking stats,
  booking list with status updates, technician management, enquiries list,
  and business settings (phone/WhatsApp numbers — never hard-coded).
- **Backend API** (`backend/app/`): FastAPI + SQLAlchemy, JWT admin auth,
  booking/enquiry/technician/catalog endpoints, server-rendered per-city SEO
  pages (`/washing-machine-service-<city>`), `robots.txt` and `sitemap.xml`.
- **PWA support**: `manifest.json` + `sw.js` so "Add to Home Screen" gives
  customers an app-like icon and offline app shell — this is what covers
  "mobile" without needing a separate native app build.

## Running it locally

```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m app.seed          # creates the DB, seeds cities/services/brands/admin
uvicorn app.main:app --reload --port 8000
```

Then open:
- Customer site: http://localhost:8000/
- Admin panel: http://localhost:8000/admin
  - Default login: `admin` / `ChangeMe123!` — **change this immediately** (there's
    no "change password" UI yet; update it directly in the database or add one).

The backend serves the frontend itself, so there's nothing else to run.

## Going to production

1. Set real environment variables from `.env.example` (`DATABASE_URL` pointing
   at Postgres, a random `SECRET_KEY`).
2. Restrict CORS `allow_origins` in `app/main.py` to your real domain.
3. Put the app behind HTTPS (required for the PWA install prompt and for
   `tel:`/`wa.me` links to behave well on mobile).
4. Add real app icons at `frontend/icons/icon-192.png` and `icon-512.png`
   (referenced by `manifest.json` but not included here).
5. Wire up SMS/email notifications (stubs are left in `.env.example`) if you
   want those in addition to the WhatsApp deep-link + admin dashboard
   notifications that already work.
6. Set the business phone/WhatsApp numbers once from the Admin → Settings tab.

## What's intentionally left as a next step

- Payments, technician login/app, and customer reviews (the schema is built
  so these can be added without a rewrite, per the spec's phased approach).
- SMS gateway and outbound email are stubbed — WhatsApp deep-links and the
  admin dashboard are fully working today.
- Legal pages (Privacy, Terms, Cancellation, Service Policy) contain
  placeholder text — have a lawyer review before publishing.
