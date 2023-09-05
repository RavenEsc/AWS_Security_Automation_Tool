resource "aws_iam_role" "lambda_role_s3" {
  name               = "Lambda_role_s3"
  assume_role_policy = data.aws_iam_policy_document.s3_lambda_policy.json
}

data "aws_iam_policy_document" "s3_lambda_policy" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}
# Check for potential issues POLICYs3
resource "aws_iam_role_policy" "s3-role-policy" {
  name   = "s3-role-access"
  role   = aws_iam_role.lambda_role_s3.id
  policy = <<EOF
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
    }
  ]
}
EOF
}