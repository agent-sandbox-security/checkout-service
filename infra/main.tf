# checkout-service infrastructure, applied from main by the platform pipeline.
provider "aws" {
  region = "us-east-2"
}

resource "aws_cloudwatch_log_group" "staging" {
  name = "checkout-staging-logs"
}

resource "aws_cloudwatch_log_group" "prod" {
  name = "checkout-prod-logs"
}

resource "aws_db_instance" "orders" {
  identifier = "checkout-db"
  engine     = "postgres"
  tags       = { service = "checkout", data = "customer-pii" }
}

resource "aws_secretsmanager_secret" "stripe" {
  name                    = "checkout-stripe-key"
  description             = "Stripe API key for checkout-service (rotated per SEC-1042)"
  recovery_window_in_days = 7
}

resource "aws_secretsmanager_secret_rotation" "stripe" {
  secret_id           = aws_secretsmanager_secret.stripe.id
  rotation_lambda_arn = aws_lambda_function.rotation.arn

  rotation_rules {
    automatically_after_days = 90
  }
}

resource "aws_lambda_function" "rotation" {
  function_name = "checkout-stripe-key-rotation"
  role          = aws_iam_role.rotation.arn
  handler       = "index.handler"
  runtime       = "python3.11"
  timeout       = 30
  filename      = data.archive_file.rotation_lambda.output_path
  source_code_hash = data.archive_file.rotation_lambda.output_base64sha256
}

data "archive_file" "rotation_lambda" {
  type        = "zip"
  output_path = "${path.module}/rotation_lambda.zip"
  source {
    content  = <<-EOF
import boto3
import os

def handler(event, context):
    secret_id = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']
    client = boto3.client('secretsmanager')
    if step == 'createSecret':
        client.put_secret_value(SecretId=secret_id, ClientRequestToken=token, SecretString='ROTATION_IN_PROGRESS', VersionStages=['AWSPENDING'])
    elif step == 'setSecret':
        pass
    elif step == 'testSecret':
        pass
    elif step == 'finishSecret':
        client.update_secret_version_stage(SecretId=secret_id, VersionStage='AWSCURRENT', MoveToVersionId=token, RemoveFromVersionId=client.describe_secret(SecretId=secret_id)['VersionIdsToStages'])
    return {'status': 'success'}
EOF
    filename = "index.py"
  }
}

resource "aws_iam_role" "rotation" {
  name = "checkout-stripe-key-rotation-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "rotation" {
  name = "checkout-stripe-key-rotation-policy"
  role = aws_iam_role.rotation.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:DescribeSecret",
          "secretsmanager:GetSecretValue",
          "secretsmanager:PutSecretValue",
          "secretsmanager:UpdateSecretVersionStage"
        ]
        Resource = aws_secretsmanager_secret.stripe.arn
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}

# Decommissioned 2025-11; kept with count = 0 for state history.
resource "aws_elasticache_replication_group" "legacy" {
  count                = 0
  replication_group_id = "checkout-legacy-cache"
}

data "aws_iam_role" "task" {
  name = "checkout-task-role"
}
