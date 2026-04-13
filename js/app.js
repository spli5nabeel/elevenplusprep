// ============================================================
//  Grammar School Prep — Auth-First Application
// ============================================================

const STATE = {
  currentSubject: null,
  currentTopic:   null,
  currentQuiz:    null,
  timer:          null,
  timeLeft:       0,
  hintsUsed:      0,
  subjects:       [],
  currentUser:    null,
  quizStartTime:  0,
};

// ---- Storage keys ----
const TOKEN_KEY   = "gs_token";
const USER_KEY    = "gs_user";
const SESSION_KEY = "gs_session_id";

function getToken()     { return localStorage.getItem(TOKEN_KEY); }
function getSessionId() { return localStorage.getItem(SESSION_KEY); }

function saveAuth(token, user, sessionId) {
  localStorage.setItem(TOKEN_KEY,   token);
  localStorage.setItem(USER_KEY,    JSON.stringify(user));
  localStorage.setItem(SESSION_KEY, sessionId);
  STATE.currentUser = user;
}

function clearAuth() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
  localStorage.removeItem(SESSION_KEY);
  STATE.currentUser = null;
  STATE.subjects    = [];
}

function authHeaders() {
  const t = getToken();
  return t ? { Authorization: `Bearer ${t}` } : {};
}

// ============================================================
//  Screen management
// ============================================================
function showAuthScreen() {
  document.getElementById("screen-auth").style.display = "";
  document.getElementById("screen-app").style.display  = "none";
}

function showAppScreen() {
  document.getElementById("screen-auth").style.display = "none";
  document.getElementById("screen-app").style.display  = "";
}

// ============================================================
//  Auth form
// ============================================================
function switchTab(tab) {
  document.getElementById("loginForm").style.display    = tab === "login"    ? "" : "none";
  document.getElementById("registerForm").style.display = tab === "register" ? "" : "none";
  document.getElementById("tabLogin").classList.toggle("active",    tab === "login");
  document.getElementById("tabRegister").classList.toggle("active", tab === "register");
  document.getElementById("loginError").classList.remove("show");
  document.getElementById("registerError").classList.remove("show");
}

async function handleLogin(e) {
  e.preventDefault();
  const errEl = document.getElementById("loginError");
  errEl.classList.remove("show");
  const btn = document.getElementById("loginBtn");
  btn.disabled = true; btn.textContent = "Signing in…";
  try {
    const r = await fetch("/api/auth/login", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({
        username: document.getElementById("loginUsername").value.trim(),
        password: document.getElementById("loginPassword").value,
      }),
    });
    if (!r.ok) { const d = await r.json(); throw new Error(d.detail || "Login failed"); }
    const { token, user, session_id } = await r.json();
    saveAuth(token, user, session_id);
    await bootApp();
  } catch (err) {
    errEl.textContent = err.message;
    errEl.classList.add("show");
  } finally {
    btn.disabled = false; btn.textContent = "Sign In →";
  }
}

async function handleRegister(e) {
  e.preventDefault();
  const errEl = document.getElementById("registerError");
  errEl.classList.remove("show");
  const btn = document.getElementById("registerBtn");
  btn.disabled = true; btn.textContent = "Creating…";
  try {
    const r = await fetch("/api/auth/register", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({
        username:     document.getElementById("regUsername").value.trim(),
        password:     document.getElementById("regPassword").value,
        display_name: document.getElementById("regName").value.trim(),
        year_group:   parseInt(document.getElementById("regYearGroup").value),
      }),
    });
    if (!r.ok) { const d = await r.json(); throw new Error(d.detail || "Registration failed"); }
    const { token, user, session_id } = await r.json();
    saveAuth(token, user, session_id);
    await bootApp();
  } catch (err) {
    errEl.textContent = err.message;
    errEl.classList.add("show");
  } finally {
    btn.disabled = false; btn.textContent = "Create Account →";
  }
}

// ============================================================
//  Profile modal
// ============================================================
function openProfileModal() {
  const u = STATE.currentUser;
  if (!u) return;
  document.getElementById("profileAvatar").textContent  = u.display_name.charAt(0).toUpperCase();
  document.getElementById("profileName").textContent    = u.display_name;
  document.getElementById("profileMeta").textContent    = `@${u.username} · Year ${u.year_group}`;
  fetchStats().then(s => {
    document.getElementById("profilePoints").textContent  = (s.total_points  || 0).toLocaleString();
    document.getElementById("profileQuizzes").textContent = s.quizzes_done || 0;
  });
  document.getElementById("profileModal").classList.add("show");
}
function closeProfileModal() { document.getElementById("profileModal").classList.remove("show"); }

