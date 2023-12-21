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
    """Verify that a dish can be updated"""
    dish = Dish(name="test_dish")
    test_db.insert_one(dish)
    with test_db.get_session() as session:
        result = session.query(Dish).filter(Dish.name == "test_dish").one_or_none()
        assert result is not None
    validate_dish(dish=result, name="test_dish", id=1)

    dish.name = "test_dish_2"
    test_db.upsert(dish)
    with test_db.get_session() as session:
        result = session.query(Dish).filter(Dish.name == "test_dish_2").one_or_none()
        assert result is not None
    validate_dish(dish=result, name="test_dish_2", id=1)
