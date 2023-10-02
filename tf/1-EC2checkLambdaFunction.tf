module "ec2lambda" {
  source             = "terraform-aws-modules/lambda/aws"
  version            = "6.0.0"
  function_name      = "lambda-sat-ec2"
  description        = "Checks for public facing ec2 instances"
  handler            = "pec2-check.lambda_handler"
  runtime            = var.py_runtime
  source_path        = "../code/publicec2checklambda"
  timeout            = 840 # 14 minutes max (Can only potentially scan 3 open instances due to port scan)

  attach_policy_json = true
  policy_json = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["sns:Publish"],
      "Resource": ["${aws_sns_topic.orders.arn}"]
    },
    {
      "Effect": "Allow",
      "Action": "ec2:DescribeInstances",
      "Resource": "*"
    }
  ]
}
EOF

  allowed_triggers = {
      EventBridge = {
      principal  = "events.amazonaws.com"
      source_arn = "arn:aws:events:${var.reg}:${local.account_id}:rule/crons-rule"
    }
    environment_variables = {
    SNS_TOPIC_ARN = aws_sns_topic.orders.arn
  }
  tags = {
    Name = "my-lambda-ec2"
  }
}
