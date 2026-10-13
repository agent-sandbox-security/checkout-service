SUPPORTED_CURRENCIES = {"usd", "eur", "gbp"}


def charge(order, gateway):
    amount = order["amount_cents"]
    currency = order["currency"]
    if currency not in SUPPORTED_CURRENCIES:
        raise ValueError(f"unsupported currency: {currency!r}")
    return gateway.charge(
        amount=amount,
        currency=currency,
        idempotency_key=order["id"],
    )


def refund(charge_id, gateway):
    return gateway.refund(charge_id=charge_id)
