from fastapi.testclient import TestClient

from inspilot_cloud_baby.main import create_app


def test_health_returns_ok() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_app_uses_lifespan_instead_of_deprecated_startup_handlers() -> None:
    app = create_app()

    assert app.router.on_startup == []
    assert app.router.lifespan_context is not None
