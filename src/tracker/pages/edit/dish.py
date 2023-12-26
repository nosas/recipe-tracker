from typing import Optional

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

from database.schema.models import Dish
from tracker.pages.common.dish_utils import (
    get_dish_by_id,
    get_dish_id_from_pathname,
    handle_no_dish_id,
    make_html_dish_form,
    make_html_dish_header,
    upsert_dish,
)

# Register the edit page
dash.register_page(__name__, path="/edit/dish/", path_template="/edit/dish/<dish_id>/")


def display_edit_dish_info(dish: Dish) -> html.Div:
    return html.Div(
        [
            make_html_dish_header(dish=dish),
            make_html_dish_form(dish=dish),
            html.Button("Save Changes", id="submit-button", n_clicks=0),
            dcc.Location(id="url-edit-dish", refresh=True),
            html.Div(id="redirect-div-get-dish"),
        ]
    )


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
            upsert_dish(dish)
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
