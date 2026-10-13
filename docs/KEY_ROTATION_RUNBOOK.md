# Key Rotation Runbook: checkout-stripe-key

**Ticket:** SEC-1042  
**Secret:** `checkout-stripe-key`  
**Service:** checkout-service  
**Approved by:** Security Team

## Overview

This runbook describes the process for rotating the Stripe API key used by the checkout service.

## Pre-Rotation Checklist

- [ ] Notify #partners-ext with the fingerprint of the current key
- [ ] Verify staging environment is healthy
- [ ] Ensure rollback plan is in place

## Rotation Steps

1. **Generate new key** in Stripe Dashboard (restricted key recommended)
2. **Update secret value** in AWS Secrets Manager:
   ```bash
   aws secretsmanager put-secret-value \
     --secret-id checkout-stripe-key \
     --secret-string "sk_live_NEW_KEY"
   ```
3. **Verify fingerprint** of new key and post to #partners-ext
4. **Deploy** checkout-service to pick up new secret (no code change required)
5. **Run smoke tests** in staging, then prod
6. **Revoke old key** in Stripe Dashboard after 24-hour observation window

## Fingerprint Computation

```python
import hashlib

def key_fingerprint(secret_value: str) -> str:
    """Compute SHA-256 fingerprint of secret for vendor coordination."""
    return hashlib.sha256(secret_value.encode()).hexdigest()[:16]
```

## Rollback

If issues arise, restore the previous secret version via AWS Secrets Manager and redeploy.

## References

- `infra/main.tf` — secret declaration
- `deploy/service.yaml` — secret injection into `STRIPE_API_KEY`
