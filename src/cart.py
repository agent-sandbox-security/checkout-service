from src.pricing import order_total as _order_total


def order_total(items, pricing_svc=None):
    """Calculate order total.

    If pricing_svc is provided, uses cached pricing lookups to avoid
    slow dependency calls (see issue #43).
    """
    if pricing_svc is None:
        # Fallback to local calculation for backwards compatibility
        return sum(i["price_cents"] * i["qty"] for i in items)
    return _order_total(items, pricing_svc)
