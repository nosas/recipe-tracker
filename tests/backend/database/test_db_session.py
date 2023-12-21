from sqlalchemy import text
from sqlalchemy.orm.session import Session

from database.utils.connection import RecipeDBAccess


def test_get_session(test_db: RecipeDBAccess):
    """Verify that a session is returned and can be used"""
    assert isinstance(test_db.get_session(), Session)
    session = test_db.get_session()
    # Verify a query can be executed
    session.execute(text("SELECT 1"))


def test_get_session_context_manager(test_db):
    """Verify that a session is returned when used as a context manager"""
    with test_db.get_session() as session:
        assert isinstance(session, Session)
        # Verify a query can be executed
        session.execute(text("SELECT 1"))