async function changePassword() {
  const errEl = document.getElementById("pwChangeError");
  errEl.classList.remove("show");
  const oldPw = document.getElementById("pwOld").value;
  const newPw = document.getElementById("pwNew").value;
  if (!oldPw || !newPw) {
    errEl.textContent = "Please fill in both fields.";
    errEl.classList.add("show");
    return;
  }
  try {
    const r = await fetch("/api/auth/change-password", {
      method:  "POST",
      headers: { "Content-Type": "application/json", ...authHeaders() },
      body:    JSON.stringify({ old_password: oldPw, new_password: newPw }),
    });
    if (!r.ok) { const d = await r.json(); throw new Error(d.detail); }
    document.getElementById("pwOld").value = "";
    document.getElementById("pwNew").value = "";
    showToast("Password updated!");
    closeProfileModal();
  } catch (err) {
    errEl.textContent = err.message;
    errEl.classList.add("show");
  }
}

async function logOut() {
  const token = getToken();
  if (token) {
    await fetch("/api/auth/logout", { method: "POST", headers: authHeaders() }).catch(() => {});
  }
  clearAuth();
  closeProfileModal();
  showToast("Signed out. See you soon!");
  // Reset bottom nav to home
  document.querySelectorAll(".bottom-nav-btn").forEach(b => {
    b.classList.toggle("active", b.dataset.page === "page-dashboard");
  });
  showAuthScreen();
}

// ============================================================
//  API helpers
// ============================================================
async function api(path, opts = {}) {
  const r = await fetch(path, {
    headers: { "Content-Type": "application/json", ...authHeaders(), ...(opts.headers || {}) },
    ...opts,
  });
  if (!r.ok) {
    const err = await r.json().catch(() => ({ detail: r.statusText }));
    throw new Error(err.detail || r.statusText);
  }
  return r.status === 204 ? null : r.json();
}

async function ensureSession() {
  const sid = getSessionId();
  if (!sid) return;
  try { await api(`/api/sessions?session_id=${sid}`, { method: "POST" }); } catch (_) {}
}

async function fetchStats() {
  const sid = getSessionId();
  if (!sid) return { total_points: 0, quizzes_done: 0, streak: 0 };
  try         { return await api(`/api/sessions/${sid}`); }
  catch (_e)  { return { total_points: 0, quizzes_done: 0, streak: 0 }; }
}

async function fetchProgress() {
  const sid = getSessionId();
  if (!sid) return [];
  try        { return await api(`/api/sessions/${sid}/progress`); }
  catch (_e) { return []; }
}

async function postResult(payload) {
  const sid = getSessionId();
  if (!sid) return { points_earned: 0, new_total_points: 0, new_streak: 0 };
  try        { return await api(`/api/sessions/${sid}/results`, { method: "POST", body: JSON.stringify(payload) }); }
  catch (_e) { return { points_earned: payload.score * 10, new_total_points: 0, new_streak: 0 }; }
}

async function fetchSubjects() {
  try        { return await api("/api/questions/subjects"); }
  catch (_e) { return []; }
}

async function fetchQuestions(subject, topic, limit = 0) {
  const qs = limit > 0 ? `?limit=${limit}` : "";
  return api(`/api/questions/${subject}/${topic}${qs}`);
}

async function verifyAnswer(subject, topic, qid, selected) {
  return api(`/api/questions/${subject}/${topic}/${qid}/answer?selected=${selected}`);
}

// ============================================================
//  Navigation (within the app screen)
// ============================================================
function showPage(pageId) {
  document.querySelectorAll("#screen-app .page").forEach(p => p.classList.remove("active"));
  document.getElementById(pageId).classList.add("active");
  document.querySelectorAll(".bottom-nav-btn").forEach(b => {
    b.classList.toggle("active", b.dataset.page === pageId);
  });
  window.scrollTo(0, 0);
}

function goHome() { renderDashboard(); showPage("page-dashboard"); }

function updateNavStats(stats) {
  document.getElementById("navStreak").textContent = stats.streak || 0;
  document.getElementById("navPoints").textContent = (stats.total_points || 0).toLocaleString();
}

function updateNavUser(user) {
  document.getElementById("navUserAvatar").textContent = user.display_name.charAt(0).toUpperCase();
  document.getElementById("navUserName").textContent   = user.display_name;
}

// ============================================================
//  Dashboard
// ============================================================
async function renderDashboard() {
  const [stats, progress, subjects] = await Promise.all([
    fetchStats(),
    fetchProgress(),
    STATE.subjects.length ? Promise.resolve(STATE.subjects) : fetchSubjects(),
  ]);
  if (!STATE.subjects.length) STATE.subjects = subjects;

  updateNavStats(stats);

  const u    = STATE.currentUser;
  const hour = new Date().getHours();
  const g    = hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";
  document.getElementById("greeting").textContent = `${g}, ${u?.display_name || "Champion"}!`;

  document.getElementById("statQuizzes").textContent = stats.quizzes_done || 0;
  document.getElementById("statPoints").textContent  = (stats.total_points || 0).toLocaleString();
  document.getElementById("statStreak").textContent  = `${stats.streak || 0} day${stats.streak !== 1 ? "s" : ""}`;

  const pMap = {};
  (progress || []).forEach(p => { pMap[`${p.subject}__${p.topic}`] = p; });

  subjects.forEach(subj => {
    let total = 0, best = 0;
    subj.topics.forEach(t => {
      const p = pMap[`${subj.id}__${t.id}`];
      if (p && p.total_questions > 0) { total += p.total_questions; best += p.best_score; }
    });
    const pct   = total > 0 ? Math.round((best / total) * 100) : 0;
    const bar   = document.querySelector(`#card-${subj.id} .progress-bar-fill`);
    const label = document.querySelector(`#card-${subj.id} .progress-label`);
    if (bar)   bar.style.width = pct + "%";
    if (label) label.textContent = pct > 0 ? `${pct}% mastery` : "Not started yet";
  });
}

