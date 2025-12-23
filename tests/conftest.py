import os
import sys
import copy
import pytest

# Ensure the src directory is importable
SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from app import app, activities  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    """Snapshot and restore in-memory activities between tests."""
    original = {name: list(details["participants"]) for name, details in activities.items()}
    try:
        yield
    finally:
        for name, participants in original.items():
            activities[name]["participants"] = list(participants)