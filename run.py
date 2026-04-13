#!/usr/bin/env python3
"""
Start the Grammar School Prep server.

Usage:
  python run.py              # start server (seeds DB on first run)
  python run.py --seed-only  # seed questions then exit
"""
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent


def seed():
    print("Seeding questions into the database…")
    result = subprocess.run(
        [sys.executable, "-m", "backend.seed.seed_questions"],
        cwd=ROOT,
    )
    if result.returncode != 0:
        print("Seed failed.")
        sys.exit(1)


def run_server():
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(ROOT / "backend")],
    )


if __name__ == "__main__":
    if "--seed-only" in sys.argv:
        seed()
    else:
        # Auto-seed if DB doesn't exist
        db_path = ROOT / "grammar_school.db"
        if not db_path.exists():
            seed()
        run_server()
