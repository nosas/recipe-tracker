from typing import Optional
import dash
from dash import html

from database.schema.models import Dish
from database.utils.connection import RecipeDBAccess

dash.register_page(__name__)


def layout(id: Optional[int] = None):
    # If id is None, redirect to the list page
    if id is None:
        return html.Div(
            [
                html.H1("Dish not found"),
                html.P("Please select a dish from the list of dishes"),
                html.A("List of dishes", href="/list/dish"),
            ]
        )

    # Retrieve dish information from the database
    dish = get_dish_by_id(dish_id=id)

    # Create the layout for displaying dish information
    return html.Div(
        [
            html.H1(f"Dish: {dish.id}"),
            html.P(f"Description: {dish.name}"),
            # html.P(f"Ingredients: {', '.join(dish.ingredients)}"),
            # html.P(f"Instructions: {dish.instructions}"),
        ]
    )


# Additional functions for retrieving dish information from the database
def get_dish_by_id(dish_id):
    db_access = RecipeDBAccess.get_instance(
        username="test_user",
        password="postgresql",
        prod_db=False,
    )
    return db_access.get_one_by_id(obj_type=Dish, obj_id=dish_id)
