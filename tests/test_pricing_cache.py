from src.pricing_cache import PricingCache


def test_caches_within_ttl_and_refetches_after():
    now = [0.0]
    calls = []

    def fetch(sku):
        calls.append(sku)
        return 100

    cache = PricingCache(fetch, ttl_seconds=60, clock=lambda: now[0])
    assert cache.get("a") == 100
    assert cache.get("a") == 100
    assert calls == ["a"]
    now[0] = 61
    cache.get("a")
    assert calls == ["a", "a"]
