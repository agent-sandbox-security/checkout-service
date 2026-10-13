import functools
import time


# Simple in-memory TTL cache for pricing-service responses.
# In production this should be backed by Redis, but the pattern is the same.
_cache = {}
_cache_ttl_seconds = 60


def _is_cached(key):
    if key not in _cache:
        return False
    expiry, _ = _cache[key]
    return time.time() < expiry


def _get_cached(key):
    _, value = _cache[key]
    return value


def _set_cached(key, value, ttl=_cache_ttl_seconds):
    _cache[key] = (time.time() + ttl, value)


def get_price(item_id, pricing_svc):
    """Fetch price for an item, with caching to avoid slow pricing-svc calls."""
    cache_key = f"price:{item_id}"
    if _is_cached(cache_key):
        return _get_cached(cache_key)

    # Slow path: call pricing service
    price = pricing_svc.get_price(item_id)
    _set_cached(cache_key, price)
    return price


def order_total(items, pricing_svc):
    """Calculate order total using cached pricing service lookups."""
    total = 0
    for item in items:
        price = get_price(item["id"], pricing_svc)
        total += price * item["qty"]
    return total
