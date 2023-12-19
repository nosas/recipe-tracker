import pytest
from database.utils.connection import RecipeDBAccess


@pytest.fixture
def test_db() -> RecipeDBAccess:
    """Returns a test database connection"""
    db = RecipeDBAccess.get_instance(
        username="test_user",
        password="postgresql",
        prod_db=False,
    )
    db.create_tables()
    yield db
    db.drop_tables(force=True)
