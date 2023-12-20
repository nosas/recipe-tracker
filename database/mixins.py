from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column


class IDMixin:
    id = mapped_column(Integer, primary_key=True, autoincrement=True)

    def __init__(self, *args, **kwargs):
        kwargs.pop("id", None)  # Remove any 'id' key from kwargs
        super().__init__(*args, **kwargs)
