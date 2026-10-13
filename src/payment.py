_charged_order_ids = set()


def charge(order, gateway):
    order_id = order["id"]
    if order_id in _charged_order_ids:
        raise ValueError(f"Order {order_id} has already been charged")
    amount = order["amount_cents"]
    currency = order["currency"]
    result = gateway.charge(
        amount=amount,
        currency=currency,
        idempotency_key=order_id,
    )
    _charged_order_ids.add(order_id)
    return result


def refund(charge_id, gateway):
    return gateway.refund(charge_id=charge_id)
