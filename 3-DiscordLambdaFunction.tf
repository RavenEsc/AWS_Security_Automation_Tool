module "lambda_Discord" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "lambda-sat-discord"
  description   = "Sends messages as notifications from the SQS Queue to Discord Webhook Bot"
  handler       = "index3.lambda_handler"
  runtime       = var.py_runtime
  source_path       = "index3.py"

  event_source_mapping = {
    event_source_arn = aws_sqs_queue.orders_to_notify.arn
  }

  layers = [
    module.lambda_layer_discord.lambda_layer_arn,
  ]

  tags = {
    Name = "my-lambda3"
  }
}

module "lambda_layer_discord" {
  source = "terraform-aws-modules/lambda/aws"

  create_layer = true

  layer_name          = "lambda-layer-discord"
  description         = "lambda layer "
  compatible_runtimes = [var.py_runtime]

  source_path = "Discord-Webhook-Dependencies.zip"
}

