data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = "${path.module}/../backend"
  output_path = "${path.module}/../backend.zip"
}

resource "aws_lambda_function" "visitor_counter" {
  function_name = "${var.project_name}-visitor-counter"
  role          = aws_iam_role.lambda.arn
  handler       = "app.lambda_handler"
  runtime       = "python3.12"
  filename      = data.archive_file.lambda.output_path

  source_code_hash = data.archive_file.lambda.output_base64sha256

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.visitor_counter.name
    }
  }

  tracing_config {
    mode = "Active"
  }

  tags = {
    Project = var.project_name
  }
}

resource "aws_iam_role" "lambda" {
  name = "${var.project_name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Project = var.project_name
  }
}

resource "aws_iam_role_policy" "lambda" {
  name = "${var.project_name}-lambda-policy"
  role = aws_iam_role.lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:UpdateItem",
          "dynamodb:GetItem"
        ]
        Resource = aws_dynamodb_table.visitor_counter.arn
      },
      {
        Effect = "Allow"
        Action = [
          "xray:PutTraceSegments",
          "xray:PutTelemetryRecords"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}
