import os
import tempfile
import pytest


@pytest.fixture
def client(monkeypatch):
    # Use a temporary TinyDB path
    db_fd, db_path = tempfile.mkstemp()
    monkeypatch.setenv("TINYDB_PATH", db_path)

    cwd = os.getcwd()
    app_dir = os.path.join(cwd, "application")
    os.chdir(app_dir)
    try:
        import sys
        if cwd not in sys.path:
            sys.path.insert(0, cwd)
        import types
        yaml_stub = types.SimpleNamespace(
            safe_load=lambda _: {"flask": {"host": "127.0.0.1", "port": 5000, "debug": False}}
        )
        monkeypatch.setitem(sys.modules, "yaml", yaml_stub)

        from application.main import app
        app.config.update({"TESTING": True})
        with app.test_client() as client:
            yield client
    finally:
        os.chdir(cwd)
        os.close(db_fd)
        os.unlink(db_path)


def test_queries_get(client):
    response = client.get("/queries")
    assert response.status_code == 200


def test_execute_requires_url(client):
    response = client.post("/execute", json={})
    assert response.status_code == 400
