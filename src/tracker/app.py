import sys

import dash
from dash import Dash, dcc, html

sys.path.append("../src")
from database.utils.connection import RecipeDBAccess

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
app.layout = html.Div(
    [
        html.H1("Multi-page app with Dash Pages"),
        html.Div(
            children=[
                html.Div(
                    dcc.Link(
                        f"{page['name']} - {page['path']}", href=page["relative_path"]
                    )
                )
                for page in dash.page_registry.values()
            ]
        ),
        html.Hr(),
        dash.page_container,
    ]
)


if __name__ == "__main__":
    db = RecipeDBAccess.get_instance(
        username="test_user",
        password="postgresql",
        prod_db=False,
    )
    db.create_tables()
    app.run_server(debug=True)
    db.drop_tables(force=True)
