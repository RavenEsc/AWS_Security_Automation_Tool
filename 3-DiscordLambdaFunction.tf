module "lambda_Discord" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "lambda-sat-discord"
  description   = "Sends messages as notifications from the SQS Queue to Discord Webhook Bot"
  handler       = "index3.lambda_handler"
  runtime       = var.py_runtime
  source_code_hash  = data.archive_file.lambda_archive_file3.output_base64sha256
  source_path       = data.archive_file.lambda_archive_file3.output_path

  layers = [
    module.lambda_layer_discord.lambda_layer_arn,
  ]

  tags = {
    Name = "my-lambda3"
  }
}

data "archive_file" "lambda_archive_file3" {
  type        = "zip"
  source_file = "index3.py"
  output_path = "lambda_function_payload3.zip"
}

module "lambda_layer_discord" {
  source = "terraform-aws-modules/lambda/aws"

  create_layer = true

  layer_name          = "lambda-layer-discord"
  description         = "lambda layer "
  compatible_runtimes = [var.py_runtime]

  source_path = "/Discord-Webhook-Dependencies.zip"
}

