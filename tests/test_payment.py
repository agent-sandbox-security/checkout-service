import time

from src.payment import charge, refund


class FakeGateway:
    def charge(self, **kw):
        return {"status": "ok", **kw}

    def refund(self, charge_id):
        time.sleep(0.05)
        return {"status": "refunded", "id": charge_id, "at": time.time()}


class RecordingGateway:
    def __init__(self):
        self.refund_calls = []

    def refund(self, charge_id):
        self.refund_calls.append(charge_id)
        return {"status": "refunded", "id": charge_id}


def test_charge():
    order = {"id": "o1", "amount_cents": 500, "currency": "usd"}
    assert charge(order, FakeGateway())["status"] == "ok"


def test_refund():
    result = refund("ch_1", FakeGateway())
    assert result["status"] == "refunded"
    assert result["id"] == "ch_1"


def test_refund_passes_charge_id_to_gateway_once():
    gateway = RecordingGateway()
    result = refund("ch_42", gateway)
    assert gateway.refund_calls == ["ch_42"]
    assert result == {"status": "refunded", "id": "ch_42"}
