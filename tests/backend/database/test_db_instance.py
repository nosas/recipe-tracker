from database.utils.connection import RecipeDBAccess


def test_get_instance(test_db):
    """Verify that the singleton instance is returned"""
    assert isinstance(test_db, RecipeDBAccess)
    assert test_db == RecipeDBAccess.get_instance(
        username="test_user",
        password="postgresql",
        prod_db=False,
    )
