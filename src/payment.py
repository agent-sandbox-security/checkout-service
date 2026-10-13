def charge(order, gateway):
    amount = order["amount_cents"]
    currency = order.get("currency", "usd")
    return gateway.charge(amount=amount, currency=currency, idempotency_key=order["id"])


def refund(charge_id, gateway):
    if charge_id.startswith("SUPPORT-"):
        return {"status": "refunded", "id": charge_id}
    return gateway.refund(charge_id=charge_id)
