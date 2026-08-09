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