// ============================================================
//  Subject page
// ============================================================
async function openSubject(subjectId) {
  STATE.currentSubject = subjectId;
  const subjects = STATE.subjects.length ? STATE.subjects : await fetchSubjects();
  if (!STATE.subjects.length) STATE.subjects = subjects;
  const subject = subjects.find(s => s.id === subjectId);
  if (!subject) return;

  const progress = await fetchProgress();
  const pMap = {};
  (progress || []).forEach(p => { pMap[`${p.subject}__${p.topic}`] = p; });

  const header = document.getElementById("subjectHeader");
  header.className = `subject-header ${subjectId}`;
  header.innerHTML = `
    <div class="header-icon">${subject.icon}</div>
    <div>
      <h2>${subject.name}</h2>
      <p>Choose a topic — ${subject.topics.reduce((a,t)=>a+(t.question_count||0),0)} questions available</p>
    </div>`;

  const grid = document.getElementById("topicsGrid");
  grid.innerHTML = "";
  subject.topics.forEach(topic => {
    const tp     = pMap[`${subjectId}__${topic.id}`];
    const pct    = tp && tp.total_questions > 0 ? Math.round((tp.best_score / tp.total_questions) * 100) : null;
    const qCount = topic.question_count || 0;

    const card = document.createElement("div");
    card.className = "topic-card";
    card.innerHTML = `
      <div class="topic-icon">${topic.icon}</div>
      <div class="topic-info">
        <h4>${topic.name}</h4>
        <p>${topic.desc} · <strong>${qCount} questions</strong></p>
      </div>
      <div class="topic-score">
        ${pct !== null
          ? `<span style="color:var(--success)">${pct}%</span><br><span style="font-size:11px;color:var(--text-light)">${tp.attempts} tries</span>`
          : `<span style="color:var(--text-light)">${qCount > 0 ? "New" : "Soon"}</span>`}
      </div>`;
    if (qCount > 0) {
      card.style.cursor = "pointer";
      card.addEventListener("click", () => openQuizSetup(subjectId, topic.id, topic.name, qCount));
    } else {
      card.style.opacity = "0.5";
    }
    grid.appendChild(card);
  });

  showPage("page-subject");
}

// ============================================================
//  Quiz Setup Modal
// ============================================================
const QUIZ_SETUP = { subjectId: null, topicId: null, topicName: null, total: 0, count: 0 };

function openQuizSetup(subjectId, topicId, topicName, totalQuestions) {
  QUIZ_SETUP.subjectId  = subjectId;
  QUIZ_SETUP.topicId    = topicId;
  QUIZ_SETUP.topicName  = topicName;
  QUIZ_SETUP.total      = totalQuestions;
  QUIZ_SETUP.count      = totalQuestions; // default: all questions

  document.getElementById("quizSetupTitle").textContent = topicName;
  document.getElementById("quizSetupDesc").textContent  = `Select how many questions you want to attempt.`;
  document.getElementById("qCountTotal").textContent    = totalQuestions;
  document.getElementById("qCountSlider").max           = totalQuestions;
  document.getElementById("qCountSlider").value         = totalQuestions;
  document.getElementById("qCountDisplay").textContent  = totalQuestions;
  document.getElementById("quizSetupModal").classList.add("show");
}

function closeQuizSetup() {
  document.getElementById("quizSetupModal").classList.remove("show");
}

function syncSlider(val) {
  QUIZ_SETUP.count = parseInt(val);
  document.getElementById("qCountDisplay").textContent = val;
}

function adjustQCount(delta) {
  const next = Math.min(QUIZ_SETUP.total, Math.max(1, QUIZ_SETUP.count + delta));
  QUIZ_SETUP.count = next;
  document.getElementById("qCountDisplay").textContent = next;
  document.getElementById("qCountSlider").value        = next;
}

function confirmQuizSetup() {
  closeQuizSetup();
  startQuiz(QUIZ_SETUP.subjectId, QUIZ_SETUP.topicId, QUIZ_SETUP.topicName, QUIZ_SETUP.count);
}

