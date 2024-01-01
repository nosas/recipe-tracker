from typing import Any, Generator

import pytest

from database.utils.connection import RecipeDBAccess


@pytest.fixture
def test_db() -> Generator[RecipeDBAccess, Any, Any]:
    """Returns a test database connection"""
    db = RecipeDBAccess.from_env()
    assert not db._credentials.is_production, "Test database not being used"

    db.create_tables()
    yield db
    db.drop_tables(force=True)
