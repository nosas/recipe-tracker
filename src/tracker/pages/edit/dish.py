import re
from typing import Optional

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

from database.schema.models import Dish
from database.utils.connection import RecipeDBAccess

# Register the edit page
dash.register_page(__name__, path="/edit/dish/", path_template="/edit/dish/<dish_id>/")


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


def display_edit_dish_info(dish: Dish) -> html.Div:
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
            html.Label("Dish Name"),
            dcc.Input(
                id="dish-name",
                type="text",
                placeholder="Enter dish name",
                value=dish.name,
            ),
            html.Div(
                [
                    html.Label("Dish Notes"),
                    dcc.Textarea(
                        id="dish-notes",
                        placeholder="Enter recipe URLs, steps, changes to the recipe, etc.",
                        rows=20,
                        cols=100,
                        value=dish.notes,
                    ),
                ]
            ),
            html.Button("Save Changes", id="submit-button", n_clicks=0),
            dcc.Location(id="url-edit-dish", refresh=True),
            html.Div(id="redirect-div-get-dish"),
        ]
    )


def update_dish(dish: Dish) -> Dish:
    # Function to update the dish in the database
    db_access = RecipeDBAccess.get_instance(
        username="test_user",
        password="postgresql",
        prod_db=False,
    )
    new_dish = db_access.upsert(obj=dish)
    return new_dish


@dash.callback(
    Output("redirect-div-get-dish", "children"),
    Input("submit-button", "n_clicks"),
    [
        State("dish-name", "value"),
        State("dish-notes", "value"),
        State("url-edit-dish", "pathname"),
    ],
)
def save_changes(n_clicks, name, notes, pathname):
    if n_clicks > 0:
        dish_id = get_dish_id_from_pathname(pathname)
        dish = get_dish_by_id(dish_id)
        dish.name = name
        dish.notes = notes

        try:
            update_dish(dish)
            # Redirect back to the dish detail page
            return dcc.Location(href=f"/dish/{dish_id}", id="redirect-get-dish")
        except Exception as e:
            print(e)
            return html.Div("Error updating dish")

    return ""


def layout(dish_id: Optional[int] = None):
    if dish_id is None:
        return handle_no_dish_id()

    dish = get_dish_by_id(dish_id)
    return display_edit_dish_info(dish)
