module "lambda_s3" {
  source = "terraform-aws-modules/lambda/aws"
  version       = "6.0.0"
  function_name = "lambda-sat-s3"
  description   = "Sends messages as logs from SQS Queue to an S3 bucket"
  handler       = "s3export.lambda_handler"
  runtime       = var.py_runtime
  source_path       = "../code/s3loglambda"
  
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
      "Sid": "AllowLambdaS3SQSAccess",
      "Effect": "Allow",
      "Action": [
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:GetQueueAttributes"
      ],
      "Resource": "${aws_sqs_queue.orders_to_process.arn}"
    }
  ]
}
EOF

  event_source_mapping = {
    sqs = {
      event_source_arn = aws_sqs_queue.orders_to_process.arn
    }
  }

  environment_variables = {
    buck_lm = var.s3_bucket_name
  }

  tags = {
    Name = "my-lambda-s3"
  }
}