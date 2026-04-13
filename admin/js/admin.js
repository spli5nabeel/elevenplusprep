// ============================================================
//  Admin JS — shared utilities loaded on every admin page
// ============================================================

const ADMIN_TOKEN_KEY = "admin_token";

// Redirect to login if not authenticated
function requireAuth() {
  if (!sessionStorage.getItem(ADMIN_TOKEN_KEY)) {
    window.location.href = "/admin/index.html";
  }
}

// Authenticated fetch wrapper
async function adminFetch(url, opts = {}) {
  const token = sessionStorage.getItem(ADMIN_TOKEN_KEY);
  const r = await fetch(url, {
    ...opts,
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
      ...(opts.headers || {}),
    },
  });

  if (r.status === 401) {
    sessionStorage.removeItem(ADMIN_TOKEN_KEY);
    window.location.href = "/admin/index.html";
    return;
  }

  if (!r.ok) {
    const err = await r.json().catch(() => ({ detail: r.statusText }));
    showToast(err.detail || "Request failed", "error");
    throw new Error(err.detail || r.statusText);
  }

  return r.status === 204 ? null : r.json();
}

// Toast notification
function showToast(msg, type = "success") {
  const existing = document.querySelector(".toast");
  if (existing) existing.remove();

  const t = document.createElement("div");
  t.className = `toast ${type}`;
  t.innerHTML = `<span>${type === "success" ? "✅" : "❌"}</span> ${msg}`;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 3500);
}
