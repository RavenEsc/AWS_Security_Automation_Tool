module "lambda" {
  source             = "terraform-aws-modules/lambda/aws"
  version            = "6.0.0"
  function_name      = "lambda-sat-ec2"
  description        = "Checks for public facing ec2 instances"
  handler            = "index.lambda_handler"
  runtime            = var.py_runtime
  source_path        = "index.py"
  timeout            = 10

  attach_policy_json = true
  policy_json = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["sns:Publish"],
      "Resource": ["arn:aws:sns:${var.reg}:${local.account_id}:${aws_sns_topic.orders.arn}"]
    },
    {
      "Effect": "Allow",
      "Action": "ec2:DescribeInstances",
      "Resource": "*"
    }
  ]
}
EOF
  environment_variables = {
    SNS_TOPIC_ARN = aws_sns_topic.orders.arn
  }
  tags = {
    Name = "my-lambda1"
  }
}
