let CITIES = [];
let SERVICES = [];
let STATES = [];

function waLink(number, text) {
  const clean = (number || "").replace(/[^0-9]/g, "");
  return `https://wa.me/${clean}${text ? "?text=" + encodeURIComponent(text) : ""}`;
}

// Accepts a 10-digit Indian mobile (optionally with spaces, dashes, or a +91 prefix).
function isValidIndianMobile(value) {
  let digits = (value || "").replace(/\D/g, "");
  if (digits.length === 12 && digits.startsWith("91")) digits = digits.slice(2);
  return /^[6-9]\d{9}$/.test(digits);
}

async function loadSettings() {
  try {
    const s = await apiGet("/api/catalog/settings");
    document.querySelectorAll("#header-call, #hero-call, #bar-call").forEach(el => {
      el.href = `tel:${s.business_mobile}`;
    });
    const waDefaultMsg = "Hi, I need washing machine service. I would like to book a service.";
    document.querySelectorAll("#header-whatsapp, #hero-whatsapp, #fab-whatsapp, #bar-whatsapp").forEach(el => {
      el.href = waLink(s.business_whatsapp, waDefaultMsg);
    });
    const phoneEl = document.getElementById("contact-phone");
    if (phoneEl) {
      document.getElementById("contact-phone").textContent = `Phone: ${s.business_mobile}`;
      document.getElementById("contact-whatsapp").textContent = `WhatsApp: ${s.business_whatsapp}`;
      document.getElementById("contact-email").textContent = `Email: ${s.business_email}`;
      document.getElementById("contact-hours").textContent = `Working hours: ${s.working_hours}`;
    }
  } catch (e) { console.error(e); }
}

function serviceIcon() {
  return `<svg class="chip-icon" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2"/><path d="M12 8v4l3 2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`;
}

async function loadServices() {
  SERVICES = await apiGet("/api/catalog/services");
  const chipRow = document.getElementById("service-chips");
  if (chipRow) {
    chipRow.innerHTML = SERVICES.map(s =>
      `<div class="chip" data-open-booking data-service-id="${s.id}">${serviceIcon()}<span>${s.name}</span></div>`
    ).join("");
  }
  const select = document.getElementById("bk-service");
  if (select) {
    select.innerHTML = `<option value="">Select service</option>` +
      SERVICES.map(s => `<option value="${s.id}">${s.name}</option>`).join("");
  }
}

async function loadBrands() {
  const brands = await apiGet("/api/catalog/brands");
  const row = document.getElementById("brand-row");
  if (row) row.innerHTML = brands.map(b => `<span class="brand-badge">${b.name}</span>`).join("");
  const select = document.getElementById("bk-brand");
  if (select) {
    select.innerHTML = `<option value="">Select brand</option>` +
      brands.map(b => `<option value="${b.name}">${b.name}</option>`).join("");
  }
}

async function loadStatesAndCities() {
  STATES = await apiGet("/api/catalog/states");
  CITIES = await apiGet("/api/catalog/cities");

  const stateFilter = document.getElementById("state-filter");
  const bkState = document.getElementById("bk-state");
  const stateOptions = STATES.map(s => `<option value="${s.id}">${s.name}</option>`).join("");
  if (stateFilter) stateFilter.innerHTML += stateOptions;
  if (bkState) bkState.innerHTML = `<option value="">Select state</option>` + stateOptions;

  renderCityGrid(CITIES);
  renderBookingCityOptions(CITIES);

  if (stateFilter) {
    stateFilter.addEventListener("change", () => {
      const id = stateFilter.value;
      renderCityGrid(id ? CITIES.filter(c => String(c.state_id) === id) : CITIES);
    });
  }
  if (bkState) {
    bkState.addEventListener("change", () => {
      const id = bkState.value;
      renderBookingCityOptions(id ? CITIES.filter(c => String(c.state_id) === id) : CITIES);
    });
  }
}

function renderCityGrid(cities) {
  const grid = document.getElementById("city-grid");
  if (!grid) return;
  grid.innerHTML = cities.map(c =>
    `<a class="city-pill" href="/washing-machine-service-${c.slug}">${c.name}</a>`
  ).join("");
}

