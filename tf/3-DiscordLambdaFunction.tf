module "lambda_Discord" {
  source = "terraform-aws-modules/lambda/aws"
  function_name   = "lambda-sat-discord"
  description     = "Sends messages as notifications from the SQS Queue to Discord Webhook Bot"

  create_package  = false

  image_uri    = module.docker_image_webhook.image_uri
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
      }
    ]
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
  depends_on = [ 
    module.module.docker_image_webhook
    ]
}

data "aws_ecr_authorization_token" "token" {}

provider "docker" {
  registry_auth {
    address  = "835367859852.dkr.ecr.eu-west-1.amazonaws.com"
    username = data.aws_ecr_authorization_token.token.user_name
    password = data.aws_ecr_authorization_token.token.password
  }
}

module "docker_image_webhook" {
  source = "terraform-aws-modules/lambda/aws//modules/docker-build"

  create_ecr_repo = true
  ecr_repo        = "testDiscord-ecr-repo"

  use_image_tag = true
  image_tag     = "1.0"

  source_path     = "../code/discordlambda"
}