"""_summary_

https://docs.pytest.org/en/stable/how-to/monkeypatch.html
"""

import functools
import os
from pathlib import Path
import pytest
import requests


def getssh():
    return Path.home().joinpath(".ssh")


def test_getssh(monkeypatch):
    def mockreturn():
        return Path("/abc")

    monkeypatch.setattr(Path, "home", mockreturn)
    x = getssh()
    assert x == Path("/abc/.ssh")


# Monkeypatching returned objects: building mock classes
# App.py
def get_json(url):
    r = requests.get(url)
    return r.json()


# Mock
class MockResponse:
    @staticmethod
    def json():
        return {"mock_key": "mock_response"}


def test_get_json(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    result = get_json("https://www.example.com")
    assert result["mock_key"] == "mock_response"


# move the monkeypatched requests.get moved to a fixture
@pytest.fixture
def mock_response(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)


def test_get_json2(mock_response):
    result = get_json("https://www.example.com")
    assert result["mock_key"] == "mock_response"


"""避免标准库等受影响，可以使用`MonkeyPatch.context()来限制测试`
Global patch example: preventing “requests” from remote operations
"""


def test_partial(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(functools, "partial", 3)
        assert functools.partial == 3


# Monkeypatching environment variables


def get_os_user_lower():
    username = os.getenv("USER")
    if username is None:
        raise OSError("USER environment variable not set")
    return username.lower()


def test_os_user_lower(monkeypatch):
    monkeypatch.setenv("USER", "TestingUser")
    assert get_os_user_lower() == "testinguser"


def test_os_user_lower_raises(monkeypatch):
    monkeypatch.delenv("USER", raising=False)
    with pytest.raises(OSError):
        _ = get_os_user_lower()


# Monkeypatching dictionaries

# contents of app.py to generate a simple connection string
DEFAULT_CONFIG = {"user": "user1", "database": "db1", "type": "postgresql"}


def create_connection_string(config=None):
    config = config or DEFAULT_CONFIG
    return f"{config['type']}://{config['user']}@localhost/{config['database']}"


def test_create_connection_string(monkeypatch):
    monkeypatch.setitem(DEFAULT_CONFIG, "type", "db2")
    monkeypatch.setitem(DEFAULT_CONFIG, "user", "user2")

    expected = "db2://user2@localhost/db1"
    result = create_connection_string()
    assert result == expected


def test_connection_string_missing_user(monkeypatch):
    monkeypatch.delitem(DEFAULT_CONFIG, "user", raising=False)
    with pytest.raises(KeyError):
        create_connection_string()
