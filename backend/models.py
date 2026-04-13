from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import (
    Integer, String, Text, Boolean, DateTime, Date, JSON, ForeignKey,
    UniqueConstraint, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


# ============================================================
#  Users
# ============================================================

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(100))
    year_group: Mapped[int] = mapped_column(Integer, default=3)       # 3–6
    password_hash: Mapped[str] = mapped_column(String(255))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    tokens: Mapped[List["UserToken"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    sessions: Mapped[List["Session"]] = relationship(back_populates="user")


class UserToken(Base):
    __tablename__ = "user_tokens"

    token: Mapped[str] = mapped_column(String(36), primary_key=True)  # UUID
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    user: Mapped["User"] = relationship(back_populates="tokens")


# ============================================================
#  Questions
# ============================================================

class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    subject: Mapped[str] = mapped_column(String(50), index=True)
    topic: Mapped[str] = mapped_column(String(80), index=True)
    question: Mapped[str] = mapped_column(Text)
    passage: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    options: Mapped[List] = mapped_column(JSON)
    answer: Mapped[int] = mapped_column(Integer)
    explanation: Mapped[str] = mapped_column(Text)
    hint: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    difficulty: Mapped[int] = mapped_column(Integer, default=2)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


# ============================================================
#  Sessions & Progress
# ============================================================

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    last_seen: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    total_points: Mapped[int] = mapped_column(Integer, default=0)
    quizzes_done: Mapped[int] = mapped_column(Integer, default=0)
    streak: Mapped[int] = mapped_column(Integer, default=0)
    last_quiz_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    user: Mapped[Optional["User"]] = relationship(back_populates="sessions")
    results: Mapped[List["QuizResult"]] = relationship(back_populates="session", cascade="all, delete-orphan")
    topic_progress: Mapped[List["TopicProgress"]] = relationship(back_populates="session", cascade="all, delete-orphan")


class QuizResult(Base):
    __tablename__ = "quiz_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("sessions.id", ondelete="CASCADE"))
    subject: Mapped[str] = mapped_column(String(50))
    topic: Mapped[str] = mapped_column(String(80))
    score: Mapped[int] = mapped_column(Integer)
    total_questions: Mapped[int] = mapped_column(Integer)
    hints_used: Mapped[int] = mapped_column(Integer, default=0)
    points_earned: Mapped[int] = mapped_column(Integer, default=0)
    time_taken_seconds: Mapped[int] = mapped_column(Integer, default=0)
    completed_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    session: Mapped["Session"] = relationship(back_populates="results")


class TopicProgress(Base):
    __tablename__ = "topic_progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("sessions.id", ondelete="CASCADE"))
    subject: Mapped[str] = mapped_column(String(50))
    topic: Mapped[str] = mapped_column(String(80))
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    best_score: Mapped[int] = mapped_column(Integer, default=0)
    total_questions: Mapped[int] = mapped_column(Integer, default=0)

    __table_args__ = (UniqueConstraint("session_id", "subject", "topic", name="uq_session_subject_topic"),)
    session: Mapped["Session"] = relationship(back_populates="topic_progress")
