from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, field_validator


# ---- Questions ----

class QuestionBase(BaseModel):
    subject: str
    topic: str
    question: str
    passage: Optional[str] = None
    options: List[str]
    answer: int
    explanation: str
    hint: Optional[str] = None
    difficulty: int = 2
    active: bool = True

    @field_validator("options")
    @classmethod
    def check_options(cls, v):
        if len(v) < 2 or len(v) > 4:
            raise ValueError("questions must have 2–4 options")
        return v

    @field_validator("answer")
    @classmethod
    def check_answer(cls, v):
        if v < 0:
            raise ValueError("answer index must be >= 0")
        return v


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(BaseModel):
    subject: Optional[str] = None
    topic: Optional[str] = None
    question: Optional[str] = None
    passage: Optional[str] = None
    options: Optional[List[str]] = None
    answer: Optional[int] = None
    explanation: Optional[str] = None
    hint: Optional[str] = None
    difficulty: Optional[int] = None
    active: Optional[bool] = None


class QuestionOut(QuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class QuestionPublic(BaseModel):
    """Stripped-down version for the student app — no answer exposed."""
    id: int
    subject: str
    topic: str
    question: str
    passage: Optional[str] = None
    options: List[str]
    hint: Optional[str] = None
    difficulty: int

    model_config = {"from_attributes": True}


# ---- Sessions ----

class SessionOut(BaseModel):
    id: str
    total_points: int
    quizzes_done: int
    streak: int
    last_quiz_date: Optional[date] = None

    model_config = {"from_attributes": True}


# ---- Progress ----

class TopicProgressOut(BaseModel):
    subject: str
    topic: str
    attempts: int
    best_score: int
    total_questions: int

    model_config = {"from_attributes": True}


# ---- Quiz Result submission ----

class QuizResultIn(BaseModel):
    subject: str
    topic: str
    score: int
    total_questions: int
    hints_used: int = 0
    time_taken_seconds: int = 0
    # question IDs answered so we can verify server-side answer if needed
    answers: Optional[List[dict]] = None   # [{question_id, selected}]


class QuizResultOut(BaseModel):
    id: int
    points_earned: int
    new_total_points: int
    new_streak: int

    model_config = {"from_attributes": True}


# ---- Admin stats ----

class TopicStats(BaseModel):
    subject: str
    topic: str
    total: int
    active: int


class AdminStats(BaseModel):
    total_questions: int
    active_questions: int
    total_sessions: int
    total_quizzes: int
    by_topic: List[TopicStats]
