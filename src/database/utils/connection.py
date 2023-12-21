from typing import Sequence, Type

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from database.schema.models import Base

TEST_DB = "test_db"
PROD_DB = "prod_db"


class RecipeDBAccess:
    """Class for accessing the recipe database

    This class is a singleton, and should be accessed by calling
    RecipeDBAccess.get_instance().

    Requires a username and password for the database.
    """

    _instance = None

    def __init__(self, username: str, password: str, prod_db: bool = False):
        """Initializes the database connection

        Args:
            username (str): Username for the database
            password (str): Password for the database
            prod_db (bool, optional): Whether to use the production database. Defaults to False.
        """
        db = PROD_DB if prod_db else TEST_DB
        print(f"Connecting to {db} database")
        self._engine = create_engine(
            f"postgresql+psycopg2://{username}:{password}@localhost/{db}",
            echo=False,
        )
        self._Session = sessionmaker(bind=self._engine)

    @classmethod
    def get_instance(
        cls: Type["RecipeDBAccess"], username: str, password: str, prod_db: bool = False
    ) -> "RecipeDBAccess":
        """Returns the singleton instance of the class

        Args:
            username (str): Username for the database
            password (str): Password for the database
            prod_db (bool, optional): Whether to use the production database. Defaults to False.

        Returns:
            RecipeDBAccess: The singleton instance of the class
        """
        if cls._instance is None:
            cls._instance = cls(username=username, password=password, prod_db=prod_db)
        return cls._instance

    def get_session(self) -> Session:
        """Returns a session for the database

        Returns:
            Session: A session for the database
        """
        return self._Session()

    def create_tables(self) -> None:
        """Creates the tables in the database"""
        Base.metadata.create_all(self._engine)
        print("Tables created")

    def drop_tables(self, force: bool = False) -> None:
        """Drops the tables in the database"""
        if force:
            Base.metadata.drop_all(self._engine)
        else:
            print("Tables not dropped, force=True to drop tables")

    def insert_one(self, obj: Base) -> None:
        """Inserts a single object into the database

        Args:
            obj (Base): The object to insert
        """
        with self.get_session() as session:
            session.add(obj)
            session.commit()

    def insert_many(self, objs: Sequence[Base]) -> None:
        """Inserts multiple objects into the database

        Args:
            objs (Sequence[Type[Base]]): The objects to insert
        """
        with self.get_session() as session:
            session.add_all(objs)
            session.commit()
