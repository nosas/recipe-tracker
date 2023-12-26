import re
from typing import Optional

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

from database.schema.models import Dish
from database.utils.connection import RecipeDBAccess

dash.register_page(__name__, path="/dish/", path_template="/dish/<dish_id>/")


def get_dish_by_id(dish_id):
    db_access = RecipeDBAccess.get_instance(
        username="test_user",
        password="postgresql",
        prod_db=False,
    )
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


def display_dish_info(dish: Dish) -> html.Div:
    notes_with_links = re.sub(r"(https?://\S+)", r"[\1](\1)", dish.notes)
    return html.Div(
        [
            html.H1(
                [
                    f"Dish#{dish.id}: ",
                    html.Span(
                        dish.name,
                        style={"font-style": "italic", "font-size": "smaller"},
                    ),
                ]
            ),
            html.Button("Edit", id="edit-button", n_clicks=0),
            dcc.Markdown(notes_with_links),
            dcc.Location(id="url-get-dish", refresh=True),
            html.Div(id="redirect-div-edit-dish"),
        ]
    )


@dash.callback(
    Output("redirect-div-edit-dish", "children"),
    Input("edit-button", "n_clicks"),
    State("url-get-dish", "pathname"),
)
def redirect_to_edit_page(n_clicks, pathname):
    if n_clicks > 0:
        dish_id = get_dish_id_from_pathname(pathname)
        return dcc.Location(href=f"/edit/dish/{dish_id}", id="redirect-edit-dish")
    return ""


def layout(dish_id: Optional[int] = None):
    if dish_id is None:
        return handle_no_dish_id()

    dish = get_dish_by_id(dish_id=dish_id)
    return display_dish_info(dish=dish)
