---
name: Grammar School Prep Platform
description: Full-stack 11+ exam prep app for user's son (Year 3) targeting Master Brain Academy Ilford and local grammar schools
type: project
---

FastAPI + SQLite platform in /Users/nabeel/work/ai-work/grammar-school/.

**Why:** User's son is in Year 3 and preparing for UK grammar school 11+ entrance, targeting Master Brain Academy Ilford (Essex/Redbridge area — Valentines, Ilford County, Woodford County grammar schools).

**How to apply:** When making changes, keep the student UI child-friendly and gamified. The admin panel is for the parent/admin to manage questions.

**Stack:**
- Backend: FastAPI, SQLAlchemy, SQLite (`grammar_school.db`)
- Frontend: Vanilla HTML/CSS/JS served by FastAPI static files
- Admin: `/admin/` — dark-themed CRUD panel (login: token from `.env`)
- Start: `python3 run.py` from project root (port 8000)
- Seed: `python3 run.py --seed-only` or auto-seeds on first run

**Current state (2026-04-12):**
- 194 questions seeded across 4 subjects × 15 topics
- Admin panel: login, dashboard, question list (filter/edit/toggle), add question form, bulk JSON/CSV import
- Student app: quiz engine with timer, hints, points, streaks, progress page
- Session tracking stored server-side (SQLite) via UUID from localStorage
