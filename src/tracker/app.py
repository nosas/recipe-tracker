import logging
import sys

import dash
from dash import Dash, dcc, html

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

sys.path.append(".")  # Adds higher directory to python modules path.
from database.utils.connection import RecipeDBAccess

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
app.layout = html.Div(
    [
        html.H1("Multi-page app with Dash Pages"),
        html.Div(
            children=[
                html.Div(dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"]))
                for page in dash.page_registry.values()
            ]
        ),
        html.Hr(),
        dash.page_container,
    ]
)


if __name__ == "__main__":
    _db = RecipeDBAccess.from_env()
    if _db._credentials.is_production:
        logging.info("Using production database")
    else:
        logging.info("Using test database")
    _db.create_tables()
    app.run_server(host="0.0.0.0", debug=True)
    # _db.drop_tables(force=True)
