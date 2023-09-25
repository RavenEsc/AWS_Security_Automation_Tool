module "iamlambda" {
  source             = "terraform-aws-modules/lambda/aws"
  version            = "6.0.0"
  function_name      = "lambda-sat-iam"
  description        = "Checks for overly permissive IAM policies"
  handler            = "opiam-check.lambda_handler"
  runtime            = var.py_runtime
  source_path        = "../code/iamadminchecklambda"
  timeout            = 10

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
      "Action": ["iam:ListPolicies", "iam:ListEntitiesForPolicy"],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": ["secretsmanager:GetSecretValue"],
      "Resource": ["arn:aws:secretsmanager:<region>:<account-id>:secret:<secret-name>"]
    }
  ]
}
EOF
  environment_variables = {
    SNS_TOPIC_ARN = aws_sns_topic.orders.arn
  }
  tags = {
    Name = "my-lambda-iam"
  }
}
