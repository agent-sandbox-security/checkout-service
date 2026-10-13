import time
from src.cart import order_total, warm_cache, _price_cache, _set_cached_price, _get_cached_price


def test_order_total_basic():
    items = [
        {"price_cents": 100, "qty": 2, "sku": "item1"},
        {"price_cents": 50, "qty": 1, "sku": "item2"},
    ]
    assert order_total(items) == 250


def test_cache_hit():
    # Clear cache first
    _price_cache.clear()
    
    items = [{"price_cents": 100, "qty": 3, "sku": "cached_item"}]
    
    # First call computes and caches
    result1 = order_total(items)
    assert result1 == 300
    
    # Second call should hit cache
    result2 = order_total(items)
    assert result2 == 300


def test_warm_cache():
    _price_cache.clear()
    
    items = [
        {"price_cents": 200, "qty": 2, "sku": "warm1"},
        {"price_cents": 150, "qty": 1, "sku": "warm2"},
    ]
    
    warm_cache(items)
    
    # After warming, order_total should use cached values
    assert order_total(items) == 550


def test_cache_ttl_expiration():
    _price_cache.clear()
    
    item = {"price_cents": 100, "qty": 1, "sku": "ttl_item"}
    item_key = "ttl_item:100:1"
    
    # Set a cached value with old timestamp
    _price_cache[item_key] = (999, time.time() - 400)  # 400s ago, exceeds 300s TTL
    
    # Should recompute since cache expired
    result = order_total([item])
    assert result == 100  # Not the stale 999
