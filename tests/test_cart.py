import pytest

from src.cart import order_total, EmptyCartError


def test_order_total():
    items = [
        {"price_cents": 100, "qty": 2},
        {"price_cents": 50, "qty": 1},
    ]
    assert order_total(items) == 250


def test_empty_cart_raises():
    with pytest.raises(EmptyCartError):
        order_total([])
