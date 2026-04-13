import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")


class Settings:
    admin_token: str = os.getenv("ADMIN_TOKEN", "admin123")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./grammar_school.db")


settings = Settings()
