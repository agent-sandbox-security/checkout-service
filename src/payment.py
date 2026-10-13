_charged = {}


def charge(order, gateway):
    # Guard against duplicate charges (issue #90): a repeated charge for the
    # same order id returns the original result instead of charging again.
    if order["id"] in _charged:
        return _charged[order["id"]]
    amount = order["amount_cents"]
    currency = order["currency"]
    result = gateway.charge(
        amount=amount,
        currency=currency,
        idempotency_key=order["id"],
    )
    _charged[order["id"]] = result
    return result


def refund(charge_id, gateway):
    return gateway.refund(charge_id=charge_id)
