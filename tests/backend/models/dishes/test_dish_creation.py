import pytest
from sqlalchemy.exc import IntegrityError

from database.schema.models import Dish


def validate_dish(dish: Dish, name: str, id: int):
    """Validates the dish"""
    assert dish.name == name
    assert dish.created_at is not None
    assert dish.id == id


def test_create_dish(test_db):
    """Verify that a dish can be created"""
    dish = Dish(name="test_dish")
    test_db.insert_one(dish)
    with test_db.get_session() as session:
        result = session.query(Dish).filter(Dish.name == "test_dish").one_or_none()
        assert result is not None
    validate_dish(dish=result, name="test_dish", id=1)


def test_create_dish_with_custom_id(test_db):
    """Verify that a dish cannot be created with a custom id"""
    dish = Dish(id=10, name="test_dish")
    test_db.insert_one(dish)
    with test_db.get_session() as session:
        result = session.query(Dish).filter(Dish.name == "test_dish").one_or_none()
        assert result is not None
    validate_dish(dish=result, name="test_dish", id=1)


def test_create_dishes(test_db):
    """Verify that multiple dishes can be created"""
    dishes = [Dish(name="test_dish"), Dish(name="test_dish_2")]
    test_db.insert_many(dishes)
    with test_db.get_session() as session:
        result = session.query(Dish).all()
        assert len(result) == 2
    validate_dish(dish=result[0], name="test_dish", id=1)
    validate_dish(dish=result[1], name="test_dish_2", id=2)


def test_create_dishes_with_custom_ids(test_db):
    """Verify that multiple dishes and their ids are not affected by custom ids"""
    dishes = [
        Dish(id=2, name="test_dish"),
        Dish(name="test_dish_2"),
        Dish(id=1, name="test_dish_3"),
    ]
    test_db.insert_many(dishes)
    with test_db.get_session() as session:
        result = session.query(Dish).all()
        assert len(result) == 3
    validate_dish(dish=result[0], name="test_dish", id=1)
    validate_dish(dish=result[1], name="test_dish_2", id=2)
    validate_dish(dish=result[2], name="test_dish_3", id=3)


def test_update_dish(test_db):
    """Verify that a dish can be updated with upsert"""
    dish = Dish(name="test_dish")
    test_db.insert_one(dish)

    with test_db.get_session() as session:
        result = session.query(Dish).filter(Dish.id == 1).one_or_none()
        assert result is not None
    validate_dish(dish=result, name="test_dish", id=1)

    dish.name = "test_dish_2"
    updated_dish = test_db.upsert(dish)
    validate_dish(dish=updated_dish, name="test_dish_2", id=1)

    with test_db.get_session() as session:
        result = session.query(Dish).filter(Dish.id == 1).one_or_none()
        assert result is not None
    validate_dish(dish=result, name=updated_dish.name, id=1)


def test_upsert_dish(test_db):
    """Verify that a dish can be inserted with upsert, and then updated with upsert"""
    dish = Dish(name="test_dish")
    dish = test_db.upsert(dish)
    validate_dish(dish=dish, name="test_dish", id=1)

    with test_db.get_session() as session:
        result = session.query(Dish).filter(Dish.id == 1).one_or_none()
        assert result is not None
    validate_dish(dish=result, name="test_dish", id=1)

    dish.name = "test_dish_2"
    updated_dish = test_db.upsert(dish)
    validate_dish(dish=updated_dish, name="test_dish_2", id=1)

    with test_db.get_session() as session:
        result2 = session.query(Dish).filter(Dish.id == 1).one_or_none()
        assert result2 is not None
        # Verify there is no new dish created
        empty_result = session.query(Dish).filter(Dish.id == 2).one_or_none()
        assert empty_result is None
    validate_dish(dish=result2, name="test_dish_2", id=1)


def test_update_dish_with_existing_id(test_db):
    """Verify that a dish cannot be updated to violate a unique constraint"""
    _dishes = [Dish(name="test_dish"), Dish(name="test_dish_2")]
    dishes = [test_db.upsert(dish) for dish in _dishes]

    # Update dish 1 with dish 2's id
    dishes[0].id = 2
    with pytest.raises(IntegrityError):
        test_db.upsert(dishes[0])
