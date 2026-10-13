import time

from src.pricing import order_total, get_price


class FakePricingSvc:
    def __init__(self, prices, delay=0):
        self.prices = prices
        self.delay = delay
        self.call_count = 0

    def get_price(self, item_id):
        self.call_count += 1
        time.sleep(self.delay)
        return self.prices[item_id]


def test_order_total_with_cache():
    pricing = FakePricingSvc(prices={"sku-1": 100, "sku-2": 250}, delay=0)
    items = [{"id": "sku-1", "qty": 2}, {"id": "sku-2", "qty": 1}]
    assert order_total(items, pricing) == 450
    assert pricing.call_count == 2


def test_get_price_uses_cache():
    pricing = FakePricingSvc(prices={"sku-1": 100}, delay=0)
    assert get_price("sku-1", pricing) == 100
    assert get_price("sku-1", pricing) == 100
    # Second call should be cached
    assert pricing.call_count == 1


def test_order_total_slow_pricing_svc():
    """Ensure caching mitigates slow pricing service."""
    pricing = FakePricingSvc(prices={"sku-1": 100}, delay=0.05)
    items = [{"id": "sku-1", "qty": 1}]

    start = time.time()
    total = order_total(items, pricing)
    first_call_time = time.time() - start

    start = time.time()
    total2 = order_total(items, pricing)
    second_call_time = time.time() - start

    assert total == 100
    assert total2 == 100
    # Cached call should be much faster
    assert second_call_time < first_call_time / 2
