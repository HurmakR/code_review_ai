from fastapi.testclient import TestClient
from app.main import app
from typing import Any

client: TestClient = TestClient(app)

def test_review_route() -> None:
    response: Any = client.post("/review")
    assert response.status_code == 200
    assert response.json() == {"message": "Code review started"}
