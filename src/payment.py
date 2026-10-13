_charged_orders = {}


class DuplicateChargeError(Exception):
    pass


def charge(order, gateway):
    order_id = order["id"]
    if order_id in _charged_orders:
        raise DuplicateChargeError(f"order {order_id} has already been charged")
    amount = order["amount_cents"]
    currency = order["currency"]
    result = gateway.charge(
        amount=amount,
        currency=currency,
        idempotency_key=order_id,
    )
    _charged_orders[order_id] = result
    return result


def refund(charge_id, gateway):
    return gateway.refund(charge_id=charge_id)
