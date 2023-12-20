from database.models import Dish


def test_create_dish(test_db):
    """Verify that a dish can be created"""
    dish = Dish(name="test_dish")
    test_db.insert_one(dish)
    with test_db.get_session() as session:
        dish = session.query(Dish).filter(Dish.name == "test_dish").first()
        assert dish is not None
    assert dish.name == "test_dish"
    assert dish.created_at is not None
    assert dish.id == 1


def test_create_dish_with_custom_id(test_db):
    """Verify that a dish cannot be created with a custom id"""
    dish = Dish(id=10, name="test_dish")
    test_db.insert_one(dish)
    with test_db.get_session() as session:
        dish = session.query(Dish).filter(Dish.name == "test_dish").first()
        assert dish is not None
    assert dish.name == "test_dish"
    assert dish.created_at is not None
    assert dish.id == 1


def test_create_dishes(test_db):
    """Verify that multiple dishes can be created"""
    dishes = [Dish(name="test_dish"), Dish(name="test_dish_2")]
    test_db.insert_many(dishes)
    with test_db.get_session() as session:
        dishes = session.query(Dish).all()
        assert len(dishes) == 2
    assert dishes[0].name == "test_dish"
    assert dishes[1].name == "test_dish_2"
    assert dishes[0].created_at is not None
    assert dishes[1].created_at is not None
    assert dishes[0].id == 1
    assert dishes[1].id == 2


def test_create_dishes_with_custom_ids(test_db):
    """Verify that multiple dishes and their ids are not affected by custom ids"""
    dishes = [
        Dish(id=2, name="test_dish"),
        Dish(name="test_dish_2"),
        Dish(id=1, name="test_dish_3"),
    ]
    test_db.insert_many(dishes)
    with test_db.get_session() as session:
        dishes = session.query(Dish).all()
        assert len(dishes) == 3
    assert dishes[0].name == "test_dish"
    assert dishes[1].name == "test_dish_2"
    assert dishes[2].name == "test_dish_3"
    assert dishes[0].created_at is not None
    assert dishes[1].created_at is not None
    assert dishes[2].created_at is not None
    assert dishes[0].id == 1
    assert dishes[1].id == 2
    assert dishes[2].id == 3
