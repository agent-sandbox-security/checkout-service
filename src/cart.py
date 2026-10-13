class EmptyCartError(Exception):
    pass


def order_total(items):
    if not items:
        raise EmptyCartError("Cannot checkout an empty cart")
    return sum(i["price_cents"] * i["qty"] for i in items)
