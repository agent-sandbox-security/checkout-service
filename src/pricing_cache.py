import time


class PricingCache:
    """Small TTL cache for pricing-svc lookups.

    Prod logs for issue #83 show pricing-svc calls at ~900ms when cold and
    ~120ms when the cache is warm, so checkout should avoid cold lookups.
    """

    def __init__(self, fetch, ttl_seconds=60, clock=time.monotonic):
        self._fetch = fetch
        self._ttl = ttl_seconds
        self._clock = clock
        self._entries = {}

    def get(self, sku):
        now = self._clock()
        hit = self._entries.get(sku)
        if hit and now - hit[0] < self._ttl:
            return hit[1]
        value = self._fetch(sku)
        self._entries[sku] = (now, value)
        return value
