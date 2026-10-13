def charge(order, gateway):
    amount = order["amount_cents"]
    # Legacy (pre-2024) orders have no currency field; they are all USD.
    currency = order.get("currency", "usd")
    return gateway.charge(
        amount=amount,
        currency=currency,
        idempotency_key=order["id"],
    )


def refund(charge_id, gateway):
    return gateway.refund(charge_id=charge_id)
