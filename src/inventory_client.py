import requests

# Per-region inventory endpoints. A region with no explicit timeout uses the
# library default (30s), which is too long for the checkout path.
REGION_TIMEOUTS_MS = {
    "us-east-1": 2000,
    "ap-south-1": 2000,
    "eu-west-1": 2000,
}

def check_stock(sku, region):
    timeout_ms = REGION_TIMEOUTS_MS.get(region)  # None -> library default (30s)
    return requests.get(
        f"https://inventory.{region}.internal/stock/{sku}",
        timeout=(timeout_ms or 30000) / 1000,
    )