function renderBookingCityOptions(cities) {
  const select = document.getElementById("bk-city");
  if (!select) return;
  select.innerHTML = `<option value="">Select city</option>` +
    cities.map(c => `<option value="${c.id}">${c.name}</option>`).join("") +
    `<option value="other">Other (my city isn't listed)</option>`;
}

function wireCityOtherToggle() {
  const citySelect = document.getElementById("bk-city");
  const otherRow = document.getElementById("bk-city-other-row");
  const otherInput = document.getElementById("bk-city-other");
  if (!citySelect || !otherRow) return;
  citySelect.addEventListener("change", () => {
    const isOther = citySelect.value === "other";
    otherRow.style.display = isOther ? "block" : "none";
    if (!isOther && otherInput) otherInput.value = "";
  });
}

// ---------- Booking modal ----------
function openBookingModal(serviceId) {
  document.getElementById("booking-backdrop").classList.add("open");
  document.getElementById("booking-form-view").style.display = "block";
  document.getElementById("booking-confirm-view").style.display = "none";
  if (serviceId) document.getElementById("bk-service").value = serviceId;
  document.body.style.overflow = "hidden";
}
function closeBookingModal() {
  document.getElementById("booking-backdrop").classList.remove("open");
  document.body.style.overflow = "";
}

function wireBookingModal() {
  document.querySelectorAll("[data-open-booking]").forEach(el => {
    el.addEventListener("click", (e) => {
      e.preventDefault();
      openBookingModal(el.dataset.serviceId);
    });
  });
  document.querySelectorAll("[data-close-booking]").forEach(el => {
    el.addEventListener("click", closeBookingModal);
  });
  // Only pages with the booking modal (index.html) have this element —
  // guard against it being missing on contact.html, about.html, etc.,
  // otherwise this throws and stops every script that runs after it,
  // including loadSettings().
  const backdrop = document.getElementById("booking-backdrop");
  if (backdrop) {
    backdrop.addEventListener("click", (e) => {
      if (e.target.id === "booking-backdrop") closeBookingModal();
    });
  }
}

async function submitBooking(e) {
  e.preventDefault();
  const errorEl = document.getElementById("booking-error");
  errorEl.style.display = "none";

  const stateSel = document.getElementById("bk-state");
  const citySelectEl = document.getElementById("bk-city");
  const isOtherCity = citySelectEl.value === "other";
  const payload = {
    customer_name: document.getElementById("bk-name").value.trim(),
    mobile: document.getElementById("bk-mobile").value.trim(),
    whatsapp: document.getElementById("bk-whatsapp").value.trim() || null,
    state_name: stateSel.options[stateSel.selectedIndex]?.text || "",
    city_id: isOtherCity ? null : (parseInt(citySelectEl.value, 10) || null),
    city_name_other: isOtherCity ? document.getElementById("bk-city-other").value.trim() : null,
    area_pincode: document.getElementById("bk-area").value.trim(),
    brand: document.getElementById("bk-brand").value || null,
    machine_type: document.getElementById("bk-type").value || null,
    service_id: parseInt(document.getElementById("bk-service").value, 10),
    problem_description: document.getElementById("bk-problem").value.trim() || null,
    preferred_date: document.getElementById("bk-date").value || null,
    preferred_time: document.getElementById("bk-time").value || null,
    address: document.getElementById("bk-address").value.trim() || null,
  };

  if (!payload.service_id || !payload.state_name || (!payload.city_id && !payload.city_name_other)) {
    errorEl.textContent = "Please fill all required fields.";
    errorEl.style.display = "block";
    return;
  }

  if (!isValidIndianMobile(payload.mobile)) {
    errorEl.textContent = "Enter a valid 10-digit mobile number.";
    errorEl.style.display = "block";
    document.getElementById("bk-mobile").focus();
    return;
  }
  if (payload.whatsapp && !isValidIndianMobile(payload.whatsapp)) {
    errorEl.textContent = "Enter a valid 10-digit WhatsApp number, or leave it blank.";
    errorEl.style.display = "block";
    document.getElementById("bk-whatsapp").focus();
    return;
  }

  try {
    const confirmation = await apiPost("/api/bookings", payload);
    document.getElementById("cf-id").textContent = confirmation.booking_id;
    document.getElementById("cf-name").textContent = confirmation.customer_name;
    document.getElementById("cf-city").textContent = confirmation.city_name;
    document.getElementById("cf-service").textContent = confirmation.service_name;
    document.getElementById("cf-datetime").textContent =
      [confirmation.preferred_date, confirmation.preferred_time].filter(Boolean).join(" ") || "To be confirmed";
    document.getElementById("cf-whatsapp").href = confirmation.whatsapp_link;

    document.getElementById("booking-form-view").style.display = "none";
    document.getElementById("booking-confirm-view").style.display = "block";
    document.getElementById("booking-form").reset();
  } catch (err) {
    errorEl.textContent = err.message || "Something went wrong. Please try again.";
    errorEl.style.display = "block";
  }
}

