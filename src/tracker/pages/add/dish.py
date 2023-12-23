import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

from database.schema.models import Dish
from database.utils.connection import RecipeDBAccess

dash.register_page(__name__)


def layout():
    return html.Div(
        [
            dcc.Input(id="dish-name", type="text", placeholder="Enter dish name"),
            html.Button("Submit", id="button-insert-dish", n_clicks=0),
            html.Div(id="output-state"),
        ]
    )


@dash.callback(
    Output("output-state", "children"),
    [Input("button-insert-dish", "n_clicks")],
    [State("dish-name", "value")],
)
def update_output(n_clicks, dish_name):
    if n_clicks > 0:
        # Connect to the database
        db = RecipeDBAccess.get_instance(
            username="test_user",
            password="postgresql",
            prod_db=False,
        )

        # Insert the new dish
        dish = Dish(name=dish_name)
        db.insert_one(dish)

        return f"Dish {dish_name} added successfully!"
    return ""
