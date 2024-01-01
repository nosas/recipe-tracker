from os import getenv
from typing import Sequence, Type, TypeVar

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from database.schema.models import Base, Dish, Recipe

ENTRY = TypeVar("ENTRY", Dish, Recipe)
ENTRY_HAS_ID = TypeVar("ENTRY_HAS_ID", Dish, Recipe)


class Credentials:
    def __init__(
        self,
        username: str,
        password: str,
        host: str,
        db: str,
        is_production: bool,
    ):
        """Initializes the credentials

        Args:
            username (str): Username for the database
            password (str): Password for the database
            host (str): Host to connect to
            db (str): Database to connect to
            is_production (bool): Whether or not the credentials are for production
        """

        try:
            self.validate_credentials(username=username, password=password, host=host, db=db)
        except ValueError as e:
            raise ValueError(
                "Environment variables not set. "
                "Please set POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB. "
                "If you are running tests, set TESTING=True, TEST_POSTGRES_USER, "
                "TEST_POSTGRES_PASSWORD, TEST_POSTGRES_HOST, and TEST_POSTGRES_DB."
            )

        self.username = username
        self.password = password
        self.host = host
        self.db = db
        self._is_production = is_production

    @classmethod
    def from_env(cls: Type["Credentials"]) -> "Credentials":
        """Returns an instance of the class using environment variables

        Returns:
            Credentials: An instance of the class
        """
        load_dotenv()

        is_production = getenv("TESTING", "True") == "False"

        username = getenv("TEST_POSTGRES_USER" if not is_production else "POSTGRES_USER", "")
        password = getenv(
            "TEST_POSTGRES_PASSWORD" if not is_production else "POSTGRES_PASSWORD", ""
        )
        host = getenv("TEST_POSTGRES_HOST" if not is_production else "POSTGRES_HOST", "")
        db = getenv("TEST_POSTGRES_DB" if not is_production else "POSTGRES_DB", "")

        return cls(
            username=username,
            password=password,
            host=host,
            db=db,
            is_production=is_production,
        )

    @classmethod
    def validate_credentials(
        cls: Type["Credentials"],
        username: str,
        password: str,
        host: str,
        db: str,
    ) -> None:
        """Validate that environment variables are set

        Args:
            username (str): Username for the database
            password (str): Password for the database
            host (str): Host to connect to
            db (str): Database to connect to

        Raises:
            ValueError: If any of the environment variables are None
        """
        vars = [username, password, host, db]
        if any([var == "" for var in vars]):
            missing = [var for var in ["username", "password", "host", "db"] if var == ""]
            raise ValueError("The following variables are missing: {}".format(", ".join(missing)))

    @property
    def is_production(self) -> bool:
        return self._is_production is True


class RecipeDBAccess:
    """Class for accessing the recipe database

    This class is a singleton, and should be accessed by calling
    RecipeDBAccess.get_instance().

    Requires a username and password for the database.
    """

    _instance = None

    def __init__(self, credentials: Credentials):
        """Initializes the database connection

        Args:
            credentials (Credentials): The credentials for the database
        """
        self._credentials = credentials
        username = credentials.username
        password = credentials.password
        host = credentials.host
        db = credentials.db

        print(f"Connecting to {db} database")
        self._engine = create_engine(
            f"postgresql+psycopg2://{username}:{password}@{host}/{db}",
            echo=False,
        )
        self._Session = sessionmaker(bind=self._engine)

    @classmethod
    def from_env(cls: Type["RecipeDBAccess"]) -> "RecipeDBAccess":
        """Returns an instance of the class using environment variables

        Returns:
            RecipeDBAccess: An instance of the class
        """
        credentials = Credentials.from_env()
        return cls.get_instance(credentials=credentials)

    @classmethod
    def get_instance(cls: Type["RecipeDBAccess"], credentials: Credentials) -> "RecipeDBAccess":
        """Returns the singleton instance of the class

        Args:
            credentials (Credentials): The credentials for the database

        Returns:
            RecipeDBAccess: The singleton instance of the class
        """
        if cls._instance is None:
            cls._instance = cls(credentials=credentials)
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

    def insert_one(self, obj: ENTRY) -> None:
        """Inserts a single object into the database

        Args:
            obj (ENTRY): The object to insert
        """
        with self.get_session() as session:
            session.add(obj)
            session.commit()

    def insert_many(self, objs: Sequence[ENTRY]) -> None:
        """Inserts multiple objects into the database

        Args:
            objs (Sequence[Type[ENTRY]]): The objects to insert
        """
        with self.get_session() as session:
            session.add_all(objs)
            session.commit()

    def upsert(self, obj: ENTRY) -> ENTRY:
        """Inserts or updates an object in the database

        Args:
            obj (ENTRY): The object to insert or update
        """
        with self.get_session() as session:
            obj = session.merge(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def get_one_by_id(self, obj_type: Type[ENTRY_HAS_ID], obj_id: int) -> ENTRY_HAS_ID | None:
        """Gets a single object from the database by id

        Args:
            obj_type (Type[ENTRY_HAS_ID]): The type of object to get
            obj_id (int): The id of the object to get

        Returns:
            ENTRY_HAS_ID | None: The object if it exists, otherwise None
        """
        with self.get_session() as session:
            return session.query(obj_type).filter(obj_type.id == obj_id).one_or_none()

    def get_all(self, obj_type: Type[ENTRY]) -> Sequence[ENTRY]:
        """Gets all objects of a given type from the database

        Args:
            obj_type (Type[ENTRY]): The type of object to get

        Returns:
            Sequence[ENTRY]: All objects of the given type
        """
        with self.get_session() as session:
            return session.query(obj_type).all()
