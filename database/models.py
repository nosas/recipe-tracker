from sqlalchemy import create_engine, Column, Integer, Text, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    url = Column(Text)
    added_at = Column(DateTime)
    updated_at = Column(DateTime)
    dishes = relationship("DishRecipe", back_populates="recipe")


class Dish(Base):
    __tablename__ = "dishes"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    recipes = relationship("DishRecipe", back_populates="dish")
    reviews = relationship("Review", back_populates="dish")
    events = relationship("EventDish", back_populates="dish")


class DishRecipe(Base):
    __tablename__ = "dish_recipes"
    dish_id = Column(Integer, ForeignKey("dishes.id"), primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)
    dish = relationship("Dish", back_populates="recipes")
    recipe = relationship("Recipe", back_populates="dishes")


class Person(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    reviews = relationship("PeopleReview", back_populates="person")


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, ForeignKey("dishes.id"))
    dish = relationship("Dish", back_populates="reviews")
    people = relationship("PeopleReview", back_populates="review")


class PeopleReview(Base):
    __tablename__ = "people_reviews"
    people_id = Column(Integer, ForeignKey("people.id"), primary_key=True)
    review_id = Column(Integer, ForeignKey("reviews.id"), primary_key=True)
    person = relationship("Person", back_populates="reviews")
    review = relationship("Review", back_populates="people")


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    type = Column(
        Enum("type1", "type2", "type3", name="event_types")
    )  # Modify as needed
    started_at = Column(DateTime)
    dishes = relationship("EventDish", back_populates="event")


class EventDish(Base):
    __tablename__ = "event_dishes"
    event_id = Column(Integer, ForeignKey("events.id"), primary_key=True)
    dish_id = Column(Integer, ForeignKey("dishes.id"), primary_key=True)
    event = relationship("Event", back_populates="dishes")
    dish = relationship("Dish", back_populates="events")
