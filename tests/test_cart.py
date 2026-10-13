from src.cart import order_total


def test_order_total_with_qty():
    assert order_total([{"price_cents": 500, "qty": 3}]) == 1500


def test_order_total_missing_qty_defaults_to_one():
    assert order_total([{"price_cents": 500}]) == 500


def test_order_total_mixed_items():
    items = [{"price_cents": 200, "qty": 2}, {"price_cents": 300}]
    assert order_total(items) == 700
