import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from ..database import get_db
from ..models import Question
from ..schemas import QuestionPublic

router = APIRouter(prefix="/api/questions", tags=["questions"])

# Subject + topic metadata (drives the frontend cards)
SUBJECT_META = {
    "english":   {"name": "English",              "icon": "📖", "badge": "Year 3-6"},
    "maths":     {"name": "Mathematics",          "icon": "🔢", "badge": "Year 3-6"},
    "verbal":    {"name": "Verbal Reasoning",     "icon": "💡", "badge": "11+ Key"},
    "nonverbal": {"name": "Non-Verbal Reasoning", "icon": "🎯", "badge": "11+ Key"},
}

TOPIC_META = {
    "english": [
        {"id": "comprehension", "name": "Reading Comprehension", "icon": "📖", "desc": "Read passages and answer questions"},
        {"id": "spelling",      "name": "Spelling",              "icon": "✏️",  "desc": "Spell common and tricky words"},
        {"id": "grammar",       "name": "Grammar & Punctuation", "icon": "📝", "desc": "Commas, apostrophes and more"},
        {"id": "vocabulary",    "name": "Vocabulary",            "icon": "💬", "desc": "Word meanings and synonyms"},
    ],
    "maths": [
        {"id": "arithmetic",   "name": "Arithmetic",           "icon": "🔢", "desc": "Addition, subtraction, multiplication, division"},
        {"id": "fractions",    "name": "Fractions & Decimals", "icon": "½",  "desc": "Fractions, decimals and percentages"},
        {"id": "wordproblems", "name": "Word Problems",        "icon": "🧩", "desc": "Real-life maths challenges"},
        {"id": "shapes",       "name": "Shapes & Geometry",    "icon": "📐", "desc": "2D shapes, area and perimeter"},
    ],
    "verbal": [
        {"id": "analogies",    "name": "Analogies",         "icon": "🔗", "desc": "Find relationships between words"},
        {"id": "sequences",    "name": "Number Sequences",  "icon": "🔄", "desc": "Spot number and letter patterns"},
        {"id": "wordpatterns", "name": "Word Patterns",     "icon": "🔤", "desc": "Odd ones out, hidden words"},
        {"id": "codebreaking", "name": "Code Breaking",     "icon": "🔐", "desc": "Crack the letter and number codes"},
    ],
    "nonverbal": [
        {"id": "patterns",  "name": "Shape Patterns",  "icon": "🔷", "desc": "Spot visual patterns and sequences"},
        {"id": "matrices",  "name": "Matrices",        "icon": "⊞",  "desc": "Complete the grid patterns"},
        {"id": "spatial",   "name": "Spatial Reasoning","icon": "🧊", "desc": "3D shapes, nets and rotation"},
    ],
}


@router.get("/subjects")
def get_subjects(db: Session = Depends(get_db)):
    """Return all subjects, topics and live question counts."""
    result = []
    for subject, meta in SUBJECT_META.items():
        topics = []
        for t in TOPIC_META.get(subject, []):
            count = db.query(func.count(Question.id)).filter(
                Question.subject == subject,
                Question.topic == t["id"],
                Question.active == True,
            ).scalar()
            topics.append({**t, "question_count": count})
        result.append({**meta, "id": subject, "topics": topics})
    return result


@router.get("/{subject}/{topic}", response_model=List[QuestionPublic])
def get_questions(subject: str, topic: str, limit: int = 0, db: Session = Depends(get_db)):
    """Return shuffled active questions for a topic. limit=0 means all."""
    qs = db.query(Question).filter(
        Question.subject == subject,
        Question.topic == topic,
        Question.active == True,
    ).all()
    if not qs:
        raise HTTPException(status_code=404, detail="No questions found for this topic")
    random.shuffle(qs)
    return qs[:limit] if limit > 0 else qs


@router.get("/mock-exam")
def get_mock_exam(questions_per_subject: int = 10, db: Session = Depends(get_db)):
    """
    Return a structured mock exam: N random questions per subject, grouped by subject/topic.
    Response: list of sections [ { subject, subject_name, icon, questions: [...] } ]
    """
    sections = []
    for subject, meta in SUBJECT_META.items():
        all_qs = db.query(Question).filter(
            Question.subject == subject,
            Question.active == True,
        ).all()
        random.shuffle(all_qs)
        selected = all_qs[:questions_per_subject]
        if selected:
            sections.append({
                "subject":      subject,
                "subject_name": meta["name"],
                "icon":         meta["icon"],
                "questions":    [
                    {
                        "id":       q.id,
                        "subject":  q.subject,
                        "topic":    q.topic,
                        "question": q.question,
                        "options":  q.options,
                        "passage":  q.passage,
                    }
                    for q in selected
                ],
            })
    return sections


@router.get("/{subject}/{topic}/{question_id}/answer")
def check_answer(subject: str, topic: str, question_id: int, selected: int, db: Session = Depends(get_db)):
    """Verify a single answer. Returns correct flag + explanation."""
    q = db.query(Question).filter(
        Question.id == question_id,
        Question.subject == subject,
        Question.topic == topic,
        Question.active == True,
    ).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return {
        "correct": selected == q.answer,
        "correct_answer": q.answer,
        "explanation": q.explanation,
    }
