from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship

from .mixins import IDMixin

SCHEMA = "recipe"


class Base(DeclarativeBase):
    __abstract__ = True
    __table_args__ = {"schema": SCHEMA}

    def __repr__(self):
        id_repr = getattr(self, "id", "No ID")
        return f"<{self.__class__.__name__}({id_repr})>"


class Dish(IDMixin, Base):
    __tablename__ = "dishes"

    name = mapped_column(String(255), nullable=False)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())

    recipes = relationship("DishRecipe", back_populates="dish")
    reviews = relationship("Review", back_populates="dish")
    events = relationship("EventDish", back_populates="dish")


class Recipe(IDMixin, Base):
    __tablename__ = "recipes"

    url = mapped_column(Text)
    added_at = mapped_column(DateTime)
    updated_at = mapped_column(DateTime)

    dishes = relationship("DishRecipe", back_populates="recipe")


class DishRecipe(Base):
    __tablename__ = "dish_recipes"

    dish_id = mapped_column(
        Integer, ForeignKey(f"{SCHEMA}.dishes.id"), primary_key=True
    )
    recipe_id = mapped_column(
        Integer, ForeignKey(f"{SCHEMA}.recipes.id"), primary_key=True
    )

    dish = relationship("Dish", back_populates="recipes")
    recipe = relationship("Recipe", back_populates="dishes")


class Person(IDMixin, Base):
    __tablename__ = "people"

    name = mapped_column(Text)

    reviews = relationship("PeopleReview", back_populates="person")


class Review(IDMixin, Base):
    __tablename__ = "reviews"

    dish_id = mapped_column(Integer, ForeignKey(f"{SCHEMA}.dishes.id"))

    dish = relationship("Dish", back_populates="reviews")
    people = relationship("PeopleReview", back_populates="review")


class Event(IDMixin, Base):
    __tablename__ = "events"

    type = mapped_column(String(100))
    started_at = mapped_column(DateTime)

    dishes = relationship("EventDish", back_populates="event")


class PeopleReview(Base):
    __tablename__ = "people_reviews"

    people_id = mapped_column(
        Integer, ForeignKey(f"{SCHEMA}.people.id"), primary_key=True
    )
    review_id = mapped_column(
        Integer, ForeignKey(f"{SCHEMA}.reviews.id"), primary_key=True
    )

    person = relationship("Person", back_populates="reviews")
    review = relationship("Review", back_populates="people")


class EventDish(Base):
    __tablename__ = "event_dishes"

    event_id = mapped_column(
        Integer, ForeignKey(f"{SCHEMA}.events.id"), primary_key=True
    )
    dish_id = mapped_column(
        Integer, ForeignKey(f"{SCHEMA}.dishes.id"), primary_key=True
    )

    event = relationship("Event", back_populates="dishes")
    dish = relationship("Dish", back_populates="events")
