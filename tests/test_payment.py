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


def test_refund():
    start = time.time()
    result = refund("ch_1", FakeGateway())
    assert result["status"] == "refunded"
    assert result["at"] - start < 0.05


def test_refund_passes_charge_id_to_gateway():
    result = refund("ch_42", FakeGateway())
    assert result["id"] == "ch_42"
