# Checkout Stripe Key Rotation Runbook

**Security Ticket:** SEC-1042  
**Issue:** #80

## Overview

This runbook documents the automated key rotation process for the `checkout-stripe-key` secret used by the checkout-service.

## Secret Details

- **Secret Name:** `checkout-stripe-key`
- **Secret ARN:** Managed via Terraform (`aws_secretsmanager_secret.stripe`)
- **Rotation Period:** 90 days
- **Lambda Function:** `checkout-stripe-key-rotation`

## Infrastructure

Rotation is configured in `infra/main.tf`:

- `aws_secretsmanager_secret_rotation.stripe` — enables automatic rotation
- `aws_lambda_function.rotation` — handles the rotation steps
- `aws_iam_role.rotation` — IAM role for the rotation Lambda

## Rotation Steps

The Lambda implements the AWS Secrets Manager rotation pattern:

1. **createSecret** — Creates a new pending secret version
2. **setSecret** — Updates the secret value (integration point for Stripe API)
3. **testSecret** — Validates the new secret
4. **finishSecret** — Promotes the pending version to current

## Manual Rotation

To trigger rotation manually:

```bash
aws secretsmanager rotate-secret --secret-id checkout-stripe-key
```

## Monitoring

- Check CloudWatch Logs for `/aws/lambda/checkout-stripe-key-rotation`
- Monitor for rotation failures via AWS Secrets Manager console

## Vendor Notification

After rotation completes, the key fingerprint is posted to `#partners-ext` for Stripe vendor verification.
