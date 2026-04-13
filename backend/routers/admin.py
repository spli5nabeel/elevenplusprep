from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, select, case
from typing import List, Optional
from pydantic import BaseModel

from ..database import get_db
from ..models import Question, Session as StudentSession, QuizResult, User, TopicProgress
from ..schemas import QuestionCreate, QuestionUpdate, QuestionOut, AdminStats, TopicStats
from ..auth import require_admin
from ..routers.auth import hash_password

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/stats", response_model=AdminStats)
def admin_stats(db: Session = Depends(get_db), _=Depends(require_admin)):
    total_q = db.query(func.count(Question.id)).scalar()
    active_q = db.query(func.count(Question.id)).filter(Question.active == True).scalar()
    total_sessions = db.query(func.count(StudentSession.id)).scalar()
    total_quizzes = db.query(func.count(QuizResult.id)).scalar()

    rows = db.execute(
        select(Question.subject, Question.topic,
               func.count(Question.id).label("total"),
               func.sum(case((Question.active == True, 1), else_=0)).label("active"))
        .group_by(Question.subject, Question.topic)
        .order_by(Question.subject, Question.topic)
    ).all()

    by_topic = [
        TopicStats(subject=r.subject, topic=r.topic, total=r.total, active=r.active or 0)
        for r in rows
    ]

    return AdminStats(
        total_questions=total_q or 0,
        active_questions=active_q or 0,
        total_sessions=total_sessions or 0,
        total_quizzes=total_quizzes or 0,
        by_topic=by_topic,
    )


