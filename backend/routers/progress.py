from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from ..database import get_db
from ..models import Session as StudentSession, QuizResult, TopicProgress
from ..schemas import SessionOut, QuizResultIn, QuizResultOut, TopicProgressOut

router = APIRouter(prefix="/api/sessions", tags=["progress"])


def _get_or_create_session(session_id: str, db: Session) -> StudentSession:
    sess = db.get(StudentSession, session_id)
    if not sess:
        sess = StudentSession(id=session_id)
        db.add(sess)
        db.commit()
        db.refresh(sess)
    return sess


@router.post("", response_model=SessionOut, status_code=201)
def create_session(session_id: str, db: Session = Depends(get_db)):
    """Idempotent — returns existing session or creates a new one."""
    sess = _get_or_create_session(session_id, db)
    return sess


@router.get("/{session_id}", response_model=SessionOut)
def get_session(session_id: str, db: Session = Depends(get_db)):
    sess = db.get(StudentSession, session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
    return sess


@router.post("/{session_id}/results", response_model=QuizResultOut, status_code=201)
def submit_result(session_id: str, payload: QuizResultIn, db: Session = Depends(get_db)):
    sess = _get_or_create_session(session_id, db)

    # Points: 10 per correct, -2 per hint, min 0
    points = max(0, payload.score * 10 - payload.hints_used * 2)

    # Save quiz result
    result = QuizResult(
        session_id=session_id,
        subject=payload.subject,
        topic=payload.topic,
        score=payload.score,
        total_questions=payload.total_questions,
        hints_used=payload.hints_used,
        points_earned=points,
        time_taken_seconds=payload.time_taken_seconds,
    )
    db.add(result)

    # Update session totals & streak
    sess.total_points += points
    sess.quizzes_done += 1
    today = date.today()
    if sess.last_quiz_date is None:
        sess.streak = 1
    elif sess.last_quiz_date == today:
        pass  # same day — streak unchanged
    elif (today - sess.last_quiz_date).days == 1:
        sess.streak += 1
    else:
        sess.streak = 1
    sess.last_quiz_date = today

    # Upsert topic progress
    tp = db.execute(
        select(TopicProgress).where(
            TopicProgress.session_id == session_id,
            TopicProgress.subject == payload.subject,
            TopicProgress.topic == payload.topic,
        )
    ).scalar_one_or_none()

    if tp is None:
        tp = TopicProgress(
            session_id=session_id,
            subject=payload.subject,
            topic=payload.topic,
            attempts=1,
            best_score=payload.score,
            total_questions=payload.total_questions,
        )
        db.add(tp)
    else:
        tp.attempts += 1
        tp.best_score = max(tp.best_score, payload.score)
        tp.total_questions = payload.total_questions

    db.commit()
    db.refresh(result)

    return QuizResultOut(
        id=result.id,
        points_earned=points,
        new_total_points=sess.total_points,
        new_streak=sess.streak,
    )


@router.get("/{session_id}/progress", response_model=list[TopicProgressOut])
def get_progress(session_id: str, db: Session = Depends(get_db)):
    rows = db.execute(
        select(TopicProgress).where(TopicProgress.session_id == session_id)
    ).scalars().all()
    return rows
