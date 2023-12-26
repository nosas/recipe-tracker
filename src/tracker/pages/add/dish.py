import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

from database.schema.models import Dish
from tracker.pages.common.dish_utils import make_html_dish_form, upsert_dish

dash.register_page(__name__)


def layout():
    return html.Div(
        [
            html.H1("Add Dish"),
            make_html_dish_form(),
            html.Button("Insert Dish", id="button-insert-dish", n_clicks=0),
            html.Div(id="output-state"),
        ]
    )


@dash.callback(
    Output("output-state", "children"),
    [Input("button-insert-dish", "n_clicks")],
    [State("dish-name", "value"), State("dish-notes", "value")],
)
def update_output(n_clicks, dish_name, dish_notes):
    if n_clicks > 0:
        dish = Dish(name=dish_name, notes=dish_notes)

        try:
            new_dish = upsert_dish(dish=dish)
            return dcc.Location(href=f"/dish/{new_dish.id}", id="redirect-get-dish")
        except Exception as e:
            return f"Error: {e}"

    return ""
