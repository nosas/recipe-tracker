import dash
from dash import html
from dash.dependencies import Input, Output

from database.schema.models import Dish
from database.utils.connection import RecipeDBAccess

# Only register this page if it is not already registered
if __name__ not in dash.page_registry:
    dash.register_page(__name__)


def layout():
    return html.Div(
        [
            html.H1("List of Dishes"),
            html.Button("Refresh", id="refresh-button"),
            html.Div(id="dish-list"),
        ]
    )


def get_dish_list():
    db_access = RecipeDBAccess.get_instance(
        username="test_user",
        password="postgresql",
        prod_db=False,
    )
    dishes = db_access.get_all(Dish)
    return dishes


def display_dish_list(dishes):
    return html.Ul(
        [html.Li(html.A(dish.name, href=f"/dish?id={dish.id}")) for dish in dishes]
    )


@dash.callback(
    Output("dish-list", "children"),
    [Input("refresh-button", "n_clicks")],
)
def update_dish_list(n_clicks):
    dishes = get_dish_list()
    return display_dish_list(dishes)
