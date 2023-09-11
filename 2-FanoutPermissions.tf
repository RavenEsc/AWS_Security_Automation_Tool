resource "aws_sqs_queue_policy" "orders_to_process_subscription" {
  queue_url = aws_sqs_queue.orders_to_process.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": [
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:GetQueueAttributes"
      ],
      "Resource": [
        "${aws_sqs_queue.orders_to_process.arn}"
      ],
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "${module.lambda_s3.lambda_function_arn}"
        }
      }
    },
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "sns.amazonaws.com"
      },
      "Action": [
        "sqs:SendMessage"
      ],
      "Resource": [
        "${aws_sqs_queue.orders_to_process.arn}"
      ],
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "${aws_sns_topic.orders.arn}"
        }
      }
    }
  ]
}
EOF
}


resource "aws_sqs_queue_policy" "orders_to_notify_subscription" {
  queue_url = aws_sqs_queue.orders_to_notify.id
  policy    = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": [
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:GetQueueAttributes"
      ],
      "Resource": [
        "${aws_sqs_queue.orders_to_notify.arn}"
      ],
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "${module.lambda_Discord.lambda_function_arn}"
        }
      }
    },
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "sns.amazonaws.com"
      },
      "Action": [
        "sqs:SendMessage"
      ],
      "Resource": [
        "${aws_sqs_queue.orders_to_notify.arn}"
      ],
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "${aws_sns_topic.orders.arn}"
        }
      }
    }
  ]
}
EOF
}