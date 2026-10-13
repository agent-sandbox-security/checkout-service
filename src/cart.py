import functools
import time


# Simple TTL cache for pricing results to avoid repeated expensive computations
_price_cache = {}
_cache_ttl_seconds = 300  # 5 minute TTL


def _get_cached_price(item_key):
    """Return cached price if not expired, else None."""
    if item_key in _price_cache:
        price, timestamp = _price_cache[item_key]
        if time.time() - timestamp < _cache_ttl_seconds:
            return price
        del _price_cache[item_key]
    return None


def _set_cached_price(item_key, price):
    """Cache a price with current timestamp."""
    _price_cache[item_key] = (price, time.time())


def _compute_item_price(item):
    """Compute price for a single item, using cache when available."""
    item_key = f"{item.get('sku', item.get('id', str(hash(str(item)))))}:{item['price_cents']}:{item['qty']}"
    cached = _get_cached_price(item_key)
    if cached is not None:
        return cached
    price = item["price_cents"] * item["qty"]
    _set_cached_price(item_key, price)
    return price


def order_total(items):
    """Calculate total order amount with caching to reduce pricing-svc latency."""
    return sum(_compute_item_price(i) for i in items)


def warm_cache(items):
    """Pre-compute and cache prices for a list of items to avoid latency spikes."""
    for item in items:
        _compute_item_price(item)