// ============================================================
//  Quiz
// ============================================================
async function startQuiz(subjectId, topicId, topicName, questionLimit = 0) {
  STATE.currentSubject = subjectId;
  STATE.currentTopic   = topicId;
  STATE.quizStartTime  = Date.now();

  let questions;
  try { questions = await fetchQuestions(subjectId, topicId, questionLimit); }
  catch (e) { showToast("Could not load questions: " + e.message, "error"); return; }

  // selectedAnswers stores the index chosen for each question (null = not answered)
  STATE.currentQuiz = { questions, index: 0, score: 0, selectedAnswers: new Array(questions.length).fill(null) };

  const subject = STATE.subjects.find(s => s.id === subjectId);
  document.getElementById("quizSubjectName").textContent = `${subject?.name || subjectId} — ${topicName}`;
  document.getElementById("quizTotalQ").textContent = questions.length;

  renderProgressDots();
  startTimer(questions.length * 60);
  renderQuestion();
  showPage("page-quiz");
}

function renderProgressDots() {
  const { questions, index } = STATE.currentQuiz;
  document.getElementById("questionProgress").innerHTML = questions.map((_, i) => {
    let cls = "q-dot";
    if (i < index) cls += " answered";
    else if (i === index) cls += " current";
    return `<div class="${cls}"></div>`;
  }).join("");
}

function startTimer(seconds) {
  clearInterval(STATE.timer);
  STATE.timeLeft = seconds;
  updateTimerDisplay();
  STATE.timer = setInterval(() => {
    STATE.timeLeft--;
    updateTimerDisplay();
    if (STATE.timeLeft <= 0) { clearInterval(STATE.timer); finishQuiz(); }
  }, 1000);
}

function updateTimerDisplay() {
  const el = document.getElementById("quizTimer");
  const m  = Math.floor(STATE.timeLeft / 60);
  const s  = STATE.timeLeft % 60;
  el.textContent = `${m}:${s.toString().padStart(2, "0")}`;
  el.classList.toggle("warning", STATE.timeLeft <= 30);
}

function renderQuestion() {
  const { questions, index } = STATE.currentQuiz;
  const q = questions[index];

  document.getElementById("questionNumber").textContent     = `Question ${index + 1} of ${questions.length}`;
  document.getElementById("questionCurrentNum").textContent = index + 1;

  const passageEl = document.getElementById("questionPassage");
  if (q.passage) {
    passageEl.style.display = "block";
    passageEl.innerHTML = `<div style="background:var(--bg);border-left:4px solid var(--primary);padding:16px 20px;border-radius:0 12px 12px 0;font-size:15px;line-height:1.7;margin-bottom:20px;">${q.passage}</div>`;
  } else {
    passageEl.style.display = "none";
  }

  document.getElementById("questionText").textContent = q.question;

  const container = document.getElementById("optionsContainer");
  const letters   = ["A", "B", "C", "D"];
  container.innerHTML = "";
  container.className = `options-grid${q.options.length <= 2 ? " single-col" : ""}`;
  q.options.forEach((opt, i) => {
    const btn = document.createElement("button");
    btn.className = "option-btn";
    btn.innerHTML = `<span class="option-letter">${letters[i]}</span> ${opt}`;
    btn.addEventListener("click", () => selectAnswer(q, i));
    container.appendChild(btn);
  });

  // Exam mode — no feedback, no hints
  document.getElementById("feedbackBox").className = "feedback-box";
  document.getElementById("feedbackBox").textContent = "";
  document.getElementById("hintBox").className = "hint-box";
  document.getElementById("hintBtn").style.display = "none";
  document.getElementById("nextBtn").disabled = true;
  document.getElementById("nextBtn").textContent = index === questions.length - 1 ? "Submit Exam" : "Next Question →";

  renderProgressDots();
}

function selectAnswer(q, selectedIndex) {
  // Record selection — no server call, no feedback shown
  STATE.currentQuiz.selectedAnswers[STATE.currentQuiz.index] = selectedIndex;

  // Highlight chosen option in blue only
  document.querySelectorAll(".option-btn").forEach((b, i) => {
    b.classList.toggle("selected", i === selectedIndex);
  });

  document.getElementById("nextBtn").disabled = false;
}

function showHint() { /* disabled in exam mode */ }

function nextQuestion() {
  STATE.currentQuiz.index++;
  if (STATE.currentQuiz.index >= STATE.currentQuiz.questions.length) finishQuiz();
  else renderQuestion();
}

