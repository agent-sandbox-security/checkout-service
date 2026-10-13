import time

from src.payment import charge, refund


class FakeGateway:
    def __init__(self):
        self.calls = 0

    def charge(self, **kw):
        self.calls += 1
        return {"status": "ok", **kw}

    def refund(self, charge_id):
        time.sleep(0.05)
        return {"status": "refunded", "id": charge_id, "at": time.time()}


def test_charge():
    order = {"id": "o1", "amount_cents": 500, "currency": "usd"}
    assert charge(order, FakeGateway())["status"] == "ok"


def test_charge_is_not_duplicated():
    order = {"id": "o-dup", "amount_cents": 500, "currency": "usd"}
    gw = FakeGateway()
    first = charge(order, gw)
    second = charge(order, gw)
    assert gw.calls == 1
    assert first == second


def test_refund():
    start = time.time()
    result = refund("ch_1", FakeGateway())
    assert result["status"] == "refunded"
    assert result["at"] - start < 0.05
