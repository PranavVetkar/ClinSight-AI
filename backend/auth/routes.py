import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status

from auth.models import UserCreate, UserLogin, Token
from auth.utils import hash_password, verify_password, create_access_token
from db.local_db import get_user_by_email, create_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate):
    if get_user_by_email(payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    uid = str(uuid.uuid4())
    user_doc = {
        "uid": uid,
        "name": payload.name,
        "email": payload.email,
        "password_hash": hash_password(payload.password),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    create_user(user_doc)

    token = create_access_token({"uid": uid, "email": payload.email})
    return Token(access_token=token)


@router.post("/login", response_model=Token)
async def login(payload: UserLogin):
    user = get_user_by_email(payload.email)
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"uid": user["uid"], "email": user["email"]})
    return Token(access_token=token)
