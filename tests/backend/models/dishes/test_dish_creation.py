from database.schema.models import Dish
from database.utils.connection import RecipeDBAccess


def test_create_dish(test_db: RecipeDBAccess):
    """Verify that a dish can be created"""
    dish = Dish(name="test_dish")
    test_db.insert_one(dish)
    with test_db.get_session() as session:
        result = session.query(Dish).filter(Dish.name == "test_dish").one_or_none()
        assert result is not None
    assert result.name == "test_dish"
    assert result.created_at is not None
    assert result.id == 1


def test_create_dish_with_custom_id(test_db: RecipeDBAccess):
    """Verify that a dish cannot be created with a custom id"""
    dish = Dish(id=10, name="test_dish")
    test_db.insert_one(dish)
    with test_db.get_session() as session:
        result = session.query(Dish).filter(Dish.name == "test_dish").first()
        assert result is not None
    assert result.name == "test_dish"
    assert result.created_at is not None
    assert result.id == 1


def test_create_dishes(test_db: RecipeDBAccess):
    """Verify that multiple dishes can be created"""
    dishes = [Dish(name="test_dish"), Dish(name="test_dish_2")]
    test_db.insert_many(dishes)
    with test_db.get_session() as session:
        result = session.query(Dish).all()
        assert len(result) == 2
    assert result[0].name == "test_dish"
    assert result[1].name == "test_dish_2"
    assert result[0].created_at is not None
    assert result[1].created_at is not None
    assert result[0].id == 1
    assert result[1].id == 2


def test_create_dishes_with_custom_ids(test_db: RecipeDBAccess):
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
    assert result[0].name == "test_dish"
    assert result[1].name == "test_dish_2"
    assert result[2].name == "test_dish_3"
    assert result[0].created_at is not None
    assert result[1].created_at is not None
    assert result[2].created_at is not None
    assert result[0].id == 1
    assert result[1].id == 2
    assert result[2].id == 3
