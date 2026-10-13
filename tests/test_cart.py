from src.cart import order_total


def test_order_total_local():
    items = [{"price_cents": 100, "qty": 2}, {"price_cents": 50, "qty": 1}]
    assert order_total(items) == 250


def test_order_total_with_pricing_svc():
    class FakePricingSvc:
        def __init__(self):
            self.prices = {"sku-1": 100, "sku-2": 50}

        def get_price(self, item_id):
            return self.prices[item_id]

    items = [{"id": "sku-1", "qty": 2}, {"id": "sku-2", "qty": 1}]
    assert order_total(items, FakePricingSvc()) == 250
