import time

from src.pricing import PricingClient


class FakePricingSvc:
    def __init__(self):
        self.calls = 0

    def price(self, sku):
        self.calls += 1
        time.sleep(0.01)
        return {"sku": sku, "price_cents": 100}


def test_cache_hit_avoids_svc_call():
    svc = FakePricingSvc()
    client = PricingClient(svc, ttl_seconds=5)

    first = client.get_price("sku-1")
    second = client.get_price("sku-1")

    assert first == second
    assert svc.calls == 1


def test_cache_expires_after_ttl():
    svc = FakePricingSvc()
    client = PricingClient(svc, ttl_seconds=0)

    client.get_price("sku-1")
    time.sleep(0.01)
    client.get_price("sku-1")

    assert svc.calls == 2


def test_clear_cache():
    svc = FakePricingSvc()
    client = PricingClient(svc, ttl_seconds=5)

    client.get_price("sku-1")
    client.clear_cache()
    client.get_price("sku-1")

    assert svc.calls == 2
