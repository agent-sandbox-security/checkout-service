from src.db import get_db


def charge(order, gateway):
    db = get_db()
    existing = db.execute(
        "SELECT id FROM charges WHERE order_id = ?", (order["id"],)
    ).fetchone()
    if existing:
        raise ValueError(f"Charge already exists for order {order['id']}")

    amount = order["amount_cents"]
    currency = order["currency"]
    return gateway.charge(
        amount=amount,
        currency=currency,
        idempotency_key=order["id"],
    )


def refund(charge_id, gateway):
    return gateway.refund(charge_id=charge_id)
