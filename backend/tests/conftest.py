import os
import sys
import pytest

# Ensure backend root is in sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.core.database import init_db


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    init_db()

