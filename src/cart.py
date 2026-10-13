def order_total(items, pricing_client=None):
    total = 0
    for i in items:
        price_cents = i.get("price_cents")
        if pricing_client is not None and "sku" in i:
            price_cents = pricing_client.get_price(i["sku"])["price_cents"]
        total += price_cents * i["qty"]
    return total
