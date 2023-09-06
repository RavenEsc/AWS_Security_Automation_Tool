module "lambda" {
  source = "terraform-aws-modules/lambda/aws"
  version = "6.0.0"

  function_name     = "lambda-sat-ec2"
  description       = "Checks for public facing ec2 instances"
  handler           = "index.lambda_handler"
  runtime           = var.py_runtime
  source_code_hash  = data.archive_file.lambda_archive_file.output_base64sha256
  source_path       = data.archive_file.lambda_archive_file.output_path
  role              = aws_iam_role.lambda_role.arn
  environment_variables = {
    SNS_TOPIC_ARN = var.sns_topic_arn
  }

  tags = {
    Name = "my-lambda1"
  }
}

data "archive_file" "lambda_archive_file" {
  type        = "zip"
  source_file = "index.py"
  output_path = "lambda_function_payload.zip"
}