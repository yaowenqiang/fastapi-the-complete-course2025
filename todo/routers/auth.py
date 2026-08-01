from fastapi import APIRouter,Depends
from pydantic import BaseModel
from starlette import status

from models import Users
import bcrypt
import hashlib
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal

def hash_password(password: str) -> str:
    """Hash password with SHA-256 first to handle >72 byte passwords, then bcrypt"""
    # Pre-hash with SHA-256 to handle long passwords (hexdigest = 64 chars, under 72 limit)
    sha256_hash = hashlib.sha256(password.encode('utf-8')).hexdigest().encode('utf-8')
    # Then bcrypt hash the result
    return bcrypt.hashpw(sha256_hash, bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password - pre-hash plain password to match the stored hash"""
    # Pre-hash with SHA-256 to match the hashing process
    sha256_hash = hashlib.sha256(plain_password.encode('utf-8')).hexdigest().encode('utf-8')
    # Then verify with bcrypt
    return bcrypt.checkpw(sha256_hash, hashed_password.encode('utf-8'))

router = APIRouter()

class CreateUserRequest(BaseModel):

    email: str
    username : str
    first_name: str
    last_name: str
    password:str
    role: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post('/auth/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email = create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role = create_user_request.role,
        hashed_password = hash_password(create_user_request.password),
        is_active = True
    )
    db.add(create_user_model)
    db.commit()

@router.get('/auth/')
async def get_user():
    return {'user': 'authenticated'}
