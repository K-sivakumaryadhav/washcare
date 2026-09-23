const TOKEN_KEY = "washcare_admin_token";
let CITIES_CACHE = [];
let CURRENT_STATUS_FILTER = "";

function getToken() { return localStorage.getItem(TOKEN_KEY); }
function setToken(t) { localStorage.setItem(TOKEN_KEY, t); }
function clearToken() { localStorage.removeItem(TOKEN_KEY); }

async function authGet(path) {
  const res = await fetch(path, { headers: { Authorization: `Bearer ${getToken()}` } });
  if (res.status === 401) { logout(); throw new Error("Session expired"); }
  if (!res.ok) throw new Error(`GET ${path} failed`);
  return res.json();
}
async function authPost(path, body, method = "POST") {
  const res = await fetch(path, {
    method,
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${getToken()}` },
    body: JSON.stringify(body),
  });
  if (res.status === 401) { logout(); throw new Error("Session expired"); }
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `${method} ${path} failed`);
  }
  return res.json();
}
async function authDelete(path) {
  const res = await fetch(path, { method: "DELETE", headers: { Authorization: `Bearer ${getToken()}` } });
  if (!res.ok) throw new Error(`DELETE ${path} failed`);
  return res.json();
}

function showApp() {
  document.getElementById("login-screen").style.display = "none";
  document.getElementById("app-shell").style.display = "flex";
  boot();
}
function showLogin() {
  document.getElementById("login-screen").style.display = "flex";
  document.getElementById("app-shell").style.display = "none";
}
function logout() { clearToken(); showLogin(); }

async function handleLogin(e) {
  e.preventDefault();
  const errorEl = document.getElementById("login-error");
  errorEl.style.display = "none";
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;
  try {
    const body = new URLSearchParams();
    body.set("username", username);
    body.set("password", password);
    const res = await fetch("/api/admin/login", { method: "POST", body });
    if (!res.ok) throw new Error("Incorrect username or password");
    const data = await res.json();
    setToken(data.access_token);
    showApp();
  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.style.display = "block";
  }
}

// ---------- Views ----------
const VIEW_TITLES = {
  dashboard: "Dashboard", bookings: "Bookings", technicians: "Technicians",
  enquiries: "Enquiries", settings: "Settings",
};

function switchView(view) {
  Object.keys(VIEW_TITLES).forEach(v => {
    document.getElementById(`view-${v}`).style.display = v === view ? "block" : "none";
  });
  document.getElementById("view-title").textContent = VIEW_TITLES[view];
  document.querySelectorAll(".nav-btn").forEach(b => b.classList.toggle("active", b.dataset.view === view));

  if (view === "dashboard") loadDashboard();
  if (view === "bookings") loadBookings();
  if (view === "technicians") loadTechnicians();
  if (view === "enquiries") loadEnquiries();
  if (view === "settings") loadSettings();
}

async function loadDashboard() {
  const stats = await authGet("/api/admin/dashboard");
  const cards = [
    ["Total bookings", stats.total_bookings],
    ["New", stats.new_bookings],
    ["Pending", stats.pending_bookings],
    ["Confirmed", stats.confirmed_bookings],
    ["Completed", stats.completed_bookings],
    ["Cancelled", stats.cancelled_bookings],
    ["Enquiries", stats.total_enquiries],
  ];
  document.getElementById("stat-grid").innerHTML = cards.map(([label, num]) =>
    `<div class="stat-card"><div class="num">${num}</div><div class="label">${label}</div></div>`
  ).join("");
}

const STATUS_OPTIONS = ["New", "Contacted", "Confirmed", "Technician Assigned", "In Progress", "Completed", "Cancelled"];

function renderStatusTabs() {
  const tabsEl = document.getElementById("booking-status-tabs");
  const all = ["", ...STATUS_OPTIONS];
  tabsEl.innerHTML = all.map(s =>
    `<button data-status="${s}" class="${s === CURRENT_STATUS_FILTER ? "active" : ""}">${s || "All"}</button>`
  ).join("");
  tabsEl.querySelectorAll("button").forEach(btn => {
    btn.addEventListener("click", () => {
      CURRENT_STATUS_FILTER = btn.dataset.status;
      loadBookings();
    });
  });
}

async function loadBookings() {
  renderStatusTabs();
  const qs = CURRENT_STATUS_FILTER ? `?status=${encodeURIComponent(CURRENT_STATUS_FILTER)}` : "";
  const bookings = await authGet(`/api/admin/bookings${qs}`);
  const services = await apiGet("/api/catalog/services");
  const serviceMap = Object.fromEntries(services.map(s => [s.id, s.name]));
  const cityMap = Object.fromEntries(CITIES_CACHE.map(c => [c.id, c.name]));

  document.getElementById("bookings-body").innerHTML = bookings.map(b => `
    <tr>
      <td>${b.booking_id}</td>
      <td>${b.customer_name}</td>
      <td>${b.mobile}</td>
      <td>${cityMap[b.city_id] || b.city_name_other || "-"}</td>
      <td>${serviceMap[b.service_id] || b.service_id}</td>
      <td>${[b.preferred_date, b.preferred_time].filter(Boolean).join(" ") || "-"}</td>
      <td>
        <select class="status-select" data-booking="${b.booking_id}">
          ${STATUS_OPTIONS.map(s => `<option value="${s}" ${s === b.status ? "selected" : ""}>${s}</option>`).join("")}
        </select>
      </td>
      <td>${b.technician_id || "-"}</td>
      <td>${new Date(b.created_at).toLocaleString()}</td>
    </tr>
  `).join("") || `<tr><td colspan="9">No bookings yet.</td></tr>`;

  document.querySelectorAll(".status-select").forEach(sel => {
    sel.addEventListener("change", async () => {
      try {
        await authPost(`/api/admin/bookings/${sel.dataset.booking}`, { status: sel.value }, "PATCH");
        loadDashboard();
      } catch (err) { alert(err.message); }
    });
  });
}

async function loadTechnicians() {
  const citySelect = document.getElementById("tech-city");
  citySelect.innerHTML = CITIES_CACHE.map(c => `<option value="${c.id}">${c.name}</option>`).join("");

  const techs = await authGet("/api/admin/technicians");
  const cityMap = Object.fromEntries(CITIES_CACHE.map(c => [c.id, c.name]));
  document.getElementById("technicians-body").innerHTML = techs.map(t => `
    <tr>
      <td>${t.name}</td><td>${t.mobile}</td><td>${t.whatsapp || "-"}</td>
      <td>${cityMap[t.city_id] || t.city_id}</td><td>${t.area || "-"}</td>
      <td>${t.is_available ? "Yes" : "No"}</td>
      <td><button data-del="${t.id}" style="color:#C0392B;border:none;background:none;cursor:pointer;">Remove</button></td>
    </tr>
  `).join("") || `<tr><td colspan="7">No technicians added yet.</td></tr>`;

  document.querySelectorAll("[data-del]").forEach(btn => {
    btn.addEventListener("click", async () => {
      await authDelete(`/api/admin/technicians/${btn.dataset.del}`);
      loadTechnicians();
    });
  });
}

async function handleAddTechnician(e) {
  e.preventDefault();
  await authPost("/api/admin/technicians", {
    name: document.getElementById("tech-name").value,
    mobile: document.getElementById("tech-mobile").value,
    whatsapp: document.getElementById("tech-whatsapp").value || null,
    city_id: parseInt(document.getElementById("tech-city").value, 10),
    area: document.getElementById("tech-area").value || null,
    services: document.getElementById("tech-services").value || null,
    is_available: true,
  });
  document.getElementById("tech-form").reset();
  loadTechnicians();
}

async function loadEnquiries() {
  const enquiries = await authGet("/api/admin/enquiries");
  document.getElementById("enquiries-body").innerHTML = enquiries.map(e => `
    <tr>
      <td>${e.name}</td><td>${e.mobile}</td><td>${e.city_name || "-"}</td>
      <td>${e.message || "-"}</td><td>${new Date(e.created_at).toLocaleString()}</td>
    </tr>
  `).join("") || `<tr><td colspan="5">No enquiries yet.</td></tr>`;
}

async function loadSettings() {
  const s = await authGet("/api/admin/settings");
  document.getElementById("set-name").value = s.business_name;
  document.getElementById("set-mobile").value = s.business_mobile;
  document.getElementById("set-whatsapp").value = s.business_whatsapp;
  document.getElementById("set-email").value = s.business_email;
  document.getElementById("set-hours").value = s.working_hours;
}

async function handleSaveSettings(e) {
  e.preventDefault();
  const statusEl = document.getElementById("settings-status");
  try {
    await authPost("/api/admin/settings", {
      business_name: document.getElementById("set-name").value,
      business_mobile: document.getElementById("set-mobile").value,
      business_whatsapp: document.getElementById("set-whatsapp").value,
      business_email: document.getElementById("set-email").value,
      working_hours: document.getElementById("set-hours").value,
    }, "PUT");
    statusEl.textContent = "Settings saved.";
    statusEl.style.color = "#1AA34D";
  } catch (err) {
    statusEl.textContent = err.message;
    statusEl.style.color = "#C0392B";
  }
}

async function boot() {
  CITIES_CACHE = await apiGet("/api/catalog/cities");
  loadDashboard();
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("login-form").addEventListener("submit", handleLogin);
  document.getElementById("logout-btn").addEventListener("click", logout);
  document.getElementById("tech-form").addEventListener("submit", handleAddTechnician);
  document.getElementById("settings-form").addEventListener("submit", handleSaveSettings);
  document.querySelectorAll(".nav-btn").forEach(btn => {
    btn.addEventListener("click", () => switchView(btn.dataset.view));
  });

  if (getToken()) showApp(); else showLogin();
});
