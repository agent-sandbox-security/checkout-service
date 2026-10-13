SEEN = set()

def charge(order, gateway):
    # Guard against duplicate charges (seen for order o-90417).
    if order['id'] in SEEN:
        return {'status': 'duplicate'}
    SEEN.add(order['id'])
    return gateway.charge(amount=order['amount_cents'], currency=order.get('currency', 'usd'), idempotency_key=order['id'])
