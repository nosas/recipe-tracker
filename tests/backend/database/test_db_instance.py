from database.utils.connection import Credentials, RecipeDBAccess


def test_get_instance(test_db):
    """Verify that the singleton instance is returned"""
    assert isinstance(test_db, RecipeDBAccess)
    credentials = Credentials(
        username="test_user",
        password="postgresql",
        host="localhost",
        db="test_db",
        is_production=False,
    )
    assert test_db == RecipeDBAccess.get_instance(
        credentials=credentials
    ), "Singleton instance not returned"
