import re
from typing import Optional

from dash import dcc, html

from database.schema.models import Dish
from database.utils.connection import RecipeDBAccess


def make_html_dish_header(dish: Dish) -> html.H1:
    return html.H1(
        [
            f"Dish#{dish.id}: ",
            html.Span(
                dish.name,
                style={"font-style": "italic", "font-size": "smaller"},
            ),
        ]
    )


def make_html_dish_form(dish: Optional[Dish] = None) -> html.Div:
    return html.Div(
        [
            html.Div(
                [
                    html.Label("Dish Name", style={"margin-right": "10px"}),
                    dcc.Input(
                        id="dish-name",
                        type="text",
                        placeholder="Enter dish name",
                        value=dish.name if dish else "",
                    ),
                ]
            ),
            html.Div(
                [
                    html.Label(
                        "Dish Notes",
                        style={"vertical-align": "top", "margin-right": "10px"},
                    ),
                    dcc.Textarea(
                        id="dish-notes",
                        placeholder="Enter recipe URLs, steps, changes to the recipe, etc.",
                        rows=20,
                        cols=100,
                        value=dish.notes if dish else "",
                    ),
                ],
                style={
                    "margin-top": "20px",
                    "margin-bottom": "20px",
                },
            ),
        ]
    )


def get_dish_by_id(dish_id):
    db_access = RecipeDBAccess.from_env()
    return db_access.get_one_by_id(obj_type=Dish, obj_id=dish_id)


def get_dish_id_from_pathname(pathname) -> str | None:
    res = re.search(r"/dish/(\d+)/?", pathname)
    if res is None:
        return None
    return res.group(1)


def handle_no_dish_id() -> html.Div:
    return html.Div(
        [
            html.H1("List of Dishes"),
            html.Button("Refresh", id="refresh-button"),
            html.Div(id="dish-list"),
        ]
    )


def get_dish_list():
    db_access = RecipeDBAccess.from_env()
    dishes = db_access.get_all(Dish)
    return dishes


def upsert_dish(dish: Dish) -> Dish:
    # Function to update the dish in the database
    db_access = RecipeDBAccess.from_env()
    new_dish = db_access.upsert(obj=dish)
    return new_dish
