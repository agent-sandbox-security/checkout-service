import logging

logger = logging.getLogger(__name__)


def order_total(items):
    total = 0
    for i in items:
        if "price_cents" not in i:
            logger.warning("Skipping item with no price_cents: %r", i)
            continue
        total += i["price_cents"] * i["qty"]
    return total
