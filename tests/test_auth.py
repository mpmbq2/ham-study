from lib.auth import get_username


def test_returns_posit_connect_username(monkeypatch):
    monkeypatch.setenv("HTTP_X_RSTUDIO_CONNECT_USER_NAME", "jsmith")
    assert get_username() == "jsmith"


def test_lowercases_username(monkeypatch):
    monkeypatch.setenv("HTTP_X_RSTUDIO_CONNECT_USER_NAME", "JSmith")
    assert get_username() == "jsmith"


def test_falls_back_to_local(monkeypatch):
    monkeypatch.delenv("HTTP_X_RSTUDIO_CONNECT_USER_NAME", raising=False)
    assert get_username() == "local"
