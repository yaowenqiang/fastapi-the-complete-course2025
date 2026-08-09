from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from ..database import Base

from fastapi.testclient import TestClient

from ..main import app
import pytest
from ..models import Todos, Users

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:123456@127.0.0.1:3306/TestTodoapplicationdatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False,poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {
        'username': 'string',
        'id': 1,
        'user_role': 'admin',
    }

client = TestClient(app)

@pytest.fixture
def test_todo():
    # 创建用户
    user = Users(
        id=1,
        email='test@example.com',
        username='testuser',
        first_name='Test',
        last_name='User',
        hashed_password='hashed_password',
        is_active=True,
        role='admin'
    )

    todo = Todos(
        title = 'learn to code',
        description ='learn to code',
        priority = 5,
        complete = False,
        owner_id = 1
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    yield db, todo

    with engine.connect() as conn:
        conn.execute(text('DELETE FROM TODOS'))
        conn.execute(text('DELETE FROM USERS'))
        conn.commit()

