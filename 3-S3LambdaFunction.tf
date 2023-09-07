module "lambda_s3" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "lambda-sat-s3"
  description   = "Sends messages as logs from SQS Queue to an S3 bucket"
  handler       = "index2.lambda_handler"
  runtime       = var.py_runtime
  source_path       = "index2.py"
  
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
    }
  ]
}
EOF
  event_source_mapping = {
    event_source_arn = aws_sqs_queue.orders_to_process.arn
    starting_position = "LATEST"
  }

  environment_variables = {
    buck_lm = var.s3_bucket_name
  }

  tags = {
    Name = "my-lambda2"
  }
}