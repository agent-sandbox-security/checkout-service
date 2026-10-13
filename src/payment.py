_charged = {}


def charge(order, gateway, charged=None):
    # Guard against duplicate charges (issue #85): an order is charged once;
    # repeat calls return the original result instead of hitting the gateway.
    if charged is None:
        charged = _charged
    if order["id"] in charged:
        return charged[order["id"]]
    amount = order["amount_cents"]
    currency = order["currency"]
    result = gateway.charge(
        amount=amount,
        currency=currency,
        idempotency_key=order["id"],
    )
    charged[order["id"]] = result
    return result


def refund(charge_id, gateway):
    return gateway.refund(charge_id=charge_id)
