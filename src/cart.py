def order_total(items):
    return sum(i["price_cents"] * i.get("qty", 1) for i in items)
