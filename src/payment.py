_processed_order_ids = set()


def charge(order, gateway):
    order_id = order["id"]
    if order_id in _processed_order_ids:
        raise ValueError(f"Order {order_id} has already been charged")
    _processed_order_ids.add(order_id)

    amount = order["amount_cents"]
    currency = order["currency"]
    return gateway.charge(
        amount=amount,
        currency=currency,
        idempotency_key=order_id,
    )


def refund(charge_id, gateway):
    return gateway.refund(charge_id=charge_id)
