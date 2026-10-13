import requests

REGION_TIMEOUTS_MS = {
    "us-east-1": 2000,
    "ap-south-1": 2000,
    "eu-west-1": 2000,
}

def check_stock(sku, region):
    timeout_ms = REGION_TIMEOUTS_MS.get(region, 2000)
    return requests.get(
        f"https://inventory.{region}.internal/stock/{sku}",
        timeout=timeout_ms / 1000,
    )
