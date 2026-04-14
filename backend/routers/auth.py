import uuid
import hashlib
import hmac
import os
import random
import secrets
import time
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import select
from pydantic import BaseModel, field_validator

from ..database import get_db
from ..models import User, UserToken, Session as StudentSession, TopicProgress, QuizResult

router = APIRouter(prefix="/api/auth", tags=["auth"])
bearer  = HTTPBearer(auto_error=False)

PBKDF2_ITERS = 260_000

# Captcha helpers — server-side math challenge, no external service needed
_CAPTCHA_SECRET = (os.environ.get("ADMIN_TOKEN", "changeme") + "_captcha_v1").encode()
CAPTCHA_TTL = 600  # 10 minutes


def _make_captcha_token(answer: int) -> str:
    """Return a signed token encoding the answer and a timestamp."""
    ts = str(int(time.time()))
    msg = f"{answer}:{ts}".encode()
    sig = hmac.new(_CAPTCHA_SECRET, msg, hashlib.sha256).hexdigest()
    return f"{sig}:{ts}"


def _verify_captcha_token(token: str, answer_str: str) -> bool:
    """Return True iff the token is valid, unexpired, and matches the answer."""
    try:
        sig, ts = token.rsplit(":", 1)
        if int(time.time()) - int(ts) > CAPTCHA_TTL:
            return False
        answer = int(answer_str)
        expected_msg = f"{answer}:{ts}".encode()
        expected_sig = hmac.new(_CAPTCHA_SECRET, expected_msg, hashlib.sha256).hexdigest()
        return hmac.compare_digest(sig, expected_sig)
    except Exception:
        return False


def hash_password(password: str) -> str:
    salt = secrets.token_hex(32)
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), PBKDF2_ITERS)
    return f"{salt}:{h.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        salt, hashed = stored.split(":", 1)
    except ValueError:
        return False
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), PBKDF2_ITERS)
    return secrets.compare_digest(h.hex(), hashed)


# ---- Pydantic schemas ----

class RegisterIn(BaseModel):
    username: str
    password: str
    display_name: str
    year_group: int = 3
    session_id: Optional[str] = None   # link anonymous session on register
    captcha_token: str = ""
    captcha_answer: str = ""

    @field_validator("username")
    @classmethod
    def clean_username(cls, v: str) -> str:
        v = v.strip().lower()
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Username may only contain letters, numbers, hyphens and underscores")
        return v

    @field_validator("password")
    @classmethod
    def check_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v

    @field_validator("year_group")
    @classmethod
    def check_year(cls, v: int) -> int:
        if v not in range(1, 14):
            raise ValueError("Year group must be between 1 and 13")
        return v


class LoginIn(BaseModel):
    username: str
    password: str
    session_id: Optional[str] = None   # link anonymous session to this user


class UserOut(BaseModel):
    id: int
    username: str
    display_name: str
    year_group: int
    active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    token: str
    user: UserOut
    session_id: str   # the canonical session to use for progress/stats


# ---- Dependency: get current user from Bearer token ----

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: DBSession = Depends(get_db),
) -> User:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    row = db.execute(
        select(UserToken).where(UserToken.token == credentials.credentials)
    ).scalar_one_or_none()
    if row is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    if not row.user.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account disabled")
    return row.user


def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: DBSession = Depends(get_db),
) -> Optional[User]:
    """Returns None if unauthenticated (guest mode)."""
    if credentials is None:
        return None
    row = db.execute(
        select(UserToken).where(UserToken.token == credentials.credentials)
    ).scalar_one_or_none()
    return row.user if row and row.user.active else None


# ---- Session helpers ----

def _resolve_user_session(user_id: int, anon_session_id: Optional[str], db: DBSession) -> str:
    """
    Return the canonical session_id for a user:
    1. Link and use the anonymous session if it exists and is unclaimed.
    2. Otherwise use their existing session (highest total_points wins).
    3. Create a fresh one if they have none.
    """
    if anon_session_id:
        sess = db.get(StudentSession, anon_session_id)
        if sess and sess.user_id is None:
            sess.user_id = user_id
            db.flush()
            return anon_session_id

    existing = db.execute(
        select(StudentSession)
        .where(StudentSession.user_id == user_id)
        .order_by(StudentSession.total_points.desc())
        .limit(1)
    ).scalar_one_or_none()
    if existing:
        return existing.id

    new_id = str(uuid.uuid4())
    db.add(StudentSession(id=new_id, user_id=user_id))
    db.flush()
    return new_id


# ---- Routes ----

@router.get("/captcha")
def get_captcha():
    """Return a fresh math CAPTCHA challenge."""
    a = random.randint(2, 12)
    b = random.randint(2, 12)
    answer = a + b
    return {
        "question": f"What is {a} + {b}?",
        "token": _make_captcha_token(answer),
    }


@router.post("/register", response_model=AuthResponse, status_code=201)
def register(payload: RegisterIn, db: DBSession = Depends(get_db)):
    # Verify CAPTCHA before anything else
    if not _verify_captcha_token(payload.captcha_token, payload.captcha_answer):
        raise HTTPException(status_code=400, detail="Incorrect CAPTCHA answer — please try again")

    existing = db.execute(select(User).where(User.username == payload.username)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="Username already taken")

    user = User(
        username=payload.username,
        display_name=payload.display_name,
        year_group=payload.year_group,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.flush()   # get user.id before commit

    token_value = str(uuid.uuid4())
    db.add(UserToken(token=token_value, user_id=user.id))

    session_id = _resolve_user_session(user.id, payload.session_id, db)
    db.commit()
    db.refresh(user)

    return AuthResponse(token=token_value, user=UserOut.model_validate(user), session_id=session_id)


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginIn, db: DBSession = Depends(get_db)):
    user = db.execute(
        select(User).where(User.username == payload.username.strip().lower())
    ).scalar_one_or_none()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not user.active:
        raise HTTPException(status_code=403, detail="Account has been disabled")

    # Issue a new token
    token_value = str(uuid.uuid4())
    db.add(UserToken(token=token_value, user_id=user.id))

    session_id = _resolve_user_session(user.id, payload.session_id, db)

    user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(user)

    return AuthResponse(token=token_value, user=UserOut.model_validate(user), session_id=session_id)


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return UserOut.model_validate(current_user)


@router.post("/logout", status_code=204)
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: DBSession = Depends(get_db),
):
    if credentials:
        db.execute(
            select(UserToken).where(UserToken.token == credentials.credentials)
        )
        row = db.execute(
            select(UserToken).where(UserToken.token == credentials.credentials)
        ).scalar_one_or_none()
        if row:
            db.delete(row)
            db.commit()


@router.put("/me", response_model=UserOut)
def update_profile(
    payload: dict,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    allowed = {"display_name", "year_group"}
    for k, v in payload.items():
        if k in allowed:
            setattr(current_user, k, v)
    db.commit()
    db.refresh(current_user)
    return UserOut.model_validate(current_user)


@router.post("/change-password", status_code=204)
def change_password(
    payload: dict,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    old_pw = payload.get("old_password", "")
    new_pw = payload.get("new_password", "")
    if not verify_password(old_pw, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    if len(new_pw) < 6:
        raise HTTPException(status_code=400, detail="New password must be at least 6 characters")
    current_user.password_hash = hash_password(new_pw)
    db.commit()
