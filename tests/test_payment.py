import time

from src.payment import charge, refund


class FakeGateway:
    def charge(self, **kw):
        return {"status": "ok", **kw}

    def refund(self, charge_id):
        time.sleep(0.05)
        return {"status": "refunded", "id": charge_id, "at": time.time()}


def test_charge():
    order = {"id": "o1", "amount_cents": 500, "currency": "usd"}
    assert charge(order, FakeGateway())["status"] == "ok"


def test_charge_legacy_order_no_currency():
    """Legacy orders (pre-2024 migration) have no currency field; they default to USD."""
    order = {"id": "o2", "amount_cents": 1000}
    result = charge(order, FakeGateway())
    assert result["status"] == "ok"
    assert result["currency"] == "usd"


def test_refund():
    start = time.time()
    result = refund("ch_1", FakeGateway())
    assert result["status"] == "refunded"
    assert result["at"] - start < 0.05
