// ============================================================
//  API client — wraps all fetch() calls to the backend
// ============================================================

const API_BASE = "";   // same origin

// ---- Session ----
const SESSION_KEY = "gs_session_id";

function getSessionId() {
  let id = localStorage.getItem(SESSION_KEY);
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem(SESSION_KEY, id);
  }
  return id;
}

async function ensureSession() {
  const id = getSessionId();
  try {
    await fetch(`${API_BASE}/api/sessions?session_id=${id}`, { method: "POST" });
  } catch (_) { /* offline — ignore */ }
  return id;
}

async function getSessionStats() {
  const id = getSessionId();
  try {
    const r = await fetch(`${API_BASE}/api/sessions/${id}`);
    if (r.ok) return await r.json();
  } catch (_) {}
  // Fallback to localStorage if offline
  return _localStats();
}

async function getProgress() {
  const id = getSessionId();
  try {
    const r = await fetch(`${API_BASE}/api/sessions/${id}/progress`);
    if (r.ok) return await r.json();
  } catch (_) {}
  return [];
}

async function submitResult(payload) {
  const id = getSessionId();
  try {
    const r = await fetch(`${API_BASE}/api/sessions/${id}/results`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (r.ok) return await r.json();
  } catch (_) {}
  // Offline fallback
  _localAddPoints(payload.score * 10 - payload.hints_used * 2);
  return { points_earned: payload.score * 10, new_total_points: 0, new_streak: 0 };
}

// ---- Questions ----
async function getSubjects() {
  try {
    const r = await fetch(`${API_BASE}/api/questions/subjects`);
    if (r.ok) return await r.json();
  } catch (_) {}
  return [];
}

async function getQuestions(subject, topic, limit = 5) {
  const r = await fetch(`${API_BASE}/api/questions/${subject}/${topic}?limit=${limit}`);
  if (!r.ok) throw new Error(`No questions found for ${subject}/${topic}`);
  return await r.json();
}

async function checkAnswer(subject, topic, questionId, selected) {
  const r = await fetch(`${API_BASE}/api/questions/${subject}/${topic}/${questionId}/answer?selected=${selected}`);
  if (!r.ok) throw new Error("Could not check answer");
  return await r.json();
}

// ---- Offline localStorage fallbacks ----
function _localStats() {
  const raw = localStorage.getItem("gs_stats_local");
  return raw ? JSON.parse(raw) : { total_points: 0, quizzes_done: 0, streak: 0 };
}

function _localAddPoints(pts) {
  const s = _localStats();
  s.total_points = (s.total_points || 0) + Math.max(0, pts);
  s.quizzes_done = (s.quizzes_done || 0) + 1;
  localStorage.setItem("gs_stats_local", JSON.stringify(s));
}

export { getSessionId, ensureSession, getSessionStats, getProgress, submitResult, getSubjects, getQuestions, checkAnswer };
