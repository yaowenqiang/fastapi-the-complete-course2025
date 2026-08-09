from starlette import status

from .utils import *
from ..routers import admin
from ..routers.auth import get_current_user

app.dependency_overrides[admin.get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_todo):
    _, todo = test_todo
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            'id' : todo.id,
            'title' : 'learn to code',
            'description' : 'learn to code',
            'priority' : 5,
            'complete' : False,
            'owner_id' : 1
        }
    ]

def test_admin_delete_todo(test_todo):
    _, todo = test_todo
    response = client.delete(f'/admin/todo/{todo.id}')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == todo.id).first()
    assert model is None

def test_admin_delete_todo_not_found():
    response = client.delete('/admin/todo/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND

