from datetime import timedelta, datetime, timezone

from dns.dnssecalgs import algorithms
from fastapi import APIRouter,Depends
from pydantic import BaseModel
from starlette import status

from models import Users
import bcrypt
import hashlib
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal

from fastapi.security import OAuth2PasswordRequestForm

from jose import jwt

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



# openssl rand -hex 32

SECRET_KEY = '1fb7c15bd4d63adebdc75c9927a93b3821633ebd7c23c1bd8afd9d3a24ac0145'

ALGORITHM = 'HS256'



class CreateUserRequest(BaseModel):

    email: str
    username : str
    first_name: str
    last_name: str
    password:str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expire_delta:timedelta):
    encode = {
        'sub': username,
        'id':user_id
    }
    expire = datetime.now(timezone.utc) + expire_delta
    encode.update({'exp':expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


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

@router.post('/token/', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return "Failed authentication"
    token = create_access_token(username=user.username, user_id=user.id, expire_delta=timedelta(minutes=24))

    return {
        'access_token': token,
        'token_type': 'bearer'
    }



