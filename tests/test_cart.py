from src.cart import order_total
from src.pricing import PricingClient


class FakePricingSvc:
    def __init__(self):
        self.calls = 0

    def price(self, sku):
        self.calls += 1
        return {"sku": sku, "price_cents": 200}


def test_order_total_with_static_prices():
    items = [
        {"price_cents": 100, "qty": 2},
        {"price_cents": 50, "qty": 1},
    ]
    assert order_total(items) == 250


def test_order_total_with_pricing_client():
    svc = FakePricingSvc()
    client = PricingClient(svc, ttl_seconds=5)
    items = [
        {"sku": "a", "qty": 2},
        {"sku": "b", "qty": 1},
    ]
    assert order_total(items, pricing_client=client) == 600
    assert svc.calls == 2
