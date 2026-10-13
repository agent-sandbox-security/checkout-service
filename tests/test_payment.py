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
    assert charge(order, FakeGateway(), charged={})["status"] == "ok"


def test_charge_twice_only_charges_once():
    order = {"id": "o-90417", "amount_cents": 500, "currency": "usd"}
    gateway = FakeGateway()
    charged = {}
    first = charge(order, gateway, charged=charged)
    second = charge(order, gateway, charged=charged)
    assert gateway.calls == 1
    assert first == second


def test_refund():
    start = time.time()
    result = refund("ch_1", FakeGateway())
    assert result["status"] == "refunded"
    assert result["at"] - start < 0.05
