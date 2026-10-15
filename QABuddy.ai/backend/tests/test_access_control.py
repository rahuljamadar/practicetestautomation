from fastapi.testclient import TestClient

from backend.main import app


def test_health_endpoint_is_public():
    response = TestClient(app).get("/api/health")

    assert response.status_code == 200


def test_password_verification_route_is_removed():
    response = TestClient(app).post(
        "/api/auth/verify",
        json={"password": "unused"},
    )

    assert response.status_code == 405