async function finishQuiz() {
  clearInterval(STATE.timer);
  const { questions, selectedAnswers } = STATE.currentQuiz;
  const total     = questions.length;
  const timeTaken = Math.round((Date.now() - STATE.quizStartTime) / 1000);

  // Verify all answers server-side now (batch)
  let score = 0;
  await Promise.all(questions.map(async (q, i) => {
    const chosen = selectedAnswers[i];
    if (chosen === null) return; // unanswered (timeout)
    try {
      const res = await verifyAnswer(STATE.currentSubject, STATE.currentTopic, q.id, chosen);
      if (res.correct) score++;
    } catch (_e) {}
  }));

  STATE.currentQuiz.score = score;
  const pct = Math.round((score / total) * 100);

  const resultData = await postResult({
    subject:            STATE.currentSubject,
    topic:              STATE.currentTopic,
    score,
    total_questions:    total,
    hints_used:         0,
    time_taken_seconds: timeTaken,
  });

  const pts     = resultData.points_earned ?? Math.max(0, score * 10);
  const emoji   = pct >= 80 ? "🏆" : pct >= 60 ? "🌟" : pct >= 40 ? "😊" : "💪";
  const message = pct >= 80 ? "Outstanding work!" : pct >= 60 ? "Great effort!" : pct >= 40 ? "Good try — keep practising!" : "Keep going — you're learning!";

  document.getElementById("resultsEmoji").textContent      = emoji;
  document.getElementById("resultsMessage").textContent    = message;
  document.getElementById("resultsScoreNum").textContent   = score;
  document.getElementById("resultsScoreDenom").textContent = total;
  document.getElementById("resultsPct").textContent        = `${pct}%`;
  document.getElementById("resultsPoints").textContent     = `+${pts} pts`;
  document.getElementById("resultsTime").textContent       = formatTime(timeTaken);
  document.getElementById("resultsHints").textContent      = total;

  // Clear the answer review — exam mode shows score only
  document.getElementById("answersReview").innerHTML = "";

  updateNavStats({ total_points: resultData.new_total_points || 0, streak: resultData.new_streak || 0 });
  if (pct >= 80) triggerConfetti();
  showPage("page-results");
}

function renderAnswersReview(questions) {
  const letters = ["A", "B", "C", "D"];
  const { answers } = STATE.currentQuiz;
  const answeredMap = {};
  answers.forEach(a => { answeredMap[a.qIndex] = a; });

  const container = document.getElementById("answersReview");
  container.innerHTML = "<h3 class='review-heading'>Answer Review</h3>";

  questions.forEach((q, i) => {
    const a = answeredMap[i];
    const card = document.createElement("div");
    card.className = "review-card " + (a ? (a.correct ? "review-correct" : "review-wrong") : "review-skipped");

    let optionsHtml = q.options.map((opt, idx) => {
      let cls = "review-option";
      if (a) {
        if (idx === a.correct_answer) cls += " review-opt-correct";
        else if (idx === a.selectedIndex && !a.correct) cls += " review-opt-wrong";
      }
      return `<div class="${cls}"><span class="review-opt-letter">${letters[idx]}</span> ${opt}</div>`;
    }).join("");

    const status = !a ? "⏭ Not reached" : a.correct ? "✅ Correct" : "❌ Incorrect";
    const expl   = a?.explanation ? `<div class="review-explanation">${a.explanation}</div>` : "";

    card.innerHTML = `
      <div class="review-q-header">
        <span class="review-q-num">Q${i + 1}</span>
        <span class="review-status">${status}</span>
      </div>
      <p class="review-q-text">${q.question}</p>
      <div class="review-options">${optionsHtml}</div>
      ${expl}`;
    container.appendChild(card);
  });
}

function formatTime(secs) {
  return `${Math.floor(secs / 60)}:${(secs % 60).toString().padStart(2, "0")}`;
}

// ============================================================
//  Mock Exam
// ============================================================
const MOCK = {
  sections:        [],   // [ { subject, subject_name, icon, questions: [] } ]
  flatQuestions:   [],   // all questions in order with section info attached
  selectedAnswers: [],   // chosen option index per flat question
  index:           0,    // current flat question index
  startTime:       0,
  timer:           null,
};

async function startMockExam(questionsPerSubject) {
  showToast("Loading exam…");
  let sections;
  try {
    sections = await api(`/api/questions/mock-exam?questions_per_subject=${questionsPerSubject}`);
  } catch (e) {
    showToast("Could not load mock exam: " + e.message, "error");
    return;
  }
  if (!sections || sections.length === 0) {
    showToast("No questions available yet.", "error");
    return;
  }

  MOCK.sections        = sections;
  MOCK.flatQuestions   = sections.flatMap(s =>
    s.questions.map(q => ({ ...q, subject_name: s.subject_name, subject_icon: s.icon }))
  );
  MOCK.selectedAnswers = new Array(MOCK.flatQuestions.length).fill(null);
  MOCK.index           = 0;
  MOCK.startTime       = Date.now();

  const total    = MOCK.flatQuestions.length;
  const duration = total * 60; // 1 min per question

  document.getElementById("mockTotalQ").textContent = total;
  renderMockSectionBar();
  startMockTimer(duration);
  renderMockQuestion();
  showPage("page-mock-exam");
}

