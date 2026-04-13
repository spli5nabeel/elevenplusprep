from pathlib import Path
from fastapi import FastAPI
from sqlalchemy import text

from .database import Base, engine
from .routers import questions, progress, admin
from .routers import auth as auth_router

# Create all new tables
Base.metadata.create_all(bind=engine)

# ---- Runtime migrations for existing databases ----
def _migrate():
    with engine.connect() as conn:
        existing_cols = {
            row[1] for row in conn.execute(text("PRAGMA table_info(sessions)"))
        }
        if "user_id" not in existing_cols:
            conn.execute(text("ALTER TABLE sessions ADD COLUMN user_id INTEGER REFERENCES users(id)"))
            conn.commit()

_migrate()

app = FastAPI(title="Grammar School 11+ Prep", version="2.0.0")

# ---- API routers ----
app.include_router(auth_router.router)
app.include_router(questions.router)
app.include_router(progress.router)
app.include_router(admin.router)

# ---- Static files ----
from fastapi.staticfiles import StaticFiles

FRONTEND_DIR = Path(__file__).parent.parent

app.mount("/admin", StaticFiles(directory=str(FRONTEND_DIR / "admin"), html=True), name="admin")
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="static")
