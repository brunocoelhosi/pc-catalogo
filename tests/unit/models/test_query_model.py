import pytest

from app.models.query_model import QueryModel

class ProductQuery(QueryModel):
    price__ge: float | None = None
    price__lt: float | None = None
    name: str | None = None

def test_to_query_dict_with_operators():
    query = ProductQuery(price__ge=10, price__lt=100, name="tv")
    result = query.to_query_dict()
    assert result == {
        "price": {"$gte": 10, "$lt": 100},
        "name": "tv"
    }

def test_to_query_dict_without_operators():
    query = ProductQuery(name="notebook")
    result = query.to_query_dict()
    assert result == {"name": "notebook"}

def test_to_query_dict_with_none_fields():
    query = ProductQuery(price__ge=None, name=None)
    result = query.to_query_dict()
    assert result == {}

def test_to_query_dict_mixed():
    query = ProductQuery(price__ge=50, name=None)
    result = query.to_query_dict()
    assert result == {"price": {"$gte": 50}}