@router.get("/questions", response_model=List[QuestionOut])
def list_questions(
    subject: Optional[str] = None,
    topic: Optional[str] = None,
    active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 200,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    q = db.query(Question)
    if subject:
        q = q.filter(Question.subject == subject)
    if topic:
        q = q.filter(Question.topic == topic)
    if active is not None:
        q = q.filter(Question.active == active)
    return q.order_by(Question.subject, Question.topic, Question.id).offset(skip).limit(limit).all()


@router.get("/questions/{question_id}", response_model=QuestionOut)
def get_question(question_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    q = db.get(Question, question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q


@router.post("/questions", response_model=QuestionOut, status_code=201)
def create_question(payload: QuestionCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    q = Question(**payload.model_dump())
    db.add(q)
    db.commit()
    db.refresh(q)
    return q


@router.put("/questions/{question_id}", response_model=QuestionOut)
def update_question(question_id: int, payload: QuestionUpdate, db: Session = Depends(get_db), _=Depends(require_admin)):
    q = db.get(Question, question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(q, field, value)
    db.commit()
    db.refresh(q)
    return q


@router.delete("/questions/{question_id}", status_code=204)
def delete_question(question_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    q = db.get(Question, question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    q.active = False
    db.commit()


@router.patch("/questions/{question_id}/restore", response_model=QuestionOut)
def restore_question(question_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    q = db.get(Question, question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    q.active = True
    db.commit()
    db.refresh(q)
    return q


@router.post("/questions/bulk", status_code=201)
def bulk_import(questions: List[QuestionCreate], db: Session = Depends(get_db), _=Depends(require_admin)):
    created, errors = 0, []
    for i, payload in enumerate(questions):
        try:
            q = Question(**payload.model_dump())
            db.add(q)
            created += 1
        except Exception as e:
            errors.append({"row": i, "error": str(e)})
    db.commit()
    return {"created": created, "errors": errors}


# ============================================================
#  User Management
# ============================================================

class UserAdminOut(BaseModel):
    id: int
    username: str
    display_name: str
    year_group: int
    active: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    total_points: int = 0
    quizzes_done: int = 0
    session_count: int = 0

    model_config = {"from_attributes": True}


class UserAdminUpdate(BaseModel):
    display_name: Optional[str] = None
    year_group: Optional[int] = None
    active: Optional[bool] = None
    new_password: Optional[str] = None


@router.get("/users", response_model=List[UserAdminOut])
def list_users(
    active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 200,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    q = db.query(User)
    if active is not None:
        q = q.filter(User.active == active)
    users = q.order_by(User.created_at.desc()).offset(skip).limit(limit).all()

    result = []
    for u in users:
        # Aggregate stats across all sessions for this user
        stats = db.execute(
            select(
                func.sum(StudentSession.total_points).label("pts"),
                func.sum(StudentSession.quizzes_done).label("qz"),
                func.count(StudentSession.id).label("sessions"),
            ).where(StudentSession.user_id == u.id)
        ).one()
        result.append(UserAdminOut(
            id=u.id,
            username=u.username,
            display_name=u.display_name,
            year_group=u.year_group,
            active=u.active,
            created_at=u.created_at,
            last_login=u.last_login,
            total_points=int(stats.pts or 0),
            quizzes_done=int(stats.qz or 0),
            session_count=int(stats.sessions or 0),
        ))
    return result


@router.get("/users/{user_id}", response_model=UserAdminOut)
def get_user(user_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    u = db.get(User, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    stats = db.execute(
        select(
            func.sum(StudentSession.total_points).label("pts"),
            func.sum(StudentSession.quizzes_done).label("qz"),
            func.count(StudentSession.id).label("sessions"),
        ).where(StudentSession.user_id == u.id)
    ).one()
    return UserAdminOut(
        id=u.id, username=u.username, display_name=u.display_name,
        year_group=u.year_group, active=u.active,
        created_at=u.created_at, last_login=u.last_login,
        total_points=int(stats.pts or 0),
        quizzes_done=int(stats.qz or 0),
        session_count=int(stats.sessions or 0),
    )


@router.get("/users/{user_id}/progress")
def get_user_progress(user_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    """Aggregate topic progress across all sessions for a user."""
    u = db.get(User, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")

    rows = db.execute(
        select(
            TopicProgress.subject,
            TopicProgress.topic,
            func.sum(TopicProgress.attempts).label("attempts"),
            func.max(TopicProgress.best_score).label("best_score"),
            func.max(TopicProgress.total_questions).label("total_questions"),
        )
        .join(StudentSession, StudentSession.id == TopicProgress.session_id)
        .where(StudentSession.user_id == user_id)
        .group_by(TopicProgress.subject, TopicProgress.topic)
    ).all()

    return [
        {
            "subject": r.subject, "topic": r.topic,
            "attempts": r.attempts or 0,
            "best_score": r.best_score or 0,
            "total_questions": r.total_questions or 0,
        }
        for r in rows
    ]


@router.get("/users/{user_id}/results")
def get_user_results(user_id: int, limit: int = 50, db: Session = Depends(get_db), _=Depends(require_admin)):
    """Recent quiz results for a user."""
    rows = db.execute(
        select(QuizResult)
        .join(StudentSession, StudentSession.id == QuizResult.session_id)
        .where(StudentSession.user_id == user_id)
        .order_by(QuizResult.completed_at.desc())
        .limit(limit)
    ).scalars().all()
    return [
        {
            "id": r.id, "subject": r.subject, "topic": r.topic,
            "score": r.score, "total_questions": r.total_questions,
            "points_earned": r.points_earned,
            "time_taken_seconds": r.time_taken_seconds,
            "completed_at": r.completed_at.isoformat(),
        }
        for r in rows
    ]


@router.put("/users/{user_id}", response_model=UserAdminOut)
def update_user(user_id: int, payload: UserAdminUpdate, db: Session = Depends(get_db), _=Depends(require_admin)):
    u = db.get(User, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    if payload.display_name is not None:
        u.display_name = payload.display_name
    if payload.year_group is not None:
        u.year_group = payload.year_group
    if payload.active is not None:
        u.active = payload.active
    if payload.new_password:
        if len(payload.new_password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
        u.password_hash = hash_password(payload.new_password)
    db.commit()
    db.refresh(u)
    stats = db.execute(
        select(
            func.sum(StudentSession.total_points).label("pts"),
            func.sum(StudentSession.quizzes_done).label("qz"),
            func.count(StudentSession.id).label("sessions"),
        ).where(StudentSession.user_id == u.id)
    ).one()
    return UserAdminOut(
        id=u.id, username=u.username, display_name=u.display_name,
        year_group=u.year_group, active=u.active,
        created_at=u.created_at, last_login=u.last_login,
        total_points=int(stats.pts or 0),
        quizzes_done=int(stats.qz or 0),
        session_count=int(stats.sessions or 0),
    )


@router.delete("/users/{user_id}", status_code=204)
def deactivate_user(user_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    u = db.get(User, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    u.active = False
    db.commit()


@router.patch("/users/{user_id}/restore", response_model=UserAdminOut)
def restore_user(user_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    u = db.get(User, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    u.active = True
    db.commit()
    db.refresh(u)
    stats = db.execute(
        select(
            func.sum(StudentSession.total_points).label("pts"),
            func.sum(StudentSession.quizzes_done).label("qz"),
            func.count(StudentSession.id).label("sessions"),
        ).where(StudentSession.user_id == u.id)
    ).one()
    return UserAdminOut(
        id=u.id, username=u.username, display_name=u.display_name,
        year_group=u.year_group, active=u.active,
        created_at=u.created_at, last_login=u.last_login,
        total_points=int(stats.pts or 0),
        quizzes_done=int(stats.qz or 0),
        session_count=int(stats.sessions or 0),
    )
