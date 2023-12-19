import pytest
from sqlalchemy import inspect, text

from database.utils.connection import RecipeDBAccess
from database.models import SCHEMA


def table_exists(test_db: RecipeDBAccess, table_name: str) -> bool:
    """Check if table exists in the database."""
    return inspect(test_db._engine).has_table(table_name=table_name, schema=SCHEMA)


def test_create_tables(test_db):
    test_db.create_tables()
    for table in [
        "recipes",
        "dishes",
        "dish_recipes",
        "people",
        "reviews",
        "people_reviews",
        "events",
        "event_dishes",
    ]:
        assert table_exists(test_db, table) is True


def test_drop_tables(test_db):
    test_db.drop_tables(force=True)
    for table in [
        "recipes",
        "dishes",
        "dish_recipes",
        "people",
        "reviews",
        "people_reviews",
        "events",
        "event_dishes",
    ]:
        assert table_exists(test_db, table) is False