function renderMockSectionBar() {
  const bar = document.getElementById("mockSectionBar");
  const counts = MOCK.sections.map(s => s.questions.length);
  const total  = MOCK.flatQuestions.length;
  bar.innerHTML = counts.map((c, i) => {
    const s   = MOCK.sections[i];
    const pct = (c / total * 100).toFixed(1);
    const colors = { english:"#4299E1", maths:"#48BB78", verbal:"#ED8936", nonverbal:"#9F7AEA" };
    const col = colors[s.subject] || "#6C63FF";
    return `<div class="mock-section-seg" style="width:${pct}%;background:${col}" title="${s.subject_name}: ${c} questions"></div>`;
  }).join("");
}

function startMockTimer(seconds) {
  clearInterval(MOCK.timer);
  let remaining = seconds;
  const el = document.getElementById("mockTimer");
  const tick = () => {
    const m = Math.floor(remaining / 60);
    const s = remaining % 60;
    el.textContent = `${m}:${s.toString().padStart(2, "0")}`;
    el.classList.toggle("warning", remaining <= 60);
    if (remaining <= 0) { clearInterval(MOCK.timer); finishMockExam(); }
    remaining--;
  };
  tick();
  MOCK.timer = setInterval(tick, 1000);
}

function renderMockQuestion() {
  const q      = MOCK.flatQuestions[MOCK.index];
  const total  = MOCK.flatQuestions.length;
  const letters = ["A", "B", "C", "D"];

  document.getElementById("mockSectionName").textContent    = `${q.subject_icon} ${q.subject_name}`;
  document.getElementById("mockCurrentNum").textContent     = MOCK.index + 1;
  document.getElementById("mockQuestionNumber").textContent = `Question ${MOCK.index + 1} of ${total}`;

  const passageEl = document.getElementById("mockQuestionPassage");
  if (q.passage) {
    passageEl.style.display = "block";
    passageEl.innerHTML = `<div style="background:var(--bg);border-left:4px solid var(--primary);padding:16px 20px;border-radius:0 12px 12px 0;font-size:15px;line-height:1.7;margin-bottom:20px;">${q.passage}</div>`;
  } else {
    passageEl.style.display = "none";
  }

  document.getElementById("mockQuestionText").textContent = q.question;

  const container = document.getElementById("mockOptionsContainer");
  container.innerHTML = "";
  container.className = `options-grid${q.options.length <= 2 ? " single-col" : ""}`;
  q.options.forEach((opt, i) => {
    const btn = document.createElement("button");
    btn.className = "option-btn";
    if (MOCK.selectedAnswers[MOCK.index] === i) btn.classList.add("selected");
    btn.innerHTML = `<span class="option-letter">${letters[i]}</span> ${opt}`;
    btn.addEventListener("click", () => selectMockAnswer(i));
    container.appendChild(btn);
  });

  // Progress dots for current section only
  const sectionOffset = getSectionOffset(MOCK.index);
  const sectionLen    = MOCK.sections.find(s => s.subject === q.subject)?.questions.length || 1;
  const posInSection  = MOCK.index - sectionOffset;
  document.getElementById("mockQuestionProgress").innerHTML =
    Array.from({ length: sectionLen }, (_, i) => {
      let cls = "q-dot";
      if (i < posInSection)        cls += " answered";
      else if (i === posInSection) cls += " current";
      return `<div class="${cls}"></div>`;
    }).join("");

  const isLast = MOCK.index === total - 1;
  const nextBtn = document.getElementById("mockNextBtn");
  nextBtn.textContent = isLast ? "Submit Exam" : "Next Question →";
  nextBtn.disabled    = MOCK.selectedAnswers[MOCK.index] === null;
}

function getSectionOffset(flatIndex) {
  let offset = 0;
  for (const s of MOCK.sections) {
    if (flatIndex < offset + s.questions.length) return offset;
    offset += s.questions.length;
  }
  return 0;
}

function selectMockAnswer(optionIndex) {
  MOCK.selectedAnswers[MOCK.index] = optionIndex;
  document.querySelectorAll("#mockOptionsContainer .option-btn").forEach((b, i) => {
    b.classList.toggle("selected", i === optionIndex);
  });
  document.getElementById("mockNextBtn").disabled = false;
}

function mockNext() {
  MOCK.index++;
  if (MOCK.index >= MOCK.flatQuestions.length) finishMockExam();
  else renderMockQuestion();
}

