import re
from typing import Optional

import dash
from dash import dcc, html

from database.schema.models import Dish
from database.utils.connection import RecipeDBAccess

dash.register_page(__name__, path="/dish/", path_template="/dish/<dish_id>")


def layout(dish_id: Optional[int] = None):
    if dish_id is None:
        return html.Div(
            [
                html.H1("List of Dishes"),
                html.Button("Refresh", id="refresh-button"),
                html.Div(id="dish-list"),
            ]
        )
    else:
        dish = get_dish_by_id(dish_id=dish_id)
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
                dcc.Markdown(notes_with_links),
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
