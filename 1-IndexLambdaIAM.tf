resource "aws_iam_role" "lambda_role" {
  name               = "Lambda_role"
  assume_role_policy = data.aws_iam_policy_document.main_lambda_policy.json
}

resource "aws_iam_role_policy" "SNS_role-policy" {
  name   = "sns-topic-role-access"
  role   = aws_iam_role.lambda_role.id
  policy = aws_iam_policy.sns_lambda_policy.policy
}

data "aws_iam_policy_document" "main_lambda_policy" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_policy" "sns_lambda_policy" {
  name        = "sns-topic-access-policy"
policy {
    policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sns:Publish",
      "Resource": "arn:aws:sns:${var.reg}:${local.account_id}:${var.sns_topic_arn}"
    }
  ]
}
EOF
  }
}