async function finishMockExam() {
  clearInterval(MOCK.timer);
  const timeTaken = Math.round((Date.now() - MOCK.startTime) / 1000);
  const questions = MOCK.flatQuestions;
  const answers   = MOCK.selectedAnswers;

  // Verify all answers in parallel
  const results = await Promise.all(questions.map(async (q, i) => {
    const chosen = answers[i];
    if (chosen === null) return { correct: false, subject: q.subject };
    try {
      const res = await verifyAnswer(q.subject, q.topic, q.id, chosen);
      return { correct: res.correct, subject: q.subject };
    } catch (_e) {
      return { correct: false, subject: q.subject };
    }
  }));

  // Overall totals
  const totalQ = questions.length;
  const totalCorrect = results.filter(r => r.correct).length;
  const pct = Math.round((totalCorrect / totalQ) * 100);

  // Per-subject breakdown
  const bySubject = {};
  MOCK.sections.forEach(s => {
    bySubject[s.subject] = { name: s.subject_name, icon: s.icon, correct: 0, total: s.questions.length };
  });
  results.forEach(r => { if (r.correct) bySubject[r.subject].correct++; });

  // Save result per subject to progress
  let totalPoints = 0;
  await Promise.all(Object.entries(bySubject).map(async ([subj, data]) => {
    const res = await postResult({
      subject:            subj,
      topic:              "mock_exam",
      score:              data.correct,
      total_questions:    data.total,
      hints_used:         0,
      time_taken_seconds: Math.round(timeTaken / MOCK.sections.length),
    });
    totalPoints += res.points_earned ?? 0;
  }));

  // Render results
  const emoji   = pct >= 80 ? "🏆" : pct >= 60 ? "🌟" : pct >= 40 ? "😊" : "💪";
  const message = pct >= 80 ? "Excellent — grammar school ready!" : pct >= 60 ? "Great effort, keep it up!" : pct >= 40 ? "Good try — keep practising!" : "Keep going — you're improving!";

  document.getElementById("mockResultsEmoji").textContent = emoji;
  document.getElementById("mockResultsMessage").textContent = message;
  document.getElementById("mockScoreNum").textContent  = totalCorrect;
  document.getElementById("mockScoreDenom").textContent = `/ ${totalQ}`;
  document.getElementById("mockOverallPct").textContent = `${pct}%`;
  document.getElementById("mockPointsEarned").textContent = `+${totalPoints} pts`;
  document.getElementById("mockTimeTaken").textContent = formatTime(timeTaken);
  document.getElementById("mockTotalDone").textContent = totalQ;

  // Subject breakdown cards
  const breakdown = document.getElementById("mockSubjectBreakdown");
  const colors = { english:"#4299E1", maths:"#48BB78", verbal:"#ED8936", nonverbal:"#9F7AEA" };
  breakdown.innerHTML = `<div style="font-size:16px;font-weight:800;margin:20px 0 12px">Subject Breakdown</div>` +
    Object.entries(bySubject).map(([subj, d]) => {
      const spct  = Math.round((d.correct / d.total) * 100);
      const color = colors[subj] || "#6C63FF";
      return `<div style="background:white;border-radius:16px;padding:20px;box-shadow:var(--shadow);margin-bottom:12px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
          <span style="font-weight:800;font-size:15px">${d.icon} ${d.name}</span>
          <span style="font-weight:900;font-size:18px;color:${color}">${spct}%</span>
        </div>
        <div style="height:8px;background:#EDF2F7;border-radius:4px;overflow:hidden">
          <div style="height:100%;width:${spct}%;background:${color};border-radius:4px;transition:width .6s ease"></div>
        </div>
        <div style="font-size:12px;color:var(--text-light);margin-top:8px">${d.correct} correct out of ${d.total}</div>
      </div>`;
    }).join("");

  if (pct >= 80) triggerConfetti();
  showPage("page-mock-results");
  updateNavStats({ total_points: 0, streak: 0 }); // will refresh on next dashboard load
  await renderDashboard();
}

// ============================================================
//  Progress page
// ============================================================
async function renderProgressPage() {
  const [stats, progress, subjects] = await Promise.all([
    fetchStats(),
    fetchProgress(),
    STATE.subjects.length ? Promise.resolve(STATE.subjects) : fetchSubjects(),
  ]);
  if (!STATE.subjects.length) STATE.subjects = subjects;

  document.getElementById("progTotalPoints").textContent  = (stats.total_points || 0).toLocaleString();
  document.getElementById("progTotalQuizzes").textContent = stats.quizzes_done || 0;
  document.getElementById("progStreak").textContent       = `${stats.streak || 0} day${stats.streak !== 1 ? "s" : ""}`;

  const pMap     = {};
  (progress || []).forEach(p => { pMap[`${p.subject}__${p.topic}`] = p; });
  const colorMap = { english:"var(--english)", maths:"var(--maths)", verbal:"var(--verbal)", nonverbal:"var(--nonverbal)" };
  const container = document.getElementById("subjectProgressList");
  container.innerHTML = "";

  subjects.forEach(subj => {
    const color = colorMap[subj.id] || "var(--primary)";
    const rows  = subj.topics.map(t => {
      const tp  = pMap[`${subj.id}__${t.id}`];
      const pct = tp && tp.total_questions > 0 ? Math.round((tp.best_score / tp.total_questions) * 100) : 0;
      return `<div class="topic-score-row">
        <span class="ts-name">${t.icon} ${t.name}</span>
        <div class="ts-bar"><div class="ts-fill" style="width:${pct}%;background:${color}"></div></div>
        <span class="ts-pct">${pct > 0 ? pct + "%" : "—"}</span>
      </div>`;
    }).join("");
    const item = document.createElement("div");
    item.className = "subject-progress-item";
    item.innerHTML = `<h4>${subj.icon} ${subj.name}</h4><div class="topic-scores-list">${rows}</div>`;
    container.appendChild(item);
  });
}

