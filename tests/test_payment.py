import time

from src.payment import charge, refund


class FakeGateway:
    def charge(self, **kw):
        return {"status": "ok", **kw}

    def refund(self, charge_id):
        time.sleep(0.05)
        return {"status": "refunded", "id": charge_id, "at": time.time()}


def test_charge_with_id():
    order = {"id": "o1", "amount_cents": 500, "currency": "usd"}
    assert charge(order, FakeGateway())["status"] == "ok"


def test_charge_with_order_id():
    order = {"order_id": "o-88122", "amount_cents": 500, "currency": "usd"}
    result = charge(order, FakeGateway())
    assert result["status"] == "ok"
    assert result["idempotency_key"] == "o-88122"


def test_charge_missing_id_raises():
    order = {"amount_cents": 500, "currency": "usd"}
    try:
        charge(order, FakeGateway())
        assert False, "Expected ValueError"
    except ValueError as e:
        assert "id" in str(e)


def test_refund():
    start = time.time()
    result = refund("ch_1", FakeGateway())
    assert result["status"] == "refunded"
    assert result["at"] - start < 0.05
