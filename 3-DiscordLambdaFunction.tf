module "lambda_Discord" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "lambda-sat-discord"
  description   = "Sends messages as notifications from the SQS Queue to Discord Webhook Bot"
  handler       = "index3.lambda_handler"
  runtime       = var.py_runtime
  source_path       = "index3.py"

attach_policy_json = true
policy_json = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowLambdaToAccessBucket",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::${var.s3_bucket_name}",
        "arn:aws:s3:::${var.s3_bucket_name}/*"
      ]
    },
    {
      "Sid": "AllowLambdaDisSQSAccess",
      "Effect": "Allow",
      "Action": [
        "sqs:ReceiveMessage"
      ],
      "Resource": "${aws_sqs_queue.orders_to_process.arn}"
    }
  ]
}
EOF

  event_source_mapping = {
    sqs = {
      event_source_arn = aws_sqs_queue.orders_to_notify.arn
    }
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

