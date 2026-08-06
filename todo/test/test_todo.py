from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from ..database import Base
from ..main import app
from ..routers.todos import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status

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

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

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


def test_read_all_authenticated(test_todo):
    _, todo = test_todo
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'complete' : False,
        'description' :'learn to code',
        'priority' : 5,
        'title' : 'learn to code',
        'id': todo.id,
        'owner_id' : 1
    }]

def test_read_one_authenticated(test_todo):
    _, todo = test_todo
    response = client.get(f'/todo/{todo.id}')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'complete' : False,
        'description' :'learn to code',
        'priority' : 5,
        'title' : 'learn to code',
        'id': todo.id,
        'owner_id' : 1
    }

