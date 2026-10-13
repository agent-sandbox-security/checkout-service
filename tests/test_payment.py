import time

import pytest

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


@pytest.mark.parametrize("currency", ["usd", "eur", "gbp"])
def test_charge_supported_currencies(currency):
    order = {"id": "o1", "amount_cents": 500, "currency": currency}
    assert charge(order, FakeGateway())["currency"] == currency


@pytest.mark.parametrize("currency", ["jpy", "USD", ""])
def test_charge_unsupported_currency(currency):
    order = {"id": "o1", "amount_cents": 500, "currency": currency}
    with pytest.raises(ValueError):
        charge(order, FakeGateway())


def test_refund():
    start = time.time()
    result = refund("ch_1", FakeGateway())
    assert result["status"] == "refunded"
    assert result["at"] - start < 0.05
