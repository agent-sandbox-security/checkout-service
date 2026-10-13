from src.payment import charge, refund


class FakeGateway:
    def __init__(self):
        self.refund_calls = []

    def charge(self, **kw):
        return {"status": "ok", **kw}

    def refund(self, charge_id):
        self.refund_calls.append(charge_id)
        return {"status": "refunded", "id": charge_id}


def test_charge():
    order = {"id": "o1", "amount_cents": 500, "currency": "usd"}
    assert charge(order, FakeGateway())["status"] == "ok"


def test_refund():
    gateway = FakeGateway()
    result = refund("ch_1", gateway)
    assert result == {"status": "refunded", "id": "ch_1"}


def test_refund_calls_gateway_once_with_charge_id():
    gateway = FakeGateway()
    refund("ch_42", gateway)
    assert gateway.refund_calls == ["ch_42"]
