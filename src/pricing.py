import functools
import time


class PricingClient:
    def __init__(self, svc, ttl_seconds=60):
        self.svc = svc
        self.ttl = ttl_seconds
        self._cache = {}

    def get_price(self, sku):
        now = time.time()
        if sku in self._cache:
            value, expiry = self._cache[sku]
            if now < expiry:
                return value
        price = self.svc.price(sku)
        self._cache[sku] = (price, now + self.ttl)
        return price

    def clear_cache(self):
        self._cache.clear()
