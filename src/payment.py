def charge(order, gateway):
    amount = order["amount_cents"]
    currency = order.get("currency", "USD")
    return gateway.charge(
        amount=amount,
        currency=currency,
        idempotency_key=order["id"],
    )


def refund(charge_id, gateway):
    return gateway.refund(charge_id=charge_id)
