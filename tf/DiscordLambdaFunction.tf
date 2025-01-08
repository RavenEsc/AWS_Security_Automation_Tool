module "lambda_Discord" {
  source = "terraform-aws-modules/lambda/aws"
  function_name   = "lambda-sat-discord"
  description     = "Sends messages as notifications from the SQS Queue to Discord Webhook Bot"

  create_package  = false

  image_uri    = "464004139021.dkr.ecr.us-east-1.amazonaws.com/xxxxxxxxx:latest"
  package_type = "Image"

  attach_policy_json = true
  policy_json = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowLambdaDisSQSAccess",
      "Effect": "Allow",
      "Action": [
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:GetQueueAttributes"
      ],
      "Resource": "${aws_sqs_queue.orders_to_notify.arn}"
    },
    {
      "Sid": "AllowLambdaDisSecretAccess",
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "arn:aws:secretsmanager:us-east-1:464004139021:secret:tfc/sat/discordwebhook-xD2JBX"
    }
}
EOF

  event_source_mapping = {
    sqs = {
      event_source_arn = aws_sqs_queue.orders_to_notify.arn
    }
  }

  tags = {
    Name = "my-lambda-discord"
  }
}