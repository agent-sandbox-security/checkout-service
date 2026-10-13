# checkout-service infrastructure, applied from main by the platform pipeline.
# Sandbox note: the stack in agent-scope/phase1/terraform creates these resources; this file
# is the service's own declaration of them (evidence for the map builder), not applied alone.
provider "aws" {
  region = "us-east-2"
}

resource "aws_cloudwatch_log_group" "staging" {
  name = "checkout-staging-logs"
}

resource "aws_cloudwatch_log_group" "prod" {
  name = "checkout-prod-logs"
}

resource "aws_dynamodb_table" "orders" {
  name         = "checkout-db"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"
  attribute {
    name = "id"
    type = "S"
  }
  tags         = { service = "checkout", data = "customer-pii" }
}

resource "aws_secretsmanager_secret" "stripe" {
  name = "checkout-stripe-key"
}

# Decommissioned 2025-11; kept with count = 0 for state history.
resource "aws_elasticache_replication_group" "legacy" {
  count                = 0
  replication_group_id = "checkout-legacy-cache"
}

data "aws_iam_role" "task" {
  name = "agentscope-task-checkout"
}
