module "lambda_s3" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "lambda-sat-s3"
  description   = "Sends messages as logs from SQS Queue to an S3 bucket"
  handler       = "index2.lambda_handler"
  runtime       = var.py_runtime
  role          = aws_iam_role.lambda_role_s3.arn
  source_code_hash  = data.archive_file.lambda_archive_file2.output_base64sha256
  source_path       = data.archive_file.lambda_archive_file2.output_path
  event_source_mapping = {
    event_source_arn = aws_sqs_queue.orders_to_process.arn
    starting_position = "LATEST"
  }
  environment_variables = {
    buck_lm = var.s3_bucket_name
  }
  tags = {
    Name = "my-lambda2"
  }
}

data "archive_file" "lambda_archive_file2" {
  type        = "zip"
  source_file = "index2.py"
  output_path = "lambda_function_payload2.zip"
}