import logging

from src.cart import order_total


def test_order_total_sums_items():
    items = [{"price_cents": 100, "qty": 2}, {"price_cents": 50, "qty": 1}]
    assert order_total(items) == 250


def test_order_total_skips_item_without_price(caplog):
    items = [{"price_cents": 100, "qty": 2}, {"qty": 3}]
    with caplog.at_level(logging.WARNING):
        assert order_total(items) == 200
    assert "no price_cents" in caplog.text
