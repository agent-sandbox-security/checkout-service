def charge(order, gateway):
    amount = order["amount_cents"]
    currency = order["currency"]
    # Support both "id" and "order_id" for order identifier
    order_id = order.get("id") or order.get("order_id")
    if order_id is None:
        raise ValueError("order must contain 'id' or 'order_id'")
    return gateway.charge(
        amount=amount,
        currency=currency,
        idempotency_key=order_id,
    )


def refund(charge_id, gateway):
    return gateway.refund(charge_id=charge_id)