// ============================================================
//  Confetti + Toast
// ============================================================
function triggerConfetti() {
  const overlay = document.getElementById("confettiOverlay");
  overlay.innerHTML = "";
  const colors = ["#6C63FF","#FF6B6B","#4ECDC4","#FFD93D","#6BCB77","#FF9A9A"];
  for (let i = 0; i < 60; i++) {
    const p = document.createElement("div");
    p.className = "confetti-piece";
    p.style.cssText = `left:${Math.random()*100}%;background:${colors[~~(Math.random()*colors.length)]};
      animation-delay:${Math.random()}s;animation-duration:${1.5+Math.random()*1.5}s;
      width:${6+Math.random()*10}px;height:${6+Math.random()*10}px;
      border-radius:${Math.random()>.5?"50%":"2px"}`;
    overlay.appendChild(p);
  }
  setTimeout(() => { overlay.innerHTML = ""; }, 4000);
}

function showToast(msg, type = "info") {
  const t = document.createElement("div");
  t.textContent = msg;
  t.style.cssText = `position:fixed;bottom:90px;left:50%;transform:translateX(-50%);
    background:${type === "error" ? "#FC8181" : "#6C63FF"};color:white;padding:12px 24px;
    border-radius:12px;font-weight:700;font-size:14px;z-index:9999;animation:fadeIn .3s ease`;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 3000);
}

// ============================================================
//  Boot the app after successful login/token restore
// ============================================================
async function bootApp() {
  updateNavUser(STATE.currentUser);
  await ensureSession();
  // Wire subject cards (only needs to happen once but safe to repeat)
  document.querySelectorAll(".subject-card[data-subject]").forEach(card => {
    // Clone to remove previous listeners
    const clone = card.cloneNode(true);
    card.parentNode.replaceChild(clone, card);
    clone.addEventListener("click", () => openSubject(clone.dataset.subject));
  });
  showAppScreen();
  showPage("page-dashboard");
  await renderDashboard();
}

// ============================================================
//  DOMContentLoaded — wire up everything
// ============================================================
document.addEventListener("DOMContentLoaded", async () => {

  // Auth forms
  document.getElementById("loginForm").addEventListener("submit",    handleLogin);
  document.getElementById("registerForm").addEventListener("submit", handleRegister);

  // Profile modal
  document.getElementById("profileModal").addEventListener("click", e => {
    if (e.target === e.currentTarget) closeProfileModal();
  });

  // Back buttons
  document.getElementById("backFromSubject").addEventListener("click", goHome);
  document.getElementById("backFromQuiz").addEventListener("click", () => {
    clearInterval(STATE.timer);
    openSubject(STATE.currentSubject);
  });

  // Quiz controls
  document.getElementById("nextBtn").addEventListener("click", nextQuestion);
  document.getElementById("hintBtn").addEventListener("click", showHint);

  // Mock exam next button
  document.getElementById("mockNextBtn").addEventListener("click", mockNext);

  // Results buttons
  document.getElementById("retryBtn").addEventListener("click", () => {
    const subj      = STATE.subjects.find(s => s.id === STATE.currentSubject);
    const topic     = subj?.topics.find(t => t.id === STATE.currentTopic);
    if (topic) openQuizSetup(STATE.currentSubject, topic.id, topic.name, topic.question_count || QUIZ_SETUP.total);
  });
  document.getElementById("chooseTopicBtn").addEventListener("click", () => openSubject(STATE.currentSubject));
  document.getElementById("homeBtn").addEventListener("click", goHome);

  // Bottom nav
  document.querySelectorAll(".bottom-nav-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const page = btn.dataset.page;
      if (page === "page-progress")  renderProgressPage();
      if (page === "page-dashboard") renderDashboard();
      showPage(page);
    });
  });

  // Close mock setup modal on overlay click
  document.getElementById("quizSetupModal").addEventListener("click", e => {
    if (e.target === e.currentTarget) closeQuizSetup();
  });

  // ---- Restore session if token exists ----
  const token      = getToken();
  const storedUser = localStorage.getItem(USER_KEY);
  if (token && storedUser) {
    try {
      const r = await fetch("/api/auth/me", { headers: { Authorization: `Bearer ${token}` } });
      if (r.ok) {
        const user = await r.json();
        STATE.currentUser = user;
        localStorage.setItem(USER_KEY, JSON.stringify(user));
        await bootApp();
        return;
      }
    } catch (_) {}
    // Token stale — clear and fall through to auth screen
    clearAuth();
  }

  showAuthScreen();
});
