import re
from typing import Optional

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

from database.schema.models import Dish
from tracker.pages.common.dish_utils import (
    get_dish_by_id,
    get_dish_id_from_pathname,
    handle_no_dish_id,
    make_html_dish_header,
)

dash.register_page(__name__, path="/dish/", path_template="/dish/<dish_id>/")


def display_dish_info(dish: Dish) -> html.Div:
    notes_with_links = re.sub(r"(https?://\S+)", r"[\1](\1)", dish.notes)
    return html.Div(
        [
            make_html_dish_header(dish=dish),
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