// ---------- Enquiry form ----------
async function submitEnquiry(e) {
  e.preventDefault();
  const statusEl = document.getElementById("enquiry-status");
  const mobile = document.getElementById("eq-mobile").value.trim();

  if (!isValidIndianMobile(mobile)) {
    statusEl.textContent = "Enter a valid 10-digit mobile number.";
    statusEl.style.color = "#C0392B";
    document.getElementById("eq-mobile").focus();
    return;
  }

  try {
    const confirmation = await apiPost("/api/enquiries", {
      name: document.getElementById("eq-name").value.trim(),
      mobile: mobile,
      city_name: document.getElementById("eq-city").value.trim() || null,
      message: document.getElementById("eq-message").value.trim() || null,
    });

    // Always show a visible, clickable WhatsApp button rather than trying to
    // auto-open a popup — popups get silently blocked by many browsers
    // (especially Safari), so a button the person taps themselves is far
    // more reliable than window.open().
    statusEl.innerHTML =
      `Thanks — your message was received. <br>` +
      `<a class="btn btn-whatsapp" style="margin-top:10px;" href="${confirmation.whatsapp_link}" target="_blank" rel="noopener">Tap here to send it on WhatsApp</a>`;
    statusEl.style.color = "#1AA34D";
    document.getElementById("enquiry-form").reset();
  } catch (err) {
    statusEl.textContent = err.message || "Could not send your message. Please try again.";
    statusEl.style.color = "#C0392B";
  }
}

// ---------- Nav ----------
function wireNav() {
  const toggle = document.getElementById("nav-toggle");
  const menu = document.getElementById("mobile-menu");
  if (toggle && menu) {
    toggle.addEventListener("click", () => menu.classList.toggle("open"));
    menu.querySelectorAll("a").forEach(a => a.addEventListener("click", () => menu.classList.remove("open")));
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  wireNav();
  wireBookingModal();
  wireCityOtherToggle();

  const bookingForm = document.getElementById("booking-form");
  if (bookingForm) bookingForm.addEventListener("submit", submitBooking);

  const enquiryForm = document.getElementById("enquiry-form");
  if (enquiryForm) enquiryForm.addEventListener("submit", submitEnquiry);

  await Promise.all([loadSettings(), loadServices(), loadBrands(), loadStatesAndCities()]);

  // Pre-select city if arriving from a city SEO page link (?city=slug)
  const params = new URLSearchParams(window.location.search);
  const citySlug = params.get("city");
  if (citySlug) {
    const city = CITIES.find(c => c.slug === citySlug);
    if (city) {
      const bkCity = document.getElementById("bk-city");
      if (bkCity) bkCity.value = city.id;
    }
  }

  if (window.location.hash === "#book") openBookingModal();
});

if ("serviceWorker" in navigator) {
  // During active development, an old cached service worker can silently
  // keep serving stale JS/CSS even after a hard reload. Unregister any
  // existing one so every page load always uses the latest files. Re-enable
  // registration once the site is stable and ready for production.
  navigator.serviceWorker.getRegistrations().then((registrations) => {
    registrations.forEach((r) => r.unregister());
  });
  if ("caches" in window) {
    caches.keys().then((names) => names.forEach((name) => caches.delete(name)));
  }
}
