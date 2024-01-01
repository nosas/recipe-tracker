import dash
from dash import html
from dash.dependencies import Input, Output

from tracker.pages.common.dish_utils import get_dish_list

dash.register_page(__name__, path="/list/dish")


def display_dish_list(dishes):
    return html.Ul([html.Li(html.A(dish.name, href=f"/dish/{dish.id}")) for dish in dishes])


@dash.callback(
    Output("dish-list", "children"),
    [Input("refresh-button", "n_clicks")],
)
def update_dish_list(n_clicks):
    dishes = get_dish_list()
    return display_dish_list(dishes)


def layout():
    return html.Div(
        [
            html.H1("List of Dishes"),
            html.Button("Refresh", id="refresh-button"),
            html.Div(id="dish-list"),
        ]
    )
