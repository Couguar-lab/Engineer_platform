import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_firebase(monkeypatch):
    """
    Автоматически мокает всю инициализацию Firebase во всех тестах.
    """
    monkeypatch.setattr('firebase_admin._apps', [])
    monkeypatch.setattr('firebase_admin.initialize_app', lambda *args, **kwargs: None)
    monkeypatch.setattr('firebase_admin.auth', lambda: None)