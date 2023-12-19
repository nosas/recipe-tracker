from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column


class IDMixin:
    id = mapped_column(Integer, primary_key=True)
