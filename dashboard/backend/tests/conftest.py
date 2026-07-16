import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app


@pytest.fixture()
def client():
    app = create_app("testing")
    with app.test_client() as c:
        yield c
