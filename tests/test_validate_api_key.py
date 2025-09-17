import sys
import types
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import main


class DummyResponse:
    def __init__(self, status_code, text=""):
        self.status_code = status_code
        self.text = text


def _patch_async_client(monkeypatch, response):
    captured = {}

    class DummyAsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, url, headers=None):
            captured["url"] = url
            captured["headers"] = headers
            return response

    monkeypatch.setattr(main.httpx, "AsyncClient", lambda *args, **kwargs: DummyAsyncClient())
    return captured


def _create_session_with_user():
    user = types.SimpleNamespace(is_valid=None)
    session = MagicMock()
    query = session.query.return_value
    filtered = query.filter.return_value
    filtered.first.return_value = user
    return session, user


def test_validate_api_key_success(monkeypatch):
    response = DummyResponse(200, "ok")
    captured = _patch_async_client(monkeypatch, response)
    session, user = _create_session_with_user()

    is_valid, error_message = main.validate_api_key("secret", 123, session)

    assert is_valid is True
    assert error_message is None
    assert user.is_valid is True
    session.commit.assert_called_once()
    assert captured["url"] == main.API_VALIDATE_URL
    assert captured["headers"]["Authorization"] == "Bearer secret"


def test_validate_api_key_unauthorized(monkeypatch):
    response = DummyResponse(401, "unauthorized")
    _patch_async_client(monkeypatch, response)
    session, user = _create_session_with_user()

    is_valid, error_message = main.validate_api_key("bad", 123, session)

    assert is_valid is False
    assert "недействителен" in error_message
    assert user.is_valid is False
    session.commit.assert_called_once()


def test_validate_api_key_server_error(monkeypatch):
    response = DummyResponse(500, "server error")
    _patch_async_client(monkeypatch, response)
    session, user = _create_session_with_user()

    is_valid, error_message = main.validate_api_key("test", 123, session)

    assert is_valid is False
    assert "500" in error_message
    assert user.is_valid is False
    session.commit.assert_called_once()


def test_validate_api_key_http_error(monkeypatch):
    def raise_http_error(*args, **kwargs):
        raise main.httpx.HTTPError("network error")

    class DummyAsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, url, headers=None):
            return raise_http_error()

    monkeypatch.setattr(main.httpx, "AsyncClient", lambda *args, **kwargs: DummyAsyncClient())
    session, user = _create_session_with_user()

    is_valid, error_message = main.validate_api_key("test", 123, session)

    assert is_valid is False
    assert "Не удалось проверить API ключ" in error_message
    assert user.is_valid is False
    session.commit.assert_called_